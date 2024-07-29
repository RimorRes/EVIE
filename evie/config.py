import sys
import numpy as np
from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

SCREEN_WIDTH = 1440
SCREEN_HEIGHT = 2560

vertex_dtype = np.dtype({
    'names': ['x', 'y', 'z', 'rgba', 's', 't'],
    'formats': [np.float32, np.float32, np.float32, np.uint32, np.float32, np.float32],
    'offsets': [0, 4, 8, 12, 16, 20],
    'itemsize': 24  # 6 * 4 bytes
})


def glfw_error_callback(err_code: int, description) -> None:
    """
    Callback function to handle GLFW errors.

    :param err_code: Error code
    :param description: Description of the error
    :return:
    """
    print(f"GLFW error [{err_code}]: {description.decode('utf-8')}", file=sys.stderr)


def create_shader_module(filepath: str, module_type: int) -> int:
    """
    Create a shader module from a file.
    :param filepath:
    :param module_type:
    :return:
    """

    with open(filepath, 'r') as file:
        source_code = file.readlines()

    return compileShader(source_code, module_type)


def create_shader_program(vertex_filepath: str, fragment_filepath: str) -> int:
    """
    Create a shader program from a vertex and fragment shader file.
    :param vertex_filepath:
    :param fragment_filepath:
    :return:
    """
    vertex_module = create_shader_module(vertex_filepath, GL_VERTEX_SHADER)
    fragment_module = create_shader_module(fragment_filepath, GL_FRAGMENT_SHADER)

    shader = compileProgram(vertex_module, fragment_module)

    glDeleteShader(vertex_module)
    glDeleteShader(fragment_module)

    return shader
