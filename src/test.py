import json

s = """[{"_id":{"matchId":"622754d1a6ca1b00072208c5","playerId":"2ca54384-bb1f-4639-b715-626f9a3ac976"},"created_at":1646744785092,"updated_at":1646744875541,"i9":"4","nickname":"leppan02","i10":"0","i13":"8","i15":"1","i6":"23","i14":"2","i7":"7","i16":"0","i8":"20","playerId":"2ca54384-bb1f-4639-b715-626f9a3ac976","c3":"0.77","c2":"1.15","c4":"35","c1":"1","i19":"0","teamId":"cbb860ae-ac5f-4816-a344-58d0e7ee1283","i3":"9","i4":"5","i5":"team_poroh-","premade":false,"c5":"14","bestOf":"2","competitionId":"a3c75828-7f0f-4940-adb9-994b4b389070","date":1646744784000,"game":"csgo","gameMode":"5v5","i0":"EU","i1":"de_overpass","i12":"30","i18":"14 / 16","i2":"a62d4f2c-66c6-4593-8a5c-75642112dbc5","matchId":"1-c801481e-061c-4fd3-b371-7045cf68d7ed","matchRound":"1","played":"1","status":"APPLIED","elo":"1459"}]"""

data = json.loads(s)
print(data[0]["matchId"])