# Grafana Slack Auto Report
this is the crawler mimic a mobile browser to **get screenshots in Grafana Dashboard then send to slack** <br />

# Why should we use this?
Grafana Reporting Tools with powerful functions, which cost ranges from **$99/mo to $3,500/mo** <br />
we only need **simple screenshots and auto report to slack daily** <br />

## how to create a slack webhook
please see <https://api.slack.com/methods/files.upload> to get more details <br />
find your slack app in <https://api.slack.com/apps> <br />
add incoming-webhook <br />
add incoming-webhook and files:write in app scopes <br />
install app to slack workspace <br />
find slack channel ID in channel details <br />
write Bot OAuth Token and channel ID in conf.ini <br />
invite bot to channel <br />

## based on platform to change crop sizes
crop sizes are determined by : platform.system() <br />
if it is Darwin, meaning you use a mac <br />
if it is Linux, meaning you use a Linux <br />

## how to use
python: 3.8 <br />
default OS = ubuntu 20.04 LTS, you can use other Linux, if you know how to use its commands <br />
`sudo apt install python3-venv` <br />
need install google-chrome and chromedriver <https://skolo.online/documents/webscrapping/#step-1-download-chrome> <br />
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

## crontab
send screenshots to slack AM 09:30 everyday <br />
30 9 * * * cd /home/john_chen/crawler_daily_jobs && /home/john_chen/crawler_daily_jobs/venv/bin/python /home/john_chen/crawler_daily_jobs/main.py >/dev/null 2>&1 <br />
