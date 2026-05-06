import numpy as np
import mapbox_earcut as earcut


def triangulate_polygon(xs, ys):
    """
    Triangulates a simple polygon.

    Input:
        xs, ys: polygon vertices in grid coordinates

    Output:
        triangles: ndarray of shape (num_triangles, 3, 2)
    """
    vertices = np.column_stack((xs, ys)).astype(np.float64)

    # one ring: the outer polygon
    ring_end_indices = np.array([len(vertices)], dtype=np.uint32)
    indices = earcut.triangulate_float64(vertices, ring_end_indices)
    triangles = vertices[indices].reshape(-1, 3, 2)

    return triangles