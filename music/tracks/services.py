import math
from typing import List, Optional, Tuple
from music.adapters.repository import repo_instance
from music.domainmodel.track import Track

TRACKS_PER_PAGE = 15

def get_tracks(page: int = 1) -> Tuple[List[Track], int, int]:
    if repo_instance is None:
        raise RuntimeError("Repository not initialised")
    all_tracks = repo_instance.sort_by_track_title()
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

def get_all_tracks() -> List[Track]:
    if repo_instance is None:
        raise RuntimeError("Repository not initialised")
    return repo_instance.sort_by_track_title()

def get_tracks_for_search(track_list: List[Track], page: int = 1, search_term: str = '') -> Tuple[List[Track], int, int]:
    if search_term:
        track_list = [track for track in track_list if search_term.lower() in track.title.lower()]

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

def get_track_by_id(track_id:int) -> Optional[Track]:
    if repo_instance is None:
        raise RuntimeError("Repository not initialised")
    return repo_instance.get_track(track_id)

def get_review_by_rating(track:Track) -> list:
    if repo_instance is None:
       raise RuntimeError("Repository not initialised")
    return repo_instance.get_review_by_rating(track)
