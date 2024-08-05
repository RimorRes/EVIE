import numpy as np
from OpenGL.GL import *
from evie.core.config import *
from evie.rendering.mesh import Mesh, ObjMesh
from evie.rendering.material import Material
from evie.rendering.shader import Shader
from evie.objects.entity import Entity
from evie.objects.camera import Camera
from evie.utils import perspective_projection_matrix

# TODO: SWITCH TO GLM!
__all__ = ['GraphicsEngine']


class GraphicsEngine:

    def __init__(self):
        """
        Initialise the graphics engine
        """
        # Initialise OpenGL
        glClearColor(0.0, 0.0, 0.0, 1)
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        # TODO: Enable backface culling
        # glEnable(GL_CULL_FACE)
        # glCullFace(GL_BACK)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Link assets
        self._link_assets()
        # Set static uniforms
        self._set_static_uniforms()
        # Get uniform locations
        self._get_uniform_locations()

    def _link_assets(self) -> None:
        """
        Link assets to the engine
        """
        # Load meshes
        self.meshes: dict[int, Mesh] = {
            ENTITY_TYPE["CUBE"]: ObjMesh("../assets/models/cube.obj")
        }

        # Load materials
        self.materials: dict[int, Material] = {
            ENTITY_TYPE["CUBE"]: Material("../assets/textures/uvgrid.png")
        }

        # Load shaders
        self.shaders: dict[int, Shader] = {
            PIPELINE_TYPE["Standard"]: Shader("../assets/shaders/vertex.vert", "../assets/shaders/fragment.frag")
        }

    def _set_static_uniforms(self) -> None:
        # TODO: Allow for multiple shaders
        shader = self.shaders[PIPELINE_TYPE["Standard"]]
        shader.use()
        glUniform1i(glGetUniformLocation(shader.program, "imageTexture"), 0)

        aspect = (SCREEN_WIDTH//2) / SCREEN_HEIGHT
        perspective_projection = perspective_projection_matrix(67.0, aspect, 0.1, 100.0)
        glUniformMatrix4fv(
            glGetUniformLocation(shader.program, "projection"),
            1, GL_FALSE, perspective_projection
        )

    def _get_uniform_locations(self) -> None:
        # TODO: Allow for multiple shaders
        shader = self.shaders[PIPELINE_TYPE["Standard"]]
        shader.use()

        shader.cache_single_uniform(UNIFORM_TYPE["MODEL"], "model")
        shader.cache_single_uniform(UNIFORM_TYPE["VIEW"], "view")
        shader.cache_single_uniform(UNIFORM_TYPE["BASE_COLOR"], "baseColor")

    def render(self, stereo_cameras: dict[int, Camera], renderables: dict[int, list[Entity]]) -> None:
        """
        Render the scene
        """

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        shader = self.shaders[PIPELINE_TYPE["Standard"]]
        shader.use()

        # Render scene with each camera
        for side, camera in stereo_cameras.items():
            # Set viewport
            if side == LEFT:
                glViewport(0, 0, SCREEN_WIDTH//2, SCREEN_HEIGHT)
            elif side == RIGHT:
                glViewport(SCREEN_WIDTH//2, 0, SCREEN_WIDTH//2, SCREEN_HEIGHT)

            # Set view matrix
            glUniformMatrix4fv(
                shader.get_single_location(UNIFORM_TYPE["VIEW"]),
                1, GL_FALSE, camera.view_matrix
            )

            for ent_type, entities in renderables.items():
                if ent_type not in self.materials:
                    continue

                mesh = self.meshes[ent_type]
                mesh.arm()
                material = self.materials[ent_type]
                material.use()

                color = np.array([1.0, 1.0, 1.0, 1.0], dtype=np.float32)  # TODO: Do this properly

                for entity in entities:
                    # Set model matrix
                    glUniformMatrix4fv(
                        shader.get_single_location(UNIFORM_TYPE["MODEL"]),
                        1, GL_FALSE, entity.model_matrix
                    )
                    # Set base color
                    glUniform4fv(
                        shader.get_single_location(UNIFORM_TYPE["BASE_COLOR"]),
                        1, color
                    )

                    mesh.draw()

        glFlush()

    def destroy(self) -> None:
        """Destroy the graphics engine

        Frees any memory allocated by the engine.

        Returns
        -------
        None
        """
        for mesh in self.meshes.values():
            mesh.destroy()

        for material in self.materials.values():
            material.destroy()

        for shader in self.shaders.values():
            shader.destroy()
