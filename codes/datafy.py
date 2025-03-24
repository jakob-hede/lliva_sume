from __future__ import annotations
from pathlib import Path

import yaml


class DoubleDumper(yaml.Dumper):
    def represent_scalar(self, tag, value, style=None):
        if tag == 'tag:yaml.org,2002:str':
            style = '"'
        return super().represent_scalar(tag, value, style=style)


class Crewie:
    def __init__(self, name, role) -> None:
        super().__init__()
        self.name = name
        self.role = role

    @property
    def data(self) -> dict:
        data = {self.name: self.role}
        return data

    @classmethod
    def create_from_dict_v1(cls, indx, crew_dict) -> Crewie:
        pass
        name, role = list(crew_dict.items())[0]
        crew = cls(name, role)
        return crew
        # name = crew_dict['name']
        # role = crew_dict['role']


#     # print(f'Crew.create_from_dict_v1: {crew_dict}')
#     key = list(crew_dict.keys())[0]
#     val = crew_dict[key]
#     name = val['name']
#     role = val['role']
#     notes = val.get('notes', '')
#     crew = cls(indx, name, role, notes)
#     return crew
#
# def print_self(self):
#     print(f'  -- {self.num} {self.name} ({self.role})')
#     if self.notes:
#         print(f'\t{self.notes}')


