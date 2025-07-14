# send_slack_message.py

import os
from datetime import datetime
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

messages = {
    "Monday": "STAAAATUSUPDATEEEE! Weekend overleefd?",
    "Tuesday": "STAAAATUSUPDATEEEE! Hoe gaat het met je dinsdagdip?",
    "Wednesday": "STAAAATUSUPDATEEEE! Het glas is halfvol: halverwege de week! Nou ja, bij jou waarschijnlijk alweer leeg... je gooit zo’n glas rode wijn toch meteen achterover.",
    "Thursday": "Geachte mevrouw Van Haeften,\nBij dezen het vriendelijke doch dringende verzoek om uw donderdagstatus mede te delen. Bij voorbaat dank.\nHoogachtend,\nUw Slackbot 🤖🎩",
    "Friday": "STAAAATUSUPDATEEEE! Bijna weekend! Nog leuke plannen (met iemand 👀)?"
}

def main():
    slack_token = os.environ["SLACK_BOT_TOKEN"]
    user_id = os.environ["SLACK_USER_ID"]

    # Bepaal dag van de week (UTC)
    day_of_week = datetime.utcnow().strftime('%A')
    message = messages.get(day_of_week, "Goedemorgen! Hoe gaat het vandaag?")

    client = WebClient(token=slack_token)

    try:
        response = client.chat_postMessage(
            channel=user_id,
            text=message
        )
        print(f"Bericht verzonden: {response['message']['text']}")
    except SlackApiError as e:
        print(f"Fout bij verzenden: {e.response['error']}")

if __name__ == "__main__":
    main()