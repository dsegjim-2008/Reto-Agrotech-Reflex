import reflex as rx
from typing import Any
from app.states.dashboard_state import DashboardState

TOOLTIP_PROPS = {
    "content_style": {
        "background": "white",
        "borderColor": "#E8E8E8",
        "borderRadius": "0.75rem",
        "boxShadow": "0px 4px 6px -1px rgba(0, 0, 0, 0.1), 0px 2px 4px -1px rgba(0, 0, 0, 0.06)",
        "fontFamily": "sans-serif",
        "fontSize": "0.875rem",
        "padding": "0.5rem 0.75rem",
    },
    "item_style": {"color": "#374151", "fontWeight": "500"},
    "separator": "",
}


def sensor_area_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.h3(
                f"{DashboardState.selected_sensor_type.capitalize()} Trends",
                class_name="text-lg font-semibold text-gray-900",
            ),
            rx.el.div(
                rx.el.select(
                    rx.el.option("Temperature", value="temperature"),
                    rx.el.option("Humidity", value="soil_humidity"),
                    rx.el.option("Luminosity", value="luminosity"),
                    value=DashboardState.selected_sensor_type,
                    on_change=DashboardState.set_sensor_type_filter,
                    class_name="text-sm border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500 mr-2",
                ),
                rx.el.select(
                    rx.el.option("Last 24 Hours", value="24h"),
                    rx.el.option("Last 7 Days", value="7d"),
                    rx.el.option("Last 30 Days", value="30d"),
                    value=DashboardState.time_filter,
                    on_change=DashboardState.set_time_filter,
                    class_name="text-sm border-gray-300 rounded-md shadow-sm focus:border-blue-500 focus:ring-blue-500",
                ),
                class_name="flex items-center",
            ),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.cond(
            DashboardState.chart_data,
            rx.recharts.area_chart(
                rx.recharts.cartesian_grid(
                    stroke_dasharray="3 3", vertical=False, class_name="stroke-gray-200"
                ),
                rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                rx.recharts.x_axis(
                    data_key="time",
                    axis_line=False,
                    tick_line=False,
                    tick={"fontSize": 12, "fill": "#6B7280"},
                    dy=10,
                ),
                rx.recharts.y_axis(
                    axis_line=False,
                    tick_line=False,
                    tick={"fontSize": 12, "fill": "#6B7280"},
                    dx=-10,
                ),
                rx.recharts.area(
                    type_="monotone",
                    data_key="value",
                    stroke="#3B82F6",
                    stroke_width=2,
                    fill="#3B82F6",
                    fill_opacity=0.3,
                    active_dot={"r": 6, "strokeWidth": 0},
                ),
                data=DashboardState.chart_data,
                height=300,
                width="100%",
            ),
            rx.el.div(
                rx.el.p(
                    "No data available for the selected period",
                    class_name="text-gray-400 text-sm",
                ),
                class_name="h-[300px] flex items-center justify-center border border-dashed border-gray-200 rounded-lg",
            ),
        ),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
    )