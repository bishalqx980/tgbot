# [tgbot 2.0 (beta)](https://bishalqx980.github.io/tgbot) 👻

This Telegram bot is built using the **[kurigram](https://github.com/kurigram-org/kurigram)** library and performs various tasks within **Telegram**.

**Checkout [tgbot v1](https://github.com/bishalqx980/tgbot/tree/v1)**

> **This bot can be found as [Ciri](https://t.me/MissCiri_bot) on Telegram.**

***If you liked this project then please give it a ⭐ | Thank You!***

## Features 🐳

> Note: tgbot v2 is underdevelopment, so many features are disabled or won't work properly. Thank you for your understanding...

- **Group Management ⚡**
    - It has just everything... 😉
    - Whisper Message (secretly message someone in a Group) 🤫

- **Misc ✨**
    - Dumper (store documents and get unique URL)
    - Built-in Language Translator
    - Decode, Encode (base64)
    - Short or Ping URL
    - Generate QR Code (Image)
    - Upload Image (Get a link for that image)
    - Pastebin (telegraph)
    - Unziper `.zip` files
    - Convert text into speech (voice)
    - Movie Information
    - Built-in [PSNDL](https://bishalqx980.github.io/psndl/) Support
    - Get Any Location Weather Information
    - Calculate basic math
    - Much more...🤩 [Start Now](https://t.me/MissCiri_bot) to explore 🌴


## How to add new command?

- Check [_\_demo\_\_.py](./app/plugins/__demo__.py)
- Edit the metadata and make your own plugin 👀
- Don't forget to open a [pull request](https://github.com/bishalqx980/tgbot/pulls)

## Deploy your own bot 👩‍🚀

**Steps**

- Preparation 📦
- Host 🚀

**Preparation 📦**
---
- Recommended python version **3.14**
- Download & Rename `sample_config.py` to `config.py` then fillup `config.py` file value's

    **⚠️ Note:** _Don't share or upload the `config.py` any public place or repository_

**[Creating MongoDB URI](https://www.mongodb.com/docs/languages/python/pymongo-driver/current/get-started/#create-a-connection-string)**

> **Note (MongoDB):** _On the left side list click on `Network Access` section click on `ADD IP ADDRESS` and set ip to `0.0.0.0/0` (Its important to access database without network restriction)_

**Host 🚀**
---
**Local Hosting 💻**

- Windows/Linux
    - Required `python 3.14` (also tested on `3.13`)
    - Open `tgbot` directory on cmd/shell
    - Run on cmd/shell `pip install -r requirements.txt`
    - Finally `python -m app`

**Render Deploy ⚡**

- Signin/Signup on [Render](https://render.com/)
- Goto dashboard & create a New `Web Service`
- Select `Public Git Repository`: `https://github.com/bishalqx980/tgbot`
- Then 👇
    ```
    > Language: Docker
    > Branch: v2
    > Instance Type: Free [or paid]
    ```
- Advanced option 👇
    ```
    Secret Files

    > Filename: 'config.py'
    > File Contents: Paste all content from 'sample_config.py' (make sure you filled up everything)
    ```

    > **Note (Render Hosting):** _If you face anyproblem accessing `Advanced option` then just click on `Create Web Service` then from `Environment` > `Secret Files` and add the `config.py` values. Then restart/redeploy the web service._

    > **Important (Render Hosting):** _After deployment complete go to [Render Dashboard](https://dashboard.render.com/) and open your service then you can see service url on top left corner [https://example.onrender.com]() copy that and go to Environments and edit config.py `server_url` with your service url. (**So that bot won't fall asleep**)_

---

<p align="center">
  Made with ❤️ by <a href="https://github.com/bishalqx980">bishalqx980</a>
</p>

---

[!["Buy Me A Coffee"](https://www.buymeacoffee.com/assets/img/custom_images/orange_img.png)](https://telegra.ph/Buy-me-a-Coffee-03-01)

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
