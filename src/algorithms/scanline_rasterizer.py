import numpy as np
from numba import njit

@njit
def scanline_fill_et_ael(xs, ys, width, height):
    """
    Scan-line polygon fill using Edge Table + Active Edge List.
    Input:
        xs, ys: polygon vertices in grid coordinates
        width, height: output grid size
    Output:
        grid: uint8 array where 1 = covered cell, 0 = outside
    """

    n = len(xs)
    grid = np.zeros((height, width), dtype=np.uint8)

    # Edge table represented as linked lists per scanline
    edge_start_y = np.empty(n, dtype=np.int64)
    edge_end_y = np.empty(n, dtype=np.int64)
    edge_x = np.empty(n, dtype=np.float64)
    edge_inv_slope = np.empty(n, dtype=np.float64)
    edge_next = np.empty(n, dtype=np.int64)

    bucket_head = np.full(height, -1, dtype=np.int64)
    edge_count = 0

    # Build edge table
    for i in range(n):
        j = (i + 1) % n

        x1 = xs[i]
        y1 = ys[i]
        x2 = xs[j]
        y2 = ys[j]

        # Ignore horizontal edges
        if y1 == y2:
            continue

        # Ensure lower endpoint first
        if y1 < y2:
            x_lower = x1
            y_lower = y1
            x_upper = x2
            y_upper = y2
        else:
            x_lower = x2
            y_lower = y2
            x_upper = x1
            y_upper = y1

        inv_slope = (x_upper - x_lower) / (y_upper - y_lower)

        # We sample grid cells at their centers: y + 0.5
        y_start = int(np.ceil(y_lower - 0.5))
        y_end = int(np.ceil(y_upper - 0.5))  # exclusive

        if y_end <= 0 or y_start >= height:
            continue

        if y_start < 0:
            y_start = 0
        if y_end > height:
            y_end = height

        if y_start >= y_end:
            continue

        scan_y = y_start + 0.5
        x_at_y_start = x_lower + (scan_y - y_lower) * inv_slope

        edge_start_y[edge_count] = y_start
        edge_end_y[edge_count] = y_end
        edge_x[edge_count] = x_at_y_start
        edge_inv_slope[edge_count] = inv_slope

        # Insert edge into bucket for y_start
        edge_next[edge_count] = bucket_head[y_start]
        bucket_head[y_start] = edge_count

        edge_count += 1

    # Active Edge List arrays
    active_edges = np.empty(n, dtype=np.int64)
    active_count = 0

    # Process scanlines
    for y in range(height):

        # Add edges that start at this scanline
        e = bucket_head[y]
        while e != -1:
            active_edges[active_count] = e
            active_count += 1
            e = edge_next[e]

        # Remove edges whose y_end has been reached
        write = 0
        for k in range(active_count):
            e_idx = active_edges[k]
            if edge_end_y[e_idx] > y:
                active_edges[write] = e_idx
                write += 1
        active_count = write

        # Sort active edges by current x using insertion sort
        for a in range(1, active_count):
            key = active_edges[a]
            key_x = edge_x[key]
            b = a - 1

            while b >= 0 and edge_x[active_edges[b]] > key_x:
                active_edges[b + 1] = active_edges[b]
                b -= 1

            active_edges[b + 1] = key

        # Fill between pairs of intersections
        for k in range(0, active_count - 1, 2):
            left_edge = active_edges[k]
            right_edge = active_edges[k + 1]

            x_left = edge_x[left_edge]
            x_right = edge_x[right_edge]

            # Sample grid cells at x + 0.5
            x_start = int(np.ceil(x_left - 0.5))
            x_end = int(np.ceil(x_right - 0.5))  # exclusive

            if x_start < 0:
                x_start = 0
            if x_end > width:
                x_end = width

            for x in range(x_start, x_end):
                grid[y, x] = 1

        # Incrementally update x-intersections
        for k in range(active_count):
            e_idx = active_edges[k]
            edge_x[e_idx] += edge_inv_slope[e_idx]

    return grid



