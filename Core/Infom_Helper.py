
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich import box  
import sys 
import pandas as pd
from rich.align import Align

console = Console()

def Help_Tables():
    try:
        table = Table(
            title="[bold underline magenta]BurnWP Framework - Command Example[/]",
            show_header=True,
            header_style="bold yellow",
            border_style="bright_blue",
            box=box.SQUARE,
            show_lines=True,
            row_styles=["none", "dim"]
        )

        table.add_column("[cyan]Command[/]", style="cyan", justify="left", width=55)
        table.add_column("[green]Description[/]", style="green", justify="left")

        table.add_row(
            f"[bold white]python3 {sys.argv[0]} attack targets.txt[/]",
            "Launch mass attack on targets from a list (*.txt), using CVE Exploiter, LFI, and Plugin Exploiter as configured."
        )
        table.add_row(
            f"[bold white]python3 {sys.argv[0]} list_plugin --list targets.txt[/]",
            "Attack Multi-Targets with Plugin_Exploiter"
        )
        table.add_row(
            f"[bold white]python3 {sys.argv[0]} list_plugin --target http://evil_host.com[/]",
            "Attack per domain with Plugin_Exploiter"
        )
        table.add_row(
            f"[bold white]python3 {sys.argv[0]} install_plugin[/]",
            "Install plugins with RealTime Tracking Plugin Valid, Error, Deleted, Modified"
        )
        table.add_row(
            f"[bold white]python3 {sys.argv[0]} ui_config[/]",
            "UI Config is help you Disable (OFF) or Enable (ON) Any Technology You Want"
     
        )
        table.add_row(
            f"[bold white]python3 {sys.argv[0]} cve_info[/]",
            "Display CVE details available in BurnWP Framework"
        )
        
        panel = Panel(table, title="[bold bright_magenta] Command Help [/]", border_style="bright_magenta")
        console.print(panel)

    except:
        pass
            #console.print(f"[bold red]Error displaying help table:[/] {e}")
def About_US():
    try:
        ABOUT_text = (
            "\n[bold cyan]BurnWP Framework : 1.0.0[/bold cyan]\n"
            "[green]CODED by Forums :[/green] DRCrypter.ru\n"
            "[yellow]CORE ENGINE VER :[/yellow] 1.0\n"
            "[magenta]DATE PUBLIC :[/magenta] 7-7-2025\n"
            "[blue]LAST UPDATE :[/blue] 7-7-2025\n"
        )
        panel = Panel.fit(ABOUT_text, title="BurnWP Framework", border_style="bright_blue")
        console.print(Align.center(panel))   # <-- This centers the panel
        print('\n')
    except:
        pass



def CVE__DB():
    try:
        df = pd.read_csv(r"Files_BurnWP/CVE_Exploiter_DB.csv")
        df.columns = df.columns.str.strip().str.lower()

        df.insert(0, "id", range(1, len(df) + 1))

        console = Console()
        table = Table(
            title="BurnWP Framework 1.0.0 — CVE Exploiter Database",
            header_style="",      
            title_style=""        
        )

        table.add_column("ID", style="cyan", no_wrap=True)
        table.add_column("Title", style="white")
        table.add_column("CVE", style="magenta")
        table.add_column("Severity", style="bold")
        table.add_column("Public Date", style="yellow")
        table.add_column("CVE Date", style="yellow")
        table.add_column("Description", style="green")
        table.add_column("From", style="bright_blue")
        table.add_column("Plugin CVE", style="bright_magenta")
        table.add_column("Technology", style="bright_cyan")

        def severity_color(sev):
            sev_str = str(sev).lower()
            if "critical" in sev_str or "9" in sev_str:
                return f"[bold red]{sev}[/]"
            elif "high" in sev_str:
                return f"[bold orange3]{sev}[/]"
            elif "medium" in sev_str:
                return f"[bold yellow]{sev}[/]"
            elif "low" in sev_str:
                return f"[bold green]{sev}[/]"
            return f"[dim]{sev}[/]"

        for _, row in df.iterrows():
            table.add_row(
                str(row.get("id", "")),
                str(row.get("title", "")),
                str(row.get("cve", "")),
                severity_color(row.get("cvss_severity", "")),
                str(row.get("public_date", "")),
                str(row.get("cve_date", "")),
                str(row.get("description", "")),
                str(row.get("from", "")),
                str(row.get("plugin_cve", "")),
                str(row.get("technology", ""))
            )

        console.print(table)
    except:pass 