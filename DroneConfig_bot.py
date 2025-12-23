from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes

BOT_TOKEN = "8234047242:AAEOA0hB1CKe9niXifIq5snhc2xXlMbZzIk"

frames = {
    "TBS Source One V5": {"price": 4500, "weight": 120, "material": "карбон"},
    "iFlight XL5 V5": {"price": 5000, "weight": 130, "material": "карбон"},
    "DJI F450": {"price": 3000, "weight": 200, "material": "пластик"},
    "AOS 5 O3": {"price": 7500, "weight": 140, "material": "карбон"},
    "Tarot Iron Man 650": {"price": 6500, "weight": 300, "material": "карбон"},
    "Eachine Tyro79": {"price": 2000, "weight": 80, "material": "пластик"},
    "BetaFPV Meteor65": {"price": 1500, "weight": 20, "material": "пластик"},
    "DIY Plywood Frame": {"price": 1000, "weight": 180, "material": "фанера"},
    "Armattan Marmotte": {"price": 5600, "weight": 125, "material": "карбон"},
    "iFlight Chimera7": {"price": 8500, "weight": 210, "material": "карбон"},
}

propellers = {
    "Gemfan 51466": {"price": 500, "weight": 20, "material": "пластик"},
    "HQProp Ethix P5": {"price": 600, "weight": 22, "material": "пластик"},
    "T-Motor T5143": {"price": 1500, "weight": 25, "material": "пластик"},
    "iFlight Nazgul Carbon": {"price": 2000, "weight": 15, "material": "карбон"},
    "Dalprop Cyclone T5046C": {"price": 800, "weight": 21, "material": "пластик"},
    "KingKong 5040": {"price": 400, "weight": 19, "material": "пластик"},
    "Azure Power 5140": {"price": 700, "weight": 20, "material": "пластик"},
    "Gemfan Flash 5552": {"price": 1200, "weight": 24, "material": "пластик"},
    "HQProp DP 5x4.3x3 V1S": {"price": 650, "weight": 22, "material": "пластик"},
    "Gemfan D76 5 blades": {"price": 1800, "weight": 18, "material": "карбон"},
}

batteries = {
    "CNHL 1500mAh 4S": {"price": 3000, "flight_time": 10},
    "Tattu R-Line V5.0 1300mAh 6S": {"price": 5000, "flight_time": 8},
    "GNB 1100mAh 4S": {"price": 3500, "flight_time": 9},
    "18650 Li-Ion 3000mAh": {"price": 800, "flight_time": 15},
    "Tattu LiHV 1550mAh 4S": {"price": 4000, "flight_time": 11},
    "Bonka Power 1800mAh 4S": {"price": 4200, "flight_time": 12},
    "Infinity Graphene 1500mAh 6S": {"price": 4700, "flight_time": 9},
    "Ovonic 2200mAh 4S": {"price": 3200, "flight_time": 14},
    "GensAce 1300mAh 6S": {"price": 4900, "flight_time": 10},
}

chips = {
    "Mamba F405": {"price": 5000},
    "Holybro F7": {"price": 8000},
    "Holybro Durandal H7": {"price": 14000},
    "SpeedyBee F7 V3": {"price": 7500},
    "Foxeer F722 V2": {"price": 6800},
    "Omnibus F4 Pro": {"price": 4000},
    "CL Racing F7": {"price": 6200},
}

cameras = {
    "RunCam Nano 3": {"price": 3500, "resolution": "1080p"},
    "Foxeer Predator": {"price": 7500, "resolution": "4K"},
    "Caddx Vista": {"price": 4000, "resolution": "720p"},
    "DJI FPV Camera": {"price": 6000, "resolution": "1080p"},
    "GoPro HERO8": {"price": 20000, "resolution": "4K"},
    "Mobius ActionCam": {"price": 4500, "resolution": "1080p"},
}

STEPS = [
    ("frame", frames, "🧩 Выберите раму"),
    ("prop", propellers, "🧿 Выберите пропеллеры"),
    ("bat", batteries, "🔋 Выберите аккумулятор"),
    ("chip", chips, "🖥 Выберите полётный контроллер"),
    ("cam", cameras, "📸 Выберите камеру"),
]

