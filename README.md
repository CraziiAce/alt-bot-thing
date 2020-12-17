<h1 align="center", style="font-size:50px;">
  Elevate
</h1>

<p align="center">
  <a href="https://discord.gg/zwyFZ7h">
    <img src="https://img.shields.io/discord/718663089318527016?style=flat-square&colorB=1c86ee">
  </a>
  <img src="https://img.shields.io/badge/dynamic/json?label=servers&query=data[0].servers&url=https://api.statcord.com/v3/763851389403136020&style=flat-square&colorB=1c86ee">
  <img src="https://img.shields.io/badge/devs-active-blue?colorB=1c86ee&style=flat-square">
  <a href="https://donatebot.io/checkout/718663089318527016">
    <img src="https://img.shields.io/badge/donate-donatebot-blue?colorB=1c86ee&style=flat-square">
  </a>
  <a href="https://github.com/psf/black">
    <img src="https://img.shields.io/badge/code%20style-black-000000.svg">
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

Both Lavalink and MongoDB need to be installed and ran
I usually run lavalink in a tmux session, and MongoDB using systemd

You also need to set up the lavalink application.yml (see [this example](https://github.com/Frederikam/Lavalink/blob/master/LavalinkServer/application.yml.example)), and change the dict in `cogs/music.py` (starting at line 357) to the credentials in the lavalink application.yml. If your Mongo database is external and/or has a password, that needs to be specified in every `MongoClient()` call.

### Running the bot

```
tmux
```

```
python3.8 bot.py
```

