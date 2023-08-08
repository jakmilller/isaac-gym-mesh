import numpy as np

# Load OBJ file
with open('rings.obj', 'r') as f:
    lines = f.readlines()

vertices = []

# Extract vertices
for line in lines:
    if line.startswith('v '):
        _, x, y, z = line.split()
        vertices.append([float(x), float(y), float(z)])

# Apply scaling
scale_factor = 0.2
scaled_vertices = np.array(vertices) * scale_factor

# Write scaled vertices to a new OBJ file
with open('rings_scaled.obj', 'w') as f:
    for v in scaled_vertices:
        f.write(f'v {v[0]} {v[1]} {v[2]}\n')
        # You would also need to write the other lines (e.g., normals, faces, etc.) from the original OBJ file.

print("Scaling completed.")
