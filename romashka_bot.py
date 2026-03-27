import urllib.request
import urllib.parse
import json
import time

TOKEN = "8627593181:AAGYyoflhrj65lkBroy89tHfc8QmcgNgRQI"
API = f"https://api.telegram.org/bot{TOKEN}"

TEXTS = {
    "welcome": "🌼 *Добро пожаловать в Апартаменты Ромашка!*\n\nЭтот бот — ваш личный путеводитель по гостинице и Петербургу.\n\nВыберите раздел:",
    "about": "🏛 *Апартаменты Ромашка*\n\n📍 *Адрес:* ул. Ломоносова, 14\n🚇 *Метро:* Владимирская, Достоевская, Звенигородская\n📞 *Телефон:* +7 906 274-16-09\n🌐 romashkarooms.ru\n\nУ нас 4 уникальных номера — Берёзки, Одуванчик, Буфет и Люстра. В каждом — кухня, ванная, до 4 гостей.",
    "romashka": "🌼 *Парадная Ромашка*\n\nПрямо в вашем доме — одна из самых известных парадных Петербурга.\n\nЖёлтые стены и белая лепнина напоминают ромашку — отсюда и название. В центре — историческая шахта *первого парового лифта Петербурга*. Кованые решётки, мозаичный пол — всё с 1892 года.\n\nСюда приезжают со всей страны. А вы живёте внутри этой истории. 🦢",
    "booking": "📅 *Бронирование*\n\nЗабронируйте напрямую — без комиссии:\n\n🌐 https://romashkarooms.ru\n\n📞 +7 906 274-16-09\n\nТакже на площадках:\n• Суточно.ру\n• Островок\n• Яндекс Путешествия",
    "feedback": "💬 *Обратная связь*\n\n⭐ Оставить отзыв на Яндекс Картах:\nhttps://yandex.ru/maps/org/103931315029/reviews/\n\n📞 Администратор: +7 906 274-16-09\n\nЕсли что-то пошло не так — сообщите нам сразу. Мы всегда готовы помочь! 🌼",
    "eat": "🍽 *Поесть рядом*\n\n☕ *Кофе и завтраки*\n• Буше — Садовая, 2 (5 мин)\n• Кофе 22 — Ломоносова, 22\n\n🍜 *Обед и ужин*\n• Шаурма на Пяти углах — культовое место\n• Рубинштейна, 15 — улица ресторанов\n• Пробка — Белинского, 5\n\n🛵 *Доставка*\nЯндекс Еда, Самокат работают в нашем районе",
    "walk": "🚶 *Погулять*\n\n🌊 *Набережные*\n• Фонтанка — 2 мин\n• Мост Ломоносова — у дома\n• Набережная Мойки — 15 мин\n\n🌳 *Парки*\n• Михайловский сад — 15 мин\n• Летний сад — 20 мин\n\n📸 *Для фото*\n• Пять углов — за углом\n• Парадная Ромашка — у вас дома 🌼",
    "see": "👁 *Посмотреть*\n\n🏛 *Музеи*\n• Русский музей — 15 мин\n• Музей Достоевского — 10 мин\n• Музей Фаберже — 20 мин\n\n⛪ *Архитектура*\n• Спас-на-Крови — 20 мин\n• Казанский собор — 20 мин\n• Аничков мост — 10 мин\n\n🎭 *Театры*\n• БДТ — 10 мин\n• Александринский — 15 мин",
    "route_2h": "🧭 *Маршрут на 2 часа*\n_«Сердце старого Петербурга»_\n\n1️⃣ Парадная Ромашка — старт 🌼\n2️⃣ Мост Ломоносова — 2 мин\n3️⃣ Набережная Фонтанки\n4️⃣ Аничков мост — кони Клодта\n5️⃣ Невский проспект\n6️⃣ Казанский собор — вход бесплатный\n\n🔙 Обратно по Садовой\n\n_~4 км, 2 часа_",
    "route_4h": "🧭 *Маршрут на 4 часа*\n_«От Фонтанки до Дворцовой»_\n\n1️⃣ Пять углов — старт\n2️⃣ Рубинштейна — кофе\n3️⃣ Михайловский замок\n4️⃣ Михайловский сад\n5️⃣ Спас-на-Крови\n6️⃣ Русский музей\n7️⃣ Невский проспект\n8️⃣ Дворцовая площадь\n\n_~7 км, 4 часа_",
    "route_day": "🧭 *Целый день*\n_«Большой Петербург»_\n\n🌅 *Утро*\n• Завтрак на Рубинштейна\n• Эрмитаж (с 10:30)\n\n☀️ *День*\n• Петропавловская крепость\n• Кронверкский проспект\n\n🌆 *Вечер*\n• Казанский собор\n• Ужин на Думской\n\n🌉 *Ночью летом*\n• Развод мостов — Дворцовый в 1:10\n\n_12-14 часов, лучший день в Петербурге_ 🌼",
}

KEYBOARDS = {
    "main": [[{"text": "🏛 О гостинице", "callback_data": "about"}, {"text": "📅 Бронирование", "callback_data": "booking"}],
             [{"text": "🗺 Развлечения", "callback_data": "entertainment"}, {"text": "💬 Обратная связь", "callback_data": "feedback"}]],
    "about": [[{"text": "🌼 Парадная Ромашка", "callback_data": "romashka"}],
              [{"text": "◀️ Главное меню", "callback_data": "start"}]],
    "entertainment": [[{"text": "🍽 Поесть", "callback_data": "eat"}, {"text": "🚶 Погулять", "callback_data": "walk"}],
                      [{"text": "👁 Посмотреть", "callback_data": "see"}, {"text": "🧭 Экскурсии", "callback_data": "routes"}],
                      [{"text": "◀️ Главное меню", "callback_data": "start"}]],
    "routes": [[{"text": "⏱ 2 часа", "callback_data": "route_2h"}],
               [{"text": "🕓 4 часа", "callback_data": "route_4h"}],
               [{"text": "🌅 Целый день", "callback_data": "route_day"}],
               [{"text": "◀️ Назад", "callback_data": "entertainment"}]],
    "back_main": [[{"text": "◀️ Главное меню", "callback_data": "start"}]],
    "back_about": [[{"text": "◀️ Назад", "callback_data": "about"}]],
    "back_entertainment": [[{"text": "◀️ Назад", "callback_data": "entertainment"}]],
    "back_routes": [[{"text": "◀️ Назад", "callback_data": "routes"}]],
}

MENU_MAP = {
    "start": ("welcome", "main"),
    "about": ("about", "about"),
    "romashka": ("romashka", "back_about"),
    "booking": ("booking", "back_main"),
    "feedback": ("feedback", "back_main"),
    "entertainment": (None, "entertainment"),
    "eat": ("eat", "back_entertainment"),
    "walk": ("walk", "back_entertainment"),
    "see": ("see", "back_entertainment"),
    "routes": (None, "routes"),
    "route_2h": ("route_2h", "back_routes"),
    "route_4h": ("route_4h", "back_routes"),
    "route_day": ("route_day", "back_routes"),
}

ENTERTAINMENT_TEXT = "🗺 *Развлечения*\n\nВыберите раздел:"
ROUTES_TEXT = "🧭 *Экскурсии*\n\nВыберите маршрут:"

def api_call(method, data):
    url = f"{API}/{method}"
    data_bytes = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"API error: {e}")
        return {}

def get_updates(offset=None):
    data = {"timeout": 30, "allowed_updates": ["message", "callback_query"]}
    if offset:
        data["offset"] = offset
    url = f"{API}/getUpdates"
    data_bytes = json.dumps(data).encode()
    req = urllib.request.Request(url, data=data_bytes, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=35) as r:
            return json.loads(r.read())
    except Exception as e:
        print(f"getUpdates error: {e}")
        return {"result": []}

def send_message(chat_id, text, keyboard_key):
    api_call("sendMessage", {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": {"inline_keyboard": KEYBOARDS[keyboard_key]}
    })

def edit_message(chat_id, message_id, text, keyboard_key):
    api_call("editMessageText", {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": text,
        "parse_mode": "Markdown",
        "reply_markup": {"inline_keyboard": KEYBOARDS[keyboard_key]}
    })

def answer_callback(callback_id):
    api_call("answerCallbackQuery", {"callback_query_id": callback_id})

def handle_update(update):
    if "message" in update:
        msg = update["message"]
        chat_id = msg["chat"]["id"]
        text = msg.get("text", "")
        if text == "/start":
            send_message(chat_id, TEXTS["welcome"], "main")

    elif "callback_query" in update:
        cq = update["callback_query"]
        chat_id = cq["message"]["chat"]["id"]
        message_id = cq["message"]["message_id"]
        data = cq["data"]
        answer_callback(cq["id"])

        if data in MENU_MAP:
            text_key, kb_key = MENU_MAP[data]
            if text_key is None:
                text = ENTERTAINMENT_TEXT if data == "entertainment" else ROUTES_TEXT
            else:
                text = TEXTS[text_key]
            edit_message(chat_id, message_id, text, kb_key)

def main():
    print("🌼 Бот Ромашка запущен!")
    offset = None
    while True:
        try:
            result = get_updates(offset)
            for update in result.get("result", []):
                offset = update["update_id"] + 1
                handle_update(update)
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(5)

if __name__ == "__main__":
    main()
