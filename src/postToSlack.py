#coding: UTF-8

import slackweb
import sys

def post():
    # *.py msg
    try:
        msg = sys.argv[1]
    except:
        msg="Some trouble happen on experiment."

    slack = slackweb.Slack(url="https://hooks.slack.com/services/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")
    slack.notify(text=msg)

    print("notify to slack")

if __name__=="__main__":
    post()