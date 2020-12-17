<h1 align="center", style="font-size:50px;">
  Elevate
</h1>

<p align="center">
  <a href="https://discord.gg/zwyFZ7h">
    <img src="https://img.shields.io/discord/718663089318527016?style=for-the-badge&colorB=1c86ee">
  </a>
  <img src="https://img.shields.io/badge/dynamic/json?color=1c86ee&label=servers&query=data%5B0%5D.servers&url=https%3A%2F%2Fapi.statcord.com%2Fv3%2F763851389403136020&style=for-the-badge">
  <img src="https://img.shields.io/badge/devs-active-blue?colorB=1c86ee&style=for-the-badge">
  <a href="https://donatebot.io/checkout/718663089318527016">
    <img src="https://img.shields.io/badge/donate-donatebot-blue?colorB=1c86ee&style=for-the-badge">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/style-Black-blue?style=for-the-badge&colorB=1c86ee">
  </a>
</p>
<h3 align="center", style="font-size:50px;">
  The only Discord bot you'll ever need
</h3>
<h2 align="center">
  Features:
</h2>

- Moderation

- Automod

- Welcomer

- Reaction roles

- Modlog

- Music

- Customizable prefix

- And more!

<h2 align="center">
  Self hosting
</h2>

Self hosting of Elevate is not officially supported, and this is the only official guide.

Python3.8 is the only version of python this has been tested on

### Installing Dependencies

---


```
sudo apt-get install python3.8 python3.8-venv
```

Install git

```
sudo apt-install git
```

We reccomend creating a venv

```
python3.8 -m venv ~/elevate
```

```
source ~/elevate/bin/activate
```

Clone the repository

```
git clone https://github.com/craziiace/elevate.git
```

```
cd Elevate
```

We also reccomend installing dependencies from `requirements.txt`

```
python3.8 -m pip install -r requirements.txt
```

Discord.ext.menus also needs to be installed

```
python -m pip install -U git+https://github.com/Rapptz/discord-ext-menus
```

### Setting up tokens

---


Create a a file in the directory `utils` called `config.json`.
This file should look something like this:

```json
{
  "TOKEN":"discord token", 
  "TOPTOKEN":"top.gg token",
  "DONATETOKEN":"donatebot.io token",
  "DELTOKEN":"discord extreme list token",
  "KSOFT":"ksoft.si token",
  "STATCORD":"statcord token"
}
```
### Installing & running non-python dependencies

---

Both Lavalink and MongoDB need to be installed and ran.

To install MongoDB, I used [this guide](https://www.digitalocean.com/community/tutorials/how-to-install-mongodb-on-ubuntu-20-04) from DigitalOcean.

For Lavalink, download the latest .jar file from [here](https://github.com/Frederikam/Lavalink/releases/latest), and use FTP to put it on your server (if it is remote).

You also need to set up the lavalink application.yml (see [this example](https://github.com/Frederikam/Lavalink/blob/master/LavalinkServer/application.yml.example)), and change the dict in [`cogs/music.py`](https://github.com/CraziiAce/Elevate/blob/main/cogs/music.py#L357) (starting at line 357) to the credentials in the lavalink application.yml. If your Mongo database is external and/or has a password, that needs to be specified in every `MongoClient()` call.

I usually run lavalink in a tmux session, and MongoDB using systemd.

### Running the bot

---

```
tmux
```

```
python3.8 bot.py
```

## Giving credit:

Elevate is licensed under the GPL-3.0 License. This means that you can use this code for commercial & private purposes, but:

- You must state any changes you made to the code

- You must disclose the source (do not modify the `about` or `credits` commands)

- Your code must be open source, and have the same license as this

- You are resposible for anything that happens as a result of the code

Violating any of these conditions will result in a DMCA takedown of your fork of the repository