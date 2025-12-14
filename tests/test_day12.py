"""Tests for Day 12."""

from solutions.day12 import (
    part1,
    part2,
    ascii_to_polygon,
    get_rotations,
    greedy_place,
    greedy_place_count,
    expand_shapes,
    can_fit,
    make_container,
    ShapeType,
    Puzzle,
)

# Paste the example input from the puzzle description here
EXAMPLE = """
0:
###
##.
##.

1:
###
##.
.##

2:
.##
###
##.

3:
##.
###
##.

4:
###
#..
###

5:
###
.#.
###

4x4: 0 0 0 0 2 0
12x5: 1 0 1 0 2 2
12x5: 1 0 1 0 3 2
"""


def test_part1():
    """Test part 1 with example input."""
    assert part1(EXAMPLE) == 2


def test_part2():
    """Test part 2 with example input."""
    assert part2(EXAMPLE) == 0


class TestAsciiToPolygon:
    """Tests for ascii_to_polygon function."""

    def test_single_block(self):
        """A single '#' should create a 1x1 square."""
        art = "#"
        poly = ascii_to_polygon(art)
        assert poly.area == 1.0
        assert poly.bounds == (0.0, 0.0, 1.0, 1.0)

    def test_horizontal_line(self):
        """Three blocks in a row should create a 3x1 rectangle."""
        art = "###"
        poly = ascii_to_polygon(art)
        assert poly.area == 3.0
        assert poly.bounds == (0.0, 0.0, 3.0, 1.0)

    def test_vertical_line(self):
        """Three blocks stacked should create a 1x3 rectangle."""
        art = """#
#
#"""
        poly = ascii_to_polygon(art)
        assert poly.area == 3.0
        assert poly.bounds == (0.0, 0.0, 1.0, 3.0)

    def test_2x2_square(self):
        """A 2x2 block of '#' should create a 2x2 square."""
        art = """##
##"""
        poly = ascii_to_polygon(art)
        assert poly.area == 4.0
        assert poly.bounds == (0.0, 0.0, 2.0, 2.0)

    def test_l_shape(self):
        """An L-shape should have correct area."""
        art = """#.
#.
##"""
        poly = ascii_to_polygon(art)
        assert poly.area == 4.0
        # Should span 2 wide and 3 tall
        assert poly.bounds == (0.0, 0.0, 2.0, 3.0)

    def test_shape_with_hole(self):
        """A shape with empty center should have correct area."""
        art = """###
#.#
###"""
        poly = ascii_to_polygon(art)
        assert poly.area == 8.0
        assert poly.bounds == (0.0, 0.0, 3.0, 3.0)

    def test_empty_input(self):
        """Empty or all-dots input should create empty polygon."""
        art = """...
...
..."""
        poly = ascii_to_polygon(art)
        assert poly.is_empty

    def test_shape_0_from_example(self):
        """Test shape 0 from the puzzle example."""
        art = """###
##.
##."""
        poly = ascii_to_polygon(art)
        assert poly.area == 7.0
        assert poly.bounds == (0.0, 0.0, 3.0, 3.0)


class TestGetRotations:
    """Tests for get_rotations function."""

    def test_returns_four_rotations(self):
        """Should return exactly 4 rotations."""
        poly = ascii_to_polygon("#")
        rotations = get_rotations(poly)
        assert len(rotations) == 4

    def test_square_rotations_same_bounds(self):
        """A square should have same bounds after any rotation."""
        art = """##
##"""
        poly = ascii_to_polygon(art)
        rotations = get_rotations(poly)
        for rot in rotations:
            assert rot.bounds == (0.0, 0.0, 2.0, 2.0)

    def test_rectangle_rotations_swap_dimensions(self):
        """A 3x1 rectangle should become 1x3 after 90 degree rotation."""
        art = "###"
        poly = ascii_to_polygon(art)
        rotations = get_rotations(poly)
        # 0 degrees: 3x1
        assert rotations[0].bounds == (0.0, 0.0, 3.0, 1.0)
        # 90 degrees: 1x3
        assert rotations[1].bounds[2] - rotations[1].bounds[0] == 1.0  # width
        assert rotations[1].bounds[3] - rotations[1].bounds[1] == 3.0  # height

    def test_all_rotations_normalized_to_origin(self):
        """All rotations should have minx=0, miny=0."""
        art = """##.
.##"""
        poly = ascii_to_polygon(art)
        rotations = get_rotations(poly)
        for rot in rotations:
            minx, miny, _, _ = rot.bounds
            assert minx == 0.0
            assert miny == 0.0

    def test_all_rotations_preserve_area(self):
        """All rotations should have the same area as original."""
        art = """###
##.
##."""
        poly = ascii_to_polygon(art)
        original_area = poly.area
        rotations = get_rotations(poly)
        for rot in rotations:
            assert rot.area == original_area


