from PIL import Image, ImageDraw
from math import sin, cos
from semantic import Operation


class Actuator(object):
    def __init__(self):
        self.origin = (0, 0)
        self.scale = [1, 1]
        self.rot = 0
        self.points = []
        self.image = None
        self.operation_queue = []

    def append(self, operation):
        if type(operation) == tuple and type(operation[0]) == Operation:
            self.operation_queue.append(operation)
        elif type(operation) in (tuple, list):
            self.operation_queue.extend(operation)

    def execute(self):
        for operation in self.operation_queue:
            if operation[0] == Operation.SET_ORIGIN:
                self.set_origin(operation[1], operation[2])
            elif operation[0] == Operation.SET_SCALE:
                self.set_scale(operation[1], operation[2])
            elif operation[0] == Operation.SET_ROT:
                self.set_rot(operation[1])
            elif operation[0] == Operation.DRAW:
                self.draw_point(operation[1], operation[2])

        self.operation_queue = []

    def create_image(self):
        min_x = 0
        min_y = 0
        max_x = 0
        max_y = 0
        for point in self.points:
            if point[0] > max_x:
                max_x = point[0]
            if point[1] > max_y:
                max_y = point[1]
            if point[0] < min_x:
                min_x = point[0]
            if point[1] < min_y:
                min_y = point[1]

        width = max_x - min_x + 21
        height = max_y - min_y + 21
        offect_x = 11 - min_x
        offect_y = 11 - min_y

        self.image = Image.new('RGB', (width, height), (255, 255, 255))
        draw = ImageDraw.Draw(self.image)
        for point in self.points:
            draw.point((point[0] + offect_x, point[1] + offect_y), (0, 0, 255))

        self.image.save('what.png', 'png')
        self.image.show()

    def set_origin(self, x, y):
        self.origin = (x, y)

    def set_scale(self, x_scale, y_scale):
        self.scale = (x_scale, y_scale)

    def set_rot(self, rot):
        self.rot = rot

    def draw_point(self, x, y):
        self.points.append((
            int(x * self.scale[0] * cos(self.rot) + y * self.scale[1] * sin(self.rot) + self.origin[0]),
            int(y * self.scale[1] * cos(self.rot) - x * self.scale[0] * sin(self.rot) + self.origin[1])
        ))