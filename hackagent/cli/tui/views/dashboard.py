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
Dashboard Tab

Overview and statistics for HackAgent.
"""

from typing import Any

from textual.app import ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Static

from hackagent.cli.config import CLIConfig
from hackagent.cli.tui.base import BaseTab


def _escape(value: Any) -> str:
    """Escape a value for safe Rich markup rendering.

    Args:
        value: Any value to escape

    Returns:
        String with Rich markup characters escaped

    Note:
        We escape ALL square brackets, not just tag-like patterns,
        because Rich's markup parser can get confused by unescaped
        brackets in certain contexts (e.g., JSON arrays inside colored text).
    """
    if value is None:
        return ""
    # Escape ALL square brackets to prevent any markup interpretation issues
    text = str(value)
    return text.replace("[", "\\[").replace("]", "\\]")


def _format_box(content: str, width: int = 57) -> str:
    """Format content in a professional ASCII box border.
    
    Args:
        content: Text content to display (can include Rich markup)
        width: Width of the box (default: 57)
        
    Returns:
        Formatted string with box borders
        
    Note:
        This is a simple implementation. For perfect alignment with Rich markup,
        consider using Rich's Text.plain to calculate visible length.
    """
    lines = content.split("\n")
    result = [f"┌{'─' * (width - 2)}┐"]
    
    for line in lines:
        # Simple padding - note this doesn't account for Rich markup lengths
        # For production, you'd want to use Rich's Text.plain to get visible length
        result.append(f"│ {line:<{width - 4}} │")
    
    result.append(f"└{'─' * (width - 2)}┘")
    return "\n".join(result)


class DashboardTab(BaseTab):
    """Dashboard tab showing overview and statistics."""

    DEFAULT_CSS = ""

    def __init__(self, cli_config: CLIConfig):
        """Initialize dashboard tab.

        Args:
            cli_config: CLI configuration object
        """
        super().__init__(cli_config)
        self.stats = {
            "agents": 0,
            "attacks": 0,
            "results": 0,
            "success_rate": 0.0,
        }

    def compose(self) -> ComposeResult:
        """Compose the dashboard layout with enhanced visuals."""
        # Animated title section with gradient
        yield Static(
            "╔═══════════════════════════════════════════════════════════════╗\n"
            "║  [bold red reverse] ⚡ HACKAGENT SECURITY OPERATIONS CENTER ⚡ [/]  ║\n"
            "╚═══════════════════════════════════════════════════════════════╝",
            id="dashboard-title",
        )

        # Welcome message with animation
        yield Static(
            "\n[bold cyan]🎯 Mission Control Dashboard[/bold cyan]\n"
            "[dim]Real-time AI Agent Security Monitoring & Testing[/dim]\n",
            id="welcome-message",
        )

        # Statistics section with enhanced formatting
        yield Static(
            "\n[bold yellow]═══ 📊 LIVE STATISTICS ═══[/bold yellow]", id="stats-header"
        )

        with Horizontal():
            with Vertical(classes="stat-card"):
                yield Static(
                    "┌─────────────────┐\n"
                    "│  🤖 [bold cyan]AGENTS[/bold cyan]   │\n"
                    "│  [bold reverse] 0 [/] ACTIVE  │\n"
                    "└─────────────────┘",
                    id="stat-agents",
                )
            with Vertical(classes="stat-card"):
                yield Static(
                    "┌─────────────────┐\n"
                    "│  ⚔️  [bold green]ATTACKS[/bold green]  │\n"
                    "│  [bold reverse] 0 [/] RUNNING │\n"
                    "└─────────────────┘",
                    id="stat-attacks",
                )
            with Vertical(classes="stat-card"):
                yield Static(
                    "┌─────────────────┐\n"
                    "│  📋 [bold yellow]RESULTS[/bold yellow]  │\n"
                    "│  [bold reverse] 0 [/] TOTAL   │\n"
                    "└─────────────────┘",
                    id="stat-results",
                )
            with Vertical(classes="stat-card"):
                yield Static(
                    "┌─────────────────┐\n"
                    "│  ✓ [bold magenta]SUCCESS[/bold magenta]  │\n"
                    "│  [bold reverse] 0% [/] RATE   │\n"
                    "└─────────────────┘",
                    id="stat-success",
                )

        # Activity section with enhanced visuals
        yield Static(
            "\n[bold yellow]═══ 📝 ACTIVITY LOG ═══[/bold yellow]", id="activity-header"
        )

        with VerticalScroll():
            yield Static(
                "┌───────────────────────────────────────────────────────┐\n"
                "│ [dim]⏳ Initializing security operations center...[/dim]   │\n"
                "│ [dim]🔍 Loading agent configurations...[/dim]            │\n"
                "│ [dim]📡 Connecting to HackAgent API...[/dim]             │\n"
                "└───────────────────────────────────────────────────────┘",
                id="activity-log",
            )

        # Quick actions guide
        yield Static(
            "\n[bold cyan]═══ ⚡ QUICK ACTIONS ═══[/bold cyan]\n"
            "[dim]Press [bold]'a'[/bold] → Agents  |  [bold]'k'[/bold] → Attacks  |  [bold]'r'[/bold] → Results  |  [bold]'c'[/bold] → Config  |  [bold]'q'[/bold] → Quit[/dim]",
            id="quick-actions",
        )

    def on_mount(self) -> None:
        """Called when the tab is mounted."""
        # Call base class mount to handle initial refresh
        super().on_mount()

        # Enable auto-refresh every 5 seconds
        self.enable_auto_refresh(interval=5.0)

    def refresh_data(self) -> None:
        """Refresh dashboard data from API."""
        try:
            from hackagent.api.agent import agent_list
            from hackagent.api.result import result_list

            # Validate configuration
            if not self.cli_config.api_key:
                activity_log = self.query_one("#activity-log", Static)
                activity_log.update(
                    "┌───────────────────────────────────────────────────────┐\n"
                    "│ [red]⚠️ API KEY NOT CONFIGURED[/red]                      │\n"
                    "│                                                       │\n"
                    "│ [yellow]Please set up your HackAgent API key:[/yellow]         │\n"
                    "│ [dim]Run: hackagent init[/dim]                             │\n"
                    "│                                                       │\n"
                    "│ [cyan]💡 Get your free API key at:[/cyan]                   │\n"
                    "│ [blue]https://app.hackagent.dev[/blue]                      │\n"
                    "└───────────────────────────────────────────────────────┘"
                )
                return

            # Create API client using base class method
            client = self.create_api_client()

            agents_data = []
            results_data = []

            # Fetch agents count
            agents_response = agent_list.sync_detailed(client=client)
            if agents_response.status_code == 200 and agents_response.parsed:
                agents_data = (
                    agents_response.parsed.results
                    if agents_response.parsed.results
                    else []
                )
                self.stats["agents"] = len(agents_data)
            elif agents_response.status_code == 401:
                activity_log = self.query_one("#activity-log", Static)
                activity_log.update(
                    "┌───────────────────────────────────────────────────────┐\n"
                    "│ [red]🔒 AUTHENTICATION FAILED[/red]                       │\n"
                    "│                                                       │\n"
                    "│ [yellow]Your API key is invalid or expired[/yellow]            │\n"
                    "│                                                       │\n"
                    "│ [cyan]To fix:[/cyan]                                          │\n"
                    "│ [dim]Run: hackagent config set --api-key YOUR_KEY[/dim]    │\n"
                    "│                                                       │\n"
                    "│ [dim]Press F5 to retry after updating[/dim]                │\n"
                    "└───────────────────────────────────────────────────────┘"
                )
                return
            elif agents_response.status_code == 403:
                activity_log = self.query_one("#activity-log", Static)
                activity_log.update(
                    "┌───────────────────────────────────────────────────────┐\n"
                    "│ [red]⛔ ACCESS FORBIDDEN[/red]                            │\n"
                    "│                                                       │\n"
                    "│ [yellow]Your API key doesn't have permission[/yellow]          │\n"
                    "│ [yellow]to access this resource[/yellow]                    │\n"
                    "│                                                       │\n"
                    "│ [cyan]Contact support if this persists[/cyan]               │\n"
                    "└───────────────────────────────────────────────────────┘"
                )
                return

            # Fetch results count
            results_response = result_list.sync_detailed(client=client)
            if results_response.status_code == 200 and results_response.parsed:
                results_data = (
                    results_response.parsed.results
                    if results_response.parsed.results
                    else []
                )
                self.stats["results"] = len(results_data)

                # Calculate success rate
                if results_data:
                    completed = sum(
                        1
                        for r in results_data
                        if hasattr(r, "evaluation_status")
                        and str(
                            r.evaluation_status.value
                            if hasattr(r.evaluation_status, "value")
                            else r.evaluation_status
                        ).upper()
                        == "COMPLETED"
                    )
                    self.stats["success_rate"] = (
                        (completed / len(results_data)) * 100
                        if len(results_data) > 0
                        else 0
                    )

            # Update stat cards
            self._update_stat_cards()

            # Update activity log
            if not agents_data and not results_data:
                activity_log = self.query_one("#activity-log", Static)
                activity_log.update(
                    "┌───────────────────────────────────────────────────────┐\n"
                    "│ [yellow]📭 NO DATA FOUND[/yellow]                            │\n"
                    "│                                                       │\n"
                    "│ [cyan]🚀 Quick Start Guide:[/cyan]                           │\n"
                    "│                                                       │\n"
                    "│ [dim]1. Press 'a' → Create an agent[/dim]                  │\n"
                    "│ [dim]2. Press 'k' → Run security attacks[/dim]             │\n"
                    "│ [dim]3. Press 'r' → View results[/dim]                     │\n"
                    "│                                                       │\n"
                    "│ [green]Ready to secure your AI agents! ⚡[/green]           │\n"
                    "└───────────────────────────────────────────────────────┘"
                )
            else:
                self._update_activity_log(agents_data, results_data)

        except Exception as e:
            # Display error in activity log with helpful context
            activity_log = self.query_one("#activity-log", Static)

            error_type = type(e).__name__
            error_msg = str(e)

            # Provide context-specific help
            if "timeout" in error_msg.lower() or "TimeoutException" in error_type:
                activity_log.update(
                    "┌───────────────────────────────────────────────────────┐\n"
                    "│ [red]⚠️ CONNECTION TIMEOUT[/red]                          │\n"
                    "│                                                       │\n"
                    f"│ [yellow]Cannot reach API:[/yellow]                           │\n"
                    f"│ [dim]{self.cli_config.base_url[:50]}[/dim]│\n"
                    "│                                                       │\n"
                    "│ [cyan]Possible causes:[/cyan]                               │\n"
                    "│ [dim]• API server unreachable[/dim]                       │\n"
                    "│ [dim]• Network issues[/dim]                               │\n"
                    "│ [dim]• Firewall blocking connection[/dim]                 │\n"
                    "│                                                       │\n"
                    "│ [green]💡 Press F5 to retry[/green]                        │\n"
                    "└───────────────────────────────────────────────────────┘"
                )
            elif "401" in error_msg or "authentication" in error_msg.lower():
                activity_log.update(
                    "┌───────────────────────────────────────────────────────┐\n"
                    "│ [red]🔒 AUTHENTICATION FAILED[/red]                       │\n"
                    "│                                                       │\n"
                    "│ [yellow]Your API key is invalid or expired[/yellow]            │\n"
                    "│                                                       │\n"
                    "│ [cyan]To fix:[/cyan]                                          │\n"
                    "│ [dim]hackagent config set --api-key YOUR_KEY[/dim]         │\n"
                    "│                                                       │\n"
                    "│ [green]Press F5 to retry after updating[/green]            │\n"
                    "└───────────────────────────────────────────────────────┘"
                )
            else:
                # Truncate long error messages
                error_display = error_msg[:80] + "..." if len(error_msg) > 80 else error_msg
                activity_log.update(
                    "┌───────────────────────────────────────────────────────┐\n"
                    f"│ [red]❌ ERROR: {_escape(error_type)[:40]}[/red]              │\n"
                    "│                                                       │\n"
                    f"│ [yellow]{_escape(error_display)[:50]}[/yellow]│\n"
                    "│                                                       │\n"
                    "│ [green]Press F5 to retry[/green]                            │\n"
                    "└───────────────────────────────────────────────────────┘"
                )

    def _update_stat_cards(self) -> None:
        """Update the statistics cards with current data and enhanced visuals."""
        try:
            # Get the values
            agents_val = self.stats.get("agents", 0)
            attacks_val = self.stats.get("attacks", 0)
            results_val = self.stats.get("results", 0)
            success_val = self.stats.get("success_rate", 0)

            # Update each stat widget with enhanced borders and formatting
            stat_agents = self.query_one("#stat-agents", Static)
            stat_agents.update(
                "┌─────────────────┐\n"
                f"│  🤖 [bold cyan]AGENTS[/bold cyan]   │\n"
                f"│  [bold reverse] {agents_val} [/] ACTIVE  │\n"
                "└─────────────────┘"
            )

            stat_attacks = self.query_one("#stat-attacks", Static)
            stat_attacks.update(
                "┌─────────────────┐\n"
                f"│  ⚔️  [bold green]ATTACKS[/bold green]  │\n"
                f"│  [bold reverse] {attacks_val} [/] RUNNING │\n"
                "└─────────────────┘"
            )

            stat_results = self.query_one("#stat-results", Static)
            stat_results.update(
                "┌─────────────────┐\n"
                f"│  📋 [bold yellow]RESULTS[/bold yellow]  │\n"
                f"│  [bold reverse] {results_val} [/] TOTAL   │\n"
                "└─────────────────┘"
            )

            stat_success = self.query_one("#stat-success", Static)
            stat_success.update(
                "┌─────────────────┐\n"
                f"│  ✓ [bold magenta]SUCCESS[/bold magenta]  │\n"
                f"│  [bold reverse] {success_val:.0f}% [/] RATE   │\n"
                "└─────────────────┘"
            )

        except Exception as e:
            # Show error in activity log if update fails
            try:
                activity_log = self.query_one("#activity-log", Static)
                activity_log.update(
                    f"[red]⚠️ Error updating statistics: {_escape(str(e))}[/red]"
                )
            except Exception:
                pass

    def _update_activity_log(self, agents: list, results: list) -> None:
        """Update activity log with recent items and enhanced visuals.

        Args:
            agents: List of agents
            results: List of results
        """
        activity_log = self.query_one("#activity-log", Static)
        log_lines = ["┌───────────────────────────────────────────────────────┐"]

        # Add recent agents with icons and borders - escape user content
        if agents:
            log_lines.append("│ [bold cyan]🤖 RECENT AGENTS:[/bold cyan]" + " " * 30 + "│")
            for i, agent in enumerate(agents[:3], 1):
                agent_type = (
                    agent.agent_type.value
                    if hasattr(agent.agent_type, "value")
                    else agent.agent_type
                )
                agent_name = _escape(agent.name) if agent.name else "Unnamed"
                # Pad the line to fit the box
                line = f"│  {i}. [cyan]⚡ {agent_name}[/cyan] [dim]({_escape(agent_type)})[/dim]"
                padding = 57 - len(f"  {i}. ⚡ {agent_name} ({agent_type})")
                log_lines.append(line + " " * max(0, padding) + "│")
            log_lines.append("│" + " " * 57 + "│")

        # Add recent results with status colors and icons - escape user content
        if results:
            log_lines.append("│ [bold green]📋 RECENT RESULTS:[/bold green]" + " " * 28 + "│")
            for i, result in enumerate(results[:5], 1):
                status = "Unknown"
                status_icon = "❓"
                status_color = "dim"

                if hasattr(result, "evaluation_status"):
                    status = (
                        result.evaluation_status.value
                        if hasattr(result.evaluation_status, "value")
                        else str(result.evaluation_status)
                    )
                    # Color code and icon based on status
                    if status.upper() == "COMPLETED":
                        status_color = "green"
                        status_icon = "✅"
                    elif status.upper() == "RUNNING":
                        status_color = "yellow"
                        status_icon = "⏳"
                    elif status.upper() == "FAILED":
                        status_color = "red"
                        status_icon = "❌"

                attack_type = getattr(result, "attack_type", "Unknown")
                line = f"│  {i}. {status_icon} [yellow]{_escape(attack_type)}[/yellow] → [{status_color}]{_escape(status)}[/{status_color}]"
                padding = 57 - len(f"  {i}. {status_icon} {attack_type} → {status}")
                log_lines.append(line + " " * max(0, padding) + "│")

        if len(log_lines) == 1:
            log_lines.append("│ [dim]⏳ No recent activity yet...[/dim]" + " " * 21 + "│")
            log_lines.append("│ [dim]🚀 Get started by creating agents and running attacks![/dim]│")

        log_lines.append("└───────────────────────────────────────────────────────┘")
        activity_log.update("\n".join(log_lines))
