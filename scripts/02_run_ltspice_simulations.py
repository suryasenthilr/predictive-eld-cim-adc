import subprocess
import os
import sys
import numpy as np

# Ensure scripts dir can find parse_raw
sys.path.append(os.path.dirname(__file__))
from parse_raw import read_ltspice_raw

LTSPICE_EXE = r"C:\Users\surya\AppData\Local\Programs\ADI\LTspice\LTspice.exe"
CIRCUITS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "circuits"))

schematics = [
    "01_Uncompensated_ELD_Instability.asc",
    "02_Predictive_LookAhead_Stabilized_Modulator.asc",
    "03_CiM_Crossbar_Streaming_Readout.asc"
]

def run_simulation(asc_name):
    asc_path = os.path.join(CIRCUITS_DIR, asc_name)
    raw_path = os.path.splitext(asc_path)[0] + ".raw"
    log_path = os.path.splitext(asc_path)[0] + ".log"
    
    print(f"\n=======================================================")
    print(f"Running LTspice batch simulation: {asc_name}")
    print(f"=======================================================")
    
    cmd = f'"{LTSPICE_EXE}" -b "{asc_path}"'
    res = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    
    if os.path.exists(raw_path):
        size_kb = os.path.getsize(raw_path) / 1024.0
        print(f"Simulation completed successfully! Output: {os.path.basename(raw_path)} ({size_kb:.1f} KB)")
        vars, data = read_ltspice_raw(raw_path)
        return vars, data
    else:
        print(f"Error: RAW file not found! Check log: {log_path}")
        if os.path.exists(log_path):
            with open(log_path, 'r', errors='ignore') as lf:
                print(lf.read()[-500:])
        return None, None

if __name__ == "__main__":
    results = {}
    for asc in schematics:
        vars, data = run_simulation(asc)
        if data is not None:
            results[asc] = data
            
    print("\n\nAll simulations finished successfully!")
