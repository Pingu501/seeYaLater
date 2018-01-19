# SeeYaLater

Some bus lines in Dresden seem to be always late ...
and nobody has the time to proof this right.

But for this we invented computer! ;)

Little Python Script running in the background asking the API of the DVB 
frequently for all departures in Dresden.

[API documentation](https://github.com/kiliankoe/vvo/blob/master/documentation/webapi.md)

## Requirements

- Python 3
- SQL to store the departure date

## Stations 

| Station | ID |
| :-------- | ---- |
| HBF | 33000028 |
| Wasaplatz | 33000115 |
| Straßburger Platz | 33000007 |

## Running this project in background

To run this in background use `nohup`. This will also survice ssh hangups.

```
nohup python3.6 main.py
```
