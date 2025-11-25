import reflex as rx
from app.states.dashboard_state import DashboardState
from app.components.navbar import navbar
from app.components.charts import sensor_area_chart
from app.components.skeletons import skeleton_card, skeleton_chart, skeleton_table_row
from app.database import Alert


def metric_card(
    title: str, value: str, icon_name: str, color_class: str
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(icon_name, class_name=f"h-6 w-6 {color_class}"),
            class_name="p-3 bg-gray-50 rounded-lg",
        ),
        rx.el.div(
            rx.el.p(title, class_name="text-sm font-medium text-gray-500"),
            rx.el.h3(value, class_name="text-2xl font-bold text-gray-900"),
            class_name="ml-4",
        ),
        class_name="flex items-center p-6 bg-white rounded-xl shadow-sm border border-gray-200",
    )


def alert_item(alert: dict[str, str | int | bool]) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.icon(
                "badge_alert",
                class_name="h-5 w-5 text-orange-500 mt-0.5 mr-3 flex-shrink-0",
            ),
            rx.el.div(
                rx.el.p(
                    alert["message"], class_name="text-sm font-medium text-gray-900"
                ),
                rx.el.p(
                    f"{alert['created_at']} • Sensor {alert['sensor_id']}",
                    class_name="text-xs text-gray-500 mt-0.5",
                ),
            ),
            class_name="flex",
        ),
        rx.el.button(
            "Dismiss",
            on_click=DashboardState.acknowledge_alert(alert["id"]),
            class_name="text-xs font-medium text-gray-400 hover:text-gray-600 ml-4",
        ),
        class_name="flex items-start justify-between p-4 border-b border-gray-100 last:border-0",
    )


def recent_reading_row(reading: dict) -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(
                rx.el.p(
                    reading["sensor_name"],
                    class_name="text-sm font-medium text-gray-900",
                ),
                rx.el.p(reading["type"], class_name="text-xs text-gray-500 capitalize"),
                class_name="flex flex-col",
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(reading["parcel_name"], class_name="text-sm text-gray-600"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(
                f"{reading['value']}", class_name="text-sm font-semibold text-gray-900"
            ),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
        rx.el.td(
            rx.el.span(reading["timestamp"], class_name="text-sm text-gray-500"),
            class_name="px-6 py-4 whitespace-nowrap",
        ),
    )


def dashboard_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1("Dashboard", class_name="text-3xl font-bold text-gray-900"),
                rx.el.p(
                    "Real-time overview of your agricultural assets",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.cond(
                    DashboardState.is_loading,
                    rx.fragment(skeleton_card(), skeleton_card(), skeleton_card()),
                    rx.fragment(
                        metric_card(
                            "Total Parcels",
                            DashboardState.total_parcels.to_string(),
                            "layout-grid",
                            "text-blue-600",
                        ),
                        metric_card(
                            "Active Sensors",
                            DashboardState.total_sensors.to_string(),
                            "activity",
                            "text-green-600",
                        ),
                        metric_card(
                            "Active Alerts",
                            DashboardState.active_alerts_count.to_string(),
                            "bell",
                            "text-orange-600",
                        ),
                    ),
                ),
                class_name="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        DashboardState.is_loading, skeleton_chart(), sensor_area_chart()
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Recent Sensor Readings",
                                class_name="text-lg font-semibold text-gray-900",
                            ),
                            class_name="p-6 border-b border-gray-200",
                        ),
                        rx.el.div(
                            rx.el.table(
                                rx.el.thead(
                                    rx.el.tr(
                                        rx.el.th(
                                            "Sensor",
                                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Parcel",
                                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Value",
                                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                        ),
                                        rx.el.th(
                                            "Time",
                                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                                        ),
                                    ),
                                    class_name="bg-gray-50",
                                ),
                                rx.el.tbody(
                                    rx.cond(
                                        DashboardState.is_loading,
                                        rx.fragment(
                                            skeleton_table_row(),
                                            skeleton_table_row(),
                                            skeleton_table_row(),
                                            skeleton_table_row(),
                                            skeleton_table_row(),
                                        ),
                                        rx.foreach(
                                            DashboardState.recent_readings,
                                            recent_reading_row,
                                        ),
                                    ),
                                    class_name="bg-white divide-y divide-gray-200",
                                ),
                                class_name="min-w-full divide-y divide-gray-200",
                            ),
                            class_name="overflow-x-auto",
                        ),
                        class_name="bg-white rounded-xl shadow-sm border border-gray-200 mt-8 overflow-hidden",
                    ),
                    class_name="lg:col-span-2",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.h3(
                                "Active Alerts",
                                class_name="text-lg font-semibold text-gray-900",
                            ),
                            rx.cond(
                                DashboardState.active_alerts_count > 0,
                                rx.el.span(
                                    f"{DashboardState.active_alerts_count} New",
                                    class_name="bg-orange-100 text-orange-700 text-xs font-bold px-2 py-1 rounded-full ml-2",
                                ),
                            ),
                            class_name="flex items-center p-6 border-b border-gray-200",
                        ),
                        rx.cond(
                            DashboardState.active_alerts,
                            rx.el.div(
                                rx.foreach(DashboardState.active_alerts, alert_item),
                                class_name="max-h-[600px] overflow-y-auto",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "check_check",
                                    class_name="h-12 w-12 text-green-500 mb-3 opacity-50",
                                ),
                                rx.el.p(
                                    "No active alerts",
                                    class_name="text-gray-500 font-medium",
                                ),
                                class_name="flex flex-col items-center justify-center py-12",
                            ),
                        ),
                        class_name="bg-white rounded-xl shadow-sm border border-gray-200 h-fit sticky top-24",
                    )
                ),
                class_name="grid grid-cols-1 lg:grid-cols-3 gap-8",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="min-h-screen bg-gray-50 font-['Roboto']",
    )