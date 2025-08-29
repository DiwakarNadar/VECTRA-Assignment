import matplotlib.pyplot as plt
import numpy as np

def draw_triangle(ax, x, y, size, upright=True, color='blue'):
    h = np.sqrt(3)/2 * size
    if upright:
        points = [(x, y), (x + size/2, y + h), (x + size, y)]
    else:
        points = [(x, y + h), (x + size/2, y), (x + size, y + h)]
    triangle = plt.Polygon(points, color=color, edgecolor='black')
    ax.add_patch(triangle)

def draw_perfect_pyramid(depth=4, size=1.0):
    fig, ax = plt.subplots()
    ax.set_aspect('equal')
    ax.axis('off')

    h = np.sqrt(3)/2 * size
    vertical_step = h

    for row in range(depth):
        num_pairs = row + 1
        start_x = -size * num_pairs / 2
        y = -row * vertical_step

        for i in range(num_pairs):
            x_upright = start_x + i * size
            draw_triangle(ax, x_upright, y, size, upright=True, color='blue')

            if i != num_pairs - 1:
                x_inverted = start_x + i * size + size / 2
                draw_triangle(ax, x_inverted, y, size, upright=False, color='gold')

    ax.set_xlim(-depth * size, depth * size)
    ax.set_ylim(-depth * h, h)
    plt.title(f"Pyramid with Depth={depth}")
    plt.show()

draw_perfect_pyramid(depth=4, size=1)
