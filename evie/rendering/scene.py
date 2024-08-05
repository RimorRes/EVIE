import numpy as np
from evie.core.config import *
from evie.objects.entity import Entity, Cube
from evie.objects.camera import Camera

__all__ = ['Scene']


class Scene:
    """
    Manages all objects and coordinates their interactions.
    """
    __slots__ = ("entities", "cameras", "midpoint")

    def __init__(self):
        """
        Initialize the scene.
        """

        self.entities: dict[int, list[Entity]] = {
            ENTITY_TYPE["CUBE"]: [
                Cube(position=[0, 0, 0], eulers=[0, 0, 0]),
            ]
        }

        self.cameras = {
            LEFT: Camera(),
            RIGHT: Camera()
        }
        ipd = 0.06  # Interpupillary distance, in meters
        self.cameras[LEFT].position = np.array([-ipd / 2, 0, 10])
        self.cameras[RIGHT].position = np.array([ipd / 2, 0, 10])
        # Track the midpoint of the two cameras
        self.midpoint = (self.cameras[LEFT].position + self.cameras[RIGHT].position) / 2

    def update(self, dt: float) -> None:
        """
            Update all objects in the scene.

            Parameters:

                dt: framerate correction factor
        """

        for entities in self.entities.values():
            for entity in entities:
                entity.update(dt, self.midpoint)
