from pathlib import Path

import yaml


class Albumor:
    def __init__(self):
        super().__init__()
        print("Albumor is ready.")
        self.data_dir = Path('/opt/projects/liva_sume/data')
        self.data_file = self.data_dir / 'albums.yml'
        self.md_file = self.data_dir / 'sume_albums.md'
        self.lines_file = self.data_dir / 'lines.yml'

    def test1(self):
        data_txt = self.data_file.read_text()
        data = yaml.safe_load(data_txt)
        data_yml = yaml.dump(data)
        print(data_yml)

    def test2(self):
        md_txt = self.md_file.read_text()
        lines = md_txt.split('\n')
        lines_yml = yaml.dump(lines)
        self.lines_file.write_text(lines_yml)


def main():
    # print("Hello, World!")
    albumor = Albumor()
    albumor.test2()


if __name__ == "__main__":
    main()
