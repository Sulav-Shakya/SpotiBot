# SpotiBot
SpotiBot is a discord bot that seeks to allow discord users to access their top tracks and artists within discord.
This bot currently allows users to see their top tracks or artists within a range from as little at 6 weeks to their entire acccount's duration.
This bot uses PythonAnywhere as a host for endpoints to allow the Spotify oAuth process to flow

oAuth

SpotiBot access what Spotify considers user sensitive data, as such Spotify requires this bot to adhere to the rules of oAuth 2.0.


A simple flow of how the system works:

------------------------------------------------------------------------------------------------------------------------------------------------------------------
Website --> User Logins --> User allows application to accesss their data --> user is redirected to an endpoint (spotify attached a code to the endpoint)

  --> app catches the code from endpoint --> app sends post request to spotify including some data confirming that it is itself --> app gets the user's data as requested
  in the scope as a json file
------------------------------------------------------------------------------------------------------------------------------------------------------------------

This system also uses Flask's endpoint system to allow the hosting of endpoints within Python to run smoothly.


