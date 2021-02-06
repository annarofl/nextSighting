import pytest
from location import pull_address_list, convert_lon_lat, visualize_locations
from unittest.mock import patch, mock_open
import pandas as pd
from pandas._testing import assert_frame_equal


def test_no_file():
    with pytest.raises(IOError):
        df = pull_address_list('invalid_filename.csv')

def test_file_read():
    df_read = pull_address_list('test_files/test_address.csv')
    d = [{'Type': 'manual',
         'Number': 1,
         'Name': 'Emily',
         'Address1': '10608 Beard Ave',
         'Address2': '',
         'City': 'Austin',
         'State': 'Texas',
         'Zip': '78748',
         'country': 'USA',
         'email': 'emily@rockman.life',
         'ADDRESS': '10608 Beard Ave, , Austin, Texas, 78748, USA'}]
    df_expected = pd.DataFrame(d)
    assert_frame_equal(df_read, df_expected)


def test_empty_file():
    with pytest.raises(pd.errors.EmptyDataError):
        df = pull_address_list('test_files/blank.csv')


def test_no_addresses_on_file():
    df_read = pull_address_list('test_files/headers_only.csv')
    column_names = ['Type',
         'Number',
         'Name',
         'Address1',
         'Address2',
         'City',
         'State',
         'Zip',
         'country',
         'email',
         'ADDRESS']

    df_expected = pd.DataFrame(columns=column_names)
    print(df_expected.dtypes)
    print('*'*20)
    print(df_read.dtypes)
    assert_frame_equal(df_read, df_expected, check_dtype=False)


def test_do_stuff_with_file():
    # open_mock = mock_open()
    # with patch("main.open", open_mock, create=True):
    #     main.write_to_file("test-data")
    #
    # open_mock.assert_called_with("output.txt", "w")
    # open_mock.return_value.write.assert_called_once_with("test-data")
    pass
