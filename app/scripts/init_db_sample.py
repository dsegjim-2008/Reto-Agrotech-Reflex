import sys
import os
import random
import math
import datetime
from sqlmodel import SQLModel, create_engine, Session, select

sys.path.append(os.getcwd())
from app.database import User, Parcel, Sensor, SensorData, Alert
import bcrypt


def init_db():
    sqlite_file_name = "reflex.db"
    sqlite_url = f"sqlite:///{sqlite_file_name}"
    engine = create_engine(sqlite_url)
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        if session.exec(select(User)).first():
            print("Data already exists. Skipping initialization.")
            return
        print("Creating sample data...")
        password_hash = bcrypt.hashpw(
            "password123".encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        farmer = User(
            username="farmer_john",
            email="john@agrotech.com",
            password_hash=password_hash,
            role="farmer",
            api_key="key_farmer_12345",
        )
        tech = User(
            username="tech_sarah",
            email="sarah@agrotech.com",
            password_hash=password_hash,
            role="technician",
            api_key="key_tech_67890",
        )
        session.add(farmer)
        session.add(tech)
        session.commit()
        session.refresh(farmer)
        parcels = [
            Parcel(
                name="North Field",
                location="Zone A, Valley",
                size=15.5,
                crop_type="Corn",
                farmer_id=farmer.id,
            ),
            Parcel(
                name="Sunny Hill",
                location="Zone B, Hillside",
                size=8.2,
                crop_type="Wheat",
                farmer_id=farmer.id,
            ),
            Parcel(
                name="River Bank",
                location="Zone C, River",
                size=12.0,
                crop_type="Soybeans",
                farmer_id=farmer.id,
            ),
        ]
        for p in parcels:
            session.add(p)
        session.commit()
        for p in parcels:
            session.refresh(p)
        sensor_types = ["temperature", "soil_humidity", "luminosity"]
        sensors = []
        for parcel in parcels:
            for s_type in sensor_types:
                sensor = Sensor(
                    name=f"{s_type.title()} Sensor {parcel.id}",
                    type=s_type,
                    parcel_id=parcel.id,
                    status="active",
                    threshold_low=10.0 if s_type == "temperature" else 30.0,
                    threshold_high=35.0 if s_type == "temperature" else 80.0,
                )
                session.add(sensor)
                sensors.append(sensor)
        session.commit()
        for s in sensors:
            session.refresh(s)
        now = datetime.datetime.now(datetime.UTC)
        print("Generating sensor readings...")
        for day in range(30):
            date = now - datetime.timedelta(days=30 - day)
            for hour in range(0, 24, 4):
                timestamp = date.replace(hour=hour, minute=0, second=0)
                for sensor in sensors:
                    base_val = 25.0 if sensor.type == "temperature" else 60.0
                    variation = 5.0 * math.sin(hour / 24 * 2 * 3.14159)
                    noise = random.uniform(-2.0, 2.0)
                    value = base_val + variation + noise
                    data = SensorData(
                        sensor_id=sensor.id, value=value, timestamp=timestamp
                    )
                    session.add(data)
                    if random.random() < 0.02:
                        alert = Alert(
                            sensor_id=sensor.id,
                            message=f"Abnormal {sensor.type} detected: {value:.1f}",
                            level="warning",
                            created_at=timestamp,
                            is_active=True,
                            acknowledged=False,
                        )
                        session.add(alert)
        session.commit()
        print("Database initialized successfully with sample data.")


if __name__ == "__main__":
    init_db()