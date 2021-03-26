#!/usr/bin/python3
import praw
import random
import requests

def main():
    titles = ["Your Daily Dose of Useless", "Sponsored By Geico", "You might want to know...", "BREAKING NEWS", "Important Mod Announcement", "Weather Report", "Terms of Service Update", "Forclosure", "2024 Elections", "5 Must Know Tricks For Gamers!", "Make Millions In 3 Easy Steps!", "Elon Musk Buys Reddit", "Message from Rick Astley", "Am I Gay? Find out NOW!!", "i plAY POKeMoN gO eVERY day", "We're no strangers to love", "You know the rules and so do I", "Never gonna make you cry", "Never gonna say goodbye", "W I D E   P U T I N", "Keanu Reeves", "Happy Little Trees", "Today's Gonna Be Great", "*Distraction Dance*", "Get Nae-Nae'd", "Noice!", "69", "YEET the child", "Task failed successfully", "say sike right now", "Me and the boys shitposting", "Joe MAMA! HA GOTEEM!", "Have COVID? It might be ligma!", "I have osteoperosis", "I dont care you broke ur elbow", "Where's Perry?", "PRESEDENTIAL ALERT", "Hacking into the mainframe...", "Got your nose!", "Im gonna do an internet!", "High five...HUNDRED!", "It's Muffin Time", "Oh boy what flavor? Pie Flavor", "No.", "Ogres are like onions: LAYERS!", "Coffin Dance"]

    reddit = praw.Reddit("CopyPasta")
    subreddit = reddit.subreddit('copypasta')
    widgets = subreddit.widgets
    widgets.refresh()
    w = subreddit.widgets.sidebar[1]
    if w.id != 'widget_15vtzwyzb170m':
        print('')
        return  # Quit the script

    choice = random.randrange(1,6)
    if choice == 1:
        # Generate random Long/Lat coords
        # Query weather API
        pass
    elif choice == 2:
        # Query a news API and get headlines
        pass
    elif choice == 3:
        # Pick a random user. Thats all.
        pass
    elif choice == 4:
        # Query a word generating API
        url = 'https://random-word.ryanrk.com/api/en/word/random'
        response = requests.get(url)
        word = response.json()[0]
        print(f'The word of the day is {word}\n')
        # ================================= #
        webster_api_key = 'b6f3f9e9-205b-4cf4-9ef1-8d37451f098a'
        url = f'https://dictionaryapi.com/api/v3/references/collegiate/json/{word}?key={webster_api_key}'
        response = requests.get(url).json()
        print(f'Definition: {response}')

        # Query a dictionary API

if __name__ == "__main__":
    main()



# Pick a number btw 1 and 5, and pick a corresponding content from the list below
    # Generate




return
'''
Content:

1) Weather for a random Long/Lat
2) Random Headlines
3) Random user / subreddit
4) Word of the Day
    a) random definition?
5) The contents of the most recent submission and or comment to Reddit at the time of code execution
'''
