import os
import csv
import ast

from music.domainmodel.artist import Artist
from music.domainmodel.album import Album
from music.domainmodel.track import Track
from music.domainmodel.genre import Genre


class CSVDataReader:
    def __init__(self, albums_file, tracks_file):
        self.__albums_file = albums_file
        self.__tracks_file = tracks_file
        self.__tracks = None
        self.__artists = None
        self.__albums = None
        self.__genres = None

    def read_csv_files(self):
        # TODO: use dict with id as key
        self.__tracks = dict()
        self.__artists = dict()
        self.__albums = dict()
        self.__genres = dict()

        track_data = dict()
        album_data = dict()

        with open(self.__tracks_file, "r", encoding="ISO-8859-1") as f:
            data = csv.DictReader(f)
            for track in data:
                # replace empty strings with None
                track = {key: val.strip() or None for key, val in track.items()}
                track_data[int(track["track_id"])] = track

        with open(self.__albums_file, "r", encoding="ISO-8859-1") as f:
            data = csv.DictReader(f)
            for album in data:
                # replace empty strings with None
                album = {key: val.strip() or None for key, val in album.items()}
                album_data[int(album["album_id"])] = album


        # fill data
        for track_id, track in track_data.items():
            self.__tracks[track_id] = Track(track_id, track["track_title"])

            # fill artists
            artist_id = int(track["artist_id"])
            if artist_id not in self.__artists:
                self.__artists[artist_id] = Artist(artist_id, track["artist_name"])

            # fill albums
            album_id = int(track["album_id"])
            if album_id not in self.__albums:
                self.__albums[album_id] = Album(album_id, track["album_title"])
                self.__albums[album_id].artist = self.__artists[artist_id]
                self.__albums[album_id].add_track(self.__tracks[track_id])
                self.__albums[album_id].album_url = track["album_url"]

                # album is sometimes not in album_data
                if album_id not in album_data:
                    break
                album = album_data[album_id]
                if album["album_year_released"] != None:
                    self.__albums[album_id].release_year = int(album["album_year_released"])
                self.__albums[album_id].album_info = album["album_information"]

            # fill genres
            track_genres = ast.literal_eval(track["track_genres"])
            for genre in track_genres:
                genre_id = int(genre["genre_id"])
                if genre_id not in self.__genres:
                    self.__genres[genre_id] = Genre(genre_id, genre["genre_title"])
                self.__tracks[track_id].add_genre(self.__genres[genre_id])

            # fill tracks
            self.__tracks[track_id].artist = self.__artists[artist_id]
            self.__tracks[track_id].album = self.__albums[album_id]
            self.__tracks[track_id].track_url = track["track_url"]
            if track["track_duration"] != None:
                self.__tracks[track_id].track_duration = int(track["track_duration"])

        # convert dicts back to list
        self.__tracks = list(self.__tracks.values())
        self.__artists = list(self.__artists.values())
        self.__albums = list(self.__albums.values())
        self.__genres = list(self.__genres.values())

    @property
    def dataset_of_tracks(self):
        return self.__tracks

    @property
    def dataset_of_artists(self):
        return self.__artists

    @property
    def dataset_of_albums(self):
        return self.__albums

    @property
    def dataset_of_genres(self):
        return self.__genres
