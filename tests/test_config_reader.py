import unittest
import os

from config import Config_Path_Generator


class TestConfig(unittest.TestCase):
    def setUp(self):
        self.tail_cat_file = "file/path/nonexistent_2022.csv"
        self.tail_accounts_file_0 = "file/path/another_statement_location_0.csv"
        self.tail_accounts_file_1 = "file/path/another_statement_location_1.csv"
        self.base_dir = "/base/dir"
        self.data_dir = "data/training.json"

        self.d = {
            "cat_files": {2022: self.tail_cat_file},
            "accounts": {
                "02": {2022: {"months": {"July": self.tail_accounts_file_0}}},
                "07": {
                    2023: {
                        "months": {
                            "January": self.tail_accounts_file_1,
                        }
                    }
                },
            },
        }

    def test_paths_updated(self):
        config_paths = Config_Path_Generator(self.data_dir, self.base_dir)
        config_paths._cur_cfg = self.d
        config = config_paths.update_paths(config_paths._cur_cfg, self.base_dir)

        # print(os.path.join(self.base_dir, self.tail_cat_file), config["cat_files"][2022])
        self.assertEqual(
            os.path.join(self.base_dir, self.tail_cat_file), config["cat_files"][2022]
        )
        self.assertEqual(
            os.path.join(self.base_dir, self.tail_accounts_file_0),
            config["accounts"]["02"][2022]["months"]["July"],
        )
        self.assertEqual(
            os.path.join(self.base_dir, self.tail_accounts_file_1),
            config["accounts"]["07"][2023]["months"]["January"],
        )
