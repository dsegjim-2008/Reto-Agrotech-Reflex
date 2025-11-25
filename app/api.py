import datetime
import reflex as rx
from fastapi import APIRouter, Header, HTTPException, Depends
from sqlmodel import Session, select, desc
from typing import Optional
from pydantic import BaseModel
from app.database import Sensor, SensorData, Alert, Parcel, User


class SensorDataPayload(BaseModel):
    value: float
    timestamp: Optional[datetime.datetime] = None


class SensorResponse(BaseModel):
    id: int
    name: str
    type: str
    status: str
    last_reading: Optional[float] = None
    last_update: Optional[datetime.datetime] = None


class ParcelResponse(BaseModel):
    id: int
    name: str
    location: str
    size: float
    crop_type: str


class DashboardSummary(BaseModel):
    total_parcels: int
    total_sensors: int
    active_alerts: int


api_router = APIRouter(tags=["agrotech"])


def get_db():
    with rx.session() as session:
        yield session


def verify_api_key(
    x_api_key: str = Header(...), session: Session = Depends(get_db)
) -> User:
    user = session.exec(select(User).where(User.api_key == x_api_key)).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid API Key")
    return user


@api_router.post("/sensors/{sensor_id}/data")
async def ingest_sensor_data(
    sensor_id: int,
    payload: SensorDataPayload,
    user: User = Depends(verify_api_key),
    session: Session = Depends(get_db),
):
    """Ingest data for a specific sensor and check for alerts."""
    sensor = session.get(Sensor, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    timestamp = payload.timestamp or datetime.datetime.utcnow()
    new_data = SensorData(sensor_id=sensor_id, value=payload.value, timestamp=timestamp)
    session.add(new_data)
    sensor.last_reading_time = timestamp
    session.add(sensor)
    alert_triggered = False
    alert_msg = ""
    if payload.value < sensor.threshold_low:
        alert_triggered = True
        alert_msg = f"Low {sensor.type} detected: {payload.value:.2f} (Threshold: {sensor.threshold_low})"
    elif payload.value > sensor.threshold_high:
        alert_triggered = True
        alert_msg = f"High {sensor.type} detected: {payload.value:.2f} (Threshold: {sensor.threshold_high})"
    if alert_triggered:
        existing_alert = session.exec(
            select(Alert).where(
                Alert.sensor_id == sensor_id,
                Alert.is_active == True,
                Alert.acknowledged == False,
            )
        ).first()
        if not existing_alert:
            new_alert = Alert(
                sensor_id=sensor_id,
                message=alert_msg,
                level="warning",
                is_active=True,
                acknowledged=False,
                created_at=timestamp,
            )
            session.add(new_alert)
    session.commit()
    return {"status": "success", "alert_triggered": alert_triggered}


@api_router.get("/sensors/{sensor_id}/data")
async def get_sensor_history(
    sensor_id: int,
    limit: int = 100,
    user: User = Depends(verify_api_key),
    session: Session = Depends(get_db),
):
    """Get historical data for a sensor."""
    sensor = session.get(Sensor, sensor_id)
    if not sensor:
        raise HTTPException(status_code=404, detail="Sensor not found")
    query = (
        select(SensorData)
        .where(SensorData.sensor_id == sensor_id)
        .order_by(desc(SensorData.timestamp))
        .limit(limit)
    )
    data = session.exec(query).all()
    return [{"timestamp": d.timestamp, "value": d.value, "id": d.id} for d in data]


@api_router.get("/parcels", response_model=list[ParcelResponse])
async def list_parcels(
    user: User = Depends(verify_api_key), session: Session = Depends(get_db)
):
    """List all parcels accessible to the user."""
    query = select(Parcel).where(Parcel.farmer_id == user.id)
    parcels = session.exec(query).all()
    return [
        ParcelResponse(
            id=p.id,
            name=p.name,
            location=p.location,
            size=p.size,
            crop_type=p.crop_type,
        )
        for p in parcels
    ]


@api_router.get("/parcels/{parcel_id}/sensors", response_model=list[SensorResponse])
async def list_parcel_sensors(
    parcel_id: int,
    user: User = Depends(verify_api_key),
    session: Session = Depends(get_db),
):
    """List sensors for a specific parcel."""
    parcel = session.get(Parcel, parcel_id)
    if not parcel or parcel.farmer_id != user.id:
        raise HTTPException(status_code=404, detail="Parcel not found or access denied")
    query = select(Sensor).where(Sensor.parcel_id == parcel_id)
    sensors = session.exec(query).all()
    results = []
    for s in sensors:
        last_data = session.exec(
            select(SensorData)
            .where(SensorData.sensor_id == s.id)
            .order_by(desc(SensorData.timestamp))
        ).first()
        results.append(
            SensorResponse(
                id=s.id,
                name=s.name,
                type=s.type,
                status=s.status,
                last_reading=last_data.value if last_data else None,
                last_update=s.last_reading_time,
            )
        )
    return results


@api_router.get("/dashboard", response_model=DashboardSummary)
async def get_dashboard_summary(
    user: User = Depends(verify_api_key), session: Session = Depends(get_db)
):
    """Get high-level dashboard stats."""
    total_parcels = session.exec(
        select(Parcel).where(Parcel.farmer_id == user.id)
    ).all()
    parcel_ids = [p.id for p in total_parcels]
    if not parcel_ids:
        return DashboardSummary(total_parcels=0, total_sensors=0, active_alerts=0)
    total_sensors = session.exec(
        select(Sensor).where(Sensor.parcel_id.in_(parcel_ids))
    ).all()
    sensor_ids = [s.id for s in total_sensors]
    active_alerts = 0
    if sensor_ids:
        active_alerts = len(
            session.exec(
                select(Alert).where(
                    Alert.sensor_id.in_(sensor_ids),
                    Alert.is_active == True,
                    Alert.acknowledged == False,
                )
            ).all()
        )
    return DashboardSummary(
        total_parcels=len(total_parcels),
        total_sensors=len(total_sensors),
        active_alerts=active_alerts,
    )