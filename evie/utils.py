import numpy as np

__all__ = ['normalize', 'perspective_projection_matrix', 'load_mesh']


def normalize(vec: np.ndarray) -> np.ndarray:
    """Normalize a vector.

    Parameters
    ----------
    vec : np.ndarray
        Vector to normalize.

    Returns
    -------
    np.ndarray
        Normalized vector.

    Raises
    ------
    ValueError
        If the vector is a zero vector.
    """
    norm = np.linalg.norm(vec)
    try:
        return vec / norm
    except ZeroDivisionError:
        raise ValueError("Cannot normalize a zero vector.")


def perspective_projection_matrix(fov: float, aspect: float, near: float, far: float) -> np.ndarray:
    """Create a perspective projection matrix.

    Parameters
    ----------
    fov : float
        Field of view in degrees.
    aspect : float
        Aspect ratio.
    near : float
        Near plane.
    far : float
        Far plane.

    Returns
    -------
    np.ndarray
        4x4 perspective projection matrix.
    """
    f = 1.0 / np.tan(np.radians(fov) / 2)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, far / (near - far), -1],
        [0, 0, (near * far) / (near - far), 0]
    ], dtype=np.float32)


def load_mesh(filename: str) -> list[float]:
    """
        Load a mesh from an obj file.

        Parameters:

            filename: the filename.

        Returns:

            The loaded data, in a flattened format.
    """

    v = []
    vt = []
    vn = []
    vertices = []

    with open(filename, "r") as file:
        line = file.readline()

        while line:

            words = line.split(" ")
            match words[0]:
                case "v":
                    v.append(read_vertex_data(words))
                case "vt":
                    vt.append(read_texcoord_data(words))
                case "vn":
                    vn.append(read_normal_data(words))
                case "f":
                    read_face_data(words, v, vt, vn, vertices)
            line = file.readline()

    return vertices


def read_vertex_data(words: list[str]) -> list[float]:
    """
        Returns a vertex description.
    """

    return [
        float(words[1]),
        float(words[2]),
        float(words[3])
    ]


def read_texcoord_data(words: list[str]) -> list[float]:
    """
        Returns a texture coordinate description.
    """

    return [
        float(words[1]),
        float(words[2])
    ]


def read_normal_data(words: list[str]) -> list[float]:
    """
        Returns a normal vector description.
    """

    return [
        float(words[1]),
        float(words[2]),
        float(words[3])
    ]


def read_face_data(
        words: list[str],
        v: list[list[float]], vt: list[list[float]],
        vn: list[list[float]], vertices: list[float]) -> None:
    """
        Reads an edgetable and makes a face from it.
    """

    triangle_count = len(words) - 3

    for i in range(triangle_count):
        make_corner(words[1], v, vt, vn, vertices)
        make_corner(words[2 + i], v, vt, vn, vertices)
        make_corner(words[3 + i], v, vt, vn, vertices)


def make_corner(corner_description: str,
                v: list[list[float]], vt: list[list[float]],
                vn: list[list[float]], vertices: list[float]) -> None:
    """
        Composes a flattened description of a vertex.
    """

    v_vt_vn = corner_description.split("/")

    for element in v[int(v_vt_vn[0]) - 1]:
        vertices.append(element)
    for element in vt[int(v_vt_vn[1]) - 1]:
        vertices.append(element)
    for element in vn[int(v_vt_vn[2]) - 1]:
        vertices.append(element)
