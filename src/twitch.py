import requests
token = "n6iolevnaa4idyty078yz1a5eacxny"
"418toyttzxwnpxum3x45ts46subydh"
API_HEADERS = {
    'Client-ID' : 'myClientID',
    'Authorization' : 'Bearer '+token,
}

def checkUser(userName): #returns true if online, false if not
    url = 'https://api.twitch.tv/helix/streams?user_login='+userName

    try:
        req = requests.get(url, headers=API_HEADERS)
        print(req.content)
        jsondata = req.json()
        if len(jsondata['data']) == 1:
            return True
        else:
            return False
    except Exception as e:
        print("Error checking user: ", e)
        return False

print(checkUser("bikestreaming"))