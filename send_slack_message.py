import os
import datetime
import json
import requests

messages = {
    "Monday": "STAAAATUSUPDATEEEE! Weekend overleefd?",
    "Tuesday": "STAAAATUSUPDATEEEE! Hoe gaat het met je dinsdagdip?",
    "Wednesday": "STAAAATUSUPDATEEEE! Het glas is halfvol: halverwege de week! Nou ja, bij jou waarschijnlijk alweer leeg... je gooit zo’n glas rode wijn toch meteen achterover.",
    "Thursday": "Geachte mevrouw Van Haeften,\nBij dezen het vriendelijke doch dringende verzoek om uw donderdagstatus mede te delen. Bij voorbaat dank.\nHoogachtend,\nUw Slackbot 🤖🎩",
    "Friday": "STAAAATUSUPDATEEEE! Bijna weekend! Nog leuke plannen (met iemand 👀)?"
}

def main():
    webhook_url = os.environ["SLACK_WEBHOOK_URL"]
    day = datetime.datetime.utcnow().strftime('%A')

    if day in ["Saturday", "Sunday"]:
        print(f"⏸ Geen statusupdate op {day}.")
        return

    message = messages[day]

    payload = {
        "text": message
    }

    response = requests.post(
        webhook_url,
        data=json.dumps(payload),
        headers={'Content-Type': 'application/json'}
    )

    if response.status_code != 200:
        raise Exception(f"Slack webhook failed: {response.status_code}, {response.text}")
    else:
        print("✅ Bericht succesvol verzonden via webhook")

if __name__ == "__main__":
    main()
