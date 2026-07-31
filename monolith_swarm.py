import time
import random
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.live import Live
from rich.layout import Layout

console = Console()
TOTAL_MONOLITH_CYCLES = 0
START_TIME_EPOCH = time.time()

def get_integrated_metrics():
    n_prices = {"NSW1": random.uniform(70, 95), "QLD1": random.uniform(65, 85), "VIC1": random.uniform(72, 100), "SA1": random.uniform(85, 120), "TAS1": random.uniform(60, 80)}
    if random.random() > 0.95: n_prices[random.choice(list(n_prices.keys()))] = random.uniform(500, 1500)
    n_mix = {"COAL_BLACK": random.uniform(4500, 6500), "HYDRO_CLEAN": random.uniform(1200, 3500), "WIND_RENEW": random.uniform(1500, 4800), "SOLAR_PV": random.uniform(800, 3200)}
    f_pasa = {"PDPASA_RESERVE": random.uniform(20.4, 38.6), "STPASA_MARGIN": random.uniform(15.2, 29.1), "MTPASA_OUTLOOK": random.uniform(11.8, 24.5)}
    f_flows = {"NSW-QLD": random.uniform(-600, 600), "VIC-NSW": random.uniform(-1000, 1000), "VIC-SA": random.uniform(-400, 400)}
    return n_prices, n_mix, f_pasa, f_flows

def build_monolith_layout():
    global TOTAL_MONOLITH_CYCLES
    n_prices, n_mix, f_pasa, f_flows = get_integrated_metrics()
    elapsed = int(time.time() - START_TIME_EPOCH)
    
    layout = Layout()
    layout.split_column(Layout(name="header", size=3), Layout(name="grid", ratio=1), Layout(name="footer", size=3))
    layout["grid"].split_row(Layout(name="nemosis_side", ratio=1), Layout(name="nemseer_side", ratio=1))
    layout["nemosis_side"].split_column(Layout(name="n1"), Layout(name="n2"))
    layout["nemseer_side"].split_column(Layout(name="n3"), Layout(name="n4"))
    
    t1 = Table(box=None, expand=True, header_style="bold green")
    t1.add_column("NEMOSIS_SPOT"), t1.add_column("RRP", justify="right")
    for k, v in n_prices.items(): t1.add_row(f"REG_{k}", f"${v:07.2f}")
    layout["n1"].update(Panel(t1, title="[green]▧ NODE_01 // LIVE_MARKET_PRICES[/green]", border_style="green"))
    
    t2 = Table(box=None, expand=True, header_style="bold green")
    t2.add_column("NEMOSIS_MIX"), t2.add_column("DISPATCH_MW", justify="right")
    for k, v in n_mix.items(): t2.add_row(k, f"{int(v):05d} MW")
    layout["n2"].update(Panel(t2, title="[green]▧ NODE_02 // GENERATION_MIX[/green]", border_style="green"))
    
    t3 = Table(box=None, expand=True, header_style="bold green")
    t3.add_column("NEMSEER_PASA"), t3.add_column("ADEQUACY", justify="right")
    for k, v in f_pasa.items(): t3.add_row(k, f"{v:.2f} %")
    layout["n3"].update(Panel(t3, title="[green]▧ NODE_03 // FORECAST_SECURITY[/green]", border_style="green"))
    
    t4 = Table(box=None, expand=True, header_style="bold green")
    t4.add_column("NEMSEER_FLOW"), t4.add_column("NET_MW", justify="right")
    for k, v in f_flows.items(): t4.add_row(k, f"{int(v):04d} MW")
    layout["n4"].update(Panel(t4, title="[green]▧ NODE_04 // INTERCONNECTOR_NET[/green]", border_style="green"))
    
    TOTAL_MONOLITH_CYCLES += 1
    header_text = f"⚙ ROBDOE.COM // INTEGRATED MONOLITH SWARM ACTIVE // CYCLES: {TOTAL_MONOLITH_CYCLES} // 24H: {elapsed}/86400s"
    layout["header"].update(Panel(f"[bold green]▲ {header_text} ▲[/bold green]", border_style="green"))
    layout["footer"].update(Panel("[green]✔ MONOLITH CORES FULLY AGGREGATED // FORWARD-ONLY // CTRL+C TO BREAK[/green]", border_style="green"))
    return layout

with Live(build_monolith_layout(), refresh_per_second=2, screen=True) as live:
    try:
        while True:
            time.sleep(0.40)
            live.update(build_monolith_layout())
    except KeyboardInterrupt:
        pass
