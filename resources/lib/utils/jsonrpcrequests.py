# -*- coding: utf-8 -*-

params = {
    "jsonrpc": "2.0",
    "method": "Player.GetActivePlayers",
    # "params": {
    #     "playerid": 0
    # },
    "id": 1
}

params2 = {
    "jsonrpc": "2.0",
    "number": "Player.Position.Percentage",
    "params": {
        "playerid": 1
    },
    "id": 1
}

getPlayedPercentage = {
    "jsonrpc": "2.0",
    "method": "Player.GetProperties",
    "params": {
        "playerid": 1,
        "properties": [
            "percentage"
        ]
    },
    "id": 1
}
