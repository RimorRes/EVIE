import ctypes
import numpy as np

__all__ = [
    'SCREEN_WIDTH', 'SCREEN_HEIGHT', 'VSYNC',
    'LEFT', 'RIGHT',
    'GLOBAL_X', 'GLOBAL_Y', 'GLOBAL_Z',
    'ENTITY_TYPE', 'UNIFORM_TYPE', 'PIPELINE_TYPE',
    'glfw_error_callback'
]


# Display Settings
SCREEN_WIDTH = 2560
SCREEN_HEIGHT = 1440
VSYNC = True

# LEFT and RIGHT flags for stereoscopic rendering.
LEFT = 0
RIGHT = 1

GLOBAL_X = np.array([1, 0, 0], dtype=np.float32)
GLOBAL_Y = np.array([0, 1, 0], dtype=np.float32)
GLOBAL_Z = np.array([0, 0, 1], dtype=np.float32)

ENTITY_TYPE = {
    "CUBE": 0
}

UNIFORM_TYPE = {
    "MODEL": 0,
    "VIEW": 1,
    "PROJECTION": 2,
    "BASE_COLOR": 3
}

PIPELINE_TYPE = {
    "Standard": 0
}


class GLFWError(Exception):
    """Custom exception for GLFW errors."""
    pass


def glfw_error_callback(err_code: int, description: ctypes.c_char_p) -> None:
    """
    Callback function to handle GLFW errors.

    Parameters
    ----------
    err_code : int
    description : ctypes.c_char_p

    Returns
    -------
    None

    Raises
    ------
    GLFWError

    """
    raise GLFWError(f"GLFW error [{err_code}]: {description.decode('utf-8')}")
