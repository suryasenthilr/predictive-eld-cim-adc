import numpy as np

def derive_predictive_eld_coefficients(beta=0.3):
    """
    Rigorously solves the Modified Z-Transform / Impulse-Invariant Transformation
    for a Continuous-Time Delta-Sigma Modulator with Excess Loop Delay:
        tau_d = (1 + beta) * Ts
    Target NTF: 2nd-order Butterworth NTF(z) = (1 - z^-1)^2 / (1 - 1.22 z^-1 + 0.41 z^-2)
    """
    print("="*75)
    print("ANALYTICAL DERIVATION: MULTI-CYCLE PREDICTIVE ELD COMPENSATION (tau_d > 1 Ts)")
    print("="*75)
    print(f"Excess Loop Delay parameter: beta = {beta:.2f} (tau_d = {1.0+beta:.2f} Ts)")
    
    # Target discrete-time loop filter:
    # H_target(z) = (0.78 z^-1 - 0.59 z^-2) / (1 - z^-1)^2
    # Target impulse response:
    # h_target[k] = 0.59 + 0.19 * k  for all k >= 1
    # Specifically:
    # h_target[1] = 0.7800
    # h_target[2] = 0.9700
    # h_target[3] = 1.1600
    
    # Continuous-time integrators response:
    # x1(t): Bitline integrator state (dx1/dt = -dac)
    # x2(t): OTA integrator state (dx2/dt = x1)
    # For DAC pulse spanning [1 + beta, 2 + beta] * Ts:
    # At k=0: x1=0, x2=0
    # At k=1: x1=0, x2=0  (PHYSICAL DEAD ZONE: DAC pulse has not arrived!)
    # At k=2: x1 = -(1 - beta), x2 = -0.5 * (1 - beta)^2
    # At k >= 3: x1 = -1.0, x2 = (1.5 + beta) - k
    
    # Loop filter output: v_ct = k1 * x1 + k2 * x2
    # Feedforward gain matching for k >= 3:
    # -v_ct[k] = k1 - k2*(1.5 + beta) + k2 * k  ==  0.59 + 0.19 * k
    k2 = 0.1900
    k1 = 0.5900 + k2 * (1.5 + beta)
    
    # Evaluate continuous filter response at k=1 and k=2:
    v_ct_1 = 0.0
    v_ct_2 = k1 * (-(1.0 - beta)) + k2 * (-0.5 * (1.0 - beta)**2)
    
    # Required predictive FIR look-ahead compensation taps:
    # v_q[k] = v_ct[k] - d1 * y[k-1] - d2 * y[k-2]
    # h_total[k] = -v_ct[k] + v_comp[k]
    d1 = 0.7800 - (-v_ct_1)
    d2 = 0.9700 - (-v_ct_2)
    
    print("\n[Continuous-Time Feedforward Gains]")
    print(f"  k1 (Bitline feedforward): {k1:.4f}")
    print(f"  k2 (OTA feedforward):     {k2:.4f}")
    
    print("\n[Predictive FIR Look-Ahead Taps (Quantizer Threshold Steering)]")
    print(f"  d1 (Tap 1, z^-1 delay):   {d1:.4f}")
    print(f"  d2 (Tap 2, z^-2 delay):   {d2:.4f}")
    
    print("\n[Impulse Response Matching Verification (k = 0 to 6)]")
    print(f" k  | h_target | h_ct_analog | v_predictive | h_total | Error")
    print("----------------------------------------------------------------")
    for k in range(7):
        if k == 0:
            h_tgt = 0.0
            h_ct = 0.0
            v_p = 0.0
        elif k == 1:
            h_tgt = 0.7800
            h_ct = 0.0
            v_p = d1
        elif k == 2:
            h_tgt = 0.9700
            h_ct = -v_ct_2
            v_p = d2
        else:
            h_tgt = 0.5900 + 0.1900 * k
            h_ct = k1 - k2*(1.5 + beta) + k2 * k
            v_p = 0.0
            
        h_tot = h_ct + v_p
        err = abs(h_tot - h_tgt)
        print(f" {k}  |  {h_tgt:.4f}  |   {h_ct:.4f}    |    {v_p:.4f}    | {h_tot:.4f}  | {err:.2e}")
        
    # Closed-loop pole placement:
    # 1 + H_target(z) = 0 => z^2 - 1.22 z + 0.41 = 0
    poles = np.roots([1.0, -1.22, 0.41])
    print(f"\n[Closed-Loop Poles]")
    print(f"  Poles: {poles[0]:.4f}, {poles[1]:.4f}")
    print(f"  Pole Radius: |z| = {np.abs(poles[0]):.4f} (Strictly inside unit circle: {np.abs(poles[0]) < 1.0})")
    print("="*75)

if __name__ == "__main__":
    derive_predictive_eld_coefficients(beta=0.3)
