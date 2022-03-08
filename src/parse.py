import requests
from typing import Optional, List
import string
from multiprocessing.pool import ThreadPool

valid_letters = set(i for i in string.ascii_letters + string.digits+"-+_?^$@!*")

def parse_content(content):
    ret = []
    if b"twitch.tv/" in content:
        for link in content.split(b"twitch.tv/")[1:]:
            s = ""
            for i in link.decode("utf8"):
                if i not in valid_letters:break
                s+=i
            if len(s):
                ret.append("twitch.tv/"+s)
    return ret

class Player:
    faceit_name = None
    faceit_id = None
    steam_id = None
    twitch = []
    def __init__(self, faceit_data):
        self.faceit_id=faceit_data["id"],
        self.faceit_name=faceit_data["nickname"]

    def __load_steam_id(self):
        r = requests.get(f"https://api.faceit.com/users/v1/nicknames/{self.faceit_name}")
        try:
            self.steam_id = r.json()["payload"]["platforms"]["steam"]["id64"]
        except:
            pass
        return self

    def load_steam(self):
        self.__load_steam_id()
        r = requests.get(f"http://steamcommunity.com/profiles/{self.steam_id}")
        self.twitch.extend(parse_content(r.content))
        return self

class FaceitLobby:
    game_id = None
    players: List[Player] = []

    def load_players(self):
        r = requests.get(f"https://api.faceit.com/match/v2/match/{self.game_id}")
        print(f"https://api.faceit.com/match/v2/match/{self.game_id}")
        data = r.json()
        with ThreadPool(10) as p:
            self.players = p.map(lambda x: Player(x), data["payload"]["teams"]["faction1"]["roster"]+data["payload"]["teams"]["faction2"]["roster"])
        return self
    
    def load_steam(self):
        with ThreadPool(10) as p:
            p.map(lambda x: x.load_steam(), self.players)
        return self

    def get_links_from_steam(self):
        links = []
        for player in self.players:
            links.extend(player.twitch)
        return links

    def get_links_from_faceit(self):
        r = requests.get(f"https://api.faceit.com/match/v2/match/{self.game_id}")
        return parse_content(r.content)

    def get_links(self):
        return self.get_links_from_steam()+self.get_links_from_faceit()


    def __init__(self, game_id):
        self.game_id = game_id
        self.players: List[Player] = []


