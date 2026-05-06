import numpy as np
from numba import njit


@njit
def orient2d(ax, ay, bx, by, cx, cy):
    return (bx - ax) * (cy - ay) - (by - ay) * (cx - ax)


@njit
def rasterize_triangles_edge_function(triangles, width, height):
    """
    Triangle rasterization using bounding boxes + edge functions.

    Input:
        triangles: shape (num_triangles, 3, 2)
        width, height: grid size

    Output:
        grid: uint8 array where 1 = covered cell, 0 = outside
    """
    grid = np.zeros((height, width), dtype=np.uint8)

    for t in range(triangles.shape[0]):
        x0 = triangles[t, 0, 0]
        y0 = triangles[t, 0, 1]
        x1 = triangles[t, 1, 0]
        y1 = triangles[t, 1, 1]
        x2 = triangles[t, 2, 0]
        y2 = triangles[t, 2, 1]

        # Skip degenerate triangles
        area = orient2d(x0, y0, x1, y1, x2, y2)
        if area == 0.0:
            continue

        # Ensure counter-clockwise orientation
        if area < 0.0:
            temp_x = x1
            temp_y = y1
            x1 = x2
            y1 = y2
            x2 = temp_x
            y2 = temp_y

        # Bounding box
        min_x = int(np.floor(min(x0, x1, x2)))
        max_x = int(np.ceil(max(x0, x1, x2)))
        min_y = int(np.floor(min(y0, y1, y2)))
        max_y = int(np.ceil(max(y0, y1, y2)))

        # Clip to grid
        if min_x < 0:
            min_x = 0
        if min_y < 0:
            min_y = 0
        if max_x >= width:
            max_x = width - 1
        if max_y >= height:
            max_y = height - 1

        # Rasterize candidate cells
        for y in range(min_y, max_y + 1):
            py = y + 0.5

            for x in range(min_x, max_x + 1):
                px = x + 0.5

                w0 = orient2d(x1, y1, x2, y2, px, py)
                w1 = orient2d(x2, y2, x0, y0, px, py)
                w2 = orient2d(x0, y0, x1, y1, px, py)

                if w0 >= 0.0 and w1 >= 0.0 and w2 >= 0.0:
                    grid[y, x] = 1

    return grid