import numpy as np

def read_ltspice_raw(raw_path):
    with open(raw_path, 'rb') as f:
        content = f.read()
        
    # In LTspice 24, the header is UTF-16 LE
    # Find the Binary: keyword in UTF-16
    binary_marker = "Binary:\n".encode('utf-16-le')
    marker_pos = content.find(binary_marker)
    if marker_pos == -1:
        # Fallback to UTF-8 / ASCII
        binary_marker = b"Binary:\n"
        marker_pos = content.find(binary_marker)
        header_bytes = content[:marker_pos]
        header_text = header_bytes.decode('utf-8', errors='ignore')
        data_start = marker_pos + len(binary_marker)
    else:
        header_bytes = content[:marker_pos]
        header_text = header_bytes.decode('utf-16-le', errors='ignore')
        data_start = marker_pos + len(binary_marker)
        
    lines = header_text.splitlines()
    n_vars = 0
    n_points = 0
    variables = []
    
    for i, line in enumerate(lines):
        line = line.strip()
        if line.startswith("No. Variables:"):
            n_vars = int(line.split(":")[1].strip())
        elif line.startswith("No. Points:"):
            n_points = int(line.split(":")[1].strip())
        elif line.startswith("Variables:"):
            for vline in lines[i+1:]:
                parts = vline.strip().split()
                if len(parts) >= 2:
                    variables.append(parts[1])
                    
    print(f"Header parsed successfully: {n_vars} variables, {n_points} points.")
    raw_data = content[data_start:]
    
    # In transient binary: time is float64 (8 bytes), variables are float32 (4 bytes each)
    point_size = 8 + 4 * (n_vars - 1)
    expected_bytes = n_points * point_size
    print(f"Data bytes available: {len(raw_data)}, Expected: {expected_bytes}")
    
    dtype_fields = [('time', '<f8')] + [(v, '<f4') for v in variables[1:]]
    parsed_array = np.frombuffer(raw_data[:expected_bytes], dtype=dtype_fields)
    
    return variables, parsed_array

vars, data = read_ltspice_raw("c:/Users/surya/OneDrive/Documents/LT_spice_cim_predictive_deltasigma/circuits/01_Uncompensated_ELD_Instability.raw")
print("\nVariables list:", vars)
print(f"Time: {data['time'][0]*1e9:.2f} ns to {data['time'][-1]*1e9:.2f} ns ({len(data)} steps)")
print(f"V(vbl) Min: {np.min(data['V(vbl)']):.4f} V, Max: {np.max(data['V(vbl)']):.4f} V")
print(f"V(v2)  Min: {np.min(data['V(v2)']):.4f} V, Max: {np.max(data['V(v2)']):.4f} V")
print(f"V(vq)  Min: {np.min(data['V(vq)']):.4f} V, Max: {np.max(data['V(vq)']):.4f} V")
