# tgbot
This Telegram bot is built using the `python-telegram-bot` library and performs various tasks within Telegram.

- This bot can be found as [Ciri](https://t.me/MissCiri_bot) on Telegram.

### Features:

- **ChatGPT AI:** I can get response from ChatGPT AI
- **AI Imazine:** 🔥 I can Imagine Image by AI from your prompt
- **Group Management:** Powerful Group Manager bot
- **YouTube Download** Can download video from YouTube
- **Movie Info:** Can provide any movie/series/episode
- **Language Translator:** Can translate any lang using Google Translator
- **Encode/Decode base64:** Can encode/decode base64 code
- **URL Shortener:** Can convert any url to shorturl (using shrinke.me api)
- **Ping Website** Can detect website response
- **Calculator:** it has built-in calculator
- **Echo:** I can echo your message (for fun) 😁
- **Webshot** I can take screenshot of any website by url 📸
- **Much more...**

- **🆘 More Feature coming soon...**

### Setup

- Fillup `sample_config.env` file value's

`bot_token` Get from https://t.me/BotFather E.g. 123456:abcdefGHIJK...

`owner_id` Get from bot by /id command E.g. 2134776547

`owner_username` Your Username E.g. paste like bishalqx980 not @bishalqx980

❗ OPTIONAL | `support_chat` Your bot support chat invite link 

`mongodb_uri` Get from https://www.mongodb.com/

`db_name` anything E.g. MissCiri_db

`server_url` E.g. for render it will be https://your_app_name.onrender.com/

❗ OPTIONAL | `shortener_api_key` Get from https://shrinkme.io/

❗ OPTIONAL | `omdb_api` Get from https://www.omdbapi.com/

`chatgpt_limit` E.g. 10

`ai_imagine_limit` E.g. 10

`usage_reset` E.g. 24 (in hour)

#### Local Deploy

- Required `python 3.11` or later
- Open `tgbot` directory on cmd
- Run on cmd `pip install -r requirements.txt`
- Finally `python main.py`

#### Render Deploy

- Signin/Signup on https://render.com/
- Goto dashboard & create a New `Web Service`
- Select `Build and deploy from a Git repository` > `Public Git repository` https://github.com/bishalqx980/tgbot

> `Branch` main

> `Runtime` Python 3

> `Build Command` pip install -r requirements.txt

> `Start Command` python main.py

> `Instance Type` Free (maybe paid)

> ⚠ Advanced option > `Add secret file` filename: `config.env` - file content: paste all content from `sample_config.env` (make sure you filled up everything)

#### 💠 Finally click on Create Web Service & wait few sec for deployment & Done | Enjoy 🎉

## License

```
MIT License

Copyright (c) 2023 Bishal Hasan Bhuiyan

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

```