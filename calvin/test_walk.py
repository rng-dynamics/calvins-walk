import unittest

import walk


class TestCalvinsWalk(unittest.TestCase):
    def test_expected_wait_time_v1(self):
        items = (
            {"signals": 1, "magic": 0, "time": 20},
            {"signals": 1, "magic": 1, "time": 0},
            {"signals": 2, "magic": 1, "time": 8.75},
            {"signals": 2, "magic": 2, "time": 0},
            {"signals": 3, "magic": 1, "time": 21.3234375},
        )
        for item in items:
            with self.subTest((item["signals"], item["magic"])):
                e_time = walk.expected_wait_time_v1(
                    n_signals=item["signals"], n_magic=item["magic"]
                )
                self.assertEqual(item["time"], e_time)

    def test_expected_wait_time_v2(self):
        items = (
            {"signals": 1, "magic": 0, "time": 20},
            {"signals": 1, "magic": 1, "time": 0},
            {"signals": 2, "magic": 1, "time": 8.75},
            {"signals": 2, "magic": 2, "time": 0},
            {"signals": 3, "magic": 1, "time": 21.3234375},
            {"signals": 56, "magic": 24, "time": 64.13360368},
        )
        for item in items:
            with self.subTest((item["signals"], item["magic"])):
                e_time = walk.expected_wait_time_v2(
                    n_signals=item["signals"], n_magic=item["magic"]
                )
                self.assertAlmostEqual(item["time"], e_time)

    def test_expected_wait_time_v1_and_v2_produce_the_same_result(self):
        items = [
            {"signals": 1, "magic": 0},
            {"signals": 1, "magic": 1},
            {"signals": 2, "magic": 1},
            {"signals": 2, "magic": 2},
            {"signals": 3, "magic": 1},
            {"signals": 8, "magic": 3},
            {"signals": 11, "magic": 4},
            {"signals": 16, "magic": 6},
        ]
        for item in items:
            with self.subTest((item["signals"], item["magic"])):
                e_time_v1 = walk.expected_wait_time_v1(
                    n_signals=item["signals"], n_magic=item["magic"]
                )
                e_time_v2 = walk.expected_wait_time_v2(
                    n_signals=item["signals"], n_magic=item["magic"]
                )
                self.assertEqual(e_time_v1, e_time_v2)

    def test_expected_wait_time_v2_and_v3_produce_the_same_result(self):
        items = [
            {"signals": 1, "magic": 0, "places": 7},
            {"signals": 1, "magic": 1, "places": 7},
            {"signals": 2, "magic": 1, "places": 7},
            {"signals": 2, "magic": 2, "places": 7},
            {"signals": 3, "magic": 1, "places": 7},
            {"signals": 4, "magic": 2, "places": 2},
            {"signals": 8, "magic": 3, "places": 2},
            {"signals": 11, "magic": 4, "places": 2},
            {"signals": 16, "magic": 6, "places": 1},
            {"signals": 32, "magic": 16, "places": 1},
            {"signals": 64, "magic": 28, "places": 1},
            {"signals": 128, "magic": 49, "places": 0},
            {"signals": 256, "magic": 128, "places": 0},
        ]
        for item in items:
            with self.subTest((item["signals"], item["magic"])):
                e_time_v2 = walk.expected_wait_time_v2(
                    n_signals=item["signals"], n_magic=item["magic"]
                )
                e_time_v3 = walk.expected_wait_time_v3(
                    n_signals=item["signals"], n_magic=item["magic"]
                )
                self.assertAlmostEqual(e_time_v2, e_time_v3, places=item["places"])


if __name__ == "__main__":
    unittest.main()
