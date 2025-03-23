from __future__ import annotations
from pathlib import Path

import yaml


class Track:
    def __init__(self, num, vinyl, greenlandic, danish, notes='') -> None:
        super().__init__()
        self.num = num
        self.vinyl = vinyl
        self.greenlandic = greenlandic
        self.danish = danish
        self.notes = notes

    @classmethod
    def from_dict_v1(cls, indx, track_dict) -> Track:
        # print(f'Track.from_dict_v1: {track_dict}')
        key = list(track_dict.keys())[0]
        val = track_dict[key]
        vinyl = val['vinyl']
        duration = val['duration']
        title_dict = val['title']
        greenlandic = title_dict['greenlandic']
        danish = title_dict['danish']
        notes = val.get('notes', '')
        track = cls(indx, vinyl, greenlandic, danish, notes)
        return track

    def print_self(self):
        print(f'  -- {self.num} {self.vinyl}:\n\t{self.greenlandic}\n\t{self.danish}')


class Album:
    def __init__(self, num, title, year, description, crew_list, tracks_list) -> None:
        super().__init__()
        self.num = num
        self.title = title
        self.year = year
        self.description = description
        self.crew_list = crew_list
        self.tracks_list = tracks_list
        self.tracks = []
        for indx, track_dict in enumerate(tracks_list):
            track = Track.from_dict_v1(indx, track_dict)
            self.tracks.append(track)

    def print_self(self):
        print(f'- Album {self.num}')
        print(f' - title:\t"{self.title}"')
        print(f' - year:\t"{self.year}"')
        for track in self.tracks:
            track.print_self()

    @classmethod
    def from_dict_v1(cls, num, album_dict) -> Album:
        # print(f'Album.from_dict_v1: {album_dict}')
        title = album_dict['title']
        year = album_dict['year']
        description = album_dict['description']
        crew_list = album_dict['crew']
        tracks_list = album_dict['tracks']
        album = cls(num, title, year, description, crew_list, tracks_list)
        return album


class Albumor:
    def __init__(self):
        super().__init__()
        print("Albumor is ready.")
        self.data_dir = Path('/opt/projects/liva_sume/data')
        self.data_file = self.data_dir / 'albums.yml'
        self.md_file = self.data_dir / 'sume_albums.md'
        self.lines_file = self.data_dir / 'lines.yml'
        self.albums: list[Album] = []

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

    def test3(self):
        data_txt = self.data_file.read_text()
        data = yaml.safe_load(data_txt)
        # data_yml = yaml.dump(data)
        # print(data_yml)
        albums_dict = data['albums']
        for num, album_dict in albums_dict.items():
            print(num, album_dict['title'])
            tracks_list = album_dict['tracks']
            for track_index, track_dict in enumerate(tracks_list):
                for track_num, track_data in track_dict.items():
                    vinyl = track_data['vinyl']
                    title_dict = track_data['title']
                    greenlandic = title_dict['greenlandic']
                    danish = title_dict['danish']
                    print(f' - {track_index} {vinyl}:\n\t{greenlandic}\n\t{danish}')

            # track_data = track_dict.values()[0]
            # for track_num, track_data in tracks.items():
            # print(track_dict['title'])
            pass
            # for track_num, track_dict in tracks.items():
            #     title_dict = track_dict['title']
            #     greenlandic = title_dict['greenlandic']
            #     danish = title_dict['danish']
            #     print(f'{track_num}: {greenlandic} - {danish}')

    def test4(self):
        data_txt = self.data_file.read_text()
        data = yaml.safe_load(data_txt)
        # data_yml = yaml.dump(data)
        # print(data_yml)
        albums_dict = data['albums']
        for num, album_dict in albums_dict.items():
            # print(f' - {album_dict["title"]}')
            album = Album.from_dict_v1(num, album_dict)
            self.albums.append(album)
            album.print_self()


def main():
    # print("Hello, World!")
    albumor = Albumor()
    albumor.test4()


if __name__ == "__main__":
    main()
