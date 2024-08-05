import numpy as np
from OpenGL.GL import *
import evie.core.datatypes as dt
from evie.utils import load_mesh

__all__ = ['Mesh', 'Quad', 'ObjMesh']


class Mesh:
    """
    Represents a 3D mesh with vertex and index data.

    Attributes
    ----------
    VAO : int
        Vertex Array Object ID.
    VBO : int
        Vertex Buffer Object ID.
    EBO : int
        Element Buffer Object ID.
    """

    def __init__(self, vertex_data: np.ndarray, index_data: np.ndarray = None) -> None:
        """Create a mesh from vertex and index data.

        Parameters
        ----------
        vertex_data : np.ndarray[dt.vertex]
            Array of vertices. Each vertex is represented by a tuple of x, y, z, s, t.
        index_data : np.ndarray[np.ubyte]
            Array of indices. Dictates the order in which vertices are drawn. Required for proper triangle rendering.

        Returns
        -------
        None
        """

        if index_data is None:
            index_data = np.arange(len(vertex_data), dtype=np.ubyte)

        self.vertex_count = len(index_data)
        self.is_armed = False

        # Generate Vertex Array Object
        # x, y, z, s, t
        self.VAO = glGenVertexArrays(1)
        glBindVertexArray(self.VAO)

        # Generate Vertex Buffer Object
        self.VBO = glGenBuffers(1)
        glBindBuffer(GL_ARRAY_BUFFER, self.VBO)
        glBufferData(GL_ARRAY_BUFFER, vertex_data.nbytes, vertex_data, GL_STATIC_DRAW)

        # Position
        attribute_index = 0
        size = 3
        stride = dt.vertex.itemsize
        offset = 0
        glVertexAttribPointer(attribute_index, size, GL_FLOAT, GL_FALSE, stride, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(attribute_index)
        # Texture coordinates
        attribute_index = 1
        size = 2
        offset += 12  # 3 * 4 bytes
        glVertexAttribIPointer(attribute_index, size, GL_UNSIGNED_INT, stride, ctypes.c_void_p(offset))
        glEnableVertexAttribArray(attribute_index)

        # Generate Element Buffer Object
        self.EBO = glGenBuffers(1)
        glBindBuffer(GL_ELEMENT_ARRAY_BUFFER, self.EBO)
        glBufferData(GL_ELEMENT_ARRAY_BUFFER, index_data.nbytes, index_data, GL_STATIC_DRAW)

    def arm(self) -> None:
        """Arms the vertex array object for rendering.
        
        Binds the vertex array object.
        
        Returns
        -------
        None
        """
        glBindVertexArray(self.VAO)
        self.is_armed = True

    def draw(self, mode: int = GL_TRIANGLES) -> None:
        """Draws the mesh.

        Draws the mesh of the currently bound vertex array.

        Returns
        -------
        None

        Raises
        ------
        RuntimeError
            If the vertex array object is not armed.

        Warnings
        --------
            To properly draw the mesh, the vertex array object must be armed. Call the `arm` method before drawing.
            This method does not unbind the vertex array object.

        """
        if not self.is_armed:
            raise RuntimeError("Vertex Array Object is not armed. Call the `arm` method before drawing.")
        glDrawElements(mode, self.vertex_count, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
        self.is_armed = False

    def destroy(self) -> None:
        glDeleteBuffers(2, (self.VBO, self.EBO))
        glDeleteVertexArrays(1, self.VAO)


class Quad(Mesh):
    """
    A simple quad mesh with texture coordinates.
    """
    def __init__(self):

        vertex_data = np.zeros(4, dtype=dt.vertex)
        vertex_data[0] = (-0.5, -0.5, 0.0, 0.0, 0.0)
        vertex_data[1] = (0.5, -0.5, 0.0, 1.0, 0.0)
        vertex_data[2] = (0.5, 0.5, 0.0, 1.0, 1.0)
        vertex_data[3] = (-0.5, 0.5, 0.0, 0.0, 1.0)

        index_data = np.array((0, 1, 2, 2, 3, 0), dtype=np.ubyte)

        super().__init__(vertex_data, index_data)


class ObjMesh(Mesh):  # TODO: Uses normals
    """
    A mesh loaded from an .obj file.
    """
    def __init__(self, filepath: str):

        raw = load_mesh(filepath)
        vertex_count = len(raw)//8

        print(vertex_count)

        vertex_data = np.zeros(vertex_count, dtype=dt.vertex)
        for i in range(vertex_count):
            vertex_data[i] = (raw[i*8], raw[i*8+1], raw[i*8+2], raw[i*8+3], raw[i*8+4])

        print(vertex_data)
        super().__init__(vertex_data)
