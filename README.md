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

## Running this project as a service (for raspberry pi)

You'll need to create a new service. Just copy the `seeYaLater.service` file to `/etc/systemd/system`.

You also have to create a new user which runs the service `sudo useradd -M --system seeYaLater`

Before enabling the service, make sure the path for python and seeYaLater for `ExecStart` are correct.

```
systemctl daemon-reload
systemctl enable seeYaLater
systemctl start seeYaLater
```

Status checking is always possible with 

```
systemctl status homebridge
```

or detailed with

```
journalctl -u seeYaLater
```