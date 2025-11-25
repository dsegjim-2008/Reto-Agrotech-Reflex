import reflex as rx
import logging
from sqlmodel import select
from typing import Optional
from app.database import Parcel, Sensor, User
from app.states.auth_state import AuthState


class ParcelState(rx.State):
    """State for managing parcels and sensors.

    Handles CRUD operations for parcels and sensors, including
    loading list views, details views, and form submissions.
    """

    parcels: list[Parcel] = []
    current_parcel: Optional[Parcel] = None
    parcel_sensors: list[Sensor] = []
    is_parcel_modal_open: bool = False
    is_sensor_modal_open: bool = False
    editing_parcel: Optional[Parcel] = None
    editing_sensor: Optional[Sensor] = None
    delete_parcel_id: Optional[int] = None
    delete_sensor_id: Optional[int] = None
    is_delete_parcel_dialog_open: bool = False
    is_delete_sensor_dialog_open: bool = False

    @rx.event
    async def load_parcels(self):
        """Load all parcels for the current user."""
        auth_state = await self.get_state(AuthState)
        if not auth_state.user:
            return
        with rx.session() as session:
            statement = select(Parcel).where(Parcel.farmer_id == auth_state.user.id)
            self.parcels = session.exec(statement).all()

    @rx.event
    async def load_parcel_detail(self):
        """Load details for a specific parcel based on URL param."""
        parcel_id_param = self.router.page.params.get("id")
        if not parcel_id_param:
            return
        try:
            parcel_id = int(parcel_id_param)
        except ValueError as e:
            logging.exception(f"Error parsing parcel ID: {e}")
            return rx.toast.error("Invalid parcel ID")
        with rx.session() as session:
            parcel = session.get(Parcel, parcel_id)
            auth_state = await self.get_state(AuthState)
            if not parcel or (
                auth_state.user and parcel.farmer_id != auth_state.user.id
            ):
                return rx.toast.error("Parcel not found or access denied")
            self.current_parcel = parcel
            statement = select(Sensor).where(Sensor.parcel_id == parcel_id)
            self.parcel_sensors = session.exec(statement).all()

    @rx.event
    def open_add_parcel_modal(self):
        self.editing_parcel = None
        self.is_parcel_modal_open = True

    @rx.event
    def open_edit_parcel_modal(self, parcel: Parcel):
        self.editing_parcel = parcel
        self.is_parcel_modal_open = True

    @rx.event
    def close_parcel_modal(self):
        self.is_parcel_modal_open = False
        self.editing_parcel = None

    @rx.event
    async def save_parcel(self, form_data: dict):
        """Create or update a parcel based on form data.

        Args:
            form_data (dict): Dictionary containing parcel details (name, location, etc.).

        Yields:
            rx.toast: Success or error messages.
        """
        auth_state = await self.get_state(AuthState)
        if not auth_state.user:
            yield rx.toast.error("You must be logged in.")
            return
        name = form_data.get("name")
        location = form_data.get("location")
        crop_type = form_data.get("crop_type")
        size_str = form_data.get("size")
        if not name or not location or (not crop_type) or (not size_str):
            yield rx.toast.error("All fields are required.")
            return
        try:
            size = float(size_str)
        except ValueError as e:
            logging.exception(f"Error parsing size: {e}")
            yield rx.toast.error("Size must be a valid number.")
            return
        with rx.session() as session:
            if self.editing_parcel:
                parcel = session.get(Parcel, self.editing_parcel.id)
                if parcel:
                    parcel.name = name
                    parcel.location = location
                    parcel.crop_type = crop_type
                    parcel.size = size
                    session.add(parcel)
                    session.commit()
                    self.close_parcel_modal()
                    yield rx.toast.success("Parcel updated successfully.")
            else:
                new_parcel = Parcel(
                    name=name,
                    location=location,
                    crop_type=crop_type,
                    size=size,
                    farmer_id=auth_state.user.id,
                )
                session.add(new_parcel)
                session.commit()
                self.close_parcel_modal()
                yield rx.toast.success("Parcel created successfully.")
        yield ParcelState.load_parcels

    @rx.event
    def confirm_delete_parcel(self, parcel_id: int):
        self.delete_parcel_id = parcel_id
        self.is_delete_parcel_dialog_open = True

    @rx.event
    def cancel_delete_parcel(self):
        self.delete_parcel_id = None
        self.is_delete_parcel_dialog_open = False

    @rx.event
    def delete_parcel(self):
        if not self.delete_parcel_id:
            return
        with rx.session() as session:
            parcel = session.get(Parcel, self.delete_parcel_id)
            if parcel:
                statement = select(Sensor).where(Sensor.parcel_id == parcel.id)
                sensors = session.exec(statement).all()
                for s in sensors:
                    session.delete(s)
                session.delete(parcel)
                session.commit()
        self.is_delete_parcel_dialog_open = False
        self.delete_parcel_id = None
        return [ParcelState.load_parcels, rx.toast.success("Parcel deleted.")]

    @rx.event
    def open_add_sensor_modal(self):
        self.editing_sensor = None
        self.is_sensor_modal_open = True

    @rx.event
    def open_edit_sensor_modal(self, sensor: Sensor):
        self.editing_sensor = sensor
        self.is_sensor_modal_open = True

    @rx.event
    def close_sensor_modal(self):
        self.is_sensor_modal_open = False
        self.editing_sensor = None

    @rx.event
    async def save_sensor(self, form_data: dict):
        if not self.current_parcel:
            return
        name = form_data.get("name")
        sensor_type = form_data.get("type")
        threshold_low_str = form_data.get("threshold_low")
        threshold_high_str = form_data.get("threshold_high")
        if not name or not sensor_type:
            yield rx.toast.error("Name and Type are required.")
            return
        threshold_low = float(threshold_low_str) if threshold_low_str else 0.0
        threshold_high = float(threshold_high_str) if threshold_high_str else 100.0
        with rx.session() as session:
            if self.editing_sensor:
                sensor = session.get(Sensor, self.editing_sensor.id)
                if sensor:
                    sensor.name = name
                    sensor.type = sensor_type
                    sensor.threshold_low = threshold_low
                    sensor.threshold_high = threshold_high
                    session.add(sensor)
                    session.commit()
                    self.close_sensor_modal()
                    yield rx.toast.success("Sensor updated.")
            else:
                new_sensor = Sensor(
                    name=name,
                    type=sensor_type,
                    parcel_id=self.current_parcel.id,
                    status="active",
                    threshold_low=threshold_low,
                    threshold_high=threshold_high,
                )
                session.add(new_sensor)
                session.commit()
                self.close_sensor_modal()
                yield rx.toast.success("Sensor added.")
        yield ParcelState.load_parcel_detail

    @rx.event
    def confirm_delete_sensor(self, sensor_id: int):
        self.delete_sensor_id = sensor_id
        self.is_delete_sensor_dialog_open = True

    @rx.event
    def cancel_delete_sensor(self):
        self.delete_sensor_id = None
        self.is_delete_sensor_dialog_open = False

    @rx.event
    def delete_sensor(self):
        if not self.delete_sensor_id:
            return
        with rx.session() as session:
            sensor = session.get(Sensor, self.delete_sensor_id)
            if sensor:
                session.delete(sensor)
                session.commit()
        self.is_delete_sensor_dialog_open = False
        self.delete_sensor_id = None
        return [ParcelState.load_parcel_detail, rx.toast.success("Sensor deleted.")]