import time
import random
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout

console = Console()

def get_swarm_metrics():
    n1 = {"NSW1": random.uniform(70, 95), "QLD1": random.uniform(65, 85), "VIC1": random.uniform(72, 100), "SA1": random.uniform(85, 120), "TAS1": random.uniform(60, 80)}
    if random.random() > 0.92:
        n1[random.choice(list(n1.keys()))] = random.uniform(450, 1450)
    n2 = {"NSW-QLD": random.uniform(-600, 600), "VIC-NSW": random.uniform(-1000, 1000), "VIC-SA": random.uniform(-400, 400), "VIC-TAS": random.uniform(-500, 500)}
    n3 = {"COAL_BLACK": random.uniform(4500, 6500), "COAL_BROWN": random.uniform(2000, 2800), "GAS_TURBINE": random.uniform(500, 1500), "HYDRO_CLEAN": random.uniform(1200, 3500), "WIND_RENEW": random.uniform(1500, 4800), "SOLAR_PV": random.uniform(800, 3200)}
    n4 = {"SYS_FREQ": random.uniform(49.95, 50.05), "SA_RESERVE": random.uniform(18.5, 34.2), "NSW_RESERVE": random.uniform(22.1, 41.0), "VIC_RESERVE": random.uniform(20.4, 38.6)}
    return n1, n2, n3, n4

def build_swarm_layout():
    n1, n2, n3, n4 = get_swarm_metrics()
    layout = Layout()
    layout.split_column(
        Layout(name="header", size=3),
        Layout(name="swarm_grid", ratio=1),
        Layout(name="footer", size=3)
    )
    layout["swarm_grid"].split_row( Layout(name="col1", ratio=1), Layout(name="col2", ratio=1) )
    layout["col1"].split_column(Layout(name="node1"), Layout(name="node2"))
    layout["col2"].split_column(Layout(name="node3"), Layout(name="node4"))
    
    # Node 1
    t1 = Table(box=None, expand=True, header_style="bold green")
    t1.add_column("REGION", style="green")
    t1.add_column("SPOT_RRP", style="green", justify="right")
    for k, v in n1.items():
        style = "bold blink red" if v > 250 else "green"
        t1.add_row(f"REG_{k}", f"[{style}]${v:07.2f}[/{style}]")
    layout["node1"].update(Panel(t1, title="[green]▧ SWARM_NODE_01 // FINANCIAL_INDEX[/green]", border_style="green"))
    
    # Node 2
    t2 = Table(box=None, expand=True, header_style="bold green")
    t2.add_column("LINK_ID", style="green")
    t2.add_column("FLOW_DIRECTION_MW", style="green", justify="right")
    for k, v in n2.items():
        direction = "➔ EXP" if v >= 0 else "◀ IMP"
        t2.add_row(k, f"{direction} {abs(int(v)):04d} MW")
    layout["node2"].update(Panel(t2, title="[green]▧ SWARM_NODE_02 // GRID_FLOW_NET[/green]", border_style="green"))
    
    # Node 3
    t3 = Table(box=None, expand=True, header_style="bold green")
    t3.add_column("FUEL_SOURCE", style="green")
    t3.add_column("DISPATCH_MW", style="green", justify="right")
    for k, v in n3.items():
        t3.add_row(k, f"{int(v):05d} MW")
    layout["node3"].update(Panel(t3, title="[green]▧ SWARM_NODE_03 // ENERGY_MIX_OUT[/green]", border_style="green"))
    
    # Node 4
    t4 = Table(box=None, expand=True, header_style="bold green")
    t4.add_column("STABILITY_ID", style="green")
    t4.add_column("METRIC_VALUE", style="green", justify="right")
    for k, v in n4.items():
        unit = " Hz" if "FREQ" in k else " %"
        t4.add_row(k, f"{v:.2f}{unit}")
    layout["node4"].update(Panel(t4, title="[green]▧ SWARM_NODE_04 // GRID_SECURITY[/green]", border_style="green"))
    
    # Brand Anchored Header Frame
    header_text = f"⚙ ROBDOE.COM // SWARM CORE TERMINAL LAYER ACTIVE // CLOCK: 40MHz // TIME: {datetime.now().strftime('%H:%M:%S')}"
    layout["header"].update(Panel(f"[bold green]▲ {header_text} ▲[/bold green]", border_style="green"))
    layout["footer"].update(Panel("[green]✔ INTEL DISPATCH STABLE // HOSTED ENTIRELY LOCAL @ ROBDOE.COM // CTRL+C TO BREAK[/green]", border_style="green"))
    return layout

with Live(build_swarm_layout(), refresh_per_second=2, screen=True) as live:
    try:
        while True:
            time.sleep(0.40)
            live.update(build_swarm_layout())
    except KeyboardInterrupt:
        pass
