from discord.ext import commands
import aiohttp
import asyncio
import json
import discord
import datetime
import time

colorfile = "utils/tools.json"
with open(colorfile) as f:
    data = json.load(f)
color = int(data["COLORS"], 16)

class weather(commands.Cog):
    """Get the day's weather or other information"""
    def __init__(self, bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()
    @commands.command(aliases=[ "zipweather"])
    async def weatherzip(self, ctx, zip_code: str):
        """Get the weather of a city/town by its zip code"""
        # Code:
        async with aiohttp.ClientSession() as session:
            url = "http://api.openweathermap.org/data/2.5/weather?zip=" + zip_code + "&appid=168ced82a72953d81d018f75eec64aa0&units=imperial"
            async with session.get(url) as response:
                weather_response = await response.json()
                if weather_response['cod'] != 200:
                    await ctx.send(f"An error ocurred: `{weather_response['message']}`. If the issue persists, please contact a support team member with this error code: `{weather_response['cod']}`")
                else:
                    currentUnix = time.time()
                    localSunrise = weather_response['sys']['sunrise'] + weather_response['timezone']
                    sunriseTime = datetime.datetime.utcfromtimestamp(localSunrise)
                    localSunset = weather_response['sys']['sunset'] + weather_response['timezone']
                    sunsetTime = datetime.datetime.utcfromtimestamp(localSunset)
                    localTimeUnix = currentUnix + weather_response['timezone']
                    localTime = datetime.datetime.utcfromtimestamp(localTimeUnix)
                    embed = discord.Embed(
                        title=f"Weather in {weather_response['name']}, {weather_response['sys']['country']}",
                        url = f"https://openweathermap.org/city/{weather_response['id']}",
                        description=weather_response['weather'][0]['description'],
                        color=color,
                    )
                    embed.add_field(name='Location:', value=f"**🏙️ City:** {weather_response['name']}\n**<:coordinates:727254888836235294> Longitude:** {weather_response['coord']['lon']}\n **<:coordinates:727254888836235294> Latitude:** {weather_response['coord']['lat']}", inline=False)
                    embed.add_field(name='Weather', value=f"**🌡️ Current Temp:** {weather_response['main']['temp']}\n**🌡️ Feels Like:** {weather_response['main']['feels_like']}\n**🌡️ Daily High:** {weather_response['main']['temp_max']}\n**🌡️ Daily Low:** {weather_response['main']['temp_min']}\n**<:humidity:727253612778094683> Humidity:** {weather_response['main']['humidity']}%\n**🌬️ Wind:** {weather_response['wind']['speed']} mph", inline=False)
                    embed.add_field(name='Time', value=f"**🕓 Local Time:** {localTime.strftime('%I:%M %p')}\n **🌅 Sunrise Time:** {sunriseTime.strftime('%I:%M %p')}\n **🌇 Sunset Time:** {sunsetTime.strftime('%I:%M %p')}")
                    embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    embed.set_footer(text='Starry | discord.gg/7mSqpXN', icon_url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    await ctx.send(embed=embed)
    @commands.command(aliases=["weather", "cityweather"])
    async def weathercity(self, ctx, *, city_name:str):
        """Get the weather of a city/town by its name. State code is US only."""
        # Code:
        async with aiohttp.ClientSession() as session:
            url = "http://api.openweathermap.org/data/2.5/weather?q=" + city_name + "&appid=168ced82a72953d81d018f75eec64aa0&units=imperial"
            async with session.get(url) as response:
                weather_response = await response.json()
                if weather_response['cod'] != 200:
                    await ctx.send(f"An error ocurred: `{weather_response['message']}`. If the issue persists, please contact a support team member with this error code: `{weather_response['cod']}`")
                else:
                    currentUnix = time.time()
                    localSunrise = weather_response['sys']['sunrise'] + weather_response['timezone']
                    sunriseTime = datetime.datetime.utcfromtimestamp(localSunrise)
                    localSunset = weather_response['sys']['sunset'] + weather_response['timezone']
                    sunsetTime = datetime.datetime.utcfromtimestamp(localSunset)
                    localTimeUnix = currentUnix + weather_response['timezone']
                    localTime = datetime.datetime.utcfromtimestamp(localTimeUnix)
                    embed = discord.Embed(
                        title=f"Weather in {weather_response['name']}, {weather_response['sys']['country']}",
                        url = f"https://openweathermap.org/city/{weather_response['id']}",
                        description=weather_response['weather'][0]['description'],
                        color=color,
                    )
                    embed.add_field(name='Location:', value=f"**🏙️ City:** {weather_response['name']}\n**<:coordinates:727254888836235294> Longitude:** {weather_response['coord']['lon']}\n **<:coordinates:727254888836235294> Latitude:** {weather_response['coord']['lat']}", inline=False)
                    embed.add_field(name='Weather', value=f"**🌡️ Current Temp:** {weather_response['main']['temp']}\n**🌡️ Feels Like:** {weather_response['main']['feels_like']}\n**🌡️ Daily High:** {weather_response['main']['temp_max']}\n**🌡️ Daily Low:** {weather_response['main']['temp_min']}\n**<:humidity:727253612778094683> Humidity:** {weather_response['main']['humidity']}%\n**🌬️ Wind:** {weather_response['wind']['speed']} mph", inline=False)
                    embed.add_field(name='Time', value=f"**🕓 Local Time:** {localTime.strftime('%I:%M %p')}\n **🌅 Sunrise Time:** {sunriseTime.strftime('%I:%M %p')}\n **🌇 Sunset Time:** {sunsetTime.strftime('%I:%M %p')}")
                    embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    embed.set_footer(text='Starry | discord.gg/7mSqpXN', icon_url=f"https://openweathermap.org/img/wn/{weather_response['weather'][0]['icon']}@2x.png")
                    await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(weather(bot))