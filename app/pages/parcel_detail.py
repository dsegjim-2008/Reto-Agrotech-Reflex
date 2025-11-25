import reflex as rx
from app.states.parcel_state import ParcelState
from app.components.navbar import navbar
from app.database import Sensor


def get_sensor_icon(sensor_type: str):
    return rx.match(
        sensor_type,
        ("temperature", rx.icon("thermometer", class_name="h-5 w-5 text-red-500")),
        ("soil_humidity", rx.icon("droplets", class_name="h-5 w-5 text-blue-500")),
        ("luminosity", rx.icon("sun", class_name="h-5 w-5 text-yellow-500")),
        ("ph_level", rx.icon("flask-conical", class_name="h-5 w-5 text-purple-500")),
        ("rain_gauge", rx.icon("cloud-rain", class_name="h-5 w-5 text-gray-500")),
        rx.icon("activity", class_name="h-5 w-5 text-gray-500"),
    )


def sensor_card(sensor: Sensor) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                get_sensor_icon(sensor.type),
                rx.el.span(sensor.name, class_name="font-semibold text-gray-900 ml-2"),
                rx.el.div(
                    rx.el.span(
                        sensor.status,
                        class_name=rx.cond(
                            sensor.status == "active",
                            "bg-green-100 text-green-700 text-xs font-bold px-2 py-0.5 rounded-full uppercase",
                            "bg-gray-100 text-gray-700 text-xs font-bold px-2 py-0.5 rounded-full uppercase",
                        ),
                    ),
                    class_name="ml-auto",
                ),
                class_name="flex items-center mb-3",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span("Type:", class_name="text-gray-500 text-xs"),
                    rx.el.span(
                        sensor.type,
                        class_name="text-gray-900 text-sm font-medium ml-1 capitalize",
                    ),
                    class_name="flex justify-between items-center",
                ),
                rx.el.div(
                    rx.el.span("Range:", class_name="text-gray-500 text-xs"),
                    rx.el.span(
                        f"{sensor.threshold_low} - {sensor.threshold_high}",
                        class_name="text-gray-900 text-sm font-medium ml-1",
                    ),
                    class_name="flex justify-between items-center mt-1",
                ),
                rx.el.div(
                    rx.el.span("Last Reading:", class_name="text-gray-500 text-xs"),
                    rx.el.span(
                        "--", class_name="text-gray-900 text-sm font-medium ml-1"
                    ),
                    class_name="flex justify-between items-center mt-1",
                ),
                class_name="space-y-1 mb-4 p-3 bg-gray-50 rounded-lg",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=ParcelState.open_edit_sensor_modal(sensor),
                    class_name="p-2 text-gray-400 hover:text-blue-600 transition-colors",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=ParcelState.confirm_delete_sensor(sensor.id),
                    class_name="p-2 text-gray-400 hover:text-red-600 transition-colors ml-2",
                ),
                class_name="flex justify-end border-t border-gray-100 pt-2",
            ),
            class_name="p-4",
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow",
    )


def sensor_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(ParcelState.editing_sensor, "Edit Sensor", "Add New Sensor"),
                class_name="text-xl font-bold mb-4",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Sensor Name",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="name",
                        placeholder="Sensor T-01",
                        default_value=rx.cond(
                            ParcelState.editing_sensor,
                            ParcelState.editing_sensor.name,
                            "",
                        ),
                        required=True,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Sensor Type",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.select(
                        rx.el.option("Temperature", value="temperature"),
                        rx.el.option("Soil Humidity", value="soil_humidity"),
                        rx.el.option("Luminosity", value="luminosity"),
                        rx.el.option("pH Level", value="ph_level"),
                        rx.el.option("Rain Gauge", value="rain_gauge"),
                        name="type",
                        default_value=rx.cond(
                            ParcelState.editing_sensor,
                            ParcelState.editing_sensor.type,
                            "temperature",
                        ),
                        required=True,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none bg-white",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.div(
                        rx.el.label(
                            "Min Threshold",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="threshold_low",
                            type="number",
                            step="0.1",
                            placeholder="0.0",
                            default_value=rx.cond(
                                ParcelState.editing_sensor,
                                ParcelState.editing_sensor.threshold_low.to_string(),
                                "0.0",
                            ),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none",
                        ),
                    ),
                    rx.el.div(
                        rx.el.label(
                            "Max Threshold",
                            class_name="block text-sm font-medium text-gray-700 mb-1",
                        ),
                        rx.el.input(
                            name="threshold_high",
                            type="number",
                            step="0.1",
                            placeholder="100.0",
                            default_value=rx.cond(
                                ParcelState.editing_sensor,
                                ParcelState.editing_sensor.threshold_high.to_string(),
                                "100.0",
                            ),
                            class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none",
                        ),
                    ),
                    class_name="grid grid-cols-2 gap-4 mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        type="button",
                        on_click=ParcelState.close_sensor_modal,
                        class_name="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 mr-2",
                    ),
                    rx.el.button(
                        "Save Sensor",
                        type="submit",
                        class_name="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                    ),
                    class_name="flex justify-end",
                ),
                on_submit=ParcelState.save_sensor,
            ),
            class_name="max-w-md",
        ),
        open=ParcelState.is_sensor_modal_open,
        on_open_change=ParcelState.close_sensor_modal,
    )


