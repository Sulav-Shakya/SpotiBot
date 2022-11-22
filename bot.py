
import time
import discord
from email import header
import requests
import json
import os
intents = discord.Intents.all()
from discord.ext import commands


bot = commands.Bot(command_prefix='!',intents=intents)

ACCESS_TOKEN = ""
REFRESH_TOKEN = ""



#given a current discord user, find their id within the data set and make a request to refresh the token
def refreshExpiredToken(authorID):
    with open('/home/SSHAKYA/mysite/userData.json', 'r') as f:
        data = json.load(f)
        if data.get("users").get(authorID).get("error") != None:
            if data.get("users").get(authorID).get("error").get("message") == "The access token expired":

                g = requests.post("http://sshakya.pythonanywhere.com/refresh?userID=" + authorID)

                access_token = g.json().get("access_token")



                with open('/home/SSHAKYA/mysite/userTokens.json', 'r') as f:
                    tokenData = json.load(f)




                with open('/home/SSHAKYA/mysite/userTokens.json', 'w') as f:
                    tokenData.get("users").get(authorID).update({'access_token': access_token})


                    json.dump(tokenData,f, indent=  4)


                with open('/home/SSHAKYA/mysite/userData.json', 'w') as f:
                    data.get("users").pop(authorID)
                    json.dump(data,f, indent=  4)






#for first time users, login to the app to have SpotiBot have access to your spotify data
@bot.command(name = "login")
async def login(ctx):
    await ctx.send("Please follow this link to let this bot read your spotify data: https://sshakya.pythonanywhere.com/login?userID=" + str(ctx.author.id))







#primary function, gets the top x amount of artists/tracks within the last 4 weeks/6 momnths/ couple years
#where x is an integer above 0 but below or equal to 50
@bot.command(name = "getTop")
async def getTop(ctx, length, itemType, timeFrame):
    top10 = ""

    if int(length) <= 0 or int(length) > 50:
        await ctx.reply("Please enter a valid item range.")
        return

    if itemType != "artists" and itemType != "tracks":
        await ctx.reply("Please enter a valid type of list.")
        return

    if timeFrame != "long" and  timeFrame != "medium" and  timeFrame != "short" :
        await ctx.reply("Please enter a valid timeframe.")
        return


    with open('/home/SSHAKYA/mysite/userTokens.json', 'r') as f:
        token = json.load(f)
        headers = {
            "Authorization": "Bearer " + token.get("users").get(str(ctx.author.id)).get("access_token"),
            "Content-Type" : "application/json"
        }

        params = {
            "time_range" : timeFrame + "_term",
            "limit" : length
        }
        #json file containing data from request to endpoint for the top artists/tracks for a user
        r = requests.get("https://api.spotify.com/v1/me/top/" + itemType, headers =headers, params = params )


    with open('/home/SSHAKYA/mysite/userData.json', 'r') as f:
        data = json.load(f)




    with open('/home/SSHAKYA/mysite/userData.json', 'w') as f:
        if data["users"].get(str(ctx.author.id)) != None:
            data["users"].pop(str(ctx.author.id))
        data["users"].update({str(ctx.author.id) : r.json()})



        json.dump(data,f, indent=  4)

    #to make sure that the access token used by the user has not been timed out yet
    refreshExpiredToken(str(ctx.author.id))





    with open('/home/SSHAKYA/mysite/userData.json', 'r') as f:

        num = 1
        data = json.load(f)
        userData = data.get("users").get(str(ctx.author.id))

        for i in userData.get("items"):
            top10 += str(num) + ".) "+  i.get('name') + "\n"
            num+= 1

    #extra flavor for when returning the list
    if timeFrame == "long":

        await ctx.reply("```Your top " + length + " " + itemType + " of all time are:\n" + top10 + "```")
    elif timeFrame == "medium":
        await ctx.reply("```Your top " + length + " " + itemType + " of the last 6 months are:\n" + top10 + "```")
    elif timeFrame == "short":
        await ctx.reply("```Your top " + length + " " + itemType + " last 4 weeks are:\n" + top10 + "```")









bot.run('MTAzMjQ3ODU2NjUwNTUxMzExMA.GXMM05.8GlpUv3pTb1KNUCq8rMDY_I16ujtbgMFCu9nlg')