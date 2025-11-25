import reflex as rx
from app.states.parcel_state import ParcelState
from app.states.auth_state import AuthState
from app.components.navbar import navbar
from app.database import Parcel


def parcel_card(parcel: Parcel) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(
                rx.icon("map-pin", class_name="h-5 w-5 text-blue-500 mr-2"),
                rx.el.h3(parcel.name, class_name="text-lg font-semibold text-gray-900"),
                class_name="flex items-center mb-2",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.span("Location:", class_name="text-gray-500 text-sm"),
                    rx.el.span(
                        parcel.location,
                        class_name="ml-1 text-sm font-medium text-gray-900",
                    ),
                    class_name="flex items-center",
                ),
                rx.el.div(
                    rx.el.span("Crop:", class_name="text-gray-500 text-sm"),
                    rx.el.span(
                        parcel.crop_type,
                        class_name="ml-1 text-sm font-medium text-gray-900",
                    ),
                    class_name="flex items-center mt-1",
                ),
                rx.el.div(
                    rx.el.span("Size:", class_name="text-gray-500 text-sm"),
                    rx.el.span(
                        f"{parcel.size} ha",
                        class_name="ml-1 text-sm font-medium text-gray-900",
                    ),
                    class_name="flex items-center mt-1",
                ),
                class_name="mb-4",
            ),
            rx.el.div(
                rx.el.button(
                    "View Details",
                    on_click=rx.redirect(f"/parcels/{parcel.id}"),
                    class_name="flex-1 bg-blue-50 text-blue-600 text-sm font-medium py-2 rounded-md hover:bg-blue-100 transition-colors",
                ),
                rx.el.button(
                    rx.icon("pencil", class_name="h-4 w-4"),
                    on_click=ParcelState.open_edit_parcel_modal(parcel),
                    class_name="p-2 text-gray-400 hover:text-blue-600 transition-colors",
                ),
                rx.el.button(
                    rx.icon("trash-2", class_name="h-4 w-4"),
                    on_click=ParcelState.confirm_delete_parcel(parcel.id),
                    class_name="p-2 text-gray-400 hover:text-red-600 transition-colors",
                ),
                class_name="flex items-center gap-2",
            ),
            class_name="p-5",
        ),
        class_name="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-shadow",
    )


def parcel_modal() -> rx.Component:
    return rx.dialog.root(
        rx.dialog.content(
            rx.dialog.title(
                rx.cond(ParcelState.editing_parcel, "Edit Parcel", "Add New Parcel"),
                class_name="text-xl font-bold mb-4",
            ),
            rx.el.form(
                rx.el.div(
                    rx.el.label(
                        "Parcel Name",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="name",
                        placeholder="North Field",
                        default_value=rx.cond(
                            ParcelState.editing_parcel,
                            ParcelState.editing_parcel.name,
                            "",
                        ),
                        required=True,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Location",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="location",
                        placeholder="Coordinates or Address",
                        default_value=rx.cond(
                            ParcelState.editing_parcel,
                            ParcelState.editing_parcel.location,
                            "",
                        ),
                        required=True,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Crop Type",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="crop_type",
                        placeholder="Wheat, Corn, etc.",
                        default_value=rx.cond(
                            ParcelState.editing_parcel,
                            ParcelState.editing_parcel.crop_type,
                            "",
                        ),
                        required=True,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none",
                    ),
                    class_name="mb-4",
                ),
                rx.el.div(
                    rx.el.label(
                        "Size (Hectares)",
                        class_name="block text-sm font-medium text-gray-700 mb-1",
                    ),
                    rx.el.input(
                        name="size",
                        type="number",
                        step="0.01",
                        placeholder="15.5",
                        default_value=rx.cond(
                            ParcelState.editing_parcel,
                            ParcelState.editing_parcel.size.to_string(),
                            "",
                        ),
                        required=True,
                        class_name="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 outline-none",
                    ),
                    class_name="mb-6",
                ),
                rx.el.div(
                    rx.el.button(
                        "Cancel",
                        type="button",
                        on_click=ParcelState.close_parcel_modal,
                        class_name="px-4 py-2 text-gray-700 bg-gray-100 rounded-lg hover:bg-gray-200 mr-2",
                    ),
                    rx.el.button(
                        "Save Parcel",
                        type="submit",
                        class_name="px-4 py-2 text-white bg-blue-600 rounded-lg hover:bg-blue-700",
                    ),
                    class_name="flex justify-end",
                ),
                on_submit=ParcelState.save_parcel,
            ),
            class_name="max-w-md",
        ),
        open=ParcelState.is_parcel_modal_open,
        on_open_change=ParcelState.close_parcel_modal,
    )


def parcels_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h1(
                        "My Parcels", class_name="text-2xl font-bold text-gray-900"
                    ),
                    rx.el.p(
                        "Manage your agricultural land", class_name="text-gray-500 mt-1"
                    ),
                ),
                rx.el.button(
                    rx.icon("plus", class_name="h-5 w-5 mr-2"),
                    "Add Parcel",
                    on_click=ParcelState.open_add_parcel_modal,
                    class_name="flex items-center bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors shadow-sm",
                ),
                class_name="flex justify-between items-center mb-8",
            ),
            rx.cond(
                ParcelState.parcels,
                rx.el.div(
                    rx.foreach(ParcelState.parcels, parcel_card),
                    class_name="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6",
                ),
                rx.el.div(
                    rx.icon("sprout", class_name="h-16 w-16 text-gray-200 mb-4"),
                    rx.el.h3(
                        "No parcels yet", class_name="text-lg font-medium text-gray-900"
                    ),
                    rx.el.p(
                        "Get started by adding your first parcel.",
                        class_name="text-gray-500 mt-2",
                    ),
                    class_name="flex flex-col items-center justify-center py-16 bg-white rounded-2xl border border-dashed border-gray-300",
                ),
            ),
            parcel_modal(),
            rx.alert_dialog.root(
                rx.alert_dialog.content(
                    rx.alert_dialog.title("Confirm Deletion"),
                    rx.alert_dialog.description(
                        "Are you sure you want to delete this parcel? This action cannot be undone and will remove all associated sensors.",
                        class_name="mb-4",
                    ),
                    rx.el.div(
                        rx.alert_dialog.cancel(
                            rx.el.button(
                                "Cancel",
                                on_click=ParcelState.cancel_delete_parcel,
                                class_name="bg-gray-100 text-gray-700 px-4 py-2 rounded-lg hover:bg-gray-200 mr-2",
                            )
                        ),
                        rx.alert_dialog.action(
                            rx.el.button(
                                "Delete",
                                on_click=ParcelState.delete_parcel,
                                class_name="bg-red-600 text-white px-4 py-2 rounded-lg hover:bg-red-700",
                            )
                        ),
                        class_name="flex justify-end",
                    ),
                ),
                open=ParcelState.is_delete_parcel_dialog_open,
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="min-h-screen bg-gray-50 font-['Roboto']",
    )