import reflex as rx
from app.states.alert_state import AlertState
from app.states.auth_state import AuthState
from app.components.navbar import navbar


def alert_card(alert: dict, is_active: bool = True) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.cond(
                    alert["level"] == "critical",
                    rx.icon("octagon_alert", class_name="h-6 w-6 text-red-500"),
                    rx.icon(
                        "flag_triangle_right", class_name="h-6 w-6 text-orange-500"
                    ),
                ),
                class_name=f"p-3 rounded-full bg-{(alert['level'] == 'critical') & 'red' | 'orange'}-100 mr-4",
            ),
            rx.el.div(
                rx.el.h4(
                    alert["message"], class_name="text-lg font-medium text-gray-900"
                ),
                rx.el.div(
                    rx.el.span(
                        f"{alert['parcel']} • {alert['sensor']}",
                        class_name="text-sm text-gray-500 font-medium",
                    ),
                    rx.el.span(" • ", class_name="text-gray-300 mx-1"),
                    rx.el.span(alert["time"], class_name="text-sm text-gray-400"),
                    class_name="flex items-center mt-1",
                ),
                class_name="flex-1",
            ),
            rx.cond(
                is_active,
                rx.el.div(
                    rx.el.button(
                        "Acknowledge",
                        on_click=lambda: AlertState.acknowledge_alert(alert["id"]),
                        class_name="px-4 py-2 text-sm font-medium text-blue-600 bg-blue-50 rounded-lg hover:bg-blue-100 transition-colors mr-2",
                    ),
                    rx.el.button(
                        "Resolve",
                        on_click=lambda: AlertState.resolve_alert(alert["id"]),
                        class_name="px-4 py-2 text-sm font-medium text-green-600 bg-green-50 rounded-lg hover:bg-green-100 transition-colors",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.span(
                    alert["status"],
                    class_name="px-3 py-1 text-xs font-semibold text-gray-500 bg-gray-100 rounded-full uppercase",
                ),
            ),
            class_name="flex items-start",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm hover:shadow-md transition-shadow",
    )


def alerts_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "System Alerts", class_name="text-3xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Monitor and manage sensor threshold alerts",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Active Alerts",
                    class_name="text-xl font-bold text-gray-800 mb-4 flex items-center gap-2",
                ),
                rx.cond(
                    AlertState.active_alerts,
                    rx.el.div(
                        rx.foreach(
                            AlertState.active_alerts, lambda a: alert_card(a, True)
                        ),
                        class_name="space-y-4",
                    ),
                    rx.el.div(
                        rx.icon(
                            "check_check", class_name="h-12 w-12 text-green-500 mb-3"
                        ),
                        rx.el.p(
                            "All systems normal. No active alerts.",
                            class_name="text-gray-600 font-medium",
                        ),
                        class_name="bg-green-50 rounded-xl p-8 flex flex-col items-center justify-center border border-green-100",
                    ),
                ),
                class_name="mb-12",
            ),
            rx.el.div(
                rx.el.h2(
                    "Alert History", class_name="text-xl font-bold text-gray-800 mb-4"
                ),
                rx.cond(
                    AlertState.alert_history,
                    rx.el.div(
                        rx.foreach(
                            AlertState.alert_history, lambda a: alert_card(a, False)
                        ),
                        class_name="space-y-4 opacity-75",
                    ),
                    rx.el.p(
                        "No alert history found.", class_name="text-gray-500 italic"
                    ),
                ),
            ),
            class_name="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="min-h-screen bg-gray-50 font-['Roboto']",
    )