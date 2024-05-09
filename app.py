from fastapi import FastAPI
from pydantic import BaseModel
from guia import guide_movie_channel
from typing import List, Optional


app = FastAPI(
    title="MyMovieGuide",
    description="My tv movie listing project",
    version="1.0.0",
    root_path="/api/v1"
)


class ResponseGuideMovies(BaseModel):
    movie_channel: Optional[str] = None
    movie_channel_number: Optional[int] = None
    img_movie_channel: Optional[str] = None
    time_init_movie: Optional[str] = None
    title_init_movie: Optional[str] = None
    progress_init_movie: Optional[str] = None
    next_movie_info: Optional[str] = None
    next_movie_info2: Optional[str] = None


@app.get('/guide', tags=["GuideTvMovies"], response_model=List[ResponseGuideMovies])
async def guide_movies_tv():
    return guide_movie_channel()


