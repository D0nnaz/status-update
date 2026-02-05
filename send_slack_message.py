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
    token = os.environ["SLACK_BOT_TOKEN"]          # nieuw
    channel = os.environ["SLACK_CHANNEL_ID"]      # nieuw (C... / G... / D...)

    day = datetime.datetime.utcnow().strftime("%A")
    message = messages.get(day, "Goedemorgen! Hoe gaat het vandaag?")

    # 1) Post het bericht (zodat we ts krijgen)
    post = slack_api("chat.postMessage", token, {"channel": channel, "text": message})
    ts = post["ts"]
    ch = post["channel"]

    print(f"✅ Bericht gepost in {ch} op ts={ts}")

    # 2) Pin het bericht (zodat het voor iedereen in die chat blijft staan)
    slack_api("pins.add", token, {"channel": ch, "timestamp": ts})
    print("📌 Bericht succesvol gepind")


if __name__ == "__main__":
    main()
