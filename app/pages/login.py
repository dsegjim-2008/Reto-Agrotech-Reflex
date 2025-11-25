import reflex as rx
from app.states.auth_state import AuthState
from app.components.navbar import navbar


def login_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.div(
                    rx.el.h2(
                        "Welcome Back",
                        class_name="text-3xl font-bold text-gray-900 text-center mb-2",
                    ),
                    rx.el.p(
                        "Enter your credentials to access your farm dashboard",
                        class_name="text-gray-500 text-center mb-8",
                    ),
                    rx.el.div(
                        rx.el.div(
                            rx.el.label(
                                "Email Address",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="email",
                                placeholder="you@example.com",
                                on_change=AuthState.set_login_email,
                                class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all",
                                default_value=AuthState.login_email,
                            ),
                            class_name="mb-4",
                        ),
                        rx.el.div(
                            rx.el.label(
                                "Password",
                                class_name="block text-sm font-medium text-gray-700 mb-1",
                            ),
                            rx.el.input(
                                type="password",
                                placeholder="••••••••",
                                on_change=AuthState.set_login_password,
                                class_name="w-full px-4 py-2 rounded-lg border border-gray-300 focus:ring-2 focus:ring-blue-500 focus:border-blue-500 outline-none transition-all",
                                default_value=AuthState.login_password,
                            ),
                            class_name="mb-6",
                        ),
                        rx.el.button(
                            "Sign In",
                            on_click=AuthState.login,
                            class_name="w-full bg-blue-600 text-white font-semibold py-2.5 rounded-lg hover:bg-blue-700 transition-colors shadow-md hover:shadow-lg transform active:scale-[0.98] duration-200",
                        ),
                        class_name="space-y-4",
                    ),
                    rx.el.div(
                        rx.el.p(
                            "Don't have an account? ",
                            rx.el.a(
                                "Register",
                                href="/register",
                                class_name="text-blue-600 hover:text-blue-700 font-semibold",
                            ),
                            class_name="text-sm text-center text-gray-600",
                        ),
                        class_name="mt-6",
                    ),
                    class_name="bg-white p-8 rounded-2xl shadow-xl border border-gray-100 w-full max-w-md",
                ),
                class_name="flex items-center justify-center min-h-[calc(100vh-4rem)] px-4",
            ),
            class_name="bg-gray-50/50",
        ),
        class_name="font-['Roboto'] min-h-screen",
    )