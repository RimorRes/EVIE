import numpy as np
from OpenGL.GL import *
from config import vertex_dtype


def rgba(r: float, g: float, b: float, a: float) -> np.uint32:
    """
    Create an RGBA color.
    :param r: Red
    :param g: Green
    :param b: Blue
    :param a: Alpha
    :return: RGBA color
    """
    return np.uint32((int(r * 255) << 24) | (int(g * 255) << 16) | (int(b * 255) << 8) | int(a * 255))


def mesh(vertex_data, index_data=None) -> tuple[int, int, int]:
    """
    Create a mesh from vertex and index data.
    :param vertex_data:
    :param index_data:
    :return: EBO, VBO, VAO
    """

    if index_data is None:
        index_data = np.arange(len(vertex_data), dtype=np.ubyte)

    vao = glGenVertexArrays(1)
    glBindVertexArray(vao)

    vbo = glGenBuffers(1)
    glBindBuffer(GL_ARRAY_BUFFER, vbo)
    glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)
    attribute_index = 0
    size = 3
    stride = vertex_dtype.itemsize
    offset = 0
    glVertexAttribPointer(attribute_index, size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset))
    glEnableVertexAttribArray(attribute_index)

    offset += 12  # 3 * 4 bytes
    attribute_index = 1
    size = 1
    glVertexAttribIPointer(attribute_index, size, GL_UNSIGNED_INT, stride, ctypes.c_void_p(offset))
    glEnableVertexAttribArray(attribute_index)

    ebo = glGenBuffers(1)
    glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, ebo)
    glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

    return ebo, vbo, vao


def build_triangle_mesh() -> tuple[int, int]:

    vertex_data = np.zeros(3, dtype=vertex_dtype)
    vertex_data[0] = (-0.5, -0.5, 0.0, rgba(1.0, 0.0, 0.0, 1.0))
    vertex_data[1] = (0.5, -0.5, 0.0, rgba(0.0, 1.0, 0.0, 1.0))
    vertex_data[2] = (0.0, 0.5, 0.0, rgba(0.0, 0.0, 1.0, 1.0))

    _, vbo, vao = mesh(vertex_data)

    return vbo, vao


def build_quad_mesh() -> tuple[int, int, int]:

    vertex_data = np.zeros(4, dtype=vertex_dtype)
    vertex_data[0] = (-0.5, 0.5, 0.1, rgba(0.0, 0.0, 1.0, 1.0))
    vertex_data[1] = (-0.5, -0.5, 0.1, rgba(0.0, 0.0, 1.0, 1.0))
    vertex_data[2] = (0.5, -0.5, 0.1, rgba(0.0, 0.0, 1.0, 1.0))
    vertex_data[3] = (0.5, 0.5, 0.1, rgba(0.0, 0.0, 1.0, 1.0))

    index_data = np.array((0, 1, 2, 2, 3, 0), dtype=np.ubyte)

    ebo, vbo, vao = mesh(vertex_data, index_data)

    return ebo, vbo, vao