def parcel_detail_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.cond(
                ParcelState.current_parcel,
                rx.el.div(
                    rx.el.div(
                        rx.el.div(
                            rx.el.button(
                                rx.icon("arrow-left", class_name="h-4 w-4 mr-1"),
                                "Back to Parcels",
                                on_click=rx.redirect("/parcels"),
                                class_name="flex items-center text-gray-500 hover:text-gray-700 mb-4",
                            ),
                            rx.el.div(
                                rx.el.div(
                                    rx.el.h1(
                                        ParcelState.current_parcel.name,
                                        class_name="text-3xl font-bold text-gray-900",
                                    ),
                                    rx.el.div(
                                        rx.icon(
                                            "map-pin",
                                            class_name="h-4 w-4 text-gray-400 mr-1",
                                        ),
                                        rx.el.span(
                                            ParcelState.current_parcel.location,
                                            class_name="text-gray-500",
                                        ),
                                        class_name="flex items-center mt-1",
                                    ),
                                ),
                                rx.el.div(
                                    rx.el.div(
                                        rx.el.span(
                                            "Crop Type",
                                            class_name="block text-xs text-gray-500 uppercase tracking-wide",
                                        ),
                                        rx.el.span(
                                            ParcelState.current_parcel.crop_type,
                                            class_name="font-medium text-gray-900",
                                        ),
                                        class_name="bg-white px-4 py-2 rounded-lg border border-gray-200",
                                    ),
                                    rx.el.div(
                                        rx.el.span(
                                            "Size",
                                            class_name="block text-xs text-gray-500 uppercase tracking-wide",
                                        ),
                                        rx.el.span(
                                            f"{ParcelState.current_parcel.size} ha",
                                            class_name="font-medium text-gray-900",
                                        ),
                                        class_name="bg-white px-4 py-2 rounded-lg border border-gray-200 ml-4",
                                    ),
                                    class_name="flex items-center",
                                ),
                                class_name="flex flex-col md:flex-row md:justify-between md:items-center mb-8",
                            ),
                        ),
                        rx.el.div(
                            rx.el.h2(
                                "Sensors", class_name="text-xl font-bold text-gray-900"
                            ),
                            rx.el.button(
                                rx.icon("plus", class_name="h-5 w-5 mr-2"),
                                "Add Sensor",
                                on_click=ParcelState.open_add_sensor_modal,
                                class_name="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors shadow-sm",
                            ),
                            class_name="flex justify-between items-center mb-6 border-b border-gray-200 pb-4",
                        ),
                        rx.cond(
                            ParcelState.parcel_sensors,
                            rx.el.div(
                                rx.foreach(ParcelState.parcel_sensors, sensor_card),
                                class_name="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6",
                            ),
                            rx.el.div(
                                rx.icon(
                                    "thermometer",
                                    class_name="h-12 w-12 text-gray-200 mb-3",
                                ),
                                rx.el.p(
                                    "No sensors installed yet",
                                    class_name="text-gray-500",
                                ),
                                class_name="flex flex-col items-center justify-center py-12 bg-white rounded-xl border border-dashed border-gray-300",
                            ),
                        ),
                    ),
                    class_name="w-full",
                ),
                rx.el.div(
                    "Loading...",
                    class_name="flex justify-center items-center h-64 text-gray-400",
                ),
            ),
            sensor_modal(),
            rx.alert_dialog.root(
                rx.alert_dialog.content(
                    rx.alert_dialog.title("Confirm Deletion"),
                    rx.alert_dialog.description(
                        "Are you sure you want to delete this sensor? This will permanently remove all associated data.",
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.alert_dialog.cancel(
                            rx.el.button(
                                "Cancel",
                                on_click=ParcelState.cancel_delete_sensor,
                                class_name="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 mr-2",
                            )
                        ),
                        rx.alert_dialog.action(
                            rx.el.button(
                                "Delete",
                                on_click=ParcelState.delete_sensor,
                                class_name="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700",
                            )
                        ),
                        class_name="flex justify-end",
                    ),
                ),
                open=ParcelState.is_delete_sensor_dialog_open,
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="min-h-screen bg-gray-50 font-['Roboto']",
    )