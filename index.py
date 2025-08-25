import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.dispatcher.filters import Text
from datetime import datetime
import csv, os

BOT_TOKEN = "8175394476:AAFssZqu2_-aQxjHraecgNnQu2zHZW5Fmic"
ADMINS = [5469122433, 1173284868]
REQUIRED_CHANNELS = ["@protrader_fx24", "@protrader_competition"]
VIP_LINK = "https://t.me/+oABwUyodAkBjMzgy"

bot = Bot(token=BOT_TOKEN, parse_mode="HTML")
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)

main_menu = ReplyKeyboardMarkup(resize_keyboard=True)
main_menu.add("🔥 ProTrader V.I.P", "🏆 ProTrader Competition")
main_menu.add("💱 Valyuta Ayirboshlash", "📞 Support")
main_menu.add("📲 Ijtimoiy Tarmoqlar")

class PaymentState(StatesGroup):
    waiting_for_check = State()

async def check_subscription(user_id):
    for ch in REQUIRED_CHANNELS:
        try:
            member = await bot.get_chat_member(chat_id=ch, user_id=user_id)
            if member.status not in ["member", "administrator", "creator"]:
                return False
        except:
            return False
    return True

@dp.message_handler(commands=['start'])
async def start_handler(message: types.Message):
    if not await check_subscription(message.from_user.id):
        markup = InlineKeyboardMarkup(row_width=1)
        for ch in REQUIRED_CHANNELS:
            markup.add(InlineKeyboardButton("➕ Kanalga qo‘shilish", url=f"https://t.me/{ch.strip('@')}"))
        markup.add(InlineKeyboardButton("✅ A’zo bo‘ldim", callback_data="check_subs"))
        await message.answer("🔐 Botdan foydalanish uchun quyidagi kanallarga obuna bo‘ling:", reply_markup=markup)
        return

    user_id = message.from_user.id
    full_name = message.from_user.full_name
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    try:
        with open("users.csv", "a", encoding="utf-8", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([user_id, full_name, now])
    except:
        pass
    await message.answer(f"👋 <b>Salom, {full_name}!</b>\nQuyidagi menyudan tanlang:", reply_markup=main_menu)

@dp.callback_query_handler(lambda c: c.data == "check_subs")
async def recheck(call: types.CallbackQuery):
    if await check_subscription(call.from_user.id):
        await call.message.answer("✅ Obuna tekshirildi. Botdan foydalanishingiz mumkin.", reply_markup=main_menu)
    else:
        await call.message.answer("❌ Hali ham obuna bo‘lmagansiz. Iltimos, yuqoridagi kanallarga qo‘shiling.")

@dp.message_handler(lambda msg: msg.text == "💱 Valyuta Ayirboshlash")
async def exchange_handler(msg: types.Message):
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("👨‍💻 Admin bilan aloqa", url="https://t.me/Protrader_admin1")
    )
    await msg.answer("💱 <b>Valyuta ayirboshlash xizmati:</b>\n\n🛠 Tez orada ishga tushadi.", reply_markup=markup)

@dp.message_handler(lambda msg: msg.text == "📞 Support")
async def support_handler(msg: types.Message):
    await msg.answer("📞 <b>Admin bilan bog‘lanish:</b> @Protrader_admin1")

@dp.message_handler(lambda msg: msg.text == "📲 Ijtimoiy Tarmoqlar")
async def social_handler(msg: types.Message):
    btn = InlineKeyboardMarkup(row_width=2)
    btn.add(
        InlineKeyboardButton("📸 Instagram", url="https://www.instagram.com/protrader.24?igsh=bWhhd2xuaWh5MGo5"),
        InlineKeyboardButton("🐦 Twitter (X)", url="https://x.com/k_rustamjonov?t=Hk84rHkBwN-HqYfyINsQdQ&s=35")
    )
    btn.add(
        InlineKeyboardButton("▶️ YouTube", url="https://youtube.com/@protrader_frx?si=DuR2U8-2sKqDyVHN"),
        InlineKeyboardButton("✈️ Telegram", url="https://t.me/protrader_fx24")
    )
    await msg.answer("📲 Bizning ijtimoiy tarmoqlarimiz:", reply_markup=btn)
vip_menu = ReplyKeyboardMarkup(resize_keyboard=True)
vip_menu.add("📅 Oylik Obuna", "♾️ Doimiy Obuna").add("⬅️ Ortga")

