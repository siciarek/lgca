from copy import deepcopy
import pytest
from lgca.utils import add_shape
from tests.helpers import get_test_data

frame_input_dat, frame_expected_dat = get_test_data("shapes/frame")
frame_data_provider = (
    (frame_input_dat[0], frame_expected_dat[0], None),
    (frame_input_dat[0], frame_expected_dat[0], 1),
    (frame_input_dat[0], frame_expected_dat[1], 2),
)

solid_square_input_dat, solid_square_expected_dat = get_test_data("shapes/solid_square")
solid_square_data_provider = (
    (solid_square_input_dat[0], solid_square_expected_dat[0], 3),
    (solid_square_input_dat[0], solid_square_expected_dat[1], 7),
)

solid_rectangle_input_dat, solid_rectangle_expected_dat = get_test_data("shapes/solid_rectangle")
solid_rectangle_data_provider = ((solid_rectangle_input_dat[0], solid_rectangle_expected_dat[0], 5, 3, 1),)

single_point_input_dat, single_point_expected_dat = get_test_data("shapes/single_point")
single_point_data_provider = ((single_point_input_dat[0], single_point_expected_dat[0], "center"),)

get_info_data_provider = (
    (300, 200, {"row": 100, "col": 150}),
    (400, 400, {"row": 200, "col": 200}),
)

solid_circle_input_dat, solid_circle_expected_dat = get_test_data("shapes/solid_circle")
solid_circle_data_provider = (
    (solid_circle_input_dat[0], solid_circle_expected_dat[0], 3, 1),
    (solid_circle_input_dat[0], solid_circle_expected_dat[1], 5, 1),
    (solid_circle_input_dat[0], solid_circle_expected_dat[2], 7, 1),
    (solid_circle_input_dat[1], solid_circle_expected_dat[3], 41, 1),
)

line_horizontal_input_dat, line_horizontal_expected_dat = get_test_data("shapes/line_horizontal")
line_horizontal_data_provider = ((line_horizontal_input_dat[0], line_horizontal_expected_dat[0], 9, 0, 0, 8),)

line_vertical_input_dat, line_vertical_expected_dat = get_test_data("shapes/line_vertical")
line_vertical_data_provider = ((line_vertical_input_dat[0], line_vertical_expected_dat[0], 1, 0, 0, 8),)


@pytest.mark.parametrize("input_grid,expected,value,col,row_start,row_end", line_vertical_data_provider)
def test_line_vertical(input_grid, expected, value, col, row_start, row_end):
    grid = deepcopy(input_grid)
    add_shape.line_vertical(grid=grid, value=value, col=len(grid) // 2, row_start=row_start, row_end=row_end)

    assert grid == expected


@pytest.mark.parametrize("input_grid,expected,value,row,col_start,col_end", line_horizontal_data_provider)
def test_line_horizontal(input_grid, expected, value, row, col_start, col_end):
    grid = deepcopy(input_grid)
    add_shape.line_horizontal(grid=grid, value=value, row=row, col_start=col_start, col_end=col_end)

    assert grid == expected


@pytest.mark.parametrize("width,height,center", get_info_data_provider)
def test_get_info(width, height, center):
    grid = [[0 for _ in range(width)] for _ in range(height)]
    info = add_shape.get_info(grid=grid)

    assert isinstance(info, dict)
    assert info["center"] == center


@pytest.mark.parametrize("input_grid,expected,size", frame_data_provider)
def test_frame(input_grid, expected, size):
    grid = deepcopy(input_grid)
    if size is None:
        add_shape.frame(grid=grid, value=1)
    else:
        add_shape.frame(grid=grid, value=1, size=size)

    assert grid == expected


@pytest.mark.parametrize("input_grid,expected,size", solid_square_data_provider)
def test_solid_square(input_grid, expected, size):
    grid = deepcopy(input_grid)
    add_shape.solid_square(grid=grid, value=1, size=size)

    assert grid == expected


@pytest.mark.parametrize("input_grid,expected,width,height,value", solid_rectangle_data_provider)
def test_solid_rectangle(input_grid, expected, width, height, value):
    grid = deepcopy(input_grid)
    add_shape.solid_rectangle(grid=grid, width=width, height=height, value=value)

    assert grid == expected


@pytest.mark.parametrize("input_grid,expected,position", single_point_data_provider)
def test_single_point(input_grid, expected, position):
    grid = deepcopy(input_grid)
    add_shape.single_point(grid=grid, value=1, position=position)

    assert grid == expected


@pytest.mark.parametrize("input_grid,expected,size, value", solid_circle_data_provider)
def test_solid_circle(input_grid, expected, size, value):
    grid = deepcopy(input_grid)
    add_shape.solid_circle(grid=grid, size=size, value=value)

    str_expected, str_grid = "", ""
    for rix, row in enumerate(grid):
        for cix, val in enumerate(row):
            str_expected += str(expected[rix][cix])
            str_grid += str(val)
        str_expected += "\n"
        str_grid += "\n"

    assert str_grid == str_expected
