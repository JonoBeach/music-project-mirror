from music.domainmodel.artist import Artist

class Album:
    def __init__(self, album_id: int, album_title: str):
        from music.domainmodel.track import Track
        if type(album_id) is not int or album_id < 0:
            raise ValueError("Album ID should be a non negative integer.")
        self.__album_id = album_id

        if type(album_title) is not str or album_title.strip() == '':
            raise ValueError("Album title should be a non-empty string.")
        self.__title = album_title.strip()

        self.__release_year: int | None = None
        self.__artist: Artist | None = None
        self.__tracks: list[Track] = []
        self.__album_url: str | None = None
        self.__album_info: str | None = None

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
    def release_year(self) -> int | None:
        return self.__release_year

    @release_year.setter
    def release_year(self, year):
        if year is not None and (not isinstance(year, int) or year < 0):
                raise ValueError("Album release year should be a non-negative integer.")
        self.__release_year = year

    @property
    def artist(self) -> Artist | None:
        return self.__artist

    @artist.setter
    def artist(self, new_artist: Artist | None):
        if new_artist is not None and not isinstance(new_artist, Artist):
            raise ValueError("artist must be an Artist instance or None.")
        self.__artist = new_artist

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
    def album_info(self) -> str | None:
        return self.__album_info

    @album_info.setter
    def album_info(self, info: str | None):
        if info is None:
            self.__album_info = None
        elif type(info) is str and info.strip() != '':
            self.album_info = info.strip()
        else:
            raise ValueError("album info must be a non-empty string or None.")

    @property
    def tracks(self):
        return self.__tracks

    def add_track(self, new_track):
        from music.domainmodel.track import Track
        if not isinstance(new_track, Track) or new_track in self.__tracks:
            return
        self.__tracks.append(new_track)

    def remove_track(self, track):
        from music.domainmodel.track import Track
        if not isinstance(track, Track) or track not in self.__tracks:
            return
        self.__tracks.remove(track)

    @property
    def total_tracks(self) -> int:
        return len(self.tracks)

    def __repr__(self):
        return f"<Album {self.title}, Album id = {self.album_id}>"

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
