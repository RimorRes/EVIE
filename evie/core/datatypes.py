import numpy as np

# Vertex data type
vertex = np.dtype({
    'names': ['x', 'y', 'z', 's', 't'],
    'formats': [np.float32, np.float32, np.float32, np.float32, np.float32],
    'offsets': [0, 4, 8, 12, 16],
    'itemsize': 20  # 5 * 4 bytes
})
