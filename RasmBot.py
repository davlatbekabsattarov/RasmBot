import requests
import asyncio
import logging
import sys
from aiogram.enums import ParseMode
from aiogram import Bot, Dispatcher, html
from aiogram.filters import CommandStart
from aiogram.types import Message
from aiogram import types


TOKEN = "7987999927:AAFWnRpM226hADJ_R307JigIApUhJAcE84k"
PIXABAY_API_KEY = "47447451-81b1be152c3dc058228477c90"

dp = Dispatcher()

# Function to get image URL from Pixabay API
def get_image_url(query):
    url = "https://pixabay.com/api/"
    params = {
        "key": PIXABAY_API_KEY,
        "q": query,
        "image_type": "photo",
        "per_page": 3 # You can set this to 1 or any number between 3 and 200
    }
    response = requests.get(url, params=params)

    # Log status code, response text, and JSON response for debugging
    logging.info(f"Status Code: {response.status_code}")
    logging.info(f"Response Text: {response.text}")

    # Try to parse JSON response
    try:
        data = response.json()
        logging.info(f"Pixabay API Response (JSON): {data}")

        if data['hits']:
            return data['hits'][0]['webformatURL']
        else:
            logging.info("No images found in the response.")
            return None
    except Exception as e:
        logging.error(f"Error parsing response JSON: {e}")
        return None

@dp.message(CommandStart())
async def command_start_handler(message: Message) -> None:
    await message.answer(f"Assalamu aleykum, <b>{message.from_user.full_name}</b>!\nQidirmoqchi bo'lgan rasmingizni kiriting:", parse_mode=ParseMode.HTML)

@dp.message()
async def image_sender(message: types.Message):
    try:
        # Get image URL
        image_url = get_image_url(message.text)

        if image_url:
            # Send the image
            await message.answer_photo(image_url)
        else:
            await message.answer("Bu mavzuga oid rasm topilmadi.")
    except Exception as e:
        # Handle other exceptions
        await message.answer(f"Yaxshi urunish! Xato: {str(e)}")

async def main() -> None:
    # Initialize Bot instance with default bot properties which will be passed to all API calls
    bot = Bot(token=TOKEN)
    # Run events dispatching
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, stream=sys.stdout)
    asyncio.run(main())
