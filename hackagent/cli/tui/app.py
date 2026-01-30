# Copyright 2025 - AI4I. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Main TUI Application

Full-screen tabbed interface for HackAgent.
"""

from typing import Any

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.widgets import Footer, TabbedContent, TabPane

from hackagent.cli.config import CLIConfig
from hackagent.cli.tui.views.agents import AgentsTab
from hackagent.cli.tui.views.attacks import AttacksTab
from hackagent.cli.tui.views.config import ConfigTab
from hackagent.cli.tui.views.dashboard import DashboardTab
from hackagent.cli.tui.views.results import ResultsTab


class HackAgentTUI(App):
    """HackAgent Terminal User Interface Application"""

    CSS = """
    /* Modern dark theme with enhanced visuals */
    Screen {
        background: #0a0a0a;
        transition: background 300ms;
    }

    Header {
        background: linear-gradient(90deg, #1a0000 0%, #8b0000 50%, #1a0000 100%);
        color: #ffffff;
        height: 3;
        text-style: bold;
        border-bottom: heavy #ff0000;
    }

    Footer {
        background: linear-gradient(90deg, #0a0a0a 0%, #2b0000 50%, #0a0a0a 100%);
        color: #cccccc;
        border-top: heavy #5b0000;
    }

    TabbedContent {
        height: 100%;
        border: heavy #ff0000;
        background: #0f0f0f;
    }

    TabPane {
        padding: 1 2;
        background: #0f0f0f;
    }

    TabbedContent > ContentSwitcher > * > * {
        background: #0f0f0f;
    }

    Tabs {
        background: linear-gradient(180deg, #1a0000 0%, #0a0a0a 100%);
        border-bottom: wide #ff0000;
    }

    Tab {
        color: #888888;
        background: transparent;
        text-style: normal;
        padding: 1 3;
        transition: all 150ms;
    }

    Tab.-active {
        color: #ff3333;
        background: linear-gradient(180deg, #2b0000 0%, #1a0000 100%);
        text-style: bold;
        border-bottom: wide #ff0000;
    }

    Tab:hover {
        background: #1a0000;
        color: #ff6666;
    }

    .title-bar {
        dock: top;
        width: 100%;
        background: linear-gradient(90deg, #1a0000 0%, #8b0000 50%, #1a0000 100%);
        color: #ffffff;
        height: 3;
        content-align: center middle;
        border: round #ff0000;
        text-style: bold;
    }

    .section {
        border: round #ff3333;
        padding: 1 2;
        margin: 1;
        height: auto;
        background: #151515;
    }

    .info-box {
        background: linear-gradient(135deg, #151515 0%, #1a0a0a 100%);
        border: round #ff3333;
        padding: 1 2;
        margin: 1;
    }

    Button {
        margin: 1;
        border: solid #ff0000;
        background: #1a0000;
        color: #ffffff;
        transition: all 150ms;
    }

    Button:hover {
        background: #2b0000;
        border: solid #ff3333;
        text-style: bold;
    }

    Button.-primary {
        background: linear-gradient(135deg, #8b0000 0%, #ff0000 100%);
        color: #ffffff;
        border: solid #ff3333;
        text-style: bold;
    }

    Button.-primary:hover {
        background: linear-gradient(135deg, #ff0000 0%, #ff3333 100%);
        border: double #ff6666;
    }

    Button:focus {
        border: double #ff6666;
    }

    DataTable {
        height: 100%;
        background: #0f0f0f;
        border: solid #ff0000;
    }

    DataTable > .datatable--header {
        background: linear-gradient(180deg, #8b0000 0%, #5b0000 100%);
        color: #ffffff;
        text-style: bold;
        border-bottom: wide #ff0000;
    }

    DataTable > .datatable--cursor {
        background: linear-gradient(90deg, #2b0000 0%, #5b0000 100%);
        color: #ffffff;
    }

    DataTable > .datatable--cursor:hover {
        background: linear-gradient(90deg, #5b0000 0%, #8b0000 100%);
    }

    /* Enhanced stat cards with glow effect */
    .stat-card {
        border: round #ff3333;
        background: linear-gradient(135deg, #1a0000 0%, #0f0f0f 100%);
        padding: 1 2;
        margin: 1;
        height: 5;
    }

    /* Results tab specific styles - horizontal split 20-80 */
    ResultsTab #results-left-panel {
        border-right: heavy #ff0000;
        background: #0f0f0f;
    }

    ResultsTab #results-right-panel {
        background: #0f0f0f;
    }

    ResultsTab #results-title {
        height: 3;
        width: 100%;
        text-align: center;
        background: linear-gradient(90deg, #1a0000 0%, #8b0000 50%, #1a0000 100%);
        color: #ffffff;
        padding: 1;
        border: round #ff0000;
        text-style: bold;
    }

    ResultsTab #details-title {
        height: 3;
        width: 100%;
        text-align: center;
        background: linear-gradient(90deg, #1a0000 0%, #8b0000 50%, #1a0000 100%);
        color: #ffffff;
        padding: 1;
        border: round #ff0000;
        text-style: bold;
    }

    ResultsTab .toolbar {
        height: 3;
        width: 100%;
        padding: 0 1;
        background: #151515;
        border: solid #5b0000;
    }

    /* Loading and progress indicators */
    LoadingIndicator {
        color: #ff0000;
        text-style: bold;
    }

    ProgressBar {
        bar-color: #ff0000;
        background: #1a0000;
    }

    /* Notification styles */
    .notification {
        background: linear-gradient(135deg, #1a0000 0%, #0f0f0f 100%);
        border: round #ff3333;
        padding: 1 2;
        margin: 1;
    }

    .success-notification {
        border: round #00ff00;
    }

    .error-notification {
        border: round #ff0000;
    }

    .warning-notification {
        border: round #ffaa00;
    }

    /* Smooth animations for containers */
    Container {
        transition: offset 200ms, opacity 200ms;
    }

    Static {
        transition: opacity 150ms;
    }
    """

    TITLE = "⚡ HACKAGENT ⚡ - Elite AI Security Platform"
    SUB_TITLE = "🔐 Zero-Code AI-Native Security Operations Center 🔐"

    BINDINGS = [
        Binding("q", "quit", "Quit", priority=True),
        Binding("d", "switch_tab('dashboard')", "Dashboard", show=False),
        Binding("a", "switch_tab('agents')", "Agents", show=False),
        Binding("k", "switch_tab('attacks')", "Attacks", show=False),
        Binding("r", "switch_tab('results')", "Results", show=False),
        Binding("c", "switch_tab('config')", "Config", show=False),
        Binding("f5", "refresh", "Refresh", show=True),
        Binding("?", "show_help", "Help", show=True),
    ]

    def __init__(
        self,
        cli_config: CLIConfig,
        initial_tab: str = "dashboard",
        initial_data: dict[Any, Any] | None = None,
    ):
        """Initialize the TUI application.

        Args:
            cli_config: CLI configuration object
            initial_tab: Which tab to show initially (default: "dashboard")
            initial_data: Initial data to pre-fill in the tab (default: None)
        """
        super().__init__()
        self.cli_config = cli_config
        self.initial_tab = initial_tab
        self.initial_data = initial_data or {}
        self.dark = True  # Use dark theme by default

    def compose(self) -> ComposeResult:
        """Compose the UI layout."""
        with TabbedContent(initial=self.initial_tab):
            with TabPane("🏠 Dashboard", id="dashboard"):
                yield DashboardTab(self.cli_config)

            with TabPane("🤖 Agents", id="agents"):
                yield AgentsTab(self.cli_config)

            with TabPane("⚔️ Attacks", id="attacks"):
                yield AttacksTab(self.cli_config, initial_data=self.initial_data)

            with TabPane("📊 Results", id="results"):
                yield ResultsTab(self.cli_config)

            with TabPane("⚙️ Config", id="config"):
                yield ConfigTab(self.cli_config)

        yield Footer()

    def action_switch_tab(self, tab_id: str) -> None:
        """Switch to a specific tab.

        Args:
            tab_id: ID of the tab to switch to
        """
        tabs = self.query_one(TabbedContent)
        tabs.active = tab_id

    def action_refresh(self) -> None:
        """Refresh the current tab's data."""
        tabs = self.query_one(TabbedContent)
        active_pane = tabs.get_pane(tabs.active)
        if active_pane and hasattr(active_pane, "refresh_data"):
            # Get the first child of the TabPane (our custom tab widget)
            for child in active_pane.children:
                if hasattr(child, "refresh_data"):
                    child.refresh_data()
                    break

    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.title = self.TITLE
        self.sub_title = self.SUB_TITLE
        
        # Show welcome notification
        self.show_info("Welcome to HackAgent! Press ? for keyboard shortcuts")

    def action_show_help(self) -> None:
        """Show keyboard shortcuts help screen."""
        help_text = (
            "═══ ⚡ KEYBOARD SHORTCUTS ═══\n\n"
            "[bold cyan]Navigation:[/bold cyan]\n"
            "  [bold]d[/bold] - Dashboard (Overview & Stats)\n"
            "  [bold]a[/bold] - Agents (Manage AI Agents)\n"
            "  [bold]k[/bold] - Attacks (Security Testing)\n"
            "  [bold]r[/bold] - Results (View Test Results)\n"
            "  [bold]c[/bold] - Config (Settings)\n\n"
            "[bold yellow]Actions:[/bold yellow]\n"
            "  [bold]F5[/bold] - Refresh current tab\n"
            "  [bold]Tab[/bold] - Navigate between elements\n"
            "  [bold]Enter[/bold] - Select/Activate\n"
            "  [bold]Esc[/bold] - Cancel/Back\n\n"
            "[bold red]System:[/bold red]\n"
            "  [bold]?[/bold] - Show this help\n"
            "  [bold]q[/bold] - Quit application\n\n"
            "[dim]Press any key to close this help screen[/dim]"
        )
        self.notify(
            help_text,
            title="⌨️ Keyboard Shortcuts",
            timeout=15,
        )

    def show_success(self, message: str, title: str = "Success") -> None:
        """Show success notification with checkmark and animation.
        
        Args:
            message: Message to display
            title: Optional title for the notification (default: "Success")
        """
        self.notify(
            f"✅ {message}",
            title=title,
            severity="information",
            timeout=3,
        )

    def show_error(self, message: str, title: str = "Error") -> None:
        """Show error notification with X mark and animation.
        
        Args:
            message: Message to display
            title: Optional title for the notification (default: "Error")
        """
        self.notify(
            f"❌ {message}",
            title=title,
            severity="error",
            timeout=5,
        )

    def show_warning(self, message: str, title: str = "Warning") -> None:
        """Show warning notification with warning sign and animation.
        
        Args:
            message: Message to display
            title: Optional title for the notification (default: "Warning")
        """
        self.notify(
            f"⚠️ {message}",
            title=title,
            severity="warning",
            timeout=4,
        )

    def show_info(self, message: str, title: str = "Information") -> None:
        """Show info notification with info icon and animation.
        
        Args:
            message: Message to display
            title: Optional title for the notification (default: "Information")
        """
        self.notify(
            f"ℹ️ {message}",
            title=title,
            severity="information",
            timeout=3,
        )
