"""
common.py - Shared UI parts.

The navigation row sits at the top of every page. Putting it here
means we change the menu in one place instead of three.
"""

from nicegui import ui


def navigation() -> None:
    """Top navigation row, identical on every page."""
    with ui.row().classes("mb-6 gap-2"):
        ui.button("Startseite",
                  on_click=lambda: ui.navigate.to("/")) \
            .props("flat color=primary")
        ui.button("Renditerechner",
                  on_click=lambda: ui.navigate.to("/renditerechner")) \
            .props("flat color=primary")
        ui.button("Vergleich",
                  on_click=lambda: ui.navigate.to("/vergleich")) \
            .props("flat color=primary")
