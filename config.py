import json
import os

class Config_Path_Generator(object):
    training_index = None
    cur_dir = None
    _cur_cfg = None

    def __init__(self, training_index_path: str, cur_dir: str = None):

        data_dir = os.path.dirname(training_index_path)
        self.training_index = training_index_path
        self.cur_dir = os.path.join(cur_dir or os.getcwd(), data_dir)

    def update_paths(self, obj, base_dir):
        """
        recursively update all string values in a nested dict/list structure
        to be absolute paths, relative to base_dir.
        """
        if isinstance(obj, dict):
            return {k: self.update_paths(v, base_dir) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [self.update_paths(item, base_dir) for item in obj]
        elif isinstance(obj, str):
            # you can add more checks here to confirm it's a file path if needed
            return os.path.abspath(os.path.join(base_dir, obj))
        else:
            return obj

    def load_config(self):
        if not os.path.exists(self.training_index):
            raise FileNotFoundError(f"Training index file {self.training_index} does not exist.")
        with open(self.training_index, 'r') as f:
            config = json.load(f)
        return self.update_paths(config, self.cur_dir)
    
    @property
    def cur_cfg(self):
        if self._cur_cfg is None:
            self._cur_cfg = self.load_config()
        return self._cur_cfg