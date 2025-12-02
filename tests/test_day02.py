"""Tests for Day 2."""

from solutions.day02 import part1, part2, invalid_sequences, get_subsequences, invalid_subsequences


def test_invalid_sequences():
    assert invalid_sequences(11, 22) == [11, 22]
    assert invalid_sequences(95, 115) == [99]
    assert invalid_sequences(998, 1012) == [1010]
    assert invalid_sequences(1188511880, 1188511890) == [1188511885]
    assert invalid_sequences(222220, 222224) == [222222]
    assert invalid_sequences(1698522, 1698528) == []
    assert invalid_sequences(446443, 446449) == [446446]
    assert invalid_sequences(38593856, 38593862) == [38593859]


def test_get_subsequences():
    assert get_subsequences(12341234) == [[1234, 1234], [12, 34, 12, 34], [1, 2, 3, 4, 1, 2, 3, 4]]


def test_invalid_subsequences():
    print (invalid_subsequences(11, 22))
    assert invalid_subsequences(11, 22) == [11, 22]
    assert invalid_subsequences(95, 115) == [99, 111]
    assert invalid_subsequences(998, 1012) == [999, 1010]
    assert invalid_subsequences(1188511880, 1188511890) == [1188511885]
    assert invalid_subsequences(222220, 222224) == [222222]
    assert invalid_subsequences(1698522, 1698528) == []
    assert invalid_subsequences(446443, 446449) == [446446]
    assert invalid_subsequences(38593856, 38593862) == [38593859]
    assert invalid_subsequences(824824821, 824824827) == [824824824]
    assert invalid_subsequences(2121212118, 2121212124) == [2121212121]


def test_part1():
    """Test part 1 with example input."""
    # Update expected value from puzzle description
    input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    assert part1(input) == 1227775554

def test_part2():
    """Test part 2 with example input."""
    input = "11-22,95-115,998-1012,1188511880-1188511890,222220-222224,1698522-1698528,446443-446449,38593856-38593862,565653-565659,824824821-824824827,2121212118-2121212124"
    assert part2(input) == 4174379265
