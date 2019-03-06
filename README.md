# SeeYaLater

This project is not about flaming bus drivers!

Some bus lines in Dresden seem to be always late ...
and nobody has the time to proof this right.

Python program based on django fetching all departures in Dresden.

[DVB API documentation](https://github.com/kiliankoe/vvo/blob/master/documentation/webapi.md)

## Development

### Backend

Before starting make sure you are running python 3.6 or newer and got some kind of database and it is configured in `seeYaLater/settings.py`

```
python3 manage.py start_miner
python3 manage.py runserver
```

### Frontend

```
cd frontend
nvm use
yarn
yarn dev
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
| 33000588 | Elbepark                                      | 
| 33000727 | Technische Universität (Fritz-Foerster-Platz) |
| 33000742 | Helmholtzstraße                               |


## Migration from Prototype

Make sure the db file is named `seeYaLater.db` and in the current directory.

```
python3 manage.py migrate_from_prototype
```

## Build & Deployment

```
cd frontend
nvm use
yarn
yarn generate
```

[Static Resource Guide](https://docs.djangoproject.com/en/2.1/howto/static-files/)
