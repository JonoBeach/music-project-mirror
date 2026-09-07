from ast import Tuple
from typing import List, Optional
from music.adapters.repository import repo_instance
from music.domainmodel.track import Track

TRACKS_PER_PAGE = 15

def get_tracks(page: int = 1) -> Tuple[List[Track], int, int]:
    if repo_instance is None:
        raise RuntimeError("Repository not initialised")
    all_tracks = repo_instance.sort_by_track_title()
    num_tracks = len(all_tracks)
    total_pages = (num_tracks + TRACKS_PER_PAGE - 1 ) // TRACKS_PER_PAGE

    page = max(page, 1)
    page = min(page, total_pages)
    start = (page - 1) * TRACKS_PER_PAGE
    end = start + TRACKS_PER_PAGE
    tracks_on_page = all_tracks[start:end]

    return tracks_on_page, page, total_pages

def get_track_by_id(track_id:int) -> Optional[Track]:
    if repo_instance is None:
        raise RuntimeError("Repository not initialised")
    return repo_instance.get_track(track_id)
