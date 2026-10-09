import math
import uuid
from typing import List, Optional, Tuple
from music.adapters.repository import AbstractRepository
from music.domainmodel.track import Track
from music.domainmodel.review import Review
from music.domainmodel.user import User

TRACKS_PER_PAGE = 15

def get_tracks(repo:AbstractRepository, page: int = 1) -> Tuple[List[Track], int, int]:
    all_tracks = repo.sort_by_track_title()
    num_tracks = len(all_tracks)
    total_pages = math.ceil(num_tracks / TRACKS_PER_PAGE)

    page = max(page, 1)
    if total_pages > 0:
        page = min(page, total_pages)
    else:
        page = 1
    start = (page - 1) * TRACKS_PER_PAGE
    end = start + TRACKS_PER_PAGE
    tracks_on_page = all_tracks[start:end]

    return tracks_on_page, page, total_pages

def get_all_tracks(repo:AbstractRepository) -> List[Track]:
    return repo.sort_by_track_title()

def get_tracks_for_search(track_list: List[Track], page: int = 1, search_term: str = '', search_type: str = '') -> Tuple[List[Track], int, int]:
    if search_term:
        if search_type == 'title':
            track_list = [track for track in track_list if search_term.lower() in track.title.lower()]
        elif search_type == 'artist':
            track_list = [track for track in track_list if track.artist and search_term.lower() in track.artist.full_name.lower()]
        elif search_type == 'album':
            track_list = [track for track in track_list if track.album and search_term.lower() in track.album.title.lower()]

    num_tracks = len(track_list)
    total_pages = math.ceil(num_tracks / TRACKS_PER_PAGE)

    page = max(page, 1)
    if total_pages > 0:
        page = min(page, total_pages)
    else:
        page = 1
    start = (page - 1) * TRACKS_PER_PAGE
    end = start + TRACKS_PER_PAGE
    tracks_on_page = track_list[start:end]

    return tracks_on_page, page, total_pages

def get_track_by_id(track_id:int, repo:AbstractRepository) -> Optional[Track]:
    return repo.get_track(track_id)

def get_reviews_by_rating(track:Track, repo:AbstractRepository) -> list:
    return repo.get_reviews_by_rating(track)

def add_review(user:User, track:Track, rating:int, review_text:str, date_submitted:int, repo:AbstractRepository):
    if not any(track.id == review.track.id for review in user.reviews):
        id = uuid.uuid4().int
        review = Review(id, user.id, track, rating, review_text, date_submitted)
        repo.add_review(user, review, track)

def remove_review(user:User, review:Review, repo:AbstractRepository):
    repo.remove_review(user, review, review.track)
