from base_dataset import BaseDataset


class RegressionDataset(BaseDataset):
    """
    Class implementing regression datasets.
    """

    def __init__(self) -> None:
        super().__init__()
        self._wrong_format_error()

    def _wrong_format_error(self):
        if self._format == "hierarchical":
            raise ValueError(
                "A regression dataset can't be organized in\
hierarchical structure"
            )


def main():
    dataset = RegressionDataset()
    dataset.load_data(root="blabla", strategy="lazy", format="hierarchical")


if __name__ == "__main__":
    main()
