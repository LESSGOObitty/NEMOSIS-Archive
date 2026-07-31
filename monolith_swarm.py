import time
import math
import random
from datetime import datetime
import threading
from flask import Flask, render_template_string, jsonify

app = Flask(__name__)
TOTAL_MONOLITH_CYCLES = 0
START_TIME_EPOCH = time.time()

def calculate_swarm_wave_mechanics():
    global TOTAL_MONOLITH_CYCLES
    m = (TOTAL_MONOLITH_CYCLES % 24) + 1
    tau_tick = m / 7200.0
    
    dPhi_dt = random.uniform(-15.5, 15.5)
    rho_k = random.uniform(85.4, 99.1)
    
    mu_0 = 1.256e-6
    sigma_k = 5.8e7  
    alpha_K = 0.05   
    
    psi_gamma = (mu_0 * sigma_k * dPhi_dt) + (alpha_K * math.sin(2 * math.pi * tau_tick)) + (rho_k * 0.01)
    
    freq_deviation = random.uniform(-0.05, 0.05) 
    df_dt = random.uniform(-0.02, 0.02)
    K_f = 12.5  
    K_p = 25.0  
    P_inj = -(K_f * df_dt) - (K_p * freq_deviation)
    
    return m, tau_tick, dPhi_dt, rho_k, psi_gamma, P_inj

@app.route('/data')
def get_live_data():
    global TOTAL_MONOLITH_CYCLES
    m, tau, dPhi, rho, psi, p_inj = calculate_swarm_wave_mechanics()
    elapsed = int(time.time() - START_TIME_EPOCH)
    TOTAL_MONOLITH_CYCLES += 1
    
    # Pack telemetry data fields into a live JSON stream
    return jsonify(
        cycles=TOTAL_MONOLITH_CYCLES,
        m=m,
        tau=f"{tau:.6f}",
        psi=f"{psi:+.6f}",
        dphi=f"{dPhi:+.4f}",
        rho=f"{rho:.2f}",
        pinj=f"{p_inj:+.4f}",
        time=datetime.now().strftime('%H:%M:%S')
    )

@app.route('/')
def home():
    # High-utility active AJAX polling interface
    return render_template_string('''
    <html>
    <head>
        <title>ROBDOE.COM // MAIN DISPATCH LIVE</title>
        <style>
            body { background-color: #000; color: #00ff00; font-family: monospace; font-size: 18px; padding: 30px; }
            .crt-frame { border: 2px solid #00ff00; padding: 20px; border-radius: 5px; box-shadow: 0 0 15px rgba(0,255,0,0.4); line-height: 1.6; }
            .highlight { color: #ff00ff; font-weight: bold; }
            .val { color: #ffff00; font-weight: bold; }
        </style>
        <script>
            function fetchTelemetry() {
                fetch('/data')
                    .then(response => response.json())
                    .then(data => {
                        document.getElementById('matrix_header').innerHTML = `⚙ <span class="highlight">ROBDOE.COM</span> // 19-NODE MONOLITH CORE MATRIX TERMINAL ACTIVE`;
                        document.getElementById('clock_line').innerHTML = `CLOCK CYCLE: ${String(data.cycles).padStart(6, '0')} &nbsp;| &nbsp;INTERVAL TRAIN STEP [m]: ${String(data.m).padStart(2, '0')}/24 &nbsp;| &nbsp;τ-TICK: ${data.tau}`;
                        
                        let body = `[<span style="color: #ff0000;">CHAKRA_01</span>] WAVE PHASE ANGLE (Ψ_γ) : <span class="val">${data.psi} rad</span> (Hallett-Bundey Substation Link)<br>` +
                                   `[<span style="color: #ff7f00;">CHAKRA_02</span>] POWER FLUX SHIFT (∂Φ/∂t): <span style="color: #00ffff; font-weight:bold;">${data.dphi} MW/s</span> (Instantaneous Grid Volatility)<br>` +
                                   `[<span style="color: #ffff00;">CHAKRA_03</span>] NODE MASS DENSITY (ρ_k): <span style="color: #ffffff; font-weight:bold;">${data.rho} kg/m³</span> (System Strength Stability Anchor)<br>` +
                                   `[<span style="color: #00ff00;">CHAKRA_04</span>] INVERTER MATCHING (P_inj): <span class="val">${data.pinj} MW</span> (Active Microprocessor Response)<br>` +
                                   `------------------------------------------------------------------------------------------<br>` +
                                   `HYDREN DOMAIN STATE OVERVIEW (7D HEXAGON RECYCLE MATRIX):<br>` +
                                   ` ⭕ TOP LAYER &nbsp; [2 CIRCLES] : GEOMETRIC MATRIX INITIALIZED<br>` +
                                   ` ⭕ MID LAYER &nbsp; [3 CIRCLES] : TETRA.4D CONTINENTAL BALANCER ACTIVE<br>` +
                                   ` ⭕ BASE LAYER [2 CIRCLES] : HEDRA.3D ZERO-POWER ANCHORS ATTACHED<br>` +
                                   `------------------------------------------------------------------------------------------<br>` +
                                   `<span style="color: #0000ff; font-weight:bold;">[ELEMENTAL_MIX]</span> EARTH, WIND, FIRE SYSTEMS PROCESSING STABLE // LIVE AT ${data.time}`;
                        document.getElementById('matrix_body').innerHTML = body;
                    });
            }
            setInterval(fetchTelemetry, 400); // Strict 400ms processing loop intervals matching 40MHz retro clock steps
            window.onload = fetchTelemetry;
        </script>
    </head>
    <body>
        <div class="crt-frame">
            <div id="matrix_header">Connecting...</div>
            <div>==========================================================================================</div>
            <div id="clock_line">Synchronizing clock cycles...</div>
            <div>==========================================================================================</div>
            <br>
            <div id="matrix_body">Waiting for active telemetry data packet stream...</div>
        </div>
    </body>
    </html>
    ''')

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=False)
