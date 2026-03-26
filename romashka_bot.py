import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

TOKEN = "8627593181:AAGYyoflhrj65lkBroy89tHfc8QmcgNgRQI"
logging.basicConfig(level=logging.INFO)

TEXTS = {
    "welcome": "🌼 *Добро пожаловать в Апартаменты Ромашка!*\n\nЭтот бот — ваш личный путеводитель по гостинице и Петербургу.\n\nВыберите раздел:",
    "about": "🏛 *Апартаменты Ромашка*\n\n📍 *Адрес:* ул. Ломоносова, 14\n🚇 *Метро:* Владимирская, Достоевская, Звенигородская\n📞 *Телефон:* +7 906 274\\-16\\-09\n🌐 romashkarooms\\.ru\n\nУ нас 4 уникальных номера — Берёзки, Одуванчик, Буфет и Люстра\\. В каждом — кухня, ванная, до 4 гостей\\.",
    "romashka": "🌼 *Парадная Ромашка*\n\nПрямо в вашем доме — одна из самых известных парадных Петербурга\\.\n\nЖёлтые стены и белая лепнина напоминают ромашку — отсюда и название\\. В центре — историческая шахта *первого парового лифта Петербурга*\\. Кованые решётки, мозаичный пол — всё с 1892 года\\.\n\nСюда приезжают со всей страны\\. А вы живёте внутри этой истории\\. 🦢",
    "booking": "📅 *Бронирование*\n\nЗабронируйте напрямую — без комиссии:\n\n🌐 [romashkarooms\\.ru](https://romashkarooms.ru)\n\n📞 \\+7 906 274\\-16\\-09\n\nТакже на площадках:\n• Суточно\\.ру\n• Островок\n• Яндекс Путешествия",
    "feedback": "💬 *Обратная связь*\n\n⭐ [Оставить отзыв на Яндекс Картах](https://yandex.ru/maps/org/103931315029/reviews/)\n\n📞 Администратор: \\+7 906 274\\-16\\-09\n\nЕсли что\\-то пошло не так — сообщите нам сразу\\. Мы всегда готовы помочь\\! 🌼",
    "eat": "🍽 *Поесть рядом*\n\n☕ *Кофе и завтраки*\n• Буше — Садовая, 2 \\(5 мин\\)\n• Кофе 22 — Ломоносова, 22\n\n🍜 *Обед и ужин*\n• Шаурма на Пяти углах — культовое место\n• Рубинштейна, 15 — улица ресторанов\n• Пробка — Белинского, 5\n\n🛵 *Доставка*\nЯндекс Еда, Самокат работают в нашем районе",
    "walk": "🚶 *Погулять*\n\n🌊 *Набережные*\n• Фонтанка — 2 мин\n• Мост Ломоносова — у дома\n• Набережная Мойки — 15 мин\n\n🌳 *Парки*\n• Михайловский сад — 15 мин\n• Летний сад — 20 мин\n\n📸 *Для фото*\n• Пять углов — за углом\n• Парадная Ромашка — у вас дома 🌼",
    "see": "👁 *Посмотреть*\n\n🏛 *Музеи*\n• Русский музей — 15 мин\n• Музей Достоевского — 10 мин\n• Музей Фаберже — 20 мин\n\n⛪ *Архитектура*\n• Спас\\-на\\-Крови — 20 мин\n• Казанский собор — 20 мин\n• Аничков мост — 10 мин\n\n🎭 *Театры*\n• БДТ — 10 мин\n• Александринский — 15 мин",
    "route_2h": "🧭 *Маршрут на 2 часа*\n_«Сердце старого Петербурга»_\n\n1️⃣ *Парадная Ромашка* — старт 🌼\n2️⃣ *Мост Ломоносова* — 2 мин\n3️⃣ *Набережная Фонтанки* — прогулка\n4️⃣ *Аничков мост* — кони Клодта\n5️⃣ *Невский проспект*\n6️⃣ *Казанский собор* — вход бесплатный\n\n🔙 Обратно по Садовой\n\n_~4 км, 2 часа_",
    "route_4h": "🧭 *Маршрут на 4 часа*\n_«От Фонтанки до Дворцовой»_\n\n1️⃣ *Пять углов* — старт\n2️⃣ *Рубинштейна* — кофе\n3️⃣ *Михайловский замок*\n4️⃣ *Михайловский сад*\n5️⃣ *Спас\\-на\\-Крови*\n6️⃣ *Русский музей*\n7️⃣ *Невский проспект*\n8️⃣ *Дворцовая площадь*\n\n_~7 км, 4 часа_",
    "route_day": "🧭 *Целый день*\n_«Большой Петербург»_\n\n🌅 *Утро*\n• Завтрак на Рубинштейна\n• Эрмитаж \\(с 10:30\\)\n\n☀️ *День*\n• Петропавловская крепость\n• Кронверкский проспект\n\n🌆 *Вечер*\n• Казанский собор\n• Ужин на Думской\n\n🌉 *Ночью летом*\n• Развод мостов — Дворцовый в 1:10\n\n_12\\-14 часов, лучший день в Петербурге_ 🌼",
}

