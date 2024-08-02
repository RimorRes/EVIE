import numpy as np
from scipy.spatial.transform import Rotation


class Entity:

    def __init__(self):
        self._pos_mat = np.identity(4, dtype=np.float32)
        self._rot_mat = np.identity(4, dtype=np.float32)
        self._scale_mat = np.identity(4, dtype=np.float32)

    @property
    def position(self):
        return self._pos_mat[:3, 3]

    @position.setter
    def position(self, vec3: np.ndarray):
        self._pos_mat[:3, 3] = vec3.astype(np.float32)

    @property
    def rotation(self):
        return self._rot_mat[:3, :3]

    @rotation.setter
    def rotation(self, mat3: np.ndarray):
        self._rot_mat[:3, :3] = mat3.astype(np.float32)

    @property
    def scale(self):
        return self._scale_mat[:3, :3] @ np.ones(3)

    @scale.setter
    def scale(self, vec3: np.ndarray):
        self._scale_mat[:3, :3] = np.diag(vec3.astype(np.float32))

    @property
    def model_matrix(self):
        # Might need to play around with the order of these operations.
        # Transpose is necessary because OpenGL uses column-major matrices.
        return (self._pos_mat @ self._rot_mat @ self._scale_mat).T

    def update(self, dt: float, camera_pos: np.ndarray) -> None:
        """Update the object.

        This is meant to be implemented by
        objects extending this class.

        Parameters
        ----------

        dt : float
            Timestep. Serves as a framerate correction factor.
        camera_pos : np.ndarray
            the position of the camera in the scene
        """
        pass


class Cube(Entity):
    """
    The beloved default cube.
    """

    def __init__(self, position: list[float], eulers: list[float]):
        super().__init__()
        self.eulers = np.array(eulers, dtype=np.float32)

        self.position = np.array(position)
        self.rotation = Rotation.from_euler("xyz", self.eulers).as_matrix()
        self.scale = np.array([1, 1, 1])

        self.t = 0

    def update(self, dt: float, player_pos: np.ndarray):
        """
            Update the cube.
        """
        omega = 2*np.pi / 10
        self.eulers += np.array([0, omega, omega]) * dt
        self.eulers %= np.pi * 2
        self.rotation = Rotation.from_euler("xyz", self.eulers).as_matrix()

        self.t += dt*2
        self.position = np.array([np.cos(self.t), np.sin(self.t), 0])

