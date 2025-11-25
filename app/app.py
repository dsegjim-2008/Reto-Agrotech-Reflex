import reflex as rx
from app.pages.login import login_page
from app.pages.register import register_page
from app.pages.dashboard import dashboard_page
from app.states.auth_state import AuthState


def index():
    """The main landing page, which is the dashboard if logged in."""
    return dashboard_page()


from app.pages.parcels import parcels_page
from app.pages.parcel_detail import parcel_detail_page
from app.states.parcel_state import ParcelState
from app.api import api_router
from fastapi import FastAPI


def api_config(api_app):
    custom_api = FastAPI()
    custom_api.include_router(api_router)
    api_app.mount("/api", custom_api)


app = rx.App(
    theme=rx.theme(appearance="light"),
    api_transformer=api_config,
    head_components=[
        rx.el.link(rel="preconnect", href="https://fonts.googleapis.com"),
        rx.el.link(rel="preconnect", href="https://fonts.gstatic.com", cross_origin=""),
        rx.el.link(
            href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700&display=swap",
            rel="stylesheet",
        ),
    ],
)
from app.states.dashboard_state import DashboardState
from app.pages.analytics import analytics_page
from app.states.analytics_state import AnalyticsState
from app.pages.alerts import alerts_page
from app.states.alert_state import AlertState
from app.pages.api_docs import api_docs_page
from app.pages.settings import settings_page

app.add_page(
    index,
    route="/",
    on_load=[AuthState.check_login, DashboardState.load_dashboard_data],
    title="Dashboard | Agrotech",
)
app.add_page(login_page, route="/login", title="Login | Agrotech")
app.add_page(register_page, route="/register", title="Register | Agrotech")
app.add_page(
    parcels_page,
    route="/parcels",
    on_load=[AuthState.check_login, ParcelState.load_parcels],
    title="Parcels | Agrotech",
)
app.add_page(
    parcel_detail_page,
    route="/parcels/[id]",
    on_load=[AuthState.check_login, ParcelState.load_parcel_detail],
    title="Parcel Details | Agrotech",
)
app.add_page(
    analytics_page,
    route="/analytics",
    on_load=[AuthState.check_login, AnalyticsState.load_initial_data],
    title="Analytics | Agrotech",
)
app.add_page(
    alerts_page,
    route="/alerts",
    on_load=[AuthState.check_login, AlertState.load_alerts],
    title="Alerts | Agrotech",
)
app.add_page(
    api_docs_page,
    route="/api-docs",
    on_load=AuthState.check_login,
    title="API Documentation | Agrotech",
)
app.add_page(
    settings_page,
    route="/settings",
    on_load=AuthState.check_login,
    title="Settings | Agrotech",
)