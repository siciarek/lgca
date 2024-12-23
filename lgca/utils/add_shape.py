from random import randint


def frame(grid: list[list[int]], value: int, size: int = 1):
    height = len(grid)
    width = len(grid[0])

    for row in range(height):
        for col in range(width):
            in_frame = any(
                [
                    row in range(size),
                    col in range(size),
                    row in (height - i for i in range(1, size + 1)),
                    col in (width - i for i in range(1, size + 1)),
                ]
            )
            if in_frame:
                grid[row][col] = value


def get_info(grid: list[list[int]]) -> dict:
    height, width = len(grid), len(grid[0])
    center_row, center_col = height // 2, width // 2

    return {
        "height": height,
        "width": width,
        "center": {
            "row": center_row,
            "col": center_col,
        },
    }


def arbitrary_single_point(grid: list, row: int, col: int, value: int = 1):
    grid[row][col] = value


def solid_rectangle(grid: list, width: int, height: int, value: int, left_offset: int = 0, top_offset: int = 0):
    params = get_info(grid=grid)

    for row in range(
            top_offset + params["center"]["row"] - height // 2, top_offset + params["center"]["row"] + height // 2 + 1
    ):
        for col in range(
                left_offset + params["center"]["col"] - width // 2,
                left_offset + params["center"]["col"] + width // 2 + 1
        ):
            arbitrary_single_point(grid=grid, row=row, col=col, value=value)


def solid_square(grid: list, size: int, value: int):
    params = get_info(grid=grid)

    for row in range(params["center"]["row"] - size // 2, params["center"]["row"] + size // 2 + 1):
        for col in range(params["center"]["col"] - size // 2, params["center"]["col"] + size // 2 + 1):
            arbitrary_single_point(grid=grid, row=row, col=col, value=value)


def circle(grid: list, size: int, value: int, rand: bool = False, row_offset: int = 0, col_offset: int = 0):
    params = get_info(grid=grid)

    radius = size // 2

    center_row = params["center"]["row"] + row_offset
    center_col = params["center"]["col"] + col_offset

    for row in range(center_row - size // 2, center_row + size // 2 + 1):
        for col in range(center_col - size // 2, center_col + size // 2 + 1):
            if (col - center_col) ** 2 + (row - center_row) ** 2 < radius ** 2:
                arbitrary_single_point(grid=grid, row=row, col=col, value=randint(0, value) if rand else value)


def diamond(grid: list, size: int, value: int, rand: bool = False):
    params = get_info(grid=grid)

    offset = size // 2 + 1

    for row in range(params["center"]["row"] - size // 2, params["center"]["row"] + size // 2 + 1):
        offset += 1 if row - params["center"]["row"] > 0 else -1
        for col in range(
                params["center"]["col"] - size // 2 + offset, params["center"]["col"] + size // 2 + 1 - offset
        ):
            arbitrary_single_point(grid=grid, row=row, col=col, value=randint(0, value) if rand else value)


def single_point(grid: list, position: str = "center", value: int = 1):
    params = get_info(grid=grid)
    positions = {
        "top": (0, params["center"]["col"]),
        "center": tuple(params["center"].values()),
        "bottom-left": (params["height"] - 2, 0),
    }
    arbitrary_single_point(grid=grid, row=positions[position][0], col=positions[position][1], value=value)
