import reflex as rx
import bcrypt
import random
import string
from sqlmodel import select
from app.database import User
from app.states.auth_state import AuthState


class SettingsState(rx.State):
    """State for user settings, profile management, and security configuration."""

    active_tab: str = "profile"
    notifications_enabled: bool = True
    new_password: str = ""
    confirm_password: str = ""

    @rx.event
    def set_active_tab_val(self, val: str):
        """Set the currently active tab in the settings page."""
        self.active_tab = val

    @rx.event
    def toggle_notifications(self, val: bool):
        self.notifications_enabled = val
        yield rx.toast.success(f"Notifications {('enabled' if val else 'disabled')}")

    @rx.event
    async def regenerate_api_key(self):
        """Regenerate the user's unique API key.

        Creates a new random alphanumeric string and updates the user record.
        This invalidates the old key immediately.
        """
        auth_state = await self.get_state(AuthState)
        if not auth_state.user:
            return
        chars = string.ascii_letters + string.digits
        new_key = "key_" + "".join((random.choice(chars) for _ in range(20)))
        with rx.session() as session:
            user = session.get(User, auth_state.user.id)
            if user:
                user.api_key = new_key
                session.add(user)
                session.commit()
                session.refresh(user)
                auth_state.user = user
                yield rx.toast.success("API Key regenerated successfully")

    @rx.event
    async def update_password(self):
        if not self.new_password:
            yield rx.toast.error("Password cannot be empty")
            return
        if self.new_password != self.confirm_password:
            yield rx.toast.error("Passwords do not match")
            return
        auth_state = await self.get_state(AuthState)
        if not auth_state.user:
            return
        hashed_pw = bcrypt.hashpw(
            self.new_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        with rx.session() as session:
            user = session.get(User, auth_state.user.id)
            if user:
                user.password_hash = hashed_pw
                session.add(user)
                session.commit()
                self.new_password = ""
                self.confirm_password = ""
                yield rx.toast.success("Password updated successfully")

    @rx.event
    def set_new_password(self, val: str):
        self.new_password = val

    @rx.event
    def set_confirm_password(self, val: str):
        self.confirm_password = val