class Track:
    def __init__(self, num, vinyl, duration, greenlandic, danish, notes='') -> None:
        super().__init__()
        self.num = num
        self.vinyl = vinyl
        self.duration = duration
        self.greenlandic = greenlandic
        self.danish = danish
        self.notes = notes

    @property
    def data(self) -> dict:
        data = {}
        # data['num'] = self.num
        data['vinyl'] = self.vinyl
        data['duration'] = self.duration
        data['title'] = {}
        data['title']['greenlandic'] = self.greenlandic
        data['title']['danish'] = self.danish
        data['notes'] = self.notes
        return data

    @classmethod
    def create_from_dict_v1(cls, indx, track_dict) -> Track:
        # print(f'Track.create_from_dict_v1: {track_dict}')
        key = list(track_dict.keys())[0]
        val = track_dict[key]
        vinyl = val['vinyl']
        duration = val['duration']
        title_dict = val['title']
        greenlandic = title_dict['greenlandic']
        danish = title_dict['danish']
        notes = val.get('notes', '')
        track = cls(indx, vinyl, duration, greenlandic, danish, notes)
        return track

    def print_self(self):
        print(f'  -- {self.num} {self.vinyl}:\n\t{self.greenlandic}\n\t{self.danish}')
        if self.notes:
            print(f'\t{self.notes}')


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
            track = Track.create_from_dict_v1(indx, track_dict)
            self.tracks.append(track)
        self.crew = []
        for indx, crew_dict in enumerate(crew_list):
            crewie = Crewie.create_from_dict_v1(indx, crew_dict)
            self.crew.append(crewie)

    @property
    def data(self):
        data = {}
        data['title'] = self.title
        data['year'] = self.year
        data['description'] = self.description
        # data['crew'] = self.crew_list
        tracks: dict = {}
        data['tracks'] = tracks
        for track in self.tracks:
            tracks[track.num] = track.data
        crews = []
        data['crew'] = crews
        for crewie in self.crew:
            crews.append(crewie.data)
        return data

        # data['tracks'] = []
        # for track in self.tracks:
        #     track_data = {}
        #     track_data['vinyl'] = track.vinyl
        #     track_data['title'] = {}
        #     track_data['title']['greenlandic'] = track.greenlandic
        #     track_data['title']['danish'] = track.danish
        #     track_data['notes'] = track.notes
        #     data['tracks'].append(track_data)

    def print_self(self):
        print(f'- Album {self.num}')
        print(f' - title:\t"{self.title}"')
        print(f' - year:\t"{self.year}"')
        for track in self.tracks:
            track.print_self()

    @classmethod
    def create_from_dict_v1(cls, num, album_dict) -> Album:
        # print(f'Album.create_from_dict_v1: {album_dict}')
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
        self.data_v2_file = self.data_dir / 'albums.v2.yml'
        self.md_file = self.data_dir / 'sume_albums.md'
        self.md_parsed_file = self.data_dir / 'sume_albums.parsed.md'
        self.lines_file = self.data_dir / 'lines.yml'
        self.albums: list[Album] = []

    def yaml_dump(self, data_v2):
        return yaml.dump(data_v2, Dumper=DoubleDumper, sort_keys=False)

    def parse_v1(self):
        data_txt = self.data_file.read_text()
        data = yaml.safe_load(data_txt)
        # data_yml = yaml.dump(data)
        # print(data_yml)
        albums_dict = data['albums']
        for num, album_dict in albums_dict.items():
            # print(f' - {album_dict["title"]}')
            album = Album.create_from_dict_v1(num, album_dict)
            self.albums.append(album)
            album.print_self()

    def generate_v2(self) -> dict:
        data: dict = {}
        albums: dict = {}
        data['albums'] = albums
        for album in self.albums:
            albums[album.num] = album.data

        data_yml = yaml.safe_dump(data, sort_keys=False)
        print(data_yml)
        return data

        # data['albums'] = {}
        # for album in self.albums:
        #     album_dict = {}
        #     album_dict['title'] = album.title
        #     album_dict['year'] = album.year
        #     album_dict['description'] = album.description
        #     album_dict['crew'] = album.crew_list
        #     album_dict['tracks'] = []
        #     for track in album.tracks:
        #         track_dict = {}
        #         track_dict['vinyl'] = track.vinyl
        #         track_dict['title'] = {}
        #         track_dict['title']['greenlandic'] = track.greenlandic
        #         track_dict['title']['danish'] = track.danish
        #         track_dict['notes'] = track.notes
        #         album_dict['tracks'].append(track_dict)
        #     data['albums'][album.num] = album_dict

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
        self.parse_v1()
        print('=====================================')
        data_v2 = self.generate_v2()
        # v2_yml = yaml.dump(data_v2, sort_keys=False)
        v2_yml = self.yaml_dump(data_v2)
        self.data_v2_file.write_text(v2_yml)

    def test5(self):
        data_txt = self.data_v2_file.read_text()
        data = yaml.safe_load(data_txt)
        # data_yml = yaml.dump(data)
        # print(data_yml)
        md_txt = '# Sume Albums\n\n'
        albums_dict = data['albums']

        md_txt += f'## Albums:\n'
        for num, album_dict in albums_dict.items():
            title = f'"{album_dict["title"]}"'
            year = album_dict['year']
            md_txt += f'{num}. {year},  {title}\n'

        for num, album_dict in albums_dict.items():
            # print(num, album_dict['title'])
            title = album_dict['title']
            year = album_dict['year']
            description = album_dict['description']
            md_txt += f'## Album #{num} "{title}" ({year})\n'
            md_txt += f'{description}\n\n'

            tracks_list = album_dict['tracks']
            md_txt += '### Tracks\n'
            for track_num, track_dict in tracks_list.items():
                vinyl = track_dict['vinyl']
                title_dict = track_dict['title']
                greenlandic = title_dict['greenlandic']
                danish = title_dict['danish']
                notes = track_dict.get('notes', '')
                md_txt += f'{track_num + 1}. {vinyl}: {greenlandic} - ({danish})\n'
                if notes:
                    md_txt += f'\t{notes}\n'

            crew_list = album_dict['crew']
            md_txt += '### Crew\n'
            for crew_dict in crew_list:
                for name, role in crew_dict.items():
                    md_txt += f'- {name} ({role})\n'
            md_txt += '\n'

            md_txt += '\n'

        print(md_txt)
        self.md_parsed_file.write_text(md_txt)


def main():
    # print("Hello, World!")
    albumor = Albumor()
    albumor.test5()


if __name__ == "__main__":
    main()
