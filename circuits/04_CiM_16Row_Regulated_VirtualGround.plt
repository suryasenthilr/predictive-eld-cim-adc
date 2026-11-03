[Transient Analysis]
{
	NPanes: 3
	{
		traces: 1 {0x0,"V(vbl)"}
		Xrange: 0 1.2e-07
		Yrange: -0.0001 0.0006
		Ylabel: "V_BL Virtual Ground (V)"
	}
	{
		traces: 2 {0x0,"V(vint)"},{0x1,"V(v2)"}
		Xrange: 0 1.2e-07
		Yrange: -0.5 1.5
		Ylabel: "Integrator States (V)"
	}
	{
		traces: 1 {0x0,"V(y_filt)"}
		Xrange: 0 1.2e-07
		Yrange: 0.2 1.1
		Ylabel: "Sinc-2 Normalized MAC [0, 1]"
	}
}
