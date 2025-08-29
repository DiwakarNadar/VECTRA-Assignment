import matplotlib.pyplot as plt
import numpy as np

# ------------------------------
# Input: Room dimensions
# ------------------------------
M, N = 12, 10   # Width × Height

tile_sizes = [4, 3, 2, 1]  # Bigger first
colors = {1: "red", 2: "blue", 3: "yellow", 4: "green"}

# ------------------------------
# Spiral Traversal Generator
# ------------------------------
def spiral_coords(M, N):
    """Generate exactly M*N coordinates in spiral order (center first)."""
    x, y = M // 2, N // 2
    steps = 1
    dx, dy = 1, 0
    visited = 0
    yield (x, y)
    visited += 1

    while visited < M * N:
        for _ in range(2):  # two turns per step length
            for _ in range(steps):
                x, y = x + dx, y + dy
                if 0 <= x < M and 0 <= y < N:
                    yield (x, y)
                    visited += 1
                    if visited >= M * N:
                        return
            dx, dy = -dy, dx   # Rotate direction
        steps += 1

# ------------------------------
# Check + Place Tile
# ------------------------------
def can_place(board, x, y, size):
    """Check if a size×size tile fits at (x,y)."""
    if x + size > M or y + size > N:
        return False
    return np.all(board[y:y+size, x:x+size] == 0)

def place_tile(board, x, y, size, tile_id):
    board[y:y+size, x:x+size] = tile_id

# ------------------------------
# Fill the room
# ------------------------------
board = np.zeros((N, M), dtype=int)
tile_count = {s:0 for s in tile_sizes}
placed_tiles = []   # keep track of (x,y,size,color)

tile_id = 1
for (cx, cy) in spiral_coords(M, N):
    if board[cy, cx] != 0:  # Already filled
        continue
    for size in tile_sizes:
        if can_place(board, cx, cy, size):
            place_tile(board, cx, cy, size, tile_id)
            tile_count[size] += 1
            placed_tiles.append((cx, cy, size, colors[size]))
            tile_id += 1
            break

# ------------------------------
# Visualization
# ------------------------------
fig, ax = plt.subplots(figsize=(6,6))
for (x, y, size, color) in placed_tiles:
    # Draw square tile (y flipped for matplotlib coord system)
    ax.add_patch(plt.Rectangle((x, N-y-size), size, size,
                               facecolor=color, edgecolor="black", alpha=0.6))

ax.set_xlim(0, M)
ax.set_ylim(0, N)
ax.set_aspect("equal")
ax.set_xticks(range(M+1))
ax.set_yticks(range(N+1))
ax.grid(True)
plt.title(f"Room Tiling {M}x{N}")

plt.show()

# ------------------------------
# Print Results
# ------------------------------
print("Tile usage:")
for s in tile_sizes:
    print(f"{s}x{s} tiles: {tile_count[s]}")
