#!/usr/bin/env python3
"""
Password Strength Analyzer
A CLI tool to evaluate password strength using entropy scoring and pattern detection.
"""

import argparse
import sys
import getpass

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.rule import Rule
from rich import box

from core.scorer import score_password

console = Console()


def render_bar(score: int, color: str) -> Text:
    filled = round(score / 5)
    empty = 20 - filled
    bar = Text()
    bar.append("█" * filled, style=color)
    bar.append("░" * empty, style="grey50")
    bar.append(f"  {score}/100", style="bold white")
    return bar


def print_report(result: dict) -> None:
    console.print()

    # Header panel
    score_bar = render_bar(result["score"], result["color"])
    label_text = Text(result["label"], style=f"bold {result['color']}")

    header = Table.grid(padding=(0, 2))
    header.add_column(justify="left")
    header.add_column(justify="left")

    header.add_row(Text("Score", style="dim"), score_bar)
    header.add_row(Text("Rating", style="dim"), label_text)
    header.add_row(
        Text("Entropy", style="dim"),
        Text(f"{result['entropy']} bits", style="bold white"),
    )
    header.add_row(
        Text("Crack time", style="dim"),
        Text(result["crack_time"], style="bold white"),
    )

    console.print(
        Panel(
            header,
            title="[bold]🔐 Password Strength Report[/bold]",
            border_style=result["color"],
            padding=(1, 2),
        )
    )

    # Warnings
    if result["warnings"]:
        console.print(Rule("[bold yellow]⚠  Warnings[/bold yellow]", style="yellow"))
        for w in result["warnings"]:
            console.print(f"  [yellow]•[/yellow] {w['detail']}  [dim](−{w['penalty']} pts)[/dim]")
        console.print()

    # Suggestions
    console.print(Rule("[bold cyan]💡 Suggestions[/bold cyan]", style="cyan"))
    for tip in result["suggestions"]:
        console.print(f"  [cyan]→[/cyan] {tip}")
    console.print()


def interactive_mode() -> None:
    console.print(
        Panel(
            "[bold]Password Strength Analyzer[/bold]\n[dim]Type a password to analyze it. Press Ctrl+C to exit.[/dim]",
            border_style="blue",
        )
    )
    while True:
        try:
            password = getpass.getpass("\n🔑 Enter password (hidden): ")
            if not password:
                console.print("[dim]No password entered, try again.[/dim]")
                continue
            result = score_password(password)
            print_report(result)
        except KeyboardInterrupt:
            console.print("\n\n[dim]Bye![/dim]")
            break


def main() -> None:
    parser = argparse.ArgumentParser(
        description="🔐 Password Strength Analyzer — entropy scoring & pattern detection",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python analyzer.py --password "MyP@ssw0rd"
  python analyzer.py --interactive
  python analyzer.py --batch passwords.txt
        """,
    )
    parser.add_argument("--password", "-p", help="Password to analyze")
    parser.add_argument(
        "--interactive", "-i", action="store_true", help="Interactive mode (hidden input)"
    )
    parser.add_argument("--batch", "-b", help="Path to file with one password per line")

    args = parser.parse_args()

    if args.interactive:
        interactive_mode()

    elif args.password:
        result = score_password(args.password)
        print_report(result)

    elif args.batch:
        try:
            with open(args.batch) as f:
                passwords = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            console.print(f"[red]File not found:[/red] {args.batch}")
            sys.exit(1)

        console.print(f"\n[bold]Analyzing {len(passwords)} passwords...[/bold]\n")

        table = Table(box=box.ROUNDED, show_lines=True)
        table.add_column("Password", style="dim", max_width=20)
        table.add_column("Score", justify="center")
        table.add_column("Rating")
        table.add_column("Entropy")
        table.add_column("Crack Time")
        table.add_column("Top Warning")

        for pwd in passwords:
            result = score_password(pwd)
            masked = pwd[:2] + "*" * (len(pwd) - 2)
            top_warning = result["warnings"][0]["detail"] if result["warnings"] else "—"
            table.add_row(
                masked,
                str(result["score"]),
                Text(result["label"], style=f"bold {result['color']}"),
                f"{result['entropy']} bits",
                result["crack_time"],
                top_warning[:45],
            )

        console.print(table)

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
