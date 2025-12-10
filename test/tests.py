import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

import main
import unittest

class TestRoVFunctions(unittest.TestCase):

    def _check_size(self, size, result):
        self.assertEqual(main.main(f'test_{size}.txt'), result)

    sizes = [10, 100, 1000, 10000, 50000]
    results = [605, 54082, 5911121, 572718137, 14160491549]
    
    def test_sizes(self):
        for size, result in zip(self.sizes, self.results):
            print(f"iteration for {size} / {result}")
            with self.subTest(size=size, result=result):
                self._check_size(size, result)

if __name__ == '__main__':
    unittest.main()