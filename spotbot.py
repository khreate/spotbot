import os
import sys
import requests
import json
import discord
import spotipy
import spotipy.util as util


def read_token():
    with open("discord_auth.txt", "r") as f:
        lines = f.readlines()
        return lines[0].strip()


token = read_token()
client = discord.Client()


@client.event
async def on_ready():
    await client.change_presence(status=discord.Status.online, activity=discord.Game('running in #music'))
    print("online")

# scope = 'playlist-modify-public user-read-email'
client_id = '<CLIENT_ID>' # put your client id from Spotify here
response_type = 'code'
client_secret = '<CLIENT_SECRET>' # put your client secret from Spotify in here
playlist_id = '<PLAYLIST_ID>' # this is the id of your Spotify playlist
username = '<SPOTIFY_USERNAME>' # spotify username
token_spotify = util.prompt_for_user_token(username, scope='playlist-modify-public', # i know prompt_for_user_token is depreciated but it's the only thing that works
                                           client_id='<CLIENT ID>',
                                           client_secret='<CLIENT SECRET>',
                                           redirect_uri='http://localhost:8888/callback')
sp = spotipy.Spotify(auth=token_spotify)


@client.event
async def on_message(message):
    channel = 'music'
    if str(message.channel) == channel:
        if message.content.find('spotify:track:') != -1:
            print(f'message received in channel {str(message.channel)}')
            await message.channel.send('Trying to add to playlist...')
            s = str(message.content)
            tracks = s.split(',') 
            for id in tracks:
                trackid = [id[14:]]
                print(trackid)
                sp.user_playlist_add_tracks(username, playlist_id=playlist_id, tracks=trackid)
            # sp.user_playlist_add_tracks(username, playlist_id=playlist_id, tracks=trackid)
            embed = discord.Embed(color=discord.Color.from_rgb(0, 240, 0), title="Success!",
                                  description="Check out the playlist at https://open.spotify.com/playlist/5Hkq93FPBgV5eDp9HvgJ5J?si=XXQSSL8mR7WJLynSXa-svg")
            await message.channel.send(content=None, embed=embed)

client.run(token)



