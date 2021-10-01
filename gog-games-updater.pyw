#!/usr/bin/python3
from bs4 import BeautifulSoup

import tkinter as tk
from tkinter import Menu
import requests

background_color = "#EEEFEF"
dark_purple = "#6D2492"
light_purple = "#B070C0"


window = tk.Tk()
window.configure(bg=background_color)
window.title("GOG Games Newsletter")

menubar = Menu(window)
window.config(menu=menubar)

filemenu = Menu(menubar, tearoff=False)
filemenu.add_command(label="Bye!", command=window.destroy)

menubar.add_cascade(label="File", menu=filemenu)

new_games = {}
updated_games = {}
game_list = []

with open("game_list", "r") as file:
    tmp_game_list = file.readlines()
    for game in tmp_game_list:
        game_list.append(game.replace("\n", ""))

##DEBUG
#print(game_list)
##

page = requests.get("https://gog-games.com/")

soup = BeautifulSoup(page.text, 'html.parser')

new_games_block = soup.findAll(class_='game-blocks grid-view')[0]
updated_games_block = soup.findAll(class_='game-blocks grid-view')[1]

new_games_page = new_games_block.findAll(class_='title')
new_last_update = new_games_block.findAll(class_='date')

updated_games_page = updated_games_block.findAll(class_='title')
updated_last_update = updated_games_block.findAll(class_='date')

##DEBUG
#print(new_games)
##

for idg, game in enumerate(new_games_page):
    if game.next_sibling.text == "NEW" and (" hours ago" in new_last_update[idg].text or " 1 day ago" in new_last_update[idg].text):
        new_games[game.text] = [game.next_sibling.text, new_last_update[idg].text.replace("\nLast Update: ",""), "POSSEDUTO" if game.text in game_list else "NON POSSEDUTO"]
    '''else:
        updated_games[game.text] = [game.next_sibling.text, last_update[idg].text.replace("\nLast Update: ",""), "POSSEDUTO" if game.text in game_list else "NON POSSEDUTO"]'''

for idg, game in enumerate(updated_games_page):
    #if " hours ago" in updated_last_update[idg].text or " 1 day ago" in updated_last_update[idg].text or " 2 days ago" in updated_last_update[idg].text:
    updated_games[game.text] = [game.next_sibling.text, updated_last_update[idg].text.replace("\nLast Update: ", ""),
                                    "POSSEDUTO" if game.text in game_list else "NON POSSEDUTO"]

#print(updated_games)
#exit(0)

new_string = "#-#-#-#-#- NEW GAMES -#-#-#-#-#\n"
print(new_string)
label = tk.Label(text=new_string, fg=dark_purple, bg=background_color, font="Helvetica 16 bold")
label.pack()
for game in new_games:
    if "NON POSSEDUTO" == new_games[game][2]:
        name = tk.Label(text=game, bg=background_color, fg=light_purple, font="Helvetica 12 bold")
        name.pack()
        lu = tk.Label(text=new_games[game][1]+"\n", bg=background_color, fg="black")
        lu.pack()
        print("{}\nLast Update: {}\n".format(game, new_games[game][1]))


update_string = "\n#-#-#-#-#- UPDATED -#-#-#-#-#\n"
print(update_string)
label = tk.Label(text=update_string, fg=dark_purple, bg=background_color, font="Helvetica 16 bold")
label.pack()
for game in updated_games:
    if "POSSEDUTO" == updated_games[game][2]:
        name = tk.Label(text=game, bg=background_color, fg=light_purple, font="Helvetica 12 bold")
        name.pack()
        #name.pack(anchor="w")
        lu = tk.Label(text=updated_games[game][1]+"\n", bg=background_color, fg="black")
        lu.pack()
        print("{}\nLast Update: {}\n".format(game, updated_games[game][1]))


window.mainloop()
