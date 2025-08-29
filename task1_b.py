import numpy as np
import matplotlib.pyplot as plt
from shapely.geometry import Polygon, Point

# ------------------------------
# Input Polygon Vertices
# ------------------------------
vertices = np.array([
    (9.05, 7.76),
    (12.5, 3.0),
    (10.0, 0.0),
    (5.0, 0.0),
    (2.5, 3.0)
])

# Close the polygon by repeating the first point
poly = Polygon(vertices)
n = len(vertices)

# ------------------------------
# 1. Represent polygon edges as vectors
# ------------------------------
edges = []
for i in range(n):
    p1, p2 = vertices[i], vertices[(i+1) % n]
    edges.append(p2 - p1)   # vector from p1 to p2
edges = np.array(edges)

# ------------------------------
# 2. Area using shoelace formula
# ------------------------------
def shoelace_area(verts):
    x = verts[:,0]
    y = verts[:,1]
    return 0.5 * abs(np.dot(x, np.roll(y, -1)) - np.dot(y, np.roll(x, -1)))

area_calc = shoelace_area(vertices)
area_shapely = poly.area

# ------------------------------
# 3. Edge lengths using vector norms
# ------------------------------
edge_lengths = np.linalg.norm(edges, axis=1)

# ------------------------------
# 4. Interior angles using dot product
# ------------------------------
angles = []
is_convex = True
for i in range(n):
    prev_vec = vertices[i-1] - vertices[i]          # vector to previous vertex
    next_vec = vertices[(i+1) % n] - vertices[i]    # vector to next vertex

    # angle formula: cosθ = (u·v)/(|u||v|)
    dot = np.dot(prev_vec, next_vec)
    norm_prod = np.linalg.norm(prev_vec) * np.linalg.norm(next_vec)
    theta = np.degrees(np.arccos(dot / norm_prod))

    # cross product (sign check for convexity)
    cross = np.cross(prev_vec, next_vec)
    if cross < 0:   # reflex angle (>180)
        theta = 360 - theta
    if theta >= 180:
        is_convex = False

    angles.append(round(theta, 2))

# ------------------------------
# 5. Centroid
# ------------------------------
centroid_calc = vertices.mean(axis=0)
centroid_shapely = (poly.centroid.x, poly.centroid.y)

# ------------------------------
# Print Results
# ------------------------------
print("Polygon Area (Shoelace):", round(area_calc, 2))
print("Polygon Area (Shapely):", round(area_shapely, 2))
print("Edge Lengths:", np.round(edge_lengths, 2).tolist())
print("Interior Angles (degrees):", angles)
print("Is Convex:", is_convex)
print("Centroid (Average):", np.round(centroid_calc, 2).tolist())
print("Centroid (Shapely):", (round(centroid_shapely[0], 2), round(centroid_shapely[1], 2)))

# ------------------------------
# 6. Visualization
# ------------------------------
plt.figure(figsize=(6,6))
x, y = vertices[:,0], vertices[:,1]

# Fill polygon
plt.fill(x, y, color="lightblue", alpha=0.6, edgecolor="black")

# Plot vertices and label
for i, (px, py) in enumerate(vertices):
    plt.plot(px, py, "bo")
    plt.text(px+0.1, py+0.1, f"V{i+1}", fontsize=10, color="blue")

# Mark centroid
plt.plot(centroid_calc[0], centroid_calc[1], "ro")
plt.text(centroid_calc[0]+0.1, centroid_calc[1], "Centroid", fontsize=10, color="red")

# Annotate angles
for i, (px, py) in enumerate(vertices):
    plt.text(px-0.5, py-0.5, f"{angles[i]}°", fontsize=9, color="darkgreen")

plt.title("Polygon Geometry with Vector Algebra")
plt.axis("equal")
plt.show()
