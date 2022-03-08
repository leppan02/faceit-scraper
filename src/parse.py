from functools import lru_cache
from typing import List, Optional
import requests
import string
from multiprocessing.pool import ThreadPool

valid_letters = set(i for i in string.ascii_letters + string.digits+"-+_?^$@!*")

@lru_cache(100)
def cached_get(url):
    return requests.get(url)

def parse_content(links: set, url:str):
    try:
        content = cached_get(url).content
        if b"twitch.tv/" in content:
            for link in content.split(b"twitch.tv/")[1:]:
                s = ""
                for i in link.decode("utf8"):
                    if i not in valid_letters:break
                    s+=i
                if len(s):
                    links.add("twitch.tv/"+s)
    except:
        pass

class Faceit:
    def get_steam_id(faceit_nickname: str) -> Optional[str]:
        r = cached_get(f"https://api.faceit.com/users/v1/nicknames/{faceit_nickname}")
        try:
            return r.json()["payload"]["platforms"]["steam"]["id64"]
        except:
            return None

    def parse_player(links: set, faceit_data: str):
        faceit_nickname = faceit_data["nickname"]
        steam_id = Faceit.get_steam_id(faceit_nickname)
        if steam_id:
            parse_content(links, f"http://steamcommunity.com/profiles/{steam_id}")

    def get_players_data(game_id: str) -> List:
        data = cached_get(f"https://api.faceit.com/match/v2/match/{game_id}").json()
        return data["payload"]["teams"]["faction1"]["roster"]+data["payload"]["teams"]["faction2"]["roster"]

    def parse_game(game_id) -> List:
        links = set()
        parse_content(links, f"https://api.faceit.com/match/v2/match/{game_id}")
        players_data = Faceit.get_players_data(game_id)
        with ThreadPool(10) as p:
            p.map(Faceit.parse_player, links*len(players_data), players_data)
        return list(links)

    