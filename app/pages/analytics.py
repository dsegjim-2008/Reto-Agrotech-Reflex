import reflex as rx
from app.states.analytics_state import AnalyticsState
from app.components.navbar import navbar


def sidebar_sensor_select() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Select Sensors",
            class_name="text-sm font-semibold text-gray-500 uppercase tracking-wider mb-4",
        ),
        rx.el.div(
            rx.foreach(
                AnalyticsState.available_sensors,
                lambda sensor: rx.el.label(
                    rx.el.input(
                        type="checkbox",
                        checked=AnalyticsState.selected_sensor_ids.contains(
                            sensor["id"]
                        ),
                        on_change=lambda c: AnalyticsState.toggle_sensor(
                            sensor["id"], c
                        ),
                        class_name="rounded border-gray-300 text-blue-600 focus:ring-blue-500 h-4 w-4 mr-3",
                    ),
                    rx.el.div(
                        rx.el.span(
                            sensor["name"],
                            class_name="block text-sm font-medium text-gray-900",
                        ),
                        rx.el.span(
                            f"{sensor['parcel_name']} • {sensor['type']}",
                            class_name="block text-xs text-gray-500",
                        ),
                        class_name="flex-1",
                    ),
                    class_name="flex items-start p-3 hover:bg-gray-50 rounded-lg transition-colors cursor-pointer border border-transparent hover:border-gray-200",
                ),
            ),
            class_name="space-y-1 max-h-[calc(100vh-300px)] overflow-y-auto pr-2",
        ),
        class_name="w-full md:w-64 flex-shrink-0 bg-white p-4 rounded-xl border border-gray-200 h-fit",
    )


def controls_bar() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Range", class_name="block text-xs font-medium text-gray-700 mb-1"
                ),
                rx.el.select(
                    rx.el.option("Last 7 Days", value="7d"),
                    rx.el.option("Last 30 Days", value="30d"),
                    rx.el.option("Last 90 Days", value="90d"),
                    rx.el.option("Custom Range", value="custom"),
                    value=AnalyticsState.date_range_preset,
                    on_change=AnalyticsState.set_range_preset,
                    class_name="block w-36 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm",
                ),
                class_name="mr-4",
            ),
            rx.el.div(
                rx.el.label(
                    "From", class_name="block text-xs font-medium text-gray-700 mb-1"
                ),
                rx.el.input(
                    type="date",
                    on_change=AnalyticsState.set_custom_start_date,
                    disabled=AnalyticsState.date_range_preset != "custom",
                    class_name="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100 disabled:text-gray-400",
                    default_value=AnalyticsState.start_date,
                ),
                class_name="mr-2",
            ),
            rx.el.div(
                rx.el.label(
                    "To", class_name="block text-xs font-medium text-gray-700 mb-1"
                ),
                rx.el.input(
                    type="date",
                    on_change=AnalyticsState.set_custom_end_date,
                    disabled=AnalyticsState.date_range_preset != "custom",
                    class_name="block w-full rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm disabled:bg-gray-100 disabled:text-gray-400",
                    default_value=AnalyticsState.end_date,
                ),
                class_name="mr-4",
            ),
            class_name="flex items-end",
        ),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Aggregation",
                    class_name="block text-xs font-medium text-gray-700 mb-1",
                ),
                rx.el.select(
                    rx.el.option("Raw Data", value="raw"),
                    rx.el.option("Hourly Avg", value="hour"),
                    rx.el.option("Daily Avg", value="day"),
                    value=AnalyticsState.aggregation,
                    on_change=AnalyticsState.set_aggregation_val,
                    class_name="block w-32 rounded-md border-gray-300 shadow-sm focus:border-blue-500 focus:ring-blue-500 sm:text-sm",
                ),
                class_name="mr-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Chart Type",
                    class_name="block text-xs font-medium text-gray-700 mb-1",
                ),
                rx.el.div(
                    rx.el.button(
                        rx.icon("chart-line", class_name="h-4 w-4"),
                        on_click=lambda: AnalyticsState.set_chart_type_val("line"),
                        class_name=rx.cond(
                            AnalyticsState.chart_type == "line",
                            "p-2 bg-blue-100 text-blue-600 rounded-l-md border border-blue-200",
                            "p-2 bg-white text-gray-500 hover:text-gray-700 rounded-l-md border border-gray-300",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("chart-area", class_name="h-4 w-4"),
                        on_click=lambda: AnalyticsState.set_chart_type_val("area"),
                        class_name=rx.cond(
                            AnalyticsState.chart_type == "area",
                            "p-2 bg-blue-100 text-blue-600 border-y border-r border-blue-200",
                            "p-2 bg-white text-gray-500 hover:text-gray-700 border-y border-r border-gray-300",
                        ),
                    ),
                    rx.el.button(
                        rx.icon("chart-bar", class_name="h-4 w-4"),
                        on_click=lambda: AnalyticsState.set_chart_type_val("bar"),
                        class_name=rx.cond(
                            AnalyticsState.chart_type == "bar",
                            "p-2 bg-blue-100 text-blue-600 rounded-r-md border-y border-r border-blue-200",
                            "p-2 bg-white text-gray-500 hover:text-gray-700 rounded-r-md border-y border-r border-gray-300",
                        ),
                    ),
                    class_name="flex shadow-sm",
                ),
            ),
            class_name="flex items-end",
        ),
        rx.el.div(
            rx.el.button(
                rx.icon("download", class_name="h-4 w-4 mr-2"),
                "CSV",
                on_click=AnalyticsState.download_csv,
                class_name="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500 mr-2",
            ),
            rx.el.button(
                rx.icon("file-json", class_name="h-4 w-4 mr-2"),
                "JSON",
                on_click=AnalyticsState.download_json,
                class_name="inline-flex items-center px-3 py-2 border border-gray-300 shadow-sm text-sm leading-4 font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
            ),
            class_name="flex items-end ml-auto",
        ),
        class_name="flex flex-col md:flex-row gap-4 p-4 bg-white rounded-xl border border-gray-200 shadow-sm mb-6",
    )


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


