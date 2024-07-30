# tgbot
This Telegram bot is built using the `python-telegram-bot` library **_version 20.7_** and performs various tasks within **Telegram**.

- **This bot can be found as [𝕮𝖎𝖗𝖎 "希里"](https://t.me/MissCiri_bot) on Telegram.**
- **Checkout [https://github.com/bishalqx980/python](https://github.com/bishalqx980/python)**

```Spread Love ❤️
>> If you liked this project then please give it a star...!
```

## Features

- **Group Management**
    - It has just everything...
- **AI**
    - ChatGPT
    - AI photo imagine
- **Misc**
    - Get any movie info
    - Translate any language
    - Decode, Encode (base64)
    - Short any url
    - Ping any url
    - Calculate basic math
    - Take webshot (website screenshot)
    - Get any location weather info
    - Download YouTube video
    - Search YouTube video
    - Generate QR code (image)
    - Convert image into a link (public)
    - Convert text into a link
    - Whisper user in group chat (secret message)
    - Search games link for PS3 & other consoles
    - Much more...


**<i>ℹ️ Todo: add more features...</i>**

• • • • • • • • • • • • • • • • • • • •

## How to deploy 🚀

<details>
<summary><b>Setup 📦</b></summary>

- Rename `sample_config.env` to `config.env` then fillup `config.env` file value's
- `BOT_TOKEN` Get from https://t.me/BotFather E.g. 123456:abcdefGHIJK...
- `OWNER_ID` Get from bot by /id command E.g. 2134776547
- `OWNER_USERNAME` Your Username E.g. paste like bishalqx980 not @bishalqx980
- `MONGODB_URI` Get from https://www.mongodb.com/
- `DB_NAME` anything E.g. MissCiri_db
- **_After deployment complete, don't forget to visit /bsettings_**
    <hr>
    <details>
    <summary><b>Local deploy</b></summary>

    ----- **Windows** -----
    - Required `python 3.11` or later
    - Open `tgbot` directory on cmd
    - Run on cmd `pip install -r requirements.txt`
    - Finally `start.cmd`

    <br>

    ----- **Linux** -----
    - Required `python 3.11` or later
    - Open `tgbot` directory on shell
    - `pip install -r requirements.txt`
    - Finally `bash start.sh`

    </details>

    <details>
    <summary><b>Render deploy</b></summary>

    - Signin/Signup on https://render.com/
    - Goto dashboard & create a New `Web Service`
    - Select `Build and deploy from a Git repository` > `Public Git repository` https://github.com/bishalqx980/tgbot

    <br>

    `Branch` main

    `Runtime` Python 3

    `Build Command` pip install -r requirements.txt

    `Start Command` python main.py

    `Instance Type` Free (maybe paid)

    ⚠ Advanced option > `Add secret file` filename: `config.env` - file content: paste all content from `sample_config.env` (make sure you filled up everything)

    **_[ If you face anyproblem accessing `Advanced option` then just click on `Create Web Service` then from `Environment` > `Secret Files` add the config.env calues... Then restart/redeploy the web service ]_**

    **Finally click on Create Web Service & wait few sec for deployment & Done | Enjoy 🎉**

    </details>

    <details>
    <summary><b>Heroku deploy</b></summary>

    - Signin/Signup on http://heroku.com/
    - Give a star ⭐ and fork this repo https://github.com/bishalqx980/tgbot
    - Goto your forked repo `settings` > `General` > Check ✅ `Template repository`
    - Come back and on the right top corner you will see a green button name `Use this template`, click on that and create a new private repo with these files
    - On that private repo upload your `config.env` file and make sure required all values are filled up
    - Then goto the private repo `settings` > `secrets and variables` > `Actions`
    - Click on `New respository secret`
        - **_Name_**: `HEROKU_EMAIL`
        - **_Secret_**: `your_heroku_email`
        - Repeat the step and add `HEROKU_APP_NAME` - unique name eg. tgbot007oc-bishalqx980
        - Add `HEROKU_API_KEY` - get from https://dashboard.heroku.com/account scroll down `API Key` click on `Reveal` button then copy the value and paste it...
    - Finally click on `Actions` tab from the top, select `Deploy to heroku`, on right side click on `Run workflow` > green button `Run workflow`
    - Now wait for deployment complete... (you can check log here https://dashboard.heroku.com/apps/HEROKU_APP_NAME/logs)
    - ⚠️ Add `Server url` from /bsettings before heroku shutdown... then restart dyno (heroku)

    **Enjoy 🍾**

    </details>

</details>

## License

GPL-3.0
<br>
Original Creator - [bishalqx980](https://t.me/bishalqx980)

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
                            based on python-telegram-bot lib
```
