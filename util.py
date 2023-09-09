"""
Alexander Burow - 2 September 2023

License: GPL3
"""


def gen_colour_id(f_id: int) -> str:
    col_id = list()

    strfid = str(f_id)

    for root_index in range(0, len(strfid), 2):
        alpha_index = int(strfid[root_index:root_index + 2])
        while alpha_index > 25:
            col_id.append("Z-")
            alpha_index -= 25

        col_id.append(chr(alpha_index + 65))

    return "".join(col_id)


# Stolen from
# https://stackoverflow.com/questions/49462195/left-rotation-on-an-array
def rotate(lst: list, degree: int):
    return lst[-degree % len(lst):] + lst[:-degree % len(lst)]


def lrotate(lst: list, degree: int):
    return rotate(lst, -degree)


if __name__ == "__main__":
    id_set = set()
    test_count = 1000
    for i in range(test_count):
        idc = gen_colour_id(i)
        print(idc)
        id_set.add(idc)

    if len(id_set) < test_count:
        print(f":(, {len(id_set)}")
