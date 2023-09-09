"""
Alexander Burow - 2 September 2023

License: GPL3
"""
import util


class RubixCube:
    def __init__(self, side_length: int):
        self._faces_count = 6
        self._cube_struct = {
            0: [1, 3, 4, 5],
            1: [0, 2, 4, 5],
            5: [0, 1, 2, 3]
        }

        self._side_length = side_length
        self._faces = self._setup_faces()
        self._bounds = self._setup_face_rotations()

    def _setup_faces(self):
        faces = dict()
        for face in range(self._faces_count):
            face_id = util.gen_colour_id(face)
            faces[face] = {
                coord: face_id for coord in range(self._side_length ** 2)}
        return faces

    def _setup_face_rotations(self):

        opposites = dict()
        for face, neighbours in self._cube_struct.items():
            opposites[face] = (sum(range(0, self._faces_count)) -
                               (face + sum(neighbours)))
            opposites[(sum(range(0, self._faces_count)) -
                       (face + sum(neighbours)))] = face

        rot_dirs = dict()

        for face in self._cube_struct:
            rot_dirs[face] = {
                "N": (face + 1) % 5,
                "W": (int(f"{bin(face)[2:]:0>3}"[0]) ^ 1) * 4,
                "E": opposites[(int(f"{bin(face)[2:]:0>3}"[0]) ^ 1) * 4],
                "S": opposites[(face + 1) % 5],
            }

        for face in opposites:
            if face in rot_dirs:
                continue

            rot_dirs[face] = {
                "N": rot_dirs[opposites[face]]["S"],
                "W": rot_dirs[opposites[face]]["E"],
                "S": rot_dirs[opposites[face]]["N"],
                "E": rot_dirs[opposites[face]]["W"],
            }

        return rot_dirs

    def get_face(self, face: int = None):
        if face is None:
            return self._faces
        return self._faces.get(face, "Face does not exist")

    def get_bounds(self, face: int = None):
        if face is None:
            return self._bounds
        return self._bounds.get(face, "Face does not exist")

    def rotate90(self, face: int, direction: str, colrow: int) -> None:
        if colrow == 1:
            raise ValueError(f"Cannot rotate central piece. {direction=}, "
                             f"{colrow=}, {face=}")
        neighbour = -1
        if direction in ["N", "S"]:
            face_vals = dict()

            while neighbour != face:
                if neighbour == -1:
                    neighbour = face
                neighbour = self.get_bounds(neighbour)[direction]

                col_vals = [
                    self.get_face(neighbour)[val]
                    for val in self.get_face(neighbour)
                    if val % self._side_length == colrow
                ]

                face_vals[neighbour] = col_vals

            faces = util.lrotate(list(face_vals.keys()), 1)
            values = list(face_vals.values())

            new_face_vals = {
                face: values[index] for index, face in enumerate(faces)
            }

            neighbour = -1
            while neighbour != face:
                if neighbour == -1:
                    neighbour = face
                neighbour = self.get_bounds(neighbour)[direction]

                for val in self.get_face(neighbour):
                    if val % self._side_length == colrow:
                        self.get_face(neighbour)[val] = new_face_vals[
                            neighbour][val // self._side_length]

        neighbour = -1
        if direction in ["E", "W"]:
            face_vals = dict()

            while neighbour != face:
                if neighbour == -1:
                    neighbour = face
                neighbour = self.get_bounds(neighbour)[direction]

                row_vals = [
                    self.get_face(neighbour)[val]
                    for val in self.get_face(neighbour)
                    if ((self._side_length * colrow) <= val <
                        (self._side_length * (colrow + 1)))
                ]
                print(row_vals)
                face_vals[neighbour] = row_vals

            faces = util.lrotate(list(face_vals.keys()), 1)
            values = list(face_vals.values())

            new_face_vals = {
                face: values[index] for index, face in enumerate(faces)
            }

            neighbour = -1
            while neighbour != face:
                if neighbour == -1:
                    neighbour = face
                neighbour = self.get_bounds(neighbour)[direction]

                for val in self.get_face(neighbour):
                    if ((self._side_length * colrow) <= val <
                            (self._side_length * (colrow + 1))):
                        self.get_face(neighbour)[val] = new_face_vals[
                            neighbour][val // self._side_length]


if __name__ == "__main__":
    rc = RubixCube(3)
    print(rc.get_face())
    print(rc.get_bounds())
    # print(rc.rotate90(0, "N", 0))
    # print(rc.get_face())
    # print(rc.rotate90(0, "S", 2))
    # print(rc.get_face())
    print(rc.rotate90(0, "E", 0))
    print(rc.get_face())
    print(rc.rotate90(0, "W", 0))
    print(rc.get_face())