@dp.message_handler(lambda msg: msg.text == "🔥 ProTrader V.I.P")
async def vip_handler(msg: types.Message):
    await msg.answer("💼 V.I.P obuna turini tanlang:", reply_markup=vip_menu)

@dp.message_handler(Text(equals=["📅 Oylik Obuna", "♾️ Doimiy Obuna"]))
async def vip_type_handler(msg: types.Message, state: FSMContext):
    if msg.text == "📅 Oylik Obuna":
        narx = "💰 Narx: $29.99"
        await state.update_data(payment_type="vip")
    else:
        narx = "💰 Narx: $99.99"
        await state.update_data(payment_type="vip")
    markup = InlineKeyboardMarkup().add(
        InlineKeyboardButton("💳 HUMO", callback_data="vip_humo"),
        InlineKeyboardButton("💸 USDT", callback_data="vip_usdt")
    )
    await msg.answer(f"{narx}\n\nTo‘lov turini tanlang:", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data in ["vip_humo", "vip_usdt"])
async def vip_payment_method(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(payment_type="vip")
    if call.data == "vip_humo":
        text = "💳 HUMO karta: <code>9860350118370674</code>\nIsm: Ismoilov Muhammadjon"
    else:
        text = "💸 USDT (TRC20): <code>TQunwPCV8whte8bp7o5AAyJmjciKpVB7zw</code>"
    markup = InlineKeyboardMarkup().add(InlineKeyboardButton("✅ To‘lov qildim", callback_data="send_check"))
    await call.message.answer(f"{text}\n\nTo‘lovni amalga oshirgach, quyidagi tugmani bosing:", reply_markup=markup)

@dp.callback_query_handler(lambda c: c.data == "send_check")
async def request_check(call: types.CallbackQuery, state: FSMContext):
    await call.message.answer("📎 To‘lov chekini yuboring (foto yoki PDF):")
    await PaymentState.waiting_for_check.set()
    await state.update_data(user_id=call.from_user.id)

@dp.message_handler(content_types=[types.ContentType.PHOTO, types.ContentType.DOCUMENT], state=PaymentState.waiting_for_check)
async def handle_check(msg: types.Message, state: FSMContext):
    data = await state.get_data()
    user_id = data.get("user_id")
    pay_type = data.get("payment_type", "vip")

    for admin in ADMINS:
        try:
            caption = f"🧾 Yangi to‘lov cheki:\n👤 ID: <code>{user_id}</code>\n📦 Turi: {pay_type}\nTasdiqlash: /tasdiqla {user_id} {pay_type}"
            if msg.content_type == types.ContentType.PHOTO:
                await bot.send_photo(admin, msg.photo[-1].file_id, caption=caption)
            else:
                await bot.send_document(admin, msg.document.file_id, caption=caption)
        except Exception as e:
            print("Adminlarga yuborishda xato:", e)
    await msg.answer("✅ Chekingiz adminga yuborildi. Tez orada javob beramiz.")
    await state.finish()

@dp.message_handler(commands=['tasdiqla'])
async def confirm_payment(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return
    parts = msg.text.strip().split()
    if len(parts) != 3:
        await msg.reply("❗ Format: /tasdiqla <user_id> <vip|competition>")
        return
    user_id = int(parts[1])
    mode = parts[2].lower()
    if mode == "vip":
        await bot.send_message(user_id, f"✅ To‘lovingiz tasdiqlandi!\nSizga V.I.P kanal manzili:\n{VIP_LINK}")
        await msg.reply("✅ V.I.P foydalanuvchiga link yuborildi.")
    elif mode == "competition":
        await bot.send_message(user_id, "✅ To‘lovingiz tasdiqlandi!\nIltimos, musobaqa tafsilotlari uchun admin bilan bog‘laning.")
        await msg.reply("✅ Competition foydalanuvchiga tasdiq xabari yuborildi.")

# === Competition ===
@dp.message_handler(lambda msg: msg.text == "🏆 ProTrader Competition")
async def competition_handler(msg: types.Message):
    btn = InlineKeyboardMarkup()
    btn.add(InlineKeyboardButton("📘 Musobaqa haqida", callback_data="comp_info"))
    btn.add(InlineKeyboardButton("🎁 Musobaqa sovrini", callback_data="comp_prize"))
    btn.add(InlineKeyboardButton("🚀 Musobaqada qatnashish", callback_data="comp_join"))
    await msg.answer("🏆 <b>ProTrader Competition:</b>\nTanlang:", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data == "comp_info")
async def comp_info(call: types.CallbackQuery):
    await call.message.answer(
        "⚠️<b>Qoida va shartlar:</b>\n"
        "1)🟠Competitionda qatnashish mutlaqo bepul, ammo balansingizni o'zingiz to'ldirasiz\n"
        "2)🟠Balans faqat 1 marta beriladi, ya'ni 15$\n"
        "3)🟠Bozorda ishlash uchun hech qanday shart yo'q (razgon, short trade, long trade)\n"
        "4)🟠Har qanday signal kanallardan foydalanish mumkin\n"
        "5)🟠Savdoga kirish uchun maksimum lot belgilanmagan\n"
        "6)🟠Agar g‘olib bo‘la olmasangiz balansingiz qaytariladi (agar 10$dan ko‘p bo‘lsa)"
    )

@dp.callback_query_handler(lambda c: c.data == "comp_prize")
async def comp_prize(call: types.CallbackQuery):
    await call.message.answer(
        "🎁 <b>Musobaqaning sovrini:</b>\n"
        "1) 500$+ balans\n"
        "2) Barcha ishtirokchilarning foydalari hamda qoʻshimcha +30$ pul mukofoti\n"
        "3) ProTrader V.I.P uchun Doimiy taʼrifga 30%lik, Oylik taʼrifiga esa 5% chegirma"
    )

@dp.callback_query_handler(lambda c: c.data == "comp_join")
async def comp_join(call: types.CallbackQuery, state: FSMContext):
    btn = InlineKeyboardMarkup().add(InlineKeyboardButton("💰 Balansni to‘ldirish", callback_data="comp_pay"))
    await state.update_data(payment_type="competition")
    await call.message.answer("🚀 <b>Musobaqada qatnashish uchun iltimos balansingizni 15$ga to‘ldiring</b>\n(1$ = 13 000 so‘m)", reply_markup=btn)

@dp.callback_query_handler(lambda c: c.data == "comp_pay")
async def comp_payment(call: types.CallbackQuery, state: FSMContext):
    await state.update_data(payment_type="competition")
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton("💳 HUMO", callback_data="vip_humo"))
    markup.add(InlineKeyboardButton("💸 USDT", callback_data="vip_usdt"))
    await call.message.answer("💳 Balansni to‘ldirish uchun to‘lov turini tanlang:", reply_markup=markup)
@dp.message_handler(commands=['admin'])
async def admin_panel(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        await msg.answer("❌ Siz admin emassiz.")
        return
    kb = ReplyKeyboardMarkup(resize_keyboard=True).add("📊 Statistika", "📥 CSV ni yuklash").add("⬅️ Ortga")
    await msg.answer("⚙️ Admin paneliga xush kelibsiz:", reply_markup=kb)

@dp.message_handler(lambda msg: msg.text == "📊 Statistika")
async def stats_handler(msg: types.Message):
    if msg.from_user.id not in ADMINS:
        return
    try:
        total_users = 0
        today_users = 0
        with open("users.csv", encoding="utf-8") as f:
            for row in csv.reader(f):
                total_users += 1
                if datetime.now().strftime("%Y-%m-%d") in row[2]:
                    today_users += 1
        await msg.answer(f"📊 Statistika:\n👥 Umumiy foydalanuvchilar: {total_users}\n🆕 Bugungi foydalanuvchilar: {today_users}")
    except Exception as e:
        await msg.answer(f"Xatolik yuz berdi: {e}")

@dp.message_handler(lambda msg: msg.text == "📥 CSV ni yuklash")
async def send_csv(msg: types.Message):
    if msg.from_user.id in ADMINS and os.path.exists("users.csv"):
        await bot.send_document(msg.chat.id, types.InputFile("users.csv"))
    else:
        await msg.answer("❗ Fayl topilmadi yoki siz admin emassiz.")

@dp.message_handler(lambda msg: msg.text == "⬅️ Ortga")
async def back_to_menu(msg: types.Message):
    await msg.answer("🏠 Asosiy menyu:", reply_markup=main_menu)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
