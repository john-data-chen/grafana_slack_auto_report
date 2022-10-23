# Grafana Slack Auto Report
this is the crawler mimic a mobile browser to **get screenshots in <https://grafana.com/> then send to slack** <br />

# Why should I use this?
Of course You can use Grafana Reporting Tools with powerful functions, which cost ranges from **$99/mo to $3,500/mo** <br />
I only need **simple screenshots and auto report to slack daily**, so I make this repo. You can use mine freely, if you like or clone it, **give me a star**, thanks! <br />

## how to create a slack webhook
please see <https://api.slack.com/methods/files.upload> to get more details <br />
find your slack app in <https://api.slack.com/apps> <br />
add incoming-webhook <br / >
add incoming-webhook and files:write in app scopes <br / >
install app to slack workspace <br / >
find slack channel ID in channel details <br / >
write Bot OAuth Token and channel ID in conf.ini <br / >
invite bot to channel <br / >

## how to use
python: 3.8 <br />
default OS = ubuntu 20.04 LTS, you can use other Linux, if you know how to use its commands <br />
`sudo apt install python3-venv` <br />
need chromedriver <br />
`python3 -m venv ./venv` <br />
`source ./venv/bin/activate` <br />
`pip install -r requirements.txt` <br />
`python main.py` <br />

## conf.ini
conf.ini which has username and password, it won't be in repository <br />
you have to create this file by yourself <br />

```
[credential]
url=https://github.com/
email=optional
password=optional
channel=channel ID
token=token of you slack app
```

## Limits
only be able to send to public slack channel <br />