def custom_legend() -> rx.Component:
    return rx.el.div(
        rx.foreach(
            AnalyticsState.current_sensors_legend,
            lambda item: rx.el.div(
                rx.el.span(
                    class_name="w-3 h-3 rounded-full mr-2",
                    style={"backgroundColor": item["color"]},
                ),
                rx.el.span(item["name"], class_name="text-sm text-gray-600"),
                class_name="flex items-center mr-6",
            ),
        ),
        class_name="flex flex-wrap items-center justify-center mt-4 px-4",
    )


def analytics_chart() -> rx.Component:
    return rx.el.div(
        rx.cond(
            AnalyticsState.is_loading,
            rx.el.div(
                rx.spinner(size="3"),
                rx.el.p("Loading data...", class_name="text-gray-500 mt-4"),
                class_name="flex flex-col items-center justify-center h-[400px]",
            ),
            rx.cond(
                AnalyticsState.chart_data,
                rx.el.div(
                    rx.recharts.composed_chart(
                        rx.recharts.cartesian_grid(
                            stroke_dasharray="3 3",
                            vertical=False,
                            class_name="stroke-gray-200",
                        ),
                        rx.recharts.graphing_tooltip(**TOOLTIP_PROPS),
                        rx.recharts.x_axis(
                            data_key="name",
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
                        rx.foreach(
                            AnalyticsState.current_sensors_legend,
                            lambda item: rx.match(
                                AnalyticsState.chart_type,
                                (
                                    "line",
                                    rx.recharts.line(
                                        data_key=item["data_key"],
                                        stroke=item["color"],
                                        stroke_width=2,
                                        dot=False,
                                        type_="monotone",
                                        name=item["name"],
                                    ),
                                ),
                                (
                                    "area",
                                    rx.recharts.area(
                                        data_key=item["data_key"],
                                        stroke=item["color"],
                                        fill=item["color"],
                                        fill_opacity=0.2,
                                        type_="monotone",
                                        name=item["name"],
                                    ),
                                ),
                                (
                                    "bar",
                                    rx.recharts.bar(
                                        data_key=item["data_key"],
                                        fill=item["color"],
                                        name=item["name"],
                                        radius=[4, 4, 0, 0],
                                    ),
                                ),
                                rx.recharts.line(
                                    data_key=item["data_key"], stroke=item["color"]
                                ),
                            ),
                        ),
                        data=AnalyticsState.chart_data,
                        height=400,
                        width="100%",
                    ),
                    custom_legend(),
                    class_name="w-full",
                ),
                rx.el.div(
                    rx.icon("bar-chart-2", class_name="h-12 w-12 text-gray-300 mb-2"),
                    rx.el.p(
                        "No data available", class_name="text-gray-500 font-medium"
                    ),
                    rx.el.p(
                        "Try selecting different sensors or date range",
                        class_name="text-gray-400 text-sm mt-1",
                    ),
                    class_name="flex flex-col items-center justify-center h-[400px] border border-dashed border-gray-200 rounded-lg bg-gray-50",
                ),
            ),
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mb-6",
    )


def stats_table() -> rx.Component:
    return rx.el.div(
        rx.el.h3(
            "Statistics Overview", class_name="text-lg font-semibold text-gray-900 mb-4"
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
                            "Type",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Min",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Max",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Avg",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                        rx.el.th(
                            "Count",
                            class_name="px-6 py-3 text-left text-xs font-medium text-gray-500 uppercase tracking-wider",
                        ),
                    ),
                    class_name="bg-gray-50",
                ),
                rx.el.tbody(
                    rx.foreach(
                        AnalyticsState.sensor_stats,
                        lambda stat: rx.el.tr(
                            rx.el.td(
                                stat["name"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm font-medium text-gray-900",
                            ),
                            rx.el.td(
                                stat["parcel"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
                            ),
                            rx.el.td(
                                stat["type"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500 capitalize",
                            ),
                            rx.el.td(
                                stat["min"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900",
                            ),
                            rx.el.td(
                                stat["max"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-900",
                            ),
                            rx.el.td(
                                stat["avg"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm font-bold text-gray-900",
                            ),
                            rx.el.td(
                                stat["count"],
                                class_name="px-6 py-4 whitespace-nowrap text-sm text-gray-500",
                            ),
                        ),
                    ),
                    class_name="bg-white divide-y divide-gray-200",
                ),
                class_name="min-w-full divide-y divide-gray-200",
            ),
            class_name="overflow-x-auto border border-gray-200 rounded-lg",
        ),
        class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
    )


def analytics_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1("Analytics", class_name="text-3xl font-bold text-gray-900"),
                rx.el.p(
                    "Deep dive into your historical sensor data",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                sidebar_sensor_select(),
                rx.el.div(
                    controls_bar(),
                    analytics_chart(),
                    stats_table(),
                    class_name="flex-1 min-w-0",
                ),
                class_name="flex flex-col md:flex-row gap-8",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="min-h-screen bg-gray-50 font-['Roboto']",
    )