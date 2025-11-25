import reflex as rx
from app.states.auth_state import AuthState
from app.states.navbar_state import NavbarState


def mobile_menu_item(text: str, href: str) -> rx.Component:
    return rx.el.a(
        text,
        href=href,
        class_name="block px-3 py-2 rounded-md text-base font-medium text-gray-700 hover:text-gray-900 hover:bg-gray-50",
        on_click=NavbarState.close_menu,
    )


def navbar() -> rx.Component:
    return rx.el.nav(
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.a(
                        rx.icon("sprout", class_name="h-6 w-6 text-green-500 mr-2"),
                        rx.el.span(
                            "Agro", class_name="text-xl font-bold text-gray-900"
                        ),
                        rx.el.span(
                            "Tech", class_name="text-xl font-bold text-blue-600"
                        ),
                        href="/",
                        class_name="flex items-center",
                    ),
                    rx.el.div(
                        rx.el.button(
                            rx.cond(
                                NavbarState.is_menu_open,
                                rx.icon("x", class_name="h-6 w-6"),
                                rx.icon("menu", class_name="h-6 w-6"),
                            ),
                            on_click=NavbarState.toggle_menu,
                            class_name="inline-flex items-center justify-center p-2 rounded-md text-gray-400 hover:text-gray-500 hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-inset focus:ring-blue-500",
                        ),
                        class_name="-mr-2 flex md:hidden",
                    ),
                    class_name="flex items-center justify-between w-full md:w-auto",
                ),
                rx.el.div(
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.el.div(
                            rx.el.div(
                                rx.el.a(
                                    "Dashboard",
                                    href="/",
                                    class_name="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors mr-6",
                                ),
                                rx.el.a(
                                    "Parcels",
                                    href="/parcels",
                                    class_name="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors mr-6",
                                ),
                                rx.el.a(
                                    "Analytics",
                                    href="/analytics",
                                    class_name="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors mr-6",
                                ),
                                rx.el.a(
                                    "Alerts",
                                    href="/alerts",
                                    class_name="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors mr-6",
                                ),
                                rx.el.a(
                                    "Settings",
                                    href="/settings",
                                    class_name="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors mr-6",
                                ),
                                class_name="hidden md:flex mr-4 border-r border-gray-200 pr-4",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Role: ",
                                    class_name="text-gray-500 text-sm hidden lg:inline",
                                ),
                                rx.el.span(
                                    AuthState.user.role,
                                    class_name="text-xs font-semibold uppercase bg-blue-100 text-blue-700 px-2 py-0.5 rounded-full ml-1 hidden lg:inline-block",
                                ),
                                class_name="flex items-center mr-6",
                            ),
                            rx.el.div(
                                rx.el.span(
                                    "Hi, ", class_name="text-gray-500 hidden sm:inline"
                                ),
                                rx.el.span(
                                    AuthState.user.username,
                                    class_name="font-semibold text-gray-900 hidden sm:inline",
                                ),
                                class_name="mr-6",
                            ),
                            rx.el.button(
                                "Logout",
                                on_click=AuthState.logout,
                                class_name="text-sm font-medium text-red-600 hover:text-red-700 transition-colors",
                            ),
                            class_name="hidden md:flex items-center",
                        ),
                        rx.el.div(
                            rx.el.a(
                                "Login",
                                href="/login",
                                class_name="text-sm font-medium text-gray-600 hover:text-blue-600 transition-colors mr-6",
                            ),
                            rx.el.a(
                                "Get Started",
                                href="/register",
                                class_name="text-sm font-medium bg-blue-600 text-white px-4 py-2 rounded-lg hover:bg-blue-700 transition-colors shadow-sm hover:shadow-md",
                            ),
                            class_name="hidden md:flex items-center",
                        ),
                    ),
                    class_name="flex items-center",
                ),
                class_name="flex items-center justify-between h-16",
            ),
            class_name="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8",
        ),
        rx.cond(
            NavbarState.is_menu_open,
            rx.el.div(
                rx.el.div(
                    rx.cond(
                        AuthState.is_authenticated,
                        rx.el.div(
                            mobile_menu_item("Dashboard", "/"),
                            mobile_menu_item("Parcels", "/parcels"),
                            mobile_menu_item("Analytics", "/analytics"),
                            mobile_menu_item("Alerts", "/alerts"),
                            mobile_menu_item("Settings", "/settings"),
                            mobile_menu_item("API Docs", "/api-docs"),
                            rx.el.div(
                                rx.el.button(
                                    "Logout",
                                    on_click=AuthState.logout,
                                    class_name="block w-full text-left px-3 py-2 rounded-md text-base font-medium text-red-600 hover:text-red-700 hover:bg-red-50",
                                ),
                                class_name="mt-2 border-t border-gray-200 pt-2",
                            ),
                        ),
                        rx.el.div(
                            mobile_menu_item("Login", "/login"),
                            mobile_menu_item("Register", "/register"),
                        ),
                    ),
                    class_name="px-2 pt-2 pb-3 space-y-1 sm:px-3",
                ),
                class_name="md:hidden bg-white border-t border-gray-200 shadow-lg absolute w-full left-0",
            ),
        ),
        class_name="bg-white border-b border-gray-200 sticky top-0 z-50 backdrop-blur-lg bg-opacity-90",
    )