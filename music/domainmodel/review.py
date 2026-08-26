class Review:
# TODO: Complete the implementation of the Review class.

    def __init__(self, review_id: int, track: Track, rating: int, review_text: str, date_submitted: int):
        if type(review_id) is not int or review_id < 0:
            raise ValueError('Review ID should be an integer!')
        self.__review_id = review_id

        if type(track) is not Track:
            raise ValueError('Review track should be a Track!')
        self.__track = track

        if type(rating) is not int or rating < 0 or rating > 5:
            raise ValueError('Review ID should be an integer between 0-5 inclusive!')
        self.__rating = rating

        if type(review_text) is not str:
            raise ValueError('Review text should be a string!')
        self.__review_text = review_text

        if type(date_submitted) is not int:
            raise ValueError('Review date_submitted should be an int!')
        self.__date_submitted = date_submitted

        self.__user: User = None

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

    @user.setter
    def user(self, user: User):
        if type(user) is not User:
            raise ValueError('user should be of type User.')
        self.__user = user

    def __repr__(self) -> str:
        return f'<{self.user.user_name}: Review {self.track.title}, review id = {self.review_id}>'

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
