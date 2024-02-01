import os

from base_dataset import BaseDataset


class ClassificationDataset(BaseDataset):
    # implement hierarchical
    def __init__(self):
        super().__init__()

    def load_data(self, root, strategy, format="csv", labels_path=None):
        super().load_data(root, strategy, format, labels_path)
        if self._format == "hierarchical":
            self._hierarchical_load_data()

    def _hierarchical_load_data(self):
        for class_name in os.listdir(self._root):
            if class_name != ".DS_Store":
                class_dir = os.path.join(self._root, class_name)
                for filename in os.listdir(class_dir):
                    if filename == ".DS_Store":
                        continue
                    path = os.path.join(class_dir, filename)

                    if self._strategy == "lazy":
                        self.data.append(path)

                    if self._strategy == "eager":
                        data = self._read_data_file(path)
                        self.data.append(data)
                    self.targets.append(class_name)
