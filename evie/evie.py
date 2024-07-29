import numpy as np
import glfw
from glfw.GLFW import *
from OpenGL.GL import *
from config import *
import mesher


def create_projection_matrix(fov, aspect, near, far):
    """
    Create a projection matrix.
    :param self:
    :param fov:
    :param aspect:
    :param near:
    :param far:
    :return:
    """
    f = 1.0 / np.tan(np.radians(fov) / 2)
    return np.array([
        [f / aspect, 0, 0, 0],
        [0, f, 0, 0],
        [0, 0, (far + near) / (near - far), (2 * far * near) / (near - far)],
        [0, 0, -1, 0]
    ], dtype=np.float32)


class App:

    def __init__(self):
        """
        Initialise the app
        """

        # Set the error callback
        glfw.set_error_callback(glfw_error_callback)

        # Initialise GLFW
        if not glfw.init():
            raise Exception("Failed to initialise GLFW")
        glfw.window_hint(GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(
            GLFW_OPENGL_FORWARD_COMPAT,
            GLFW_TRUE
        )

        self.window = glfw.create_window(
            SCREEN_WIDTH, SCREEN_HEIGHT, "Title", glfw.get_primary_monitor(), None)
        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create window")

        glfw.make_context_current(self.window)
        glfw.swap_interval(1)

        glfw.set_input_mode(self.window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN)

        # Initialise OpenGL
        glEnable(GL_DEPTH_TEST)
        glDepthFunc(GL_LESS)
        glEnable(GL_DEPTH_TEST)
        # TODO: Enable backface culling
        # glEnable(GL_CULL_FACE)
        # glCullFace(GL_BACK)
        glEnable(GL_LINE_SMOOTH)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        self.shader = create_shader_program("../assets/shaders/vertex.vert", "../assets/shaders/fragment.frag")
        self.triangle_vbo, self.triangle_vao = mesher.build_triangle_mesh()
        self.quad_ebo, self.quad_vbo, self.quad_vao = mesher.build_quad_mesh()
        self.test_tex1 = mesher.Material("../assets/textures/RCA_Indian_Head_Test_Pattern.png")
        self.test_tex2 = mesher.Material("../assets/textures/Philips_PM5544_Test_Pattern.png")

        glUseProgram(self.shader)
        glUniform1i(glGetUniformLocation(self.shader, "imageTexture"), 0)

        # Initialise timers
        self.t = glfw.get_time()
        self.frame_counter = 0
        self.frame_sample_rate = 100

    def run(self):
        """ Run the app """
        while not glfw.window_should_close(self.window):

            # check events
            if glfw.get_key(self.window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
                break
            glfw.poll_events()

            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)

            if self.frame_counter % 10 == 0:
                self.test_tex1.use()
            else:
                self.test_tex2.use()

            # Render to the left half of the screen
            glViewport(0, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT)
            glBindVertexArray(self.quad_vao)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
            glBindVertexArray(self.triangle_vao)
            glDrawArrays(GL_TRIANGLES, 0, 3)

            # Render to the right half of the screen
            glViewport(SCREEN_WIDTH // 2, 0, SCREEN_WIDTH // 2, SCREEN_HEIGHT)
            glBindVertexArray(self.quad_vao)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
            glBindVertexArray(self.triangle_vao)
            glDrawArrays(GL_TRIANGLES, 0, 3)

            glfw.swap_buffers(self.window)

            # Print FPS
            self.get_fps()

    def get_fps(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_sample_rate == 0:
            fps = round(self.frame_sample_rate / (glfw.get_time() - self.t), 2)
            frame_time = round((glfw.get_time() - self.t) * 1000 / self.frame_sample_rate, 2)
            print(f"FPS: {fps}".ljust(15) + f"Frame time: {frame_time} ms".ljust(20), end='\r')
            self.t = glfw.get_time()
        return

    def quit(self):
        """ Cleanup the app, run exit code """
        glDeleteBuffers(3, (self.triangle_vbo, self.quad_ebo, self.quad_vbo))
        glDeleteVertexArrays(2, (self.triangle_vao, self.quad_vao))
        glDeleteProgram(self.shader)
        glfw.destroy_window(self.window)
        glfw.terminate()


my_app = App()
my_app.run()
my_app.quit()
