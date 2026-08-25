class Review:
# TODO: Complete the implementation of the Review class.

    def __init__(self, review_id: int, user: User, track: Track, rating: int, review_text: String, date_submitted: int):
        self.__review_id = review_id
        self.__review_user = user
        self.__track = track
        self.__rating = rating
        self.__review_text = review_text
        self.__date_submitted = date_submitted

    @property
    def review_id(self) -> int:
        return self.__review_id

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def track(self) -> Track:
        return self.__track

    @property
    def review_text(self) -> String:
        return self.__review_text

    @property
    def user(self) -> User:
        return self.__user

    @property
    def date_submitted(self) -> int:
        return self.__date_submitted

    def __repr__(self) -> str:
        return f'<Review {self.track.title}, review id = {self.review_id}>'

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return self.review_id == other.review_id

    def __lt__(self, other):
        if not isinstance(other, self.__class__):
            return True
        return self.review_id < other.review_id

    def __hash__(self):
        return hash(self.review_id)
