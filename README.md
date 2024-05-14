# tgbot
This Telegram bot is built using the `python-telegram-bot` library **_version 20.7_** and performs various tasks within **Telegram**.

- **This bot can be found as [𝕮𝖎𝖗𝖎 "希里"](https://t.me/MissCiri_bot) on Telegram.**

## Features ✨:

- **ChatGPT AI:** Get response from _ChatGPT AI_
- **AI Imazine:** Generate image from your prompt
- **Group Management:** Manage Group as an active admin
    - Welcome user, notify when user leave
    - **Moderation**: ban, unban, mute, unmute, kick, kickme...
    - Antibot, etc.
    - many more feature...
- **YouTube Download** Download/Search videos from YouTube
- **Movie Info:** Provide movie information
- **Language Translator:** Translate languages
- **Encode/Decode base64:** Encode/decode base64
- **URL Shortener:** Shorten URLs using shrinke.me api
- **Ping Website** Ping any URL
- **Calculator:** Works as everyday calculator
- **Echo:** Echo your message for fun
- **Webshot** Take website screenshot
- **Weather** Provide weather information
- **& Much more...**

**<i>More Feature coming soon...</i>**

• • • • • • • • • • • • • • • • • • • •

## How to Deploy 🚀:

<details>
<summary><b>Setup 📦</b></summary>

- Fillup `sample_config.env` file value's
- `bot_token` Get from https://t.me/BotFather E.g. 123456:abcdefGHIJK...
- `owner_id` Get from bot by /id command E.g. 2134776547
- `owner_username` Your Username E.g. paste like bishalqx980 not @bishalqx980
- ❗ OPTIONAL | `support_chat` Your bot support chat invite link 
- `mongodb_uri` Get from https://www.mongodb.com/
- `db_name` anything E.g. MissCiri_db
- `server_url` E.g. for render it will be https://your_app_name.onrender.com/
- ❗ OPTIONAL | `shortener_api_key` Get from https://shrinkme.io/
- ❗ OPTIONAL | `omdb_api` Get from https://www.omdbapi.com/
- ❗ OPTIONAL | `weather_api_key` Get from https://www.weatherapi.com/
- `chatgpt_limit` E.g. 10
- `ai_imagine_limit` E.g. 10
- `usage_reset` E.g. 24 (in hour)
    <hr>
    <details>
    <summary><b>Local Deploy 🚀</b></summary>

    - Required `python 3.11` or later
    - Open `tgbot` directory on cmd
    - Run on cmd `pip install -r requirements.txt`
    - Finally `python main.py`

    </details>

    <details>
    <summary><b>Render Deploy 🚀</b></summary>

    - Signin/Signup on https://render.com/
    - Goto dashboard & create a New `Web Service`
    - Select `Build and deploy from a Git repository` > `Public Git repository` https://github.com/bishalqx980/tgbot

    ```
    `Branch` main

    `Runtime` Python 3

    `Build Command` pip install -r requirements.txt

    `Start Command` python main.py

    `Instance Type` Free (maybe paid)

    ⚠ Advanced option > `Add secret file` filename: `config.env` - file content: paste all content from `sample_config.env` (make sure you filled up everything)

    **Finally click on Create Web Service & wait few sec for deployment & Done | Enjoy 🎉**
    ```
    </details>
</details>

## License

GPL-3.0 © @bishalqx980
<br>
Original Creator - [bishalqx980](https://t.me/bishalqx980)
