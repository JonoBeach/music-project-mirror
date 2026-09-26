class Artist:

    def __init__(self, id: int, full_name: str):
        if type(id) is not int or id < 0:
            raise ValueError("Artist ID should be a non negative integer!")
        self.__id: int = id

        if type(full_name) is not str or full_name.strip() == '':
            raise ValueError("Artist name should be a non-empty string.")
        self.__full_name: str = full_name.strip()

    @property
    def id(self) -> int:
        return self.__id

    @property
    def full_name(self) -> str:
        return self.__full_name

    @full_name.setter
    def full_name(self, new_full_name):
        if type(new_full_name) is not str or new_full_name.strip() == '':
            raise ValueError("Artist name should be a non-empty string.")
        self.__full_name = new_full_name.strip()


    def __repr__(self):
        return f"<Artist {self.full_name}, artist id = {self.id}>"

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
