import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState
from app.states.settings_state import SettingsState


def profile_tab() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Profile Information", class_name="text-lg font-medium text-gray-900"),
        rx.el.p("View your account details", class_name="text-sm text-gray-500 mb-6"),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Username", class_name="block text-sm font-medium text-gray-700"
                ),
                rx.el.div(
                    AuthState.user.username,
                    class_name="mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-md text-gray-700",
                ),
                class_name="col-span-6 sm:col-span-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Email Address",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.div(
                    AuthState.user.email,
                    class_name="mt-1 block w-full px-3 py-2 bg-gray-50 border border-gray-300 rounded-md text-gray-700",
                ),
                class_name="col-span-6 sm:col-span-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Role", class_name="block text-sm font-medium text-gray-700"
                ),
                rx.el.div(
                    rx.el.span(
                        AuthState.user.role,
                        class_name="inline-flex items-center px-2.5 py-0.5 rounded-full text-xs font-medium bg-blue-100 text-blue-800 uppercase",
                    ),
                    class_name="mt-1",
                ),
                class_name="col-span-6 sm:col-span-4",
            ),
            class_name="grid grid-cols-6 gap-6",
        ),
        class_name="space-y-6",
    )


def security_tab() -> rx.Component:
    return rx.el.div(
        rx.el.h3("Security Settings", class_name="text-lg font-medium text-gray-900"),
        rx.el.p("Manage your password", class_name="text-sm text-gray-500 mb-6"),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "New Password", class_name="block text-sm font-medium text-gray-700"
                ),
                rx.el.input(
                    type="password",
                    on_change=SettingsState.set_new_password,
                    class_name="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                    default_value=SettingsState.new_password,
                ),
                class_name="col-span-6 sm:col-span-4",
            ),
            rx.el.div(
                rx.el.label(
                    "Confirm Password",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.input(
                    type="password",
                    on_change=SettingsState.set_confirm_password,
                    class_name="mt-1 block w-full px-3 py-2 border border-gray-300 rounded-md shadow-sm focus:ring-blue-500 focus:border-blue-500 sm:text-sm",
                    default_value=SettingsState.confirm_password,
                ),
                class_name="col-span-6 sm:col-span-4",
            ),
            rx.el.div(
                rx.el.button(
                    "Update Password",
                    on_click=SettingsState.update_password,
                    class_name="inline-flex justify-center py-2 px-4 border border-transparent shadow-sm text-sm font-medium rounded-md text-white bg-blue-600 hover:bg-blue-700 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                ),
                class_name="col-span-6",
            ),
            class_name="grid grid-cols-6 gap-6",
        ),
        class_name="space-y-6",
    )


def api_tab() -> rx.Component:
    return rx.el.div(
        rx.el.h3("API Configuration", class_name="text-lg font-medium text-gray-900"),
        rx.el.p("Manage your API access keys", class_name="text-sm text-gray-500 mb-6"),
        rx.el.div(
            rx.el.div(
                rx.el.label(
                    "Current API Key",
                    class_name="block text-sm font-medium text-gray-700",
                ),
                rx.el.div(
                    rx.el.code(
                        AuthState.user.api_key,
                        class_name="font-mono text-sm text-gray-800 bg-gray-100 px-2 py-1 rounded border border-gray-200 block overflow-x-auto",
                    ),
                    class_name="mt-1 flex rounded-md shadow-sm",
                ),
                rx.el.p(
                    "Keep this key secret. It allows full access to your sensor data.",
                    class_name="mt-2 text-sm text-gray-500",
                ),
                class_name="col-span-6",
            ),
            rx.el.div(
                rx.el.button(
                    rx.icon("refresh-cw", class_name="h-4 w-4 mr-2"),
                    "Regenerate Key",
                    on_click=SettingsState.regenerate_api_key,
                    class_name="inline-flex items-center px-4 py-2 border border-gray-300 shadow-sm text-sm font-medium rounded-md text-gray-700 bg-white hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-500",
                ),
                class_name="col-span-6",
            ),
            class_name="grid grid-cols-6 gap-6",
        ),
        class_name="space-y-6",
    )


def settings_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "Account Settings", class_name="text-3xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Manage your profile and preferences",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.div(
                    rx.el.nav(
                        rx.el.button(
                            rx.icon("user", class_name="h-5 w-5 mr-3 text-gray-500"),
                            "Profile",
                            on_click=lambda: SettingsState.set_active_tab_val(
                                "profile"
                            ),
                            class_name=rx.cond(
                                SettingsState.active_tab == "profile",
                                "bg-blue-50 border-l-4 border-blue-600 text-blue-700 flex items-center px-3 py-3 text-sm font-medium w-full",
                                "border-l-4 border-transparent text-gray-900 hover:bg-gray-50 hover:text-gray-900 flex items-center px-3 py-3 text-sm font-medium w-full",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("lock", class_name="h-5 w-5 mr-3 text-gray-500"),
                            "Security",
                            on_click=lambda: SettingsState.set_active_tab_val(
                                "security"
                            ),
                            class_name=rx.cond(
                                SettingsState.active_tab == "security",
                                "bg-blue-50 border-l-4 border-blue-600 text-blue-700 flex items-center px-3 py-3 text-sm font-medium w-full",
                                "border-l-4 border-transparent text-gray-900 hover:bg-gray-50 hover:text-gray-900 flex items-center px-3 py-3 text-sm font-medium w-full",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("key", class_name="h-5 w-5 mr-3 text-gray-500"),
                            "API Key",
                            on_click=lambda: SettingsState.set_active_tab_val("api"),
                            class_name=rx.cond(
                                SettingsState.active_tab == "api",
                                "bg-blue-50 border-l-4 border-blue-600 text-blue-700 flex items-center px-3 py-3 text-sm font-medium w-full",
                                "border-l-4 border-transparent text-gray-900 hover:bg-gray-50 hover:text-gray-900 flex items-center px-3 py-3 text-sm font-medium w-full",
                            ),
                        ),
                        rx.el.button(
                            rx.icon("bell", class_name="h-5 w-5 mr-3 text-gray-500"),
                            "Notifications",
                            class_name="border-l-4 border-transparent text-gray-400 cursor-not-allowed flex items-center px-3 py-3 text-sm font-medium w-full",
                        ),
                        class_name="space-y-1",
                    ),
                    class_name="col-span-12 md:col-span-3",
                ),
                rx.el.div(
                    rx.cond(
                        SettingsState.active_tab == "profile",
                        profile_tab(),
                        rx.cond(
                            SettingsState.active_tab == "security",
                            security_tab(),
                            api_tab(),
                        ),
                    ),
                    class_name="col-span-12 md:col-span-9 bg-white shadow rounded-lg p-6",
                ),
                class_name="grid grid-cols-12 gap-6",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="min-h-screen bg-gray-50 font-['Roboto']",
    )