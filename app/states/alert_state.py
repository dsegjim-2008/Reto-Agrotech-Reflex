import reflex as rx
from sqlmodel import select, desc, and_
from app.database import Alert, Sensor, Parcel
from app.states.auth_state import AuthState


class AlertState(rx.State):
    """State management for the alerts system.

    Handles fetching and filtering of system alerts, separating them into
    active (unacknowledged) and historical lists.
    """

    active_alerts: list[dict] = []
    alert_history: list[dict] = []
    filter_type: str = "all"

    @rx.event
    async def load_alerts(self):
        """Fetch and categorize active and historical alerts for the current user.

        Populates `active_alerts` with triggered, unacknowledged warnings,
        and `alert_history` with resolved or acknowledged past alerts.
        """
        auth_state = await self.get_state(AuthState)
        if not auth_state.user:
            return
        user_id = auth_state.user.id
        with rx.session() as session:
            active_query = (
                select(Alert, Sensor, Parcel)
                .join(Sensor)
                .join(Parcel)
                .where(
                    Parcel.farmer_id == user_id,
                    Alert.is_active == True,
                    Alert.acknowledged == False,
                )
                .order_by(desc(Alert.created_at))
            )
            active_results = session.exec(active_query).all()
            self.active_alerts = [
                {
                    "id": row.Alert.id,
                    "sensor": row.Sensor.name,
                    "sensor_id": row.Sensor.id,
                    "parcel": row.Parcel.name,
                    "message": row.Alert.message,
                    "level": row.Alert.level,
                    "time": row.Alert.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                }
                for row in active_results
            ]
            history_query = (
                select(Alert, Sensor, Parcel)
                .join(Sensor)
                .join(Parcel)
                .where(
                    Parcel.farmer_id == user_id,
                    (Alert.acknowledged == True) | (Alert.is_active == False),
                )
                .order_by(desc(Alert.created_at))
                .limit(50)
            )
            history_results = session.exec(history_query).all()
            self.alert_history = [
                {
                    "id": row.Alert.id,
                    "sensor": row.Sensor.name,
                    "sensor_id": row.Sensor.id,
                    "parcel": row.Parcel.name,
                    "message": row.Alert.message,
                    "level": row.Alert.level,
                    "time": row.Alert.created_at.strftime("%Y-%m-%d %H:%M:%S"),
                    "status": "Resolved" if not row.Alert.is_active else "Acknowledged",
                }
                for row in history_results
            ]

    @rx.event
    def acknowledge_alert(self, alert_id: int):
        with rx.session() as session:
            alert = session.get(Alert, alert_id)
            if alert:
                alert.acknowledged = True
                session.add(alert)
                session.commit()
        return [AlertState.load_alerts, rx.toast.success("Alert acknowledged.")]

    @rx.event
    def resolve_alert(self, alert_id: int):
        with rx.session() as session:
            alert = session.get(Alert, alert_id)
            if alert:
                alert.is_active = False
                alert.acknowledged = True
                session.add(alert)
                session.commit()
        return [AlertState.load_alerts, rx.toast.success("Alert marked as resolved.")]