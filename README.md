# SeeYaLater

> This branch is currently WIP while the project gets rewritten with django.

This project is not about flaming bus drivers!

Some bus lines in Dresden seem to be always late ...
and nobody has the time to proof this right.

But for this we invented computer! ;)

Small **Python3** Script running in the background asking the API of the DVB
frequently for all departures in Dresden.

[DVB API documentation](https://github.com/kiliankoe/vvo/blob/master/documentation/webapi.md)

## Quick Start

Before starting make sure you are running some kind of database and it is configured in `seeYaLater/settings.py`

```
python3 manage.py start_miner
```

## Options

By default the following stations are checked

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

Use `--all` to fetch nearly all stations in Dresden

## Running this project in background

To run this in background use `nohup`. This will survive ssh hangups. Make sure to run this command
always from the same directory. Otherwise you will end up with more than one database.

```
nohup python3.6 main.py &
```

___TODO:___ run this as a service is much better for servers

## TODOs

- some kind of UI for users to use the data (React?)
- analyse the data
- use weather information
- maybe machine learning could be used here?
