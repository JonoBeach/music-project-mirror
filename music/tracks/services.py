from typing import List, Optional

from music.adapters.repository import repo_instance
from music.domainmodel.track import Track

def get_tracks() -> List[Track]:
    if repo_instance is None:
        raise RuntimeError("Repository not initialised")
    return repo_instance.sort_by_track_title()

def get_track_by_id(track_id:int) -> Optional[Track]:
    if repo_instance is None:
        raise RuntimeError("Repository not initialised")
    return repo_instance.get_track(track_id)
