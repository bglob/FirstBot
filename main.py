# This code is based on the following example:
# https://discordpy.readthedocs.io/en/stable/quickstart.html#a-minimal-bot

import discord
from discord import app_commands
import os
import search_berserk
from dotenv import load_dotenv
from enum import Enum
from VincentCode.Vincent import *
from CalebCode.Vincent import *
from ZackCode.Vincent import *

load_dotenv()

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

berserk_web = search_berserk.BerserkWeb()

no_result_message = '''Sorry, we can\'t find what you are searching for.'''

class GuildID(Enum):
    testServer = 1118210036154515496
    leagueServer = 1090509064791932930

def storeChapter(value):
    f = open("stored.txt","w")
    f.write(value)
    f.close()

def getChapter():
    f = open("stored.txt","r")
    val = (f.read())
    f.close()
    return val

def incrementChapter():
    f = open("stored.txt","r")
    val = (f.read())
    f.close()
    if (val.isnumeric()):
        req_chap = int(val)
        if (req_chap > 372):
            print('Searching out of bounds.')
            return "OOB"
        else:
            chap = int(val)
            chap += 1
            if (chap < 10):
                # preserved.chapter = "00" + str(chap)
                storeChapter("00" + str(chap))
            elif (chap < 100):
                storeChapter("0" + str(chap))
            else:
                storeChapter(str(chap))
            return "W"
    else:
        # lower the case
        if ord(val[0]) > 64 and ord(val[0]) < 91:
            lowerchar = chr(ord(val[0])+32)
        elif ord(val[0]) < 97 or ord(val[0]) > 122:
            print('Letter chap invalid.')
            return "LCI"
        else:
            lowerchar = chr(ord(val[0]))

        if ord(lowerchar) < ord('p'):
            storeChapter(str(chr(ord(lowerchar)+1)) + "0")
            return "W"
        elif ord(lowerchar) == ord('p'):
            storeChapter("001")
            return "W"
        elif ord(lowerchar) < ord('a'):
            print('Letter chap invalid.')
            return "LCI"
        else:
            print('Weirdly too high of a letter chap. Going to 001.')
            storeChapter("001")
            return "W"

@client.event
async def on_ready():
    os.system('cls')
    await tree.sync(guild=discord.Object(id=GuildID.leagueServer.value))
    await tree.sync(guild=discord.Object(id=GuildID.testServer.value))
    print('We have logged in as {0.user}'.format(client))

@tree.command(name = "search", description = "Scrapes berserk chapters into a forum post", guilds=(discord.Object(id=GuildID.leagueServer.value),discord.Object(id=GuildID.testServer.value))) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def search(interaction, chapter: str):
    chap = berserk_web.key_words_search_words("$search "+chapter)
    if (chap == "OOB" or chap == "LCI"):
        print("Tried to call search2 on bad input, code " + chap)
        await interaction.response.send_message("Stored chapter was bad. Error code " + chap + ".")
        return
    storeChapter(chap)
    divs = berserk_web.search(chap)
    links = berserk_web.send_link(divs)
    if len(links) > 0:
        await interaction.response.send_message("Chapter found!")
        forum = discord.utils.get(interaction.guild.forums, name="peak-chapters")
        thread = await forum.create_thread(
            name= 'Berserk Chapter ' + str(chap),
            auto_archive_duration=4320,
            content="A place to relax and read chapter " + str(chap) + " of Berserk.",
            reason="Created from bot command"
        )
        print("Printing chapter " + chap + " (" + str(len(links)) + " pages)")
        for j in range(len(links)):
            await thread.thread.send(links[j])
        print("Done printing chapter " + chap)

    else:
        await interaction.response.send_message(no_result_message)

@tree.command(name = "next", description = "Scrape the next chapter into a forum post", guilds=(discord.Object(id=GuildID.leagueServer.value),discord.Object(id=GuildID.testServer.value))) #Add the guild ids in which the slash command will appear. If it should be in all, remove the argument, but note that it will take some time (up to an hour) to register the command if it's for all guilds.
async def search(interaction):
    success = incrementChapter()
    chap = getChapter()
    # f = open("stored.txt","r")
    # chap = (f.read())
    # f.close()
    if (success != "W"):
        print("Increment failed, code " + success)
        await interaction.response.send_message("Stored chapter was bad. Error code " + success + ".")
        return
    divs = berserk_web.search(chap)
    links = berserk_web.send_link(divs)
    if len(links) > 0:
        await interaction.response.send_message("Chapter found!")
        forum = discord.utils.get(interaction.guild.forums, name="peak-chapters")
        thread = await forum.create_thread(
            name= 'Berserk Chapter ' + str(chap),
            auto_archive_duration=4320,
            content="A place to relax and read chapter " + str(chap) + " of Berserk.",
            reason="Created from bot command"
        )
        print("Printing chapter " + chap + " (" + str(len(links)) + " pages)")
        for j in range(len(links)):
            await thread.thread.send(links[j])
        print("Done printing chapter " + chap)

    else:
        await interaction.response.send_message(no_result_message)

@client.event
async def on_message(message):
    # make sure bot doesn't respond to it's own messages to avoid infinite loop
    if message.author == client.user:
        return
    # lower case message
    message.content = message.content.lower()

    # I am the admin B)
    admin_id = 243912487655833600

    # only admin can run $commands
    if message.author.id != admin_id:
        return

    if f'$party' in message.content:
        await message.channel.send("Party time")

    if f'$preserved' in message.content:
        await message.channel.send("Preserved has " + str(getChapter()) + ".")

    if f'$set' in message.content:
        storeChapter(message.content[5:])
        await message.channel.send("Stored chapter " + str(getChapter()) + ".")

    # we can add some $commands now

    # if f'$search' in message.content:
    #
    #     chap = berserk_web.key_words_search_words(message.content)
    #     divs = berserk_web.search(chap)
    #     links = berserk_web.send_link(divs)
    #     if len(links) > 0:
    #         channel = discord.utils.get(client.get_all_channels(), name=message.channel.name, guild=message.guild)
    #         print("Channel found: " + str(channel))
    #         thread = await channel.create_thread(
    #         	name= 'chapter-' + str(chap),
    #             auto_archive_duration=4320,
    #         	type=discord.ChannelType.public_thread
    #         )
    #         for j in range(len(links)):
    #             os.system('cls')
    #             print("Printing chapter " + chap + "...")
    #             print("[" + str(j+1) + "/" + str(len(links)) + "]" + " printed")
    #             await thread.send(links[j])
    #         os.system('cls')
    #         print("Done printing chapter " + chap)
    #
    #     else:
    #         os.system('cls')
    #         await message.channel.send(no_result_message)
    #     # print("DEBUG -- User was " + str(message.author))
    #     print("Waiting for commands...")


try:
    client.run(os.getenv("TOKEN"))
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
