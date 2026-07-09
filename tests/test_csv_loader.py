import os
import tempfile
import csv
from services.csv_loader import load_csv_as_2d_array, array2d_to_dicts, delete_csv_file, clear_loaded_csv_from_memory

class TestCsvLoader:
    def setup_method(self):
        self.tmp = tempfile.NamedTemporaryFile(mode='w', newline='', delete=False, suffix='.csv')
        self.path = self.tmp.name

    def teardown_method(self):
        if os.path.exists(self.path):
            os.unlink(self.path)

    def test_load_csv_as_2d_array(self):
        self.tmp.write("student_id,name\nS001,Alice\nS002,Bob\n")
        self.tmp.close()
        header, data = load_csv_as_2d_array(self.path)
        assert header == ['student_id', 'name']
        assert data == [['S001', 'Alice'], ['S002', 'Bob']]

    def test_raises_on_no_data_rows(self):
        self.tmp.write("header1,header2\n")
        self.tmp.close()
        try:
            load_csv_as_2d_array(self.path)
            assert False, "Should have raised ValueError"
        except ValueError:
            pass

    def test_array2d_to_dicts(self):
        header = ['a', 'b']
        data = [['1', '2'], ['3', '4']]
        records, summary = array2d_to_dicts(header, data)
        assert records == [{'a': '1', 'b': '2'}, {'a': '3', 'b': '4'}]
        assert summary['rows'] == 2

    def test_array2d_to_dicts_pads_short_rows(self):
        header = ['a', 'b', 'c']
        data = [['1', '2']]
        records, _ = array2d_to_dicts(header, data)
        assert records == [{'a': '1', 'b': '2', 'c': ''}]

    def test_delete_csv_file_removes_file(self):
        with open(self.path, 'w') as f:
            f.write("test")
        assert delete_csv_file(self.path) is True
        assert os.path.exists(self.path) is False

    def test_delete_csv_file_missing(self):
        assert delete_csv_file('/nonexistent/file.csv') is False

    def test_clear_loaded_csv_from_memory(self):
        state = {'header': ['a'], 'data_2d': [['1']], 'csv_dicts': [{'a': '1'}]}
        clear_loaded_csv_from_memory(state)
        assert state['header'] is None
        assert state['data_2d'] is None
        assert state['csv_dicts'] is None
