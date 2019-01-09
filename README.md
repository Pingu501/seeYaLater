# SeeYaLater

This project is not about flaming bus drivers!

Some bus lines in Dresden seem to be always late ...
and nobody has the time to proof this right.

But for this we invented computer! ;)

Small **Python3** Script running in the background asking the API of the DVB
frequently for all departures in Dresden.

> Please make sure you are running Python 3.7

[DVB API documentation](https://github.com/kiliankoe/vvo/blob/master/documentation/webapi.md)

## Quick Start

Before starting make sure you are running some kind of database and it is configured in `seeYaLater/settings.py`

```
python3 manage.py start_miner
```

## Initial Stops

| ID       | Station Name                                  |
| :------- | --------------------------------------------- |
| 33000001 | Bahnhof Mitte                                 |
| 33000005 | Pirnaischer Platz                             |
| 33000007 | Straßburger Platz                             |
| 33000028 | HBF                                           |
| 33000037 | Postplatz                                     |
| 33000052 | Schillerplatz                                 |
| 33000111 | Lenneplatz                                    |
| 33000115 | Wasaplatz                                     |
| 33000144 | Tharandter Straße                             | 
| 33000727 | Technische Universität (Fritz-Foerster-Platz) |
| 33000742 | Helmholtzstraße                               |


## Running this project in background

To run this in background use `nohup`. This will survive ssh hangups.

```
nohup python3 manage.py start_miner
```

## Migration from Prototype

Make sure the db file is named `seeYaLater.db` and in the current directory.

```
python3 manage.py migrate_from_prototype
```

## TODOs

- [ ] API
- [ ] some kind of UI for users to use the data (VueJS)
- [ ] analyse the data
- [ ] use weather information
- [ ] maybe machine learning could be used here?
