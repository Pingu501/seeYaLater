# SeeYaLater

This project is not about flaming bus drivers!

Some bus lines in Dresden seem to be always late ...
and nobody has the time to proof this right.

But for this we invented computer! ;)

Small **Python3** Script running in the background asking the API of the DVB 
frequently for all departures in Dresden.


[API documentation](https://github.com/kiliankoe/vvo/blob/master/documentation/webapi.md)

## Stations 

| Station | ID |
| :-------- | ---- |
| Pirnaischer Platz | 33000005 |
| Straßburger Platz | 33000007 |
| HBF | 33000028 |
| Wasaplatz | 33000115 |
| Technische Universität (Fritz-Foerster-Platz) | 33000727 |

## Running this project in background

To run this in background use `nohup`. This will also survive ssh hangups. Make sure to run this command
always from the same directory. Otherwise you will end up with more than one database.

```
nohup python3.6 main.py &
```
