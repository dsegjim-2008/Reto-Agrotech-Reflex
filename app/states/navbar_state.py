import reflex as rx


class NavbarState(rx.State):
    """State management for the navigation bar component."""

    is_menu_open: bool = False

    @rx.event
    def toggle_menu(self):
        """Toggle the mobile navigation menu open or closed."""
        self.is_menu_open = not self.is_menu_open

    @rx.event
    def close_menu(self):
        """Close the mobile navigation menu."""
        self.is_menu_open = False