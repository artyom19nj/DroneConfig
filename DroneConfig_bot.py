from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

BOT_TOKEN = "8234047242:AAEOA0hB1CKe9niXifIq5snhc2xXlMbZzIk"

frames = {
    "TBS Source One V5": {"price": 4500, "weight": 120, "material": "карбон"},
    "iFlight XL5 V5": {"price": 5000, "weight": 130, "material": "карбон"},
    "DJI F450": {"price": 3000, "weight": 200, "material": "пластик"},
}

propellers = {
    "Gemfan 51466": {"price": 500, "weight": 20, "material": "пластик"},
    "HQProp Ethix P5": {"price": 600, "weight": 22, "material": "пластик"},
}

batteries = {
    "CNHL 1500mAh 4S": {"price": 3000, "flight_time": 10},
    "Li-Ion 3000mAh": {"price": 800, "flight_time": 15},
}

chips = {
    "Mamba F405": {"price": 5000},
    "Holybro F7": {"price": 8000},
}

cameras = {
    "RunCam Nano 3": {"price": 3500, "resolution": "1080p"},
    "Foxeer Predator": {"price": 7500, "resolution": "4K"},
}

STEPS = [
    ("frame", frames, "🧱 Выберите раму"),
    ("prop", propellers, "🌀 Выберите пропеллеры"),
    ("bat", batteries, "🔋 Выберите батарею"),
    ("chip", chips, "🖥️ Выберите контроллер"),
    ("cam", cameras, "📷 Выберите камеру"),
]

def build_keyboard(data, prefix):
    keyboard = []
    for i, name in enumerate(data):
        keyboard.append(
            [InlineKeyboardButton(name, callback_data=f"{prefix}_{i}")]
        )
    keyboard.append([InlineKeyboardButton("🏠 Главное меню", callback_data="main")])
    return InlineKeyboardMarkup(keyboard)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["step"] = 0

    step_key, data, title = STEPS[0]
    context.user_data[step_key] = data

    await update.message.reply_text(
        title,
        reply_markup=build_keyboard(data, step_key)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main":
        await start(update, context)
        return

    step = context.user_data.get("step", 0)

    step_key, step_data, _ = STEPS[step]

    if not data.startswith(step_key):
        await query.edit_message_text("Ошибка выбора")
        return

    index = int(data.split("_")[1])
    selected_name = list(step_data.keys())[index]

    context.user_data[step_key + "_selected"] = selected_name
    context.user_data["step"] += 1

    if context.user_data["step"] < len(STEPS):
        next_step_key, next_data, next_title = STEPS[context.user_data["step"]]
        await query.edit_message_text(
            next_title,
            reply_markup=build_keyboard(next_data, next_step_key)
        )
        return

    f = frames[context.user_data["frame_selected"]]
    p = propellers[context.user_data["prop_selected"]]
    b = batteries[context.user_data["bat_selected"]]
    c = chips[context.user_data["chip_selected"]]
    cam = cameras[context.user_data["cam_selected"]]

    total_price = f["price"] + p["price"] + b["price"] + c["price"] + cam["price"]
    total_weight = f["weight"] + p["weight"]

    text = (
        "🚁 <b>Ваш дрон собран!</b>\n\n"
        f"💰 Цена: <b>{total_price} ₽</b>\n"
        f"⚖️ Вес: <b>{total_weight} г</b>\n"
        f"⏱️ Полёт: <b>{b['flight_time']} мин</b>\n\n"
        f"🧱 Рама: {context.user_data['frame_selected']} ({f['material']})\n"
        f"🌀 Пропеллеры: {context.user_data['prop_selected']} ({p['material']})\n"
        f"🔋 Батарея: {context.user_data['bat_selected']}\n"
        f"🖥️ Контроллер: {context.user_data['chip_selected']}\n"
        f"📷 Камера: {context.user_data['cam_selected']} ({cam['resolution']})"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔄 Собрать заново", callback_data="main")]
        ])
    )

if name == "main":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(button))
    print("Бот запущен...")
    app.run_polling()