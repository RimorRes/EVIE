import glfw
from glfw.GLFW import *
from evie.core.config import *
from evie.rendering.engine import *
from evie.rendering.scene import Scene


class App:

    __slots__ = ["window", "renderer", "scene", "_keys", "poll_interval", "last_time", "frame_count", "frametime"]

    def __init__(self):
        """
        Initialise the app
        """
        self._init_glfw()
        self._keys = {}
        self._init_input_handlers()

        # Set up timers
        self.poll_interval = 10  # Number of frames before FPS and frame time are updated
        self.last_time = glfw.get_time()
        self.frame_count = 0
        self.frametime = 0

        # TODO: Make this cleaner
        self.scene = Scene()
        self.renderer = GraphicsEngine()

    def _init_glfw(self):
        """Initialise the windowing system with GLFW
        Returns
        -------
        None
        """
        # Set the error callback
        glfw.set_error_callback(glfw_error_callback)

        # Initialise GLFW
        if not glfw.init():
            raise Exception("Failed to initialise GLFW")
        glfw.window_hint(GLFW_CONTEXT_VERSION_MAJOR, 3)
        glfw.window_hint(GLFW_CONTEXT_VERSION_MINOR, 1)
        glfw.window_hint(GLFW_OPENGL_FORWARD_COMPAT, GLFW_TRUE)

        self.window = glfw.create_window(SCREEN_WIDTH, SCREEN_HEIGHT, "EVIE", glfw.get_primary_monitor(), None)
        if not self.window:
            glfw.terminate()
            raise Exception("Failed to create window")

        glfw.make_context_current(self.window)
        # Enable VSYNC
        if VSYNC:
            glfw.swap_interval(1)
        else:
            glfw.swap_interval(0)

    def _init_input_handlers(self):
        """Initialise input handlers

        Sets up mouse and keyboard input handlers.

        Returns
        -------
        None
        """
        # Mouse/cursor input
        glfw.set_input_mode(self.window, GLFW_CURSOR, GLFW_CURSOR_HIDDEN)
        # Keyboard input
        glfw.set_key_callback(self.window, self._key_callback)

    def _key_callback(self, window, key, scancode, action, mods):
        """
        Handle a key event
        Parameters
        ----------
        window :
            The window the event occurred in.
        key :
            The key that was pressed or released.
        scancode :
            The system-specific scancode of the key.
        action :
            The action that was taken (press, release, etc.).
        mods :
            Any modifier keys that were pressed.

        Returns
        -------
        None
        """
        key_state = (action == GLFW_PRESS)
        self._keys[key] = key_state

    def _calculate_fps(self):
        """Calculate the frames per second

        Returns
        -------
        None
        """
        self.frame_count += 1
        if (self.frame_count % self.poll_interval) == 0:
            current_time = glfw.get_time()
            elapsed_time = current_time - self.last_time

            fps = self.frame_count / elapsed_time
            self.frametime = (elapsed_time / self.frame_count)

            # STDOUT the FPS and frame time
            print(f"FPS: {fps}, Frame Time: {self.frametime * 1000} ms")

            self.last_time = current_time
            self.frame_count = 0

    def run(self):
        """Run the main application loop

        Returns
        -------
        None
        """
        running = True
        while running:
            glfw.poll_events()

            if glfw.window_should_close(self.window) or self._keys.get(GLFW_KEY_ESCAPE, False):
                running = False

            # TODO: Add loop logic here
            self.scene.update(self.frametime)
            # Render both eyes
            self.renderer.render(self.scene.cameras, self.scene.entities)

            glfw.swap_buffers(self.window)

            self._calculate_fps()

    def quit(self):
        """Clean up the application

        Returns
        -------
        None
        """
        self.renderer.destroy()
        glfw.destroy_window(self.window)
        glfw.terminate()


my_app = App()
my_app.run()
my_app.quit()
