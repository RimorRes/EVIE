import numpy as np
import glfw
from glfw.GLFW import *
from OpenGL.GL import *
from config import *
import mesher
from picamera2 import Picamera2

CAM_WIDTH = 1440
CAM_HEIGHT = 1280


def init_camera(index):
    picam = Picamera2(index)
    config = picam.create_video_configuration(main={"size": (CAM_WIDTH, CAM_HEIGHT)})
    print(config["main"])
    # picam.align_configuration(config)
    picam.configure(config)
    picam.set_controls({"FrameRate": 56})
    return picam


def init_pbo(pbo):
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, pbo)
    glBufferData(GL_PIXEL_UNPACK_BUFFER, CAM_WIDTH * CAM_HEIGHT * 4, None, GL_STREAM_DRAW)
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0)


def update_texture_with_pbo(pbo, texture, frame_data):
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, pbo)
    ptr = glMapBuffer(GL_PIXEL_UNPACK_BUFFER, GL_WRITE_ONLY)
    if ptr:
        ctypes.memmove(ptr, frame_data, len(frame_data))
        glUnmapBuffer(GL_PIXEL_UNPACK_BUFFER)
    glBindTexture(GL_TEXTURE_2D, texture)
    glTexSubImage2D(GL_TEXTURE_2D, 0, 0, 0, CAM_WIDTH, CAM_HEIGHT, GL_RGBA, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))
    glBindBuffer(GL_PIXEL_UNPACK_BUFFER, 0)


class App:

    def __init__(self):
        """
        Initialise the app
        """

        # Set the error callback
        glfw.set_error_callback(glfw_error_callback)

        # Initialize Picamera
        self.cam_L = init_camera(0)
        self.cam_R = init_camera(1)
        self.cam_L.start()
        self.cam_R.start()

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
        glfw.swap_interval(0)

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
        self.quad_ebo, self.quad_vbo, self.quad_vao = mesher.build_quad_mesh()

        glUseProgram(self.shader)

        # Create OpenGL textures
        self.texture_l = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_l)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, CAM_WIDTH, CAM_HEIGHT, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)

        self.texture_r = glGenTextures(1)
        glBindTexture(GL_TEXTURE_2D, self.texture_r)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
        glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, CAM_WIDTH, CAM_HEIGHT, 0, GL_RGBA, GL_UNSIGNED_BYTE, None)

        # Create PBOs
        self.pbo_L = glGenBuffers(1)
        self.pbo_R = glGenBuffers(1)

        # Initialize PBOs
        init_pbo(self.pbo_L)
        init_pbo(self.pbo_R)

        self.frame_l = np.zeros((CAM_WIDTH, CAM_HEIGHT, 4), dtype=np.uint8).tobytes()
        self.frame_r = np.zeros((CAM_WIDTH, CAM_HEIGHT, 4), dtype=np.uint8).tobytes()

        # Initialise timers
        self.t = glfw.get_time()
        self.frame_counter = 0
        self.frame_sample_rate = 100

    def run(self):
        """ Run the app """
        while not glfw.window_should_close(self.window):
            glActiveTexture(GL_TEXTURE0)
            glBindTexture(GL_TEXTURE_2D, self.texture_l)
            glActiveTexture(GL_TEXTURE1)
            glBindTexture(GL_TEXTURE_2D, self.texture_r)

            # check events
            if glfw.get_key(self.window, GLFW_KEY_ESCAPE) == GLFW_PRESS:
                break
            glfw.poll_events()

            # refresh screen
            glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
            glUseProgram(self.shader)

            self.capture_frame_l()
            update_texture_with_pbo(self.pbo_L, self.texture_l, self.frame_l)
            # Render to the left half of the screen
            glViewport(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT//2)
            glBindVertexArray(self.quad_vao)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))

            self.capture_frame_r()
            update_texture_with_pbo(self.pbo_R, self.texture_r, self.frame_r)
            # Render to the right half of the screen
            glViewport(0, SCREEN_HEIGHT//2, SCREEN_WIDTH, SCREEN_HEIGHT//2)
            glBindVertexArray(self.quad_vao)
            glDrawElements(GL_TRIANGLES, 6, GL_UNSIGNED_BYTE, ctypes.c_void_p(0))

            glfw.swap_buffers(self.window)

            # Print FPS
            self.get_fps()

    def capture_frame_l(self):
        self.cam_L.capture_array(wait=False, signal_function=self.update_texture_l)

    def update_texture_l(self, job):
        frame = self.cam_L.wait(job)
        self.frame_l = frame.tobytes()

    def capture_frame_r(self):
        self.cam_R.capture_array(wait=False, signal_function=self.update_texture_r)

    def update_texture_r(self, job):
        frame = self.cam_R.wait(job)
        self.frame_r = frame.tobytes()

    def get_fps(self):
        self.frame_counter += 1
        if self.frame_counter % self.frame_sample_rate == 0:
            fps = round(self.frame_sample_rate / (glfw.get_time() - self.t), 2)
            frame_time = round((glfw.get_time() - self.t) * 1000 / self.frame_sample_rate, 2)
            print(f"FPS: {fps}".ljust(15) + f"Frame time: {frame_time} ms".ljust(20))
            self.t = glfw.get_time()
        return

    def quit(self):
        """ Cleanup the app, run exit code """
        glDeleteBuffers(2, (self.quad_ebo, self.quad_vbo))
        glDeleteVertexArrays(1, self.quad_vao)
        glDeleteProgram(self.shader)
        self.cam_L.close()
        self.cam_R.close()
        glfw.destroy_window(self.window)
        glfw.terminate()


my_app = App()
my_app.run()
my_app.quit()
