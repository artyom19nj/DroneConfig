import asyncio
from telegram import (
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Update
)
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    CallbackQueryHandler,
    ContextTypes
)

TOKEN = "8234047242:AAEOA0hB1CKe9niXifIq5snhc2xXlMbZzIk"

frames = {
    "TBS Source One V5": {"price": 4500, "weight": 120, "material": "карбон"},
    "iFlight XL5 V5": {"price": 5000, "weight": 130, "material": "карбон"},
    "AOS 5 O3": {"price": 7500, "weight": 140, "material": "карбон"},
    "DJI F450": {"price": 3000, "weight": 200, "material": "пластик"}
}

propellers = {
    "Gemfan 51466": {"price": 500, "weight": 20, "material": "пластик"},
    "HQProp Ethix P5": {"price": 600, "weight": 22, "material": "пластик"},
    "Gemfan Carbon": {"price": 1800, "weight": 18, "material": "карбон"}
}

batteries = {
    "CNHL 1500mAh 4S": {"price": 3000, "flight_time": 10},
    "Tattu 1300mAh 6S": {"price": 5000, "flight_time": 8},
    "Li-Ion 3000mAh": {"price": 800, "flight_time": 15}
}

chips = {
    "Mamba F405": {"price": 5000},
    "Holybro F7": {"price": 8000}
}

cameras = {
    "RunCam Nano 3": {"price": 3500, "resolution": "1080p"},
    "Foxeer Predator": {"price": 7500, "resolution": "4K"}
}

def make_keyboard(data: dict, prefix: str):
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(text=name, callback_data=f"{prefix}|{name}")]
        for name in data
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    await update.message.reply_text(
        "🚁 *Конфигуратор FPV-дрона*\n\nВыберите раму:",
        reply_markup=make_keyboard(frames, "frame"),
        parse_mode="Markdown"
    )

async def callbacks(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    prefix, value = query.data.split("|", 1)

    if prefix == "frame":
        context.user_data["frame"] = value
        await query.edit_message_text(
            "🌀 Выберите пропеллеры:",
            reply_markup=make_keyboard(propellers, "prop")
        )

    elif prefix == "prop":
        context.user_data["prop"] = value
        await query.edit_message_text(
            "🔋 Выберите батарею:",
            reply_markup=make_keyboard(batteries, "bat")
        )

    elif prefix == "bat":
        context.user_data["bat"] = value
        await query.edit_message_text(
            "🖥️ Выберите контроллер:",
            reply_markup=make_keyboard(chips, "chip")
        )

    elif prefix == "chip":
        context.user_data["chip"] = value
        await query.edit_message_text(
            "📷 Выберите камеру:",
            reply_markup=make_keyboard(cameras, "cam")
        )

    elif prefix == "cam":
        context.user_data["cam"] = value

        f = frames[context.user_data["frame"]]
        p = propellers[context.user_data["prop"]]
        b = batteries[context.user_data["bat"]]
        c = chips[context.user_data["chip"]]
        cam = cameras[value]

        total_price = f["price"] + p["price"] + b["price"] + c["price"] + cam["price"]
        total_weight = f["weight"] + p["weight"]

        text = (
            "🚁 *Ваш дрон собран!*\n\n"
            f"💰 Цена: *{total_price} ₽*\n"
            f"⚖️ Вес (рама + пропы): *{total_weight} г*\n"
            f"⏱️ Время полёта: *{b['flight_time']} мин*\n\n"
            f"🧱 Рама: {context.user_data['frame']} ({f['material']})\n"
            f"🌀 Пропеллеры: {context.user_data['prop']} ({p['material']})\n"
            f"🔋 Батарея: {context.user_data['bat']}\n"
            f"🖥️ Контроллер: {context.user_data['chip']}\n"
            f"📷 Камера: {value} ({cam['resolution']})"
        )

        await query.edit_message_text(text, parse_mode="Markdown")

async def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callbacks))

    await app.run_polling()

if __name__ == "__main__":
    asyncio.run(main())