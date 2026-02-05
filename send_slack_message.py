import os
import datetime
import requests

# Statusberichten per dag
messages = {
    "Monday": "STAAAATUSUPDATEEEE! Weekend overleefd?",
    "Tuesday": "STAAAATUSUPDATEEEE! Hoe gaat het met je dinsdagdip?",
    "Wednesday": "STAAAATUSUPDATEEEE! Het glas is halfvol: halverwege de week! Nou ja, bij jou waarschijnlijk alweer leeg... je gooit zo’n glas rode wijn toch meteen achterover.",
    "Thursday": "Geachte mevrouw Van Haeften,\nBij dezen het vriendelijke doch dringende verzoek om uw donderdagstatus mede te delen. Bij voorbaat dank.\nHoogachtend,\nUw Slackbot 🤖🎩",
    "Friday": "STAAAATUSUPDATEEEE! Bijna weekend! Nog leuke plannen (met iemand 👀)?"
}

SLACK_API_BASE = "https://slack.com/api"


def slack_api(method: str, token: str, payload: dict) -> dict:
    resp = requests.post(
        f"{SLACK_API_BASE}/{method}",
        headers={
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json; charset=utf-8",
        },
        json=payload,
        timeout=20,
    )
    data = resp.json()
    if resp.status_code != 200:
        raise Exception(f"Slack API HTTP {resp.status_code}: {resp.text}")
    if not data.get("ok"):
        raise Exception(f"Slack API error in {method}: {data.get('error')} | response={data}")
    return data


def main():
    token = os.environ["SLACK_BOT_TOKEN"]
    channel = os.environ["SLACK_CHANNEL_ID"]

    # 0) One-time pinned status message (editable via GitHub Secret)
    status_message = os.environ.get("STATUS_MESSAGE", "Donna’s status: 🙂")

    status_post = slack_api("chat.postMessage", token, {"channel": channel, "text": status_message})
    slack_api("pins.add", token, {"channel": status_post["channel"], "timestamp": status_post["ts"]})
    print("📌 Statusbericht gepost en gepind")

    # 1) Dagelijkse message (niet gepind)
    day = datetime.datetime.utcnow().strftime("%A")
    message = messages.get(day, "Goedemorgen! Hoe gaat het vandaag?")

    post = slack_api("chat.postMessage", token, {"channel": channel, "text": message})
    print(f"✅ Dagelijkse message gepost in {post['channel']} op ts={post['ts']}")


if __name__ == "__main__":
    main()
