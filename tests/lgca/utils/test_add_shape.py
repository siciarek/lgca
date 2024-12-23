from copy import deepcopy
import pytest
from lgca.utils import add_shape
from tests.helpers.utils import get_test_data

frame_input_dat, frame_expected_dat = get_test_data("shapes/frame")

frame_data_provider = (
    (frame_input_dat[0], frame_expected_dat[0], None),
    (frame_input_dat[0], frame_expected_dat[0], 1),
    (frame_input_dat[0], frame_expected_dat[1], 2),
)

square_input_dat, square_expected_dat = get_test_data("shapes/square")

square_data_provider = (
    (square_input_dat[0], square_expected_dat[0], 3),
    (square_input_dat[0], square_expected_dat[1], 7),
)

single_point_input_dat, single_point_expected_dat = get_test_data("shapes/single_point")

single_point_data_provider = ((single_point_input_dat[0], single_point_expected_dat[0], "center"),)

get_info_data_provider = (
    (300, 200, {"row": 100, "col": 150}),
    (400, 400, {"row": 200, "col": 200}),
)


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


@pytest.mark.parametrize("input_grid,expected,size", square_data_provider)
def test_square(input_grid, expected, size):
    grid = deepcopy(input_grid)
    add_shape.solid_square(grid=grid, value=1, size=size)

    assert grid == expected


@pytest.mark.parametrize("input_grid,expected,position", single_point_data_provider)
def test_single_point(input_grid, expected, position):
    grid = deepcopy(input_grid)
    add_shape.single_point(grid=grid, value=1, position=position)

    assert grid == expected
