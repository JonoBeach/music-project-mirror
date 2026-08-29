from multiprocessing import Value

from music.domainmodel.artist import Artist
from music.domainmodel.track import Track

class Album:
# TODO: Complete the implementation of the Album class.

#   album_info? album_image?
    def __init__(self, album_id: int, album_title: str, release_year: int, artist: Artist | None):
        if type(album_id) is not int or album_id < 0:
            raise ValueError("Album ID should be a non negative integer.")
        self.__album_id = album_id

        if type(album_title) is not str or album_title.strip() == '':
            raise ValueError("Album title should be a non-empty string.")
        self.__title = album_title.strip()

        if type(release_year) is not int or release_year <= 0 or release_year > 2026:
            raise ValueError("Alnum release year should be a non negative integer and no more than 2026.")
        self.__release_year = release_year

        if type(artist) is not Artist | None:
            raise ValueError("artist must be an Artist instance or None.")
        self.__artist = artist

        self.__tracks: list[Track] = []
        self.__album_url: str | None = None

    @property
    def album_id(self) -> int:
        return self.__album_id

    @property
    def title(self) -> str:
        return self.__title

    @title.setter
    def title(self, new_title: str):
        if type(new_title) is not str or new_title.strip() == '':
            raise ValueError("Album title should be a non-empty string.")
        self.__title = new_title.strip()

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def artist(self) -> Artist | None:
        return self.__artist

    @artist.setter
    def artist(self, new_artist: Artist | None):
        if new_artist is None:
            self.__artist = None
        elif isinstance(new_artist, Artist):
            self.__artist = new_artist
        else:
            raise ValueError("artist must be an Artist instance or None.")

    @property
    def album_url(self) -> str | None:
        return self.__album_url

    @album_url.setter
    def album_url(self, new_url: str | None):
        if new_url is None:
            self.__album_url = None
        elif type(new_url) is str and new_url.strip() != '':
            self.__album_url = new_url.strip()
        else:
            raise ValueError("album_url must be a non-empty string or None.")

    @property
    def tracks(self) -> list[Track]:
        return self.__tracks

    def add_track(self, new_track: Track):
        if not isinstance(new_track, Track) or new_track in self.__tracks:
            return
        self.__tracks.append(new_track)

    def remove_track(self, track: Track):
        if not isinstance(track, Track) or track not in self.__tracks:
            return
        self.__tracks.remove(track)

    @property
    def total_tracks(self) -> int:
        return len(self.tracks)

    def __repr__(self):
        return f"<Album {self.title}, Album id = {self.album_id}, release year: {self.release_year}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.album_id == other.album_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.album_id < other.album_id

    def __hash__(self):
        return hash(self.__album_id)
