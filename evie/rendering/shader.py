from OpenGL.GL import *
from OpenGL.GL.shaders import compileProgram, compileShader

__all__ = ['Shader']


def create_shader_module(filepath: str, module_type: int) -> int:
    """
    Create a shader module from a file.
    Parameters
    ----------
    filepath
    module_type

    Returns
    -------
    Shader module
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


class Shader:
    """
    Represents a shader program.
    """

    def __init__(self, vertex_path: str, fragment_path: str):
        """Create a shader program from vertex and fragment paths.

        Parameters
        ----------
        vertex_path : str
            Path to the vertex shader.
        fragment_path : str
            Path to the fragment shader.
        """

        self.program = create_shader_program(vertex_path, fragment_path)

        # Initialise uniform location caches
        self.single_uniforms: dict[int, int] = {}
        self.multi_uniforms: dict[int, list[int]] = {}

    def cache_single_uniform(self, uniform_type: int, uniform_name: str) -> None:
        """Cache a uniform location. This is for uniforms that have one location

        Parameters
        ----------
        uniform_type
        uniform_name

        Returns
        -------
        None
        """
        location = glGetUniformLocation(self.program, uniform_name)
        self.single_uniforms[uniform_type] = location

    def cache_multi_uniform(self, uniform_type: int, uniform_name: list[str]) -> None:
        """Cache a uniform location. This is for uniforms that have multiple locations.

        Searches and stores the locations of uniforms with multiple locations per variable.
        e.g. Arrays

        Parameters
        ----------
        uniform_type
        uniform_name

        Returns
        -------

        """
        if uniform_type not in self.multi_uniforms:
            self.multi_uniforms[uniform_type] = []

        location = glGetUniformLocation(self.program, uniform_name)
        self.multi_uniforms[uniform_type].append(location)

    def get_single_location(self, uniform_type: int) -> int:
        """Fetch a single uniform location.

        Parameters
        ----------
        uniform_type

        Returns
        -------
        int
            Uniform location
        """
        return self.single_uniforms[uniform_type]

    def get_index_from_multi_location(self, uniform_type: int, index: int) -> int:
        """Fetch a multi uniform location.

        Parameters
        ----------
        uniform_type : int
        index : int

        Returns
        -------
        int
            Uniform location of chosen index
        """
        return self.multi_uniforms[uniform_type][index]

    def use(self) -> None:
        """Use the shader program.

        Returns
        -------
        None
        """
        glUseProgram(self.program)

    def destroy(self) -> None:
        """Destroy the shader program.

        Free any allocated memory.

        Returns
        -------
        None
        """
        glDeleteProgram(self.program)