def build_keyboard(data, prefix, step):
    keyboard = [
        [InlineKeyboardButton(name, callback_data=f"{prefix}_{i}")]
        for i, name in enumerate(data)
    ]
    nav = []
    if step > 0:
        nav.append(InlineKeyboardButton("⬅️ Назад", callback_data="back"))
    nav.append(InlineKeyboardButton("🏠 Меню", callback_data="main"))
    keyboard.append(nav)
    return InlineKeyboardMarkup(keyboard)

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    kb = InlineKeyboardMarkup([
        [InlineKeyboardButton("🚁 Собрать FPV-дрон", callback_data="build")],
        [InlineKeyboardButton("ℹ️ О боте", callback_data="about")]
    ])
    text = (
        "👋 <b>FPV Builder Bot</b>\n\n"
        "Интерактивный подбор компонентов FPV-дрона.\n"
        "Посчитаем цену, вес и время полёта."
    )
    if update.message:
        await update.message.reply_text(text, parse_mode="HTML", reply_markup=kb)
    else:
        await update.callback_query.edit_message_text(text, parse_mode="HTML", reply_markup=kb)

async def start_build(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data.clear()
    context.user_data["step"] = 0
    step_key, data, title = STEPS[0]
    await update.callback_query.edit_message_text(
        title,
        reply_markup=build_keyboard(data, step_key, 0)
    )

async def button(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "main":
        await show_main_menu(update, context)
        return

    if data == "about":
        await query.edit_message_text(
            "ℹ️ <b>FPV Builder Bot</b>\n\nПошаговый конструктор FPV-дронов.",
            parse_mode="HTML",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("🏠 Меню", callback_data="main")]
            ])
        )
        return

    if data == "build":
        await start_build(update, context)
        return

    if data == "back":
        context.user_data["step"] -= 1
        step = context.user_data["step"]
        step_key, step_data, title = STEPS[step]
        await query.edit_message_text(
            title,
            reply_markup=build_keyboard(step_data, step_key, step)
        )
        return

    step = context.user_data.get("step", 0)
    step_key, step_data, _ = STEPS[step]

    if not data.startswith(step_key):
        await show_main_menu(update, context)
        return

    index = int(data.split("_")[1])
    context.user_data[f"{step_key}_selected"] = list(step_data.keys())[index]
    context.user_data["step"] += 1

    if context.user_data["step"] < len(STEPS):
        step = context.user_data["step"]
        next_key, next_data, next_title = STEPS[step]
        await query.edit_message_text(
            next_title,
            reply_markup=build_keyboard(next_data, next_key, step)
        )
        return

    f = frames[context.user_data["frame_selected"]]
    p = propellers[context.user_data["prop_selected"]]
    b = batteries[context.user_data["bat_selected"]]
    c = chips[context.user_data["chip_selected"]]
    cam = cameras[context.user_data["cam_selected"]]

    total_price = sum(x["price"] for x in (f, p, b, c, cam))
    total_weight = f["weight"] + p["weight"]

    text = (
        "🛠 <b>ДРОН СОБРАН</b>\n\n"
        f"💰 Цена: <b>{total_price} ₽</b>\n"
        f"⚖️ Вес: <b>{total_weight} г</b>\n"
        f"⏱ Полёт: <b>{b['flight_time']} мин</b>\n\n"
        "📦 <b>Комплектация:</b>\n"
        f"• {context.user_data['frame_selected']}\n"
        f"• {context.user_data['prop_selected']}\n"
        f"• {context.user_data['bat_selected']}\n"
        f"• {context.user_data['chip_selected']}\n"
        f"• {context.user_data['cam_selected']}"
    )

    await query.edit_message_text(
        text,
        parse_mode="HTML",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("🔁 Собрать ещё", callback_data="build")],
            [InlineKeyboardButton("🏠 Меню", callback_data="main")]
        ])
    )

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", show_main_menu))
    app.add_handler(CallbackQueryHandler(button))
    print("Бот запущен...")
    app.run_polling()