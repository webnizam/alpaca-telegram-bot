
# ChatGPT-Alpaca Telegram Bot

This program is designed to deploy a simple Telegram bot using the results from LLaMa or Sanford Alpaca LLM, with the assistance of Dalai.



## Deployment

To create a Telegram bot, you can send a message to BotFather on Telegram and obtain an API key. BotFather is a bot provided by Telegram that can help you create and manage bots.

To get started, open Telegram and search for @BotFather. Once you've found the bot, send a message to it and follow the prompts to create your bot. BotFather will ask you for details like the name and username of your bot, and will provide you with an API key once you've completed the setup process.

Then run commands below,

```bash
  git clone https://github.com/webnizam/alpaca-telegram-bot
  cd alpaca-telegram-bot
  cp .example.env .env
```

Add the API key to **.env** file.

```bash
  docker compose build
  docker compose run dalai npx dalai alpaca install 7B
  docker compose up -d
```

Your bot is now ready to chat! To start interacting with it, you'll need to add the bot to your Telegram account.

To do this, search for your bot's username in Telegram, and then click on the bot's profile that appears in the search results. Once you've done this, click the 'Start' button to begin chatting with the bot.

You can then send messages to the bot and receive responses, depending on the functionality that you've built into the bot. Have fun chatting with your new bot!
## Development

This is a basic script that has ample room for further development. I will continue to improve it, but in the meantime, please feel free to fork and contribute to the project.



## References

[Dalai](https://github.com/cocktailpeanut/dalai)

[Stanford Alpaca](https://github.com/tatsu-lab/stanford_alpaca)
