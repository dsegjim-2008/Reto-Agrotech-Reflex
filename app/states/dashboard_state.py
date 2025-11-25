import reflex as rx
import datetime
from sqlmodel import select, func, desc
from typing import Any, Optional
from app.database import Parcel, Sensor, SensorData, Alert
from app.states.auth_state import AuthState


class DashboardState(rx.State):
    """State management for the main dashboard visualization.

    Handles loading and formatting of high-level metrics, active alerts,
    recent sensor readings, and chart data aggregations.
    """

    total_parcels: int = 0
    total_sensors: int = 0
    active_alerts_count: int = 0
    active_alerts: list[dict[str, str | int | bool]] = []
    recent_readings: list[dict[str, str | float | int]] = []
    chart_data: list[dict[str, str | float | int]] = []
    time_filter: str = "24h"
    selected_sensor_type: str = "temperature"
    is_loading: bool = False

    @rx.event
    async def load_dashboard_data(self):
        """Load all dashboard metrics and data from the database.

        Fetches total counts, active alerts, recent readings, and prepares
        chart data based on the current time filters.
        """
        self.is_loading = True
        yield
        auth_state = await self.get_state(AuthState)
        if not auth_state.user:
            self.is_loading = False
            return
        user_id = auth_state.user.id
        with rx.session() as session:
            self.total_parcels = session.exec(
                select(func.count(Parcel.id)).where(Parcel.farmer_id == user_id)
            ).one()
            self.total_sensors = session.exec(
                select(func.count(Sensor.id))
                .join(Parcel)
                .where(Parcel.farmer_id == user_id)
            ).one()
            alerts_query = (
                select(Alert)
                .join(Sensor)
                .join(Parcel)
                .where(
                    Parcel.farmer_id == user_id,
                    Alert.is_active == True,
                    Alert.acknowledged == False,
                )
                .order_by(desc(Alert.created_at))
            )
            alerts_data = session.exec(alerts_query).all()
            self.active_alerts = [
                {
                    "id": a.id,
                    "sensor_id": a.sensor_id,
                    "message": a.message,
                    "level": a.level,
                    "is_active": a.is_active,
                    "acknowledged": a.acknowledged,
                    "created_at": a.created_at.strftime("%Y-%m-%d %H:%M"),
                }
                for a in alerts_data
            ]
            self.active_alerts_count = len(self.active_alerts)
            readings_query = (
                select(SensorData, Sensor, Parcel)
                .join(Sensor)
                .join(Parcel)
                .where(Parcel.farmer_id == user_id)
                .order_by(desc(SensorData.timestamp))
                .limit(10)
            )
            results = session.exec(readings_query).all()
            self.recent_readings = [
                {
                    "id": r.SensorData.id,
                    "sensor_name": r.Sensor.name,
                    "type": r.Sensor.type,
                    "value": r.SensorData.value,
                    "parcel_name": r.Parcel.name,
                    "timestamp": r.SensorData.timestamp.strftime("%Y-%m-%d %H:%M"),
                }
                for r in results
            ]
            self._load_chart_data(session, user_id)
        self.is_loading = False

    def _load_chart_data(self, session, user_id):
        """Helper to load chart data based on filter."""
        now = datetime.datetime.utcnow()
        if self.time_filter == "24h":
            start_time = now - datetime.timedelta(hours=24)
        elif self.time_filter == "7d":
            start_time = now - datetime.timedelta(days=7)
        else:
            start_time = now - datetime.timedelta(days=30)
        query = (
            select(SensorData.timestamp, SensorData.value)
            .join(Sensor)
            .join(Parcel)
            .where(
                Parcel.farmer_id == user_id,
                Sensor.type == self.selected_sensor_type,
                SensorData.timestamp >= start_time,
            )
            .order_by(SensorData.timestamp)
        )
        data_points = session.exec(query).all()
        formatted_data = []
        if data_points:
            step = max(1, len(data_points) // 50)
            for i in range(0, len(data_points), step):
                point = data_points[i]
                formatted_data.append(
                    {
                        "time": point.timestamp.strftime(
                            "%H:%M" if self.time_filter == "24h" else "%m-%d"
                        ),
                        "value": round(point.value, 1),
                        "full_date": point.timestamp.strftime("%Y-%m-%d %H:%M"),
                    }
                )
        self.chart_data = formatted_data

    @rx.event
    async def set_time_filter(self, value: str):
        self.time_filter = value
        await self.load_dashboard_data()

    @rx.event
    async def set_sensor_type_filter(self, value: str):
        self.selected_sensor_type = value
        await self.load_dashboard_data()

    @rx.event
    def acknowledge_alert(self, alert_id: int):
        with rx.session() as session:
            alert = session.get(Alert, alert_id)
            if alert:
                alert.acknowledged = True
                session.add(alert)
                session.commit()
        return DashboardState.load_dashboard_data