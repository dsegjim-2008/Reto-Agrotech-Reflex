import reflex as rx
from app.components.navbar import navbar
from app.states.auth_state import AuthState


def code_block(code: str) -> rx.Component:
    return rx.el.div(
        rx.el.pre(
            rx.el.code(code, class_name="text-sm font-mono text-gray-100"),
            class_name="overflow-x-auto",
        ),
        class_name="bg-gray-800 p-4 rounded-lg my-4 shadow-inner",
    )


def endpoint_doc(
    method: str, path: str, desc: str, payload: str = "", response: str = ""
) -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.span(
                method,
                class_name=f"px-2 py-1 rounded text-xs font-bold mr-3 {('bg-green-100 text-green-700' if method == 'POST' else 'bg-blue-100 text-blue-700')}",
            ),
            rx.el.code(path, class_name="text-sm font-mono text-gray-800"),
            class_name="flex items-center mb-2",
        ),
        rx.el.p(desc, class_name="text-gray-600 text-sm mb-3"),
        rx.cond(
            payload,
            rx.el.div(
                rx.el.p(
                    "Request Payload",
                    class_name="text-xs font-bold text-gray-500 uppercase mb-1",
                ),
                code_block(payload),
            ),
        ),
        rx.cond(
            response,
            rx.el.div(
                rx.el.p(
                    "Response Example",
                    class_name="text-xs font-bold text-gray-500 uppercase mb-1",
                ),
                code_block(response),
            ),
        ),
        class_name="border-b border-gray-200 pb-6 mb-6 last:border-0",
    )


def api_docs_page() -> rx.Component:
    return rx.el.div(
        navbar(),
        rx.el.div(
            rx.el.div(
                rx.el.h1(
                    "API Documentation", class_name="text-3xl font-bold text-gray-900"
                ),
                rx.el.p(
                    "Integrate your sensors with Agrotech",
                    class_name="text-gray-500 mt-1",
                ),
                class_name="mb-8",
            ),
            rx.el.div(
                rx.el.h2(
                    "Authentication", class_name="text-xl font-bold text-gray-800 mb-4"
                ),
                rx.el.div(
                    rx.el.p(
                        "All API requests must include your API Key in the header.",
                        class_name="text-gray-600 mb-2",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Header Name:",
                            class_name="font-semibold text-gray-700 mr-2",
                        ),
                        rx.el.code(
                            "X-API-Key",
                            class_name="bg-gray-100 px-1 rounded text-sm font-mono text-red-600",
                        ),
                        class_name="mb-2",
                    ),
                    rx.el.div(
                        rx.el.span(
                            "Your API Key:",
                            class_name="font-semibold text-gray-700 mr-2",
                        ),
                        rx.cond(
                            AuthState.user,
                            rx.el.code(
                                AuthState.user.api_key,
                                class_name="bg-blue-50 px-2 py-1 rounded text-sm font-mono text-blue-600 border border-blue-100",
                            ),
                            rx.el.span(
                                "Please log in to view your API key",
                                class_name="text-gray-400 italic",
                            ),
                        ),
                        class_name="flex items-center",
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm mb-8",
                ),
                rx.el.h2(
                    "Endpoints", class_name="text-xl font-bold text-gray-800 mb-4"
                ),
                rx.el.div(
                    endpoint_doc(
                        "POST",
                        "/api/sensors/{sensor_id}/data",
                        "Ingest a new reading for a specific sensor. Triggers alerts if thresholds are exceeded.",
                        """{
  "value": 25.4,
  "timestamp": "2023-10-27T10:00:00Z"  // optional
}""",
                        """{
  "status": "success",
  "alert_triggered": false
}""",
                    ),
                    endpoint_doc(
                        "GET",
                        "/api/parcels",
                        "Retrieve a list of all parcels associated with your account.",
                        "",
                        """[
  {
    "id": 1,
    "name": "North Field",
    "location": "Zone A",
    "size": 15.5,
    "crop_type": "Corn"
  }
]""",
                    ),
                    endpoint_doc(
                        "GET",
                        "/api/parcels/{id}/sensors",
                        "Retrieve all sensors and their status for a given parcel.",
                        "",
                        """[
  {
    "id": 5,
    "name": "Temp Sensor 1",
    "type": "temperature",
    "last_reading": 24.5
  }
]""",
                    ),
                    class_name="bg-white p-6 rounded-xl border border-gray-200 shadow-sm",
                ),
                class_name="w-full",
            ),
            class_name="max-w-4xl mx-auto px-4 sm:px-6 lg:px-8 py-8",
        ),
        class_name="min-h-screen bg-gray-50 font-['Roboto']",
    )