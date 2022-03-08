import fastapi
from parse import FaceitLobby
app = fastapi.FastAPI()

@app.get("/parse/{game_id}")
def get_game_id(game_id:str):
    return {"twitch": list(set(FaceitLobby(game_id).load_players().load_steam().get_links()))}
