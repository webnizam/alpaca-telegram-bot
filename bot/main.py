import nest_asyncio
import asyncio
from telebot.async_telebot import AsyncTeleBot
import socketio
from decouple import config
import time

TELEGRAM_KEY = config("TELEGRAM_KEY")
DALAI_HOST = "http://dalai"
DALAI_PORT = 3000

nest_asyncio.apply()


bot = AsyncTeleBot(TELEGRAM_KEY)
sio = socketio.AsyncClient()
msg = None
content = ""
chat_id = None
msg_id = None


@sio.on("result")
async def on_message(data):
    global content
    global chat_id
    ctn = content + data["response"]
    content = ctn
    try:
        if len(content.split("AI:")) > 2:
            message_ = content.split("AI:")[-1].replace("<end>", "")
            if message_:
                await bot.edit_message_text(message_, chat_id, msg_id)
            if data["response"].lower() == "user:":
                await sio.emit("request", {"prompt": "/stop"})
    except Exception as e:
        print(e)

    if data["response"].strip() == "<end>":
        content = ""
        await sio.emit("request", {"prompt": "/stop"})


@sio.event
def connect():
    print("I'm connected!")


@sio.event
def connect_error(data):
    print("The connection failed!")


@sio.event
def disconnect():
    print("I'm disconnected!")


model_name = "alpaca.7B"

config = {
    "seed": -1,
    "threads": 4,
    "n_predict": 40,
    "top_k": 40,
    "top_p": 0.9,
    "temp": 0.1,
    "repeat_last_n": 64,
    "repeat_penalty": 1.3,
    "debug": False,
    "models": ["alpaca.7B", "alpaca.13B"],
    "model": model_name,
    "prompt": "",
    "id": None,
}

history = []
prompt = """Below is a dialog, where User interacts with AI. AI is helpful, \
    kind, obedient,honest, and knows its own limits.
\n
Instruction\n
Write the last AI response to complete the dialog.\n

Dialog\n
User: Hello, AI.\n
AI: Hello! How can I assist you today?\n
User: ><PROMPT>

Response\n
AI:"""


@bot.message_handler(commands=["start", "help"])
async def send_welcome(message):
    bot.reply_to(message, "Howdy, how are you doing?")


@bot.message_handler(func=lambda message: True)
async def reply_with_llama(message):
    print(message.text)

    if "set:" in message.text.lower():
        global model_name
        if message.text.split(":")[1].lower() == "13b":
            model_name = "alpaca.13B"
        else:
            model_name = "alpaca.7B"
        config["model"] = model_name
        await bot.send_message(message.chat.id, f"Model set to {model_name}")
        return

    msg_ = await bot.send_message(message.chat.id, "Please wait...")
    global chat_id, msg_id
    # print(msg_)
    chat_id = msg_.chat.id
    msg_id = msg_.id
    config["prompt"] = prompt.replace("<PROMPT>", message.text)
    await sio.emit("request", config)


content_types = [
    "audio",
    "photo",
    "voice",
    "video",
    "document",
    "text",
    "location",
    "contact",
    "sticker",
]


@bot.message_handler(func=lambda message: True, content_types=content_types)
def default_command(message):
    bot.send_message(message.chat.id, "This is the default command handler.")


if __name__ == "__main__":
    print(DALAI_HOST, DALAI_PORT)
    print("Starting...")
    try:
        start_time = time.perf_counter()
        TIMEOUT = 30.0
        # while True:
        #     try:
        #         with socket.create_connection(
        #             (DALAI_HOST, DALAI_PORT), timeout=TIMEOUT
        #         ):
        #             break
        #     except OSError as ex:
        #         time.sleep(0.01)
        #         if time.perf_counter() - start_time >= TIMEOUT:
        #             raise TimeoutError(
        #                 "Waited too long for the port {} on host {} to start accepting "
        #                 "connections.".format(DALAI_PORT, DALAI_HOST)
        #             ) from ex
        asyncio.run(sio.connect(f"{DALAI_HOST}:{DALAI_PORT}"))
        asyncio.run(bot.infinity_polling())
    except Exception as e:
        print(e)
