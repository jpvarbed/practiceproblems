import unittest # https://docs.python.org/3/library/unittest.html
from main import process_stdin
from io import StringIO

# stringio objects https://docs.python.org/3/library/io.html
class TestOurUniq(unittest.TestCase):
    def run_test(self, input):
        output = StringIO()
        process_stdin(input, output)
        return output.getvalue()
    
    def test_basic_sorted(self):
        input = StringIO("1\n2\n3\n4\n6\n6\n6\n")
        expected_output = ("1\n2\n3\n4\n6\n")
        output = self.run_test(input)
        self.assertEqual(output, expected_output)
    
    def test_basic_unsorted(self):
        input = StringIO("6\n1\n3\n2\n4\n6\n6\n6\n")
        expected_output = ("6\n1\n3\n2\n4\n")
        output = self.run_test(input)
        self.assertEqual(output, expected_output)

    # do longer lines
    def test_basic_lines(self):
        input = StringIO("hello how are you\ngood\n")
        expected_output = ("hello how are you\ngood\n")
        self.assertEqual(self.run_test(input), expected_output)

    def test_basic_lines_repeat(self):
        input = StringIO("hello how are you\ngood right\ngood right\n")
        expected_output = ("hello how are you\ngood right\n")
        self.assertEqual(self.run_test(input), expected_output)

    def test_basic_empty(self):
        input = StringIO()
        expected_output = ("")
        output = self.run_test(input)
        self.assertEqual(output, expected_output)

if __name__ == "__main__":
    unittest.main()