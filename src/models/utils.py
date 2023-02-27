from enum import Enum


class Status(str, Enum):
    DONE = 'DONE'
    ON_PROGRESS = 'ON PROGRESS'
    PENDING = 'PENDING'
    NOTED = 'NOTED'


class Usernames(str, Enum):
    alfa = "urbiscuit"
    arigo = "Arigofhrz"
    iki = "iki_be_ph"
    nasri = "nanassssa"
    nathan = "nathan_aptanta"
    okta = "Oktapiancaw"
    pasca = "pascarmdn"
    rizal = "rizalwidiatmaja"


class UsernamesAndId(int, Enum):
    iki_be_ph = 1211950206
    urbiscuit = 1268637225
    Arigofhrz = 1415008365
    nanassssa = 731203660
    nathan_aptanta = 1239587269
    Oktapiancaw = 916823025
    rizalwidiatmaja = 757866026


class FromUser(dict):
    username: str
    user_id: int
