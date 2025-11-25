import reflex as rx


def skeleton_card() -> rx.Component:
    return rx.el.div(
        rx.el.div(class_name="h-10 w-10 bg-gray-200 rounded-lg animate-pulse"),
        rx.el.div(
            rx.el.div(class_name="h-4 w-24 bg-gray-200 rounded animate-pulse mb-2"),
            rx.el.div(class_name="h-8 w-16 bg-gray-200 rounded animate-pulse"),
            class_name="ml-4",
        ),
        class_name="flex items-center p-6 bg-white rounded-xl shadow-sm border border-gray-200",
    )


def skeleton_chart() -> rx.Component:
    return rx.el.div(
        rx.el.div(
            rx.el.div(class_name="h-6 w-48 bg-gray-200 rounded animate-pulse"),
            rx.el.div(class_name="h-8 w-32 bg-gray-200 rounded animate-pulse"),
            class_name="flex justify-between items-center mb-6",
        ),
        rx.el.div(class_name="h-[300px] w-full bg-gray-100 rounded-lg animate-pulse"),
        class_name="bg-white p-6 rounded-xl shadow-sm border border-gray-200",
    )


def skeleton_table_row() -> rx.Component:
    return rx.el.tr(
        rx.el.td(
            rx.el.div(class_name="h-4 w-32 bg-gray-200 rounded animate-pulse"),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(class_name="h-4 w-24 bg-gray-200 rounded animate-pulse"),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(class_name="h-4 w-16 bg-gray-200 rounded animate-pulse"),
            class_name="px-6 py-4",
        ),
        rx.el.td(
            rx.el.div(class_name="h-4 w-20 bg-gray-200 rounded animate-pulse"),
            class_name="px-6 py-4",
        ),
    )