def main_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🏛 О гостинице", callback_data="about"),
         InlineKeyboardButton("📅 Бронирование", callback_data="booking")],
        [InlineKeyboardButton("🗺 Развлечения", callback_data="entertainment"),
         InlineKeyboardButton("💬 Обратная связь", callback_data="feedback")],
    ])

def about_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🌼 Парадная Ромашка", callback_data="romashka")],
        [InlineKeyboardButton("◀️ Главное меню", callback_data="start")],
    ])

def entertainment_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🍽 Поесть", callback_data="eat"),
         InlineKeyboardButton("🚶 Погулять", callback_data="walk")],
        [InlineKeyboardButton("👁 Посмотреть", callback_data="see"),
         InlineKeyboardButton("🧭 Экскурсии", callback_data="routes")],
        [InlineKeyboardButton("◀️ Главное меню", callback_data="start")],
    ])

def routes_menu():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("⏱ 2 часа", callback_data="route_2h")],
        [InlineKeyboardButton("🕓 4 часа", callback_data="route_4h")],
        [InlineKeyboardButton("🌅 Целый день", callback_data="route_day")],
        [InlineKeyboardButton("◀️ Назад", callback_data="entertainment")],
    ])

def back(target):
    return InlineKeyboardMarkup([[InlineKeyboardButton("◀️ Назад", callback_data=target)]])

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(TEXTS["welcome"], parse_mode="MarkdownV2", reply_markup=main_menu())

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    d = query.data

    if d == "start":
        await query.edit_message_text(TEXTS["welcome"], parse_mode="MarkdownV2", reply_markup=main_menu())
    elif d == "about":
        await query.edit_message_text(TEXTS["about"], parse_mode="MarkdownV2", reply_markup=about_menu())
    elif d == "romashka":
        await query.edit_message_text(TEXTS["romashka"], parse_mode="MarkdownV2", reply_markup=back("about"))
    elif d == "booking":
        await query.edit_message_text(TEXTS["booking"], parse_mode="MarkdownV2", reply_markup=back("start"))
    elif d == "feedback":
        await query.edit_message_text(TEXTS["feedback"], parse_mode="MarkdownV2", reply_markup=back("start"))
    elif d == "entertainment":
        await query.edit_message_text("🗺 *Развлечения*\n\nВыберите раздел:", parse_mode="MarkdownV2", reply_markup=entertainment_menu())
    elif d == "eat":
        await query.edit_message_text(TEXTS["eat"], parse_mode="MarkdownV2", reply_markup=back("entertainment"))
    elif d == "walk":
        await query.edit_message_text(TEXTS["walk"], parse_mode="MarkdownV2", reply_markup=back("entertainment"))
    elif d == "see":
        await query.edit_message_text(TEXTS["see"], parse_mode="MarkdownV2", reply_markup=back("entertainment"))
    elif d == "routes":
        await query.edit_message_text("🧭 *Экскурсии*\n\nВыберите маршрут:", parse_mode="MarkdownV2", reply_markup=routes_menu())
    elif d == "route_2h":
        await query.edit_message_text(TEXTS["route_2h"], parse_mode="MarkdownV2", reply_markup=back("routes"))
    elif d == "route_4h":
        await query.edit_message_text(TEXTS["route_4h"], parse_mode="MarkdownV2", reply_markup=back("routes"))
    elif d == "route_day":
        await query.edit_message_text(TEXTS["route_day"], parse_mode="MarkdownV2", reply_markup=back("routes"))

def main():
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CallbackQueryHandler(button))
    print("🌼 Бот Ромашка запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