class TestGreedyPlace:
    """Tests for greedy_place and greedy_place_count functions."""

    def test_single_shape_fits(self):
        """A single small shape should fit in a larger container."""
        shape = ascii_to_polygon("##")
        container = make_container(4, 4)
        assert greedy_place([shape], container) is True
        assert greedy_place_count([shape], container) == 1

    def test_shape_too_large(self):
        """A shape larger than container should not fit."""
        shape = ascii_to_polygon("####")
        container = make_container(3, 3)
        assert greedy_place([shape], container) is False
        assert greedy_place_count([shape], container) == 0

    def test_two_shapes_fit_side_by_side(self):
        """Two 2x1 shapes should fit in a 4x1 container."""
        shape = ascii_to_polygon("##")
        container = make_container(4, 1)
        assert greedy_place([shape, shape], container) is True
        assert greedy_place_count([shape, shape], container) == 2

    def test_shapes_dont_overlap(self):
        """Shapes placed should not overlap."""
        shape = ascii_to_polygon("##")
        container = make_container(3, 1)
        # Two 2x1 shapes can't fit in 3x1 without overlap
        assert greedy_place([shape, shape], container) is False
        assert greedy_place_count([shape, shape], container) == 1

    def test_empty_shapes_list(self):
        """Empty shapes list should return True."""
        container = make_container(4, 4)
        assert greedy_place([], container) is True
        assert greedy_place_count([], container) == 0

    def test_exact_fit(self):
        """Shapes that exactly fill the container should fit."""
        shape = ascii_to_polygon("##")
        container = make_container(2, 2)
        assert greedy_place([shape, shape], container) is True


class TestExpandShapes:
    """Tests for expand_shapes function."""

    def test_expands_by_count(self):
        """Should create correct number of shape copies."""
        shape1 = ShapeType(name="0", geom=ascii_to_polygon("#"))
        shape2 = ShapeType(name="1", geom=ascii_to_polygon("##"))
        expanded = expand_shapes([shape1, shape2], [2, 3])
        assert len(expanded) == 5
        # First 2 should be type 0
        assert expanded[0][0] == 0
        assert expanded[1][0] == 0
        # Next 3 should be type 1
        assert expanded[2][0] == 1
        assert expanded[3][0] == 1
        assert expanded[4][0] == 1

    def test_zero_count(self):
        """Zero count should create no shapes of that type."""
        shape1 = ShapeType(name="0", geom=ascii_to_polygon("#"))
        shape2 = ShapeType(name="1", geom=ascii_to_polygon("##"))
        expanded = expand_shapes([shape1, shape2], [0, 2])
        assert len(expanded) == 2
        assert all(idx == 1 for idx, _ in expanded)


class TestCanFit:
    """Tests for can_fit function (full bin packing)."""

    def test_single_shape_fits(self):
        """A simple case with one shape that fits."""
        shape = ShapeType(name="0", geom=ascii_to_polygon("##"))
        puzzle = Puzzle(container=make_container(4, 4), shape_counts=[1])
        assert can_fit([shape], puzzle) is True

    def test_impossible_fit(self):
        """Shape too large for container should return False."""
        shape = ShapeType(name="0", geom=ascii_to_polygon("######"))
        puzzle = Puzzle(container=make_container(4, 4), shape_counts=[1])
        assert can_fit([shape], puzzle) is False

    def test_empty_puzzle(self):
        """Puzzle with no shapes should return True."""
        shape = ShapeType(name="0", geom=ascii_to_polygon("##"))
        puzzle = Puzzle(container=make_container(4, 4), shape_counts=[0])
        assert can_fit([shape], puzzle) is True

    def test_multiple_shapes_fit_with_rotation(self):
        """Test that rotation helps fit shapes."""
        # A 3x1 horizontal bar
        shape = ShapeType(name="0", geom=ascii_to_polygon("###"))
        # In a 3x2 container, two bars can fit: one horizontal, one needs rotation
        # Actually both can be horizontal stacked
        puzzle = Puzzle(container=make_container(3, 2), shape_counts=[2])
        assert can_fit([shape], puzzle) is True

