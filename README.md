# [tgbot](https://bishalqx980.github.io/tgbot) <img src="https://i.ibb.co/h7bL5bn/download.png" width="20px">

This Telegram bot is built using the `python-telegram-bot` library **_version 21.9_** and performs various tasks within **Telegram**.

- **This bot can be found as [𝕮𝖎𝖗𝖎 "希里"](https://t.me/MissCiri_bot) on Telegram.**
- **📚 Archive modules/functions can be found [HERE](https://github.com/bishalqx980/python)**

<center><b><i>If you liked this project then please give it a ⭐</i></b></center>

## 🎃 Features 🎃

- **🔰 Note (14/12/2024):** _Certain features have been temporarily removed due to limitations. They may be reintroduced in future updates. Additionally, not all features are listed here. We encourage you to start the bot and explore its full functionality. Thank you for your understanding._

- **Group Management 🛠️**
    - It has just everything...
- **AI 🤖**
    - <s>ChatGPT</s> `Removed due to limitations`
    - AI photo imagine
- **Misc 🎁**
    - Get any movie info
    - Translate any language
    - Decode, Encode (base64)
    - Short any url
    - Ping any url
    - Calculate basic math
    - <s>Take webshot (website screenshot)</s> `Removed due to limitations`
    - Get any location weather info
    - <s>Download YouTube video</s> `Removed due to limitations`
    - <s>Search YouTube video</s> `Removed due to limitations`
    - Generate QR code (image)
    - Convert image into a link (public)
    - Convert text into a link
    - Whisper user in group chat (secret message)
    - Search games link for PS3 & other consoles
    - Much more... [Start](https://t.me/MissCiri_bot) now to see 👀

**<i>ℹ️ Todo: add more features... 🎉</i>**

• • • • • • • • • • • • • • • • • • • •

## How to deploy 🚀

<h3>Setup 📦</h3>

- Download & rename `sample_config.env` to `config.env` then fillup `config.env` file value's

<h6>⚠️ Don't share or upload the `config.env` any public place or repository</h6>

- `BOT_TOKEN` Get from [https://t.me/BotFather](https://t.me/BotFather) E.g. `123456:abcdefGHIJK...`
- `OWNER_ID` Get from bot by /id command E.g. `2134776547`
- `OWNER_USERNAME` Your Username E.g. paste like ✅ `bishalqx980` not ❌ `@bishalqx980`
- `MONGODB_URI` Get from [https://www.mongodb.com/](https://www.mongodb.com/) (Check Below for instruction)
- `DB_NAME` anything E.g. `MissCiri_db`

<h3>Creating MongoDB URI</h3>

- Signin/Signup on [MongoDB](https://www.mongodb.com/)
- on [MongoDB Atlas](https://cloud.mongodb.com/) create `New Project`
- After creating click on the project to access
- on the left side list, click on `Clusters` > create a `cluster`
- After creating again on the left side list, `Database Access` click on `ADD NEW DATABASE USER`

1. `Authentication Method`: `Password`

2. `Password Authentication`: give `username` and `password` (remember that)

3. on `Database User Privileges` section

4. `Built-in Role`: `Atlas admin`

5. Finally click on `Add User`

6. Now again goto `cluster` section and click on `connect`

7. `Connect to your application` section `Drivers`

8. `Connecting with MongoDB Driver` section `3. Add your connection string into your application code`

9. Here you can see something like `mongodb+srv://something:<db_password>@cluster9800.AA11.mongodb.net/?retryWrites=true&w=majority&appName=Cluster9800`

10. Remove the `<db_password>` from that URI and add your password which one you gave on `2. 'Password Authentication'`

🥳 Done you have created your `MongoDB_URI` successfully...

> **Note:** One last thing, on the left side list click on `Network Access` section click on `ADD IP ADDRESS` and set ip to `0.0.0.0/0` (Its important to access database without network restriction)


<h3>Deploy Section 🎯</h3>

<center><h3>🖥️ <u>Local deploy</u></h3></center>

----- **Windows** -----
- Required `python 3.11` or later
- Open `tgbot` directory on cmd
- Run on cmd `pip install -r requirements.txt`
- Finally `python main.py`

----- **Linux** -----
- Required `python 3.11` or later
- Open `tgbot` directory on shell
- Run on shell `pip install -r requirements.txt`
- Finally `python main.py`

<center><h3>📡 <u>Render deploy</u></h3></center>

- Signin/Signup on [Render](https://render.com/)
- Goto dashboard & create a New `Web Service`
- Select `Public Git repository` > `https://github.com/bishalqx980/tgbot`

- Then 👇
```
> Language: Docker
> Branch: main
> Instance Type: Free [or paid]
```

- Advanced option 👇
```
> Secret Files ⬇️
> Filename: 'config.env'
> File Contents: paste all content from 'sample_config.env' (make sure you filled up everything)
```

> **Note:** _If you face anyproblem accessing `Advanced option` then just click on `Create Web Service` then from `Environment` > `Secret Files` add the `config.env` values. Then restart/redeploy the web service._

> **Important:** _After deployment complete go to [Render Dashboard](https://dashboard.render.com/) and open your service then you can see service url on top left corner [https://example.onrender.com]() copy that and go to bot `/bsettings` server url and edit with your service url. (**So that bot won't go to sleep**)_

**D.O.N.E 🥳**

<center><h3>📡 <u>Heroku deploy</u></h3></center>

- Signin/Signup on [http://heroku.com/](http://heroku.com/)
- Give a ⭐ and fork this repo [https://github.com/bishalqx980/tgbot](https://github.com/bishalqx980/tgbot)
- Goto your forked repo `settings` > `General` > Check ✅ `Template repository`
- Come back and on the right top corner you will see a green button name `Use this template` <img src="https://i.ibb.co.com/LrW5Z4G/image.png" width="50px">, click on that and create a new private repo with these files
- On that private repo upload your `config.env` file and make sure required all values are filled up
- Then goto the private repo `settings` > `secrets and variables` > `Actions`
- Click on `New respository secret`
    - **_Name_**: `HEROKU_EMAIL`
    - **_Secret_**: `your_heroku_email`
    - Repeat the step and add `HEROKU_APP_NAME` - unique name eg. tgbot007oc-bishalqx980
    - Add `HEROKU_API_KEY` - get from [https://dashboard.heroku.com/account](https://dashboard.heroku.com/account) scroll down `API Key` click on `Reveal` button then copy the value and paste it...
- Finally click on `Actions` tab from the top, select `Deploy to heroku`, on right side click on `Run workflow` > green button `Run workflow`
- Now wait for deployment complete... (you can check log here [https://dashboard.heroku.com/apps/HEROKU_APP_NAME/logs](https://dashboard.heroku.com/apps/HEROKU_APP_NAME/logs))
- ⚠️ Add `Server url` from `/bsettings` before heroku shutdown... then restart dyno (heroku app)

**D.O.N.E 🥳**

- **_After deployment complete, don't forget to visit `/bsettings`_**

## License 📝

_GPL-3.0_

<br>

_Original Creator_ - [@bishalqx980](https://t.me/bishalqx980)

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
