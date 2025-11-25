import reflex as rx
import bcrypt
import random
import string
from typing import Optional
from sqlmodel import select
from app.database import User


class AuthState(rx.State):
    """State management for user authentication, login, and registration flows."""

    user: Optional[User] = None
    is_authenticated: bool = False
    auth_token: str = ""
    login_email: str = ""
    login_password: str = ""
    register_username: str = ""
    register_email: str = ""
    register_password: str = ""
    register_role: str = "farmer"

    def _get_user_by_email(self, email: str) -> Optional[User]:
        """Helper to fetch a user from the database by email.

        Args:
            email (str): The email address to search for.

        Returns:
            Optional[User]: The User object if found, None otherwise.
        """
        with rx.session() as session:
            statement = select(User).where(User.email == email)
            return session.exec(statement).first()

    @rx.event
    def login(self):
        """Handle user login."""
        if not self.login_email or not self.login_password:
            return rx.toast.error("Please fill in all fields.")
        user = self._get_user_by_email(self.login_email)
        if user and bcrypt.checkpw(
            self.login_password.encode("utf-8"), user.password_hash.encode("utf-8")
        ):
            self.user = user
            self.is_authenticated = True
            self.login_password = ""
            return [
                rx.toast.success(f"Welcome back, {user.username}!"),
                rx.redirect("/"),
            ]
        else:
            return rx.toast.error("Invalid email or password.")

    @rx.event
    def logout(self):
        """Handle user logout."""
        self.user = None
        self.is_authenticated = False
        return [rx.toast.info("Logged out successfully."), rx.redirect("/login")]

    @rx.event
    def register(self):
        """Handle user registration."""
        if (
            not self.register_username
            or not self.register_email
            or (not self.register_password)
        ):
            return rx.toast.error("Please fill in all fields.")
        existing_user = self._get_user_by_email(self.register_email)
        if existing_user:
            return rx.toast.error("User with this email already exists.")
        hashed_pw = bcrypt.hashpw(
            self.register_password.encode("utf-8"), bcrypt.gensalt()
        ).decode("utf-8")
        chars = string.ascii_letters + string.digits
        api_key = "key_" + "".join((random.choice(chars) for _ in range(20)))
        new_user = User(
            username=self.register_username,
            email=self.register_email,
            password_hash=hashed_pw,
            role=self.register_role,
            api_key=api_key,
        )
        with rx.session() as session:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
        self.user = new_user
        self.is_authenticated = True
        self.register_password = ""
        self.register_username = ""
        self.register_email = ""
        return [rx.toast.success("Account created successfully!"), rx.redirect("/")]

    @rx.event
    async def check_login(self):
        """Redirect to login if not authenticated."""
        if not self.is_authenticated:
            return rx.redirect("/login")

    @rx.event
    async def check_already_logged_in(self):
        """Redirect to dashboard if already authenticated (for login/register pages)."""
        if self.is_authenticated:
            return rx.redirect("/")

    @rx.event
    def set_login_email(self, value: str):
        self.login_email = value

    @rx.event
    def set_login_password(self, value: str):
        self.login_password = value

    @rx.event
    def set_register_username(self, value: str):
        self.register_username = value

    @rx.event
    def set_register_email(self, value: str):
        self.register_email = value

    @rx.event
    def set_register_password(self, value: str):
        self.register_password = value

    @rx.event
    def set_register_role(self, value: str):
        self.register_role = value