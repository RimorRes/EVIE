import numpy as np
from bisect import insort
from PIL import Image
from scipy.spatial.transform import Rotation


def get_perspective_transform_coeffs(dst, src):
    print(src, dst)
    #  Math for perspective transform:
    #  https://web.archive.org/web/20150222120106/xenia.media.mit.edu/~cwren/interpolator/
    in_matrix = []
    for (x, y), (X, Y) in zip(src, dst):
        in_matrix.extend([
            [x, y, 1, 0, 0, 0, -X * x, -X * y],
            [0, 0, 0, x, y, 1, -Y * x, -Y * y],
        ])

    a = np.matrix(in_matrix, dtype=np.float64)
    b = np.array(dst).reshape(8)
    cf = np.dot(np.linalg.inv(a.T * a) * a.T, b)

    return np.array(cf).reshape(8)


class Scene:

    def __init__(self):
        self.objects = []

    def pack(self, obj):
        # Insert, objects sorted by ascending z-depth
        insort(self.objects, obj, key=lambda x: x.pos[2])

    def render(self, active_camera):
        # TODO: figure out a solution for z-hierarchy of clipping objects
        out = Image.new('RGBA', active_camera.resolution)

        for obj in self.objects[::-1]:  # display according to descending z-order
            vertices = obj.get_vertices()
            w, h = obj.image.size
            src_points = [(0, 0), (w, 0), (0, h), (w, h)]
            dst_points = []
            for v in vertices:
                dst_points.append(active_camera.project(v))

            coeffs = get_perspective_transform_coeffs(src_points, dst_points)

            layer = obj.image.transform(active_camera.resolution, Image.PERSPECTIVE, coeffs, Image.BICUBIC)
            layer = layer.convert('RGBA')
            out = Image.alpha_composite(out, layer)

        return out


class VirtualCamera:
    #  Camera projection matrix explanations:
    #  https://www.cs.cmu.edu/~16385/s17/Slides/11.1_Camera_matrix.pdf
    def __init__(self, resolution, intrinsic_matrix, pos=None, rot=None):
        self.resolution = resolution
        self.k_matrix = intrinsic_matrix
        if pos:
            self._pos = pos
        else:
            self._pos = np.zeros(3)
        if rot:
            self._rot = rot
        else:
            self._rot = np.zeros(3)

        self.p_matrix = self.get_projection_matrix()

    def get_projection_matrix(self):
        r = Rotation.from_euler('zyx', self._rot).as_matrix()
        p = self.k_matrix * r * np.c_[np.identity(3), - self._pos]

        return p

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, position):
        self._pos = np.array(position)
        self.p_matrix = self.get_projection_matrix()

    @property
    def rot(self):
        return self._rot

    @rot.setter
    def rot(self, angles):
        self._rot = np.array(angles)
        self.p_matrix = self.get_projection_matrix()

    def project(self, vertex):
        h_coords = np.r_[vertex, 1].reshape((4, 1))  # Get world homogenous coordinates
        x, y, z = np.asarray(self.p_matrix * h_coords).flatten()  # Get image homogenous coords
        return np.array((x, y))/z


class ImagePlane:

    def __init__(self, image, size, pos=None, rot=None):
        self.image = image
        self.phys_size = size  # Physical size
        if pos:
            self._pos = pos  # Center of image
        else:
            self._pos = np.zeros(3)
        if rot:
            self._rot = rot
        else:
            self._rot = np.zeros(3)

    def get_vertices(self):
        w, h = self.phys_size

        # 2D coords relative to plane center
        x = np.linspace(-1, 1, 2) * w/2
        y = np.linspace(-1, 1, 2) * h/2
        # 3D coords relative to plane center
        vertices = np.dstack((np.dstack(np.meshgrid(x, y)), np.zeros((2, 2))))

        # Rotate
        r = Rotation.from_euler('zyx', self._rot)
        vertices = r.apply(vertices.reshape(4, 3))
        # Translate
        vertices += self._pos

        return vertices

    @property
    def pos(self):
        return self._pos

    @pos.setter
    def pos(self, position):
        self._pos = np.array(position)

    @property
    def rot(self):
        return self._rot

    @rot.setter
    def rot(self, angles):
        self._rot = np.array(angles)


f = 50e-3  # 50mm focal length
res = (960, 960)
px = res[0]/2
py = res[1]/2
k = 960
cam_matrix = np.matrix([
    [f*k, 0, px],
    [0, f*k, py],
    [0, 0, 1]
])

img = Image.open('../res/img.png')
phys_size = (1, 1)

SCENE = Scene()
CAM = VirtualCamera(res, cam_matrix)
LENNA = ImagePlane(img, phys_size)
LENNA.pos = (0, 0, 0.1)
LENNA.rot = (0, np.pi/16, 0)  # TODO: fix rotation

SCENE.pack(LENNA)
res = SCENE.render(CAM)
res.show('Render')
