import pytest
from location import pull_address_list, convert_lon_lat, visualize_locations


def test_no_file():
    df = pull_address_list('invalid_filename.csv')
    with pytest.raises(IOError):
        pass


def test_file_exists():
    df = pull_address_list('test_address.csv')

