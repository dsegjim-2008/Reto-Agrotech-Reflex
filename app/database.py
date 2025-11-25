import reflex as rx
import datetime
from sqlmodel import Field, Relationship, SQLModel
from typing import Optional


class User(SQLModel, table=True):
    """User model for authentication and role management."""

    id: Optional[int] = Field(default=None, primary_key=True)
    username: str
    email: str = Field(unique=True, index=True)
    password_hash: str
    role: str = "farmer"
    api_key: Optional[str] = Field(default=None, index=True)
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    parcels: list["Parcel"] = Relationship(back_populates="farmer")


class Parcel(SQLModel, table=True):
    """Represents a land parcel owned by a farmer."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    size: float
    crop_type: str
    location: str
    farmer_id: int = Field(foreign_key="user.id")
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    farmer: Optional[User] = Relationship(back_populates="parcels")
    sensors: list["Sensor"] = Relationship(back_populates="parcel")


class Sensor(SQLModel, table=True):
    """IoT Sensor deployed in a parcel."""

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    type: str
    status: str = "active"
    parcel_id: int = Field(foreign_key="parcel.id")
    last_reading_time: Optional[datetime.datetime] = None
    threshold_low: float = 0.0
    threshold_high: float = 100.0
    parcel: Optional[Parcel] = Relationship(back_populates="sensors")
    readings: list["SensorData"] = Relationship(back_populates="sensor")
    alerts: list["Alert"] = Relationship(back_populates="sensor")


class SensorData(SQLModel, table=True):
    """Historical data readings from sensors."""

    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id")
    value: float
    timestamp: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    sensor: Optional[Sensor] = Relationship(back_populates="readings")


class Alert(SQLModel, table=True):
    """System alerts triggered by sensor thresholds."""

    id: Optional[int] = Field(default=None, primary_key=True)
    sensor_id: int = Field(foreign_key="sensor.id")
    message: str
    level: str = "warning"
    is_active: bool = True
    acknowledged: bool = False
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
    sensor: Optional[Sensor] = Relationship(back_populates="alerts")