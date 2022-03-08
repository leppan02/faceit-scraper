import fastapi
from parse import Faceit
app = fastapi.FastAPI()

@app.get("/parse/{game_id}")
def get_game_id(game_id:str):
    return {"twitch": list(set(Faceit.parse_game(game_id)))}
