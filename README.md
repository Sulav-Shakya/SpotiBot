# SpotiBot
SpotiBot is a discord bot that seeks to allow discord users to access their top tracks and artists within discord.
This bot currently allows users to see their top tracks or artists within a range from as little at 6 weeks to their entire acccount's duration.

This bot draws upon what is considered sensitive user data by Spotify. Spotify protects their users from potential malicious users trying to access their API
by implementing the oAuth 2 authorization flow. 

The oAuth 2 authorization flow is a way for the API to verify that the application asking for the user's data is one to be trusted.

This bot also uses discord.py to implement the actual bot used by the user. It checks for commands run by the user and retrieves the appropriate data from Spotify's 
servers to then reply to the user with within discord.

PythonAnywhere is used to host endpoints in combination with Flask. This is so that the user can be directed/redirected to a website to transmit data and login 
information to Spotify's servers with the context of the use of this application.


# WIP

Currently SpotiBot supports the command !getTop list length type time span

Where:

list length is an integer greater than 0 and less then or equal to 50

type is either "tracks" or "artists"
  
time span is either "short", "medium", and "long". Which translates to the user's data being looked at within the past 4 weeks, 6 months, and account duration 
  respectivley
  
SpotiBot seeks to add future commands that allow all tracked users within a server to compare data and to see who listens to what the most, what two users listen to
  in common, and a multitude of other features.

# DISCLAIMER
  
 Due to the nature of this project, Spotify is limiting the user scope of this project to a whitelist that is controlled from the Spotify Developer page. A quota 
  extension can be requested to increase the scope to the public, but the nature of this project's interaction with discord unfortunately violates the Spotify
  Developer TOS. 

If you would like to try and test this bot out in an environment, please join this test server with this link and provide the email associated with your Spotify account. 

https://discord.gg/5kjnmtp5




