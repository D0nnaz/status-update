def main():
    token = os.environ["SLACK_BOT_TOKEN"]
    channel = os.environ["SLACK_CHANNEL_ID"]

    mode = os.environ.get("MODE", "reminder").lower()

    STATUS_PREFIX = "Donna’s status:"
    status_message = os.environ.get("STATUS_MESSAGE", f"{STATUS_PREFIX} 🙂")

    def upsert_pinned_status():
        # Zoek bestaande pinned status en update die; anders: post + pin
        pins = slack_api("pins.list", token, {"channel": channel}).get("items", [])

        existing_ts = None
        for item in pins:
            msg = item.get("message")
            if not msg:
                continue
            text = msg.get("text", "")
            if text.startswith(STATUS_PREFIX):
                existing_ts = msg.get("ts")
                break

        if existing_ts:
            slack_api("chat.update", token, {"channel": channel, "ts": existing_ts, "text": status_message})
            print(f"📝 Status-pin geüpdatet (ts={existing_ts})")
        else:
            post = slack_api("chat.postMessage", token, {"channel": channel, "text": status_message})
            slack_api("pins.add", token, {"channel": post["channel"], "timestamp": post["ts"]})
            print(f"📌 Status-pin aangemaakt + gepind (ts={post['ts']})")

    if mode == "status":
        upsert_pinned_status()
        return

    day = datetime.datetime.utcnow().strftime("%A")
    message = messages.get(day, "Goedemorgen! Hoe gaat het vandaag?")

    post = slack_api("chat.postMessage", token, {"channel": channel, "text": message})
    print(f"✅ Dagelijkse message gepost in {post['channel']} op ts={post['ts']}")
