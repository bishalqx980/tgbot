# [tgbot](https://bishalqx980.github.io/tgbot) 👻

This Telegram bot is built using the `python-telegram-bot` library *`version 21.9`* and performs various tasks within **Telegram**.

> **This bot can be found as [Ciri](https://t.me/MissCiri_bot) on Telegram.**

***If you liked this project then please give it a ⭐ | Thank You!***

## Features 🐳

> **📝 Note (14/12/2024):** _Certain features have been temporarily removed due to limitations. They may be reintroduced in future updates. Additionally, not all features are listed here. We encourage you to start the bot and explore its full functionality. I appreciate your understanding._

- **Group Management ⚡**
    - It has just everything... 😉
    - Whisper Message (secretly message a user in Group) 🤫
- **AI 🤖**
    - ChatGPT
    - AI Imagine
- **Misc ✨**
    - Get Movie Information
    - Built-in Language Translator
    - Decode, Encode (base64)
    - Short URL / Ping URL
    - Generate QR Code (Image)
    - Host Image Publicly (Link)
    - Pastebin (telegraph)
    - Convert text into speech (voice)
    - Built-in [PSNDL](https://bishalqx980.github.io/psndl/) Support
    - Get Any Location Weather Information
    - Calculate basic math
    - ~~Take webshot (website screenshot)~~ `Removed due to limitations`
    - ~~Download YouTube video~~ `Removed due to limitations`
        - Added YouTube audio/song download (14/01/2025)
    - ~~Search YouTube video~~ `Removed due to limitations`
    - Much more...🤩 [Start Now](https://t.me/MissCiri_bot) to explore 🌴

## Deploy your own bot 👩‍🚀

**Steps**

- Preparation 📦
- Host 🚀

**Preparation 📦**
---
- Download & Rename `sample_config.env` to `config.env` then fillup `config.env` file value's

    **⚠️ Note:** _Don't share or upload the `config.env` any public place or repository_

**`config.env` Values**

- `BOT_TOKEN` Get from [https://t.me/BotFather](https://t.me/BotFather) E.g. `123456:abcdefGHIJK...`
- `OWNER_ID` Get from bot by /id command E.g. `2134776547`
- `MONGODB_URI` Get from [https://www.mongodb.com/](https://www.mongodb.com/) (Check Below for instruction)
- `DB_NAME` anything E.g. `MissCiri_db`

**[Creating MongoDB URI](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/get-started/#create-a-connection-string)**

> **Note (MongoDB):** _On the left side list click on `Network Access` section click on `ADD IP ADDRESS` and set ip to `0.0.0.0/0` (Its important to access database without network restriction)_

**Host 🚀**
---
**Local Hosting 💻**

- Windows/Linux
    - Required `python 3.11` (also tested on `3.13`)
    - Open `tgbot` directory on cmd/shell
    - Run on cmd/shell `pip install -r requirements.txt`
    - Finally `python -m bot`

**Render Deploy ⚡**

- Signin/Signup on [Render](https://render.com/)
- Goto dashboard & create a New `Web Service`
- Select `Public Git Repository`: `https://github.com/bishalqx980/tgbot`
- Then 👇
    ```
    > Language: Docker
    > Branch: main
    > Instance Type: Free [or paid]
    ```
- Advanced option 👇
    ```
    Secret Files

    > Filename: 'config.env'
    > File Contents: Paste all content from 'sample_config.env' (make sure you filled up everything)
    ```

    > **Note (Render Hosting):** _If you face anyproblem accessing `Advanced option` then just click on `Create Web Service` then from `Environment` > `Secret Files` and add the `config.env` values. Then restart/redeploy the web service._

    > **Important (Render Hosting):** _After deployment complete go to [Render Dashboard](https://dashboard.render.com/) and open your service then you can see service url on top left corner [https://example.onrender.com]() copy that and go to bot `/bsettings` server url and edit with your service url. (**So that bot won't go to sleep**)_

**_After deployment complete, don't forget to visit `/bsettings`_**

---

```
𝓐 𝓹𝓻𝓸𝓳𝓮𝓬𝓽 𝓸𝓯

 ▄▄▄▄    ██▓  ██████  ██░ ██  ▄▄▄       ██▓    
▓█████▄ ▓██▒▒██    ▒ ▓██░ ██▒▒████▄    ▓██▒    
▒██▒ ▄██▒██▒░ ▓██▄   ▒██▀▀██░▒██  ▀█▄  ▒██░    
▒██░█▀  ░██░  ▒   ██▒░▓█ ░██ ░██▄▄▄▄██ ▒██░    
░▓█  ▀█▓░██░▒██████▒▒░▓█▒░██▓ ▓█   ▓██▒░██████▒
░▒▓███▀▒░▓  ▒ ▒▓▒ ▒ ░ ▒ ░░▒░▒ ▒▒   ▓▒█░░ ▒░▓  ░
▒░▒   ░  ▒ ░░ ░▒  ░ ░ ▒ ░▒░ ░  ▒   ▒▒ ░░ ░ ▒  ░
 ░    ░  ▒ ░░  ░  ░   ░  ░░ ░  ░   ▒     ░ ░   
 ░       ░        ░   ░  ░  ░      ░  ░    ░  ░
      ░                                        
```
