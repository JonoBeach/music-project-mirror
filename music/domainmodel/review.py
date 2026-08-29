from music.domainmodel.track import Track

class Review:
# TODO: Complete the implementation of the Review class.

    def __init__(self, review_id: int, user_id: int, track: Track, rating: int, review_text: str, date_submitted: int):
        if type(review_id) is not int or review_id < 0:
            raise ValueError('Review ID should be an integer!')
        self.__review_id = review_id

        if type(user_id) is not int or user_id < 0:
            raise ValueError('User ID should be an integer above 0.')
        self.__user_id = user_id

        if type(track) is not Track:
            raise ValueError('Track should be an Track object')
        self.__track = track

        if type(rating) is not int or rating < 0 or rating > 5:
            raise ValueError('Review ID should be an integer between 0-5 inclusive.')
        self.__rating = rating

        if type(review_text) is not str:
            raise ValueError('Review text should be a string.')
        self.__review_text = review_text

        if type(date_submitted) is not int:
            raise ValueError('Review date_submitted should be an int.')
        self.__date_submitted = date_submitted

    @property
    def review_id(self) -> int:
        return self.__review_id

    @property
    def rating(self) -> int:
        return self.__rating

    @property
    def review_text(self) -> str:
        return self.__review_text

    @property
    def user_id(self) -> int:
        return self.__user_id

    @property
    def track(self) -> Track:
        return self.__track

    @property
    def date_submitted(self) -> int:
        return self.__date_submitted

    def __repr__(self) -> str:
        return f'<By: {self.user_id}, Review {self.track.title}, review id = {self.review_id}>'

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
