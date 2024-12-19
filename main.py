from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

TELEGRAM_BOT_TOKEN = "6469816090:AAHK9pm9l3PsshONxKa0UfH9HNw0q8kEPkM"
CHAT_ID = "-1002448510220"  # ID чата или пользователя, куда отправлять заявки


def send_to_telegram(message):
    """ Отправка сообщения в Telegram """
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {
        "chat_id": CHAT_ID,
        "text": message,
        "parse_mode": "HTML",
    }
    response = requests.post(url, json=payload)
    return response.status_code == 200


@app.route('/webhook', methods=['POST'])
def webhook():
    """ Обработка данных от Tilda """
    data = request.json
    if not data:
        return jsonify({"status": "error", "message": "No data received"}), 400

    # Получаем данные из запроса (если передается строкой)
    content = data.get("text", "").strip()

    # Проверяем, содержит ли заявка все части
    try:
        brand, model, phone = content.split(maxsplit=2)  # Разделяем по пробелам (марка, модель, телефон)
    except ValueError:
        return jsonify({"status": "error", "message": "Invalid format"}), 400

    # Формируем сообщение для Telegram
    message = (
        f"<b>Новая заявка с сайта</b>\n\n"
        f"<b>Марка:</b> {brand}\n"
        f"<b>Модель:</b> {model}\n"
        f"<b>Телефон:</b> {phone}"
    )

    # Отправляем сообщение в Telegram
    if send_to_telegram(message):
        return jsonify({"status": "success"}), 200
    else:
        return jsonify({"status": "error", "message": "Failed to send to Telegram"}), 500


if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
