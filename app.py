``python
import os
import random
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)

# คัดลอก Channel Access Token ที่ได้จาก LINE Developers มาใส่ตรงนี้แทนข้อความเดิม
CHANNEL_ACCESS_TOKEN = "9LyFUq5UWsfChJJLWZBCaVZdQKOfzVl6rKkkxOH5/kqrKrxc459iOymRRQXNgxKjItwthIyNtVt5o23F3usOUejKVfMYIfiAvNEl/blAk+e2hgdGBbnCfOtM6qxQUTXVVCNp/zZ+eO3aQSK8aT4QPQdB04t89/1O/w1cDnyilFU="

HELLO_REPLIES = [
    "สวัสดีครับผม! มีอะไรให้ช่วยพิมพ์ถามได้เลยนะ 🙏",
    "ยินดีต้อนรับครับ! 😊",
    "ฮัลโหลลล วันนี้เป็นยังไงบ้างคุยกันได้นะ 🎉",
    "สวัสดีจ้า ดีใจที่ได้เจอนะ ✨"
]

@app.route("/")
def index():
    return "OpenChat Bot is running!"

@app.route("/callback", methods=["POST"])
def callback():
    body = request.get_json()
    for event in body.get("events", []):
        event_type = event.get("type")
        
        # เมื่อมีคนพิมพ์ "สวัสดี", "หวัดดี", "hello"
        if event_type == "message":
            msg_text = event["message"].get("text", "").strip()
            reply_token = event["replyToken"]
            
            if msg_text in ["สวัสดี", "หวัดดี", "hello", "Hello"]:
                reply_message = random.choice(HELLO_REPLIES)
                send_reply(reply_token, reply_message)
                
        # เมื่อมีคนกดเข้าห้อง OpenChat มาใหม่
        elif event_type == "join":
            reply_token = event["replyToken"]
            welcome_text = "ยินดีต้อนรับสมาชิกใหม่ครับ! 🎉 " + random.choice(HELLO_REPLIES)
            send_reply(reply_token, welcome_text)

    return jsonify({"status": "success"}), 200

def send_reply(reply_token, text_content):
    url = "https://api.line.me/v2/bot/message/reply"
    headers = {
        "Content-Type": "application/json",
        "Authorization": f"Bearer {CHANNEL_ACCESS_TOKEN}"
    }
    payload = {
        "replyToken": reply_token,
        "messages": [{"type": "text", "text": text_content}]
    }
    requests.post(url, json=payload, headers=headers)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
