# -*- coding: utf-8 -*-
"""spotifyapi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1Z8z1hE57raqlYQVea5xBKrEl7YXk7t9H
"""

pip install spotipy

import csv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

birdy_uri = 'spotify:artist:716NhGYqD1jl2wI1Qkgq36'
spotify = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id='222e39e86f25492f8c56c838f06cc640',
        client_secret='5022a75d4fc84e6a985cc428137854c5',))


results = spotify.user_playlist(birdy_uri, '7eMf6WibCyGLLZEHR3TjGT')
songs = results["tracks"]["items"]

canciones=[]
for i in songs:
  cancion=i["track"]
  

  duracion=cancion["duration_ms"]
  nombre=cancion["name"]
  can=[]
  can.append(duracion)
  can.append(nombre)
  canciones.append(can)
filtrada=[u for u in canciones if "Session" in u[1]]

print(len(filtrada))

file = open('bza.csv', 'w+', newline ='')
for minutos in filtrada:
  print(minutos)
  cambio=minutos[0]/60000
  file.write(minutos[1]+';'+str(cambio)+'\n')

file.close()