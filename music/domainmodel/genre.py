class Genre:

    def __init__(self, id: int, genre_name: str):
        if type(id) is not int or id < 0:
            raise ValueError('Genre ID should be an integer!')
        self.__id = id

        if type(genre_name) is not str or genre_name.strip() == '':
            raise ValueError('Genre name should be a non-empty string.')
        self.__name = genre_name.strip()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def name(self) -> str:
        return self.__name


    @name.setter
    def name(self, name: str):
        if type(name) is not str or name.strip() == '':
            raise ValueError('Genre name should be a non-empty string.')
        self.__name = name.strip()

    def __repr__(self) -> str:
        return f'<Genre {self.name}, genre id = {self.id}>'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)
