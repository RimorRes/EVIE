import numpy as np
from .entity import Entity
from evie.core.config import GLOBAL_Y
from evie.utils import normalize

__all__ = ['Camera']


class Camera(Entity):

    def __init__(self):
        super().__init__()
        self._view_mat = np.identity(4, dtype=np.float32)

    @property
    def view_matrix(self):
        """Updates and returns the view matrix.

        Returns
        -------
        np.ndarray
            4x4 view matrix.

        References
        ----------
        https://learnopengl.com/Getting-started/Camera
        https://medium.com/@carmencincotti/lets-look-at-magic-lookat-matrices-c77e53ebdf78
        """

        # Yes it updates every time you access it, but it's only passed on to the shader once per frame.
        # Should check if this is a bottleneck.
        self._view_mat[:3, :3] = self.rotation.T
        self._view_mat[3, :3] = - self.rotation @ self.position
        return self._view_mat

    def look_at(self, target: np.ndarray):
        """ Look at a target.

        Calculate the camera's forward, right, and up vectors of a right-handed coordinate system (OPENGL)
        to look at a target position in world space.
        Sets the rotation matrix accordingly.

        Parameters
        ----------
        target: np.ndarray

        Returns
        -------
        None

        References
        ----------
        https://learnopengl.com/Getting-started/Camera
        https://medium.com/@carmencincotti/lets-look-at-magic-lookat-matrices-c77e53ebdf78

        """
        forward = normalize(target - self.position)
        right = normalize(np.cross(GLOBAL_Y, forward))
        up = normalize(np.cross(forward, right))
        self.rotation = np.vstack((right, up, forward))
