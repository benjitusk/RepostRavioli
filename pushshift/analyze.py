#!/usr/bin/python3
from datetime import datetime
import re
import os
import json
import time
import calendar

now = datetime.now()

def main():
    sub_char_count = {}
    com_char_count = {}
    sub_emoji_count = {}
    com_emoji_count = {}
    sub_authors = {}
    com_authors = {}
    sub_word_count = {}
    com_word_count = {}
    sub_scoring_tier = {'<=0': [], '==1': [], '<=10': [], '<=50': [
    ], '<=100': [], '<=500': [], '<=1000': [], '<=5000': [], '>5000': []}
    total_sub_chars = 0
    total_com_chars = 0
    total_sub_words = 0
    total_com_words = 0
    total_sub_emojis = 0
    total_com_emojis = 0
    removed_subs = 0
    removed_coms = 0
    nsfw_posts = 0
    total_subs = 0


    month = input('What month do you want statistics of? ').lower()
    files = []
    for file in os.listdir('/home/music/reddit_bots/RepostRavioli/pushshift'):
        if file.startswith(month) and file.endswith('.json') and len(file.split('.')) == 4:      # month.year.type.JSON
            files.append(file)
    if len(files) == 0:
        print(f'No archives for the month beginning with "{month}". Exiting...')
        exit()
    for file in files:
            print(f'Opening ./{file}')
            file_data = file.split('.')
            type = file_data[2]         # month.year.TYPE.json
            year = file_data[1]         # month.YEAR.type.json
            month = file_data[0]        # MONTH.year.type.json
            with open(f'/home/music/reddit_bots/RepostRavioli/pushshift/{file}') as subreddit_json:
                print(f'Loading {type} for {month.capitalize()} {year}...')
                data = json.load(subreddit_json)
                print(
                    f'Loaded {type}. Data analysis starting at {time.ctime()}')
                if type == 'submissions':
                    total_subs = len(data)
                    top_score = data[0][len(data[0]) - 1]
                    bottom_score = data[0][len(data[0]) - 1]
                    for sub in data:
                        info = sub[len(sub) - 1]
                        if info['author'] in ['[deleted]', ['removed']]:
                            removed_subs += 1
                            continue
                        body = info['selftext']
                        title = info['title']
                        author = info['author']
                        score = info['score']
                        if info['over_18'] == True:
                            nsfw_posts += 1
                        text_contents = (body + ' ' + title)
                        if score <= 0:
                            sub_scoring_tier['<=0'].append(info)
                        elif score == 1:
                            sub_scoring_tier['==1'].append(info)
                        elif score <= 10:
                            sub_scoring_tier['<=10'].append(info)
                        elif score <= 50:
                            sub_scoring_tier['<=50'].append(info)
                        elif score <= 100:
                            sub_scoring_tier['<=100'].append(info)
                        elif score <= 500:
                            sub_scoring_tier['<=500'].append(info)
                        elif score <= 1000:
                            sub_scoring_tier['<=1000'].append(info)
                        elif score <= 5000:
                            sub_scoring_tier['<=5000'].append(info)
                        elif score > 5000:
                            sub_scoring_tier['>5000'].append(info)
                        if score > top_score['score']:
                            top_score = info
                        if score < bottom_score['score']:
                            bottom_score = info
                        words = re.split(' |\n', text_contents)
                        # Removes empty elements
                        words = [i for i in words if i]
                        for word in words:
                            total_sub_words += 1
                            sub_word_count = count_occurances(
                                word, sub_word_count)
                            for letter in word:
                                total_sub_chars += 1
                                sub_char_count = count_occurances(
                                letter, sub_char_count)
                        sub_authors = count_occurances(author, sub_authors)
                    print('Done.')
                if type == 'comments':
                    total_coms = len(data)
                    top_com = data[0][len(data[0]) - 1]
                    bottom_com = data[0][len(data[0]) - 1]
                    for com in data:
                        info = com[len(com) - 1]
                        author = info['author']
                        if info['author'] in ['[deleted]', ['removed']]:
                            removed_coms += 1
                            continue
                        score = info['score']
                        body = info['body']
                        words = re.split(' |\n', body)
                        # Removes empty elements
                        words = [i for i in words if i]
                        for word in words:
                            total_com_words += 1
                            com_word_count = count_occurances(
                                word, com_word_count)
                            for letter in word:
                                total_com_chars += 1
                                com_char_count = count_occurances(
                                letter, com_char_count)
                        com_authors = count_occurances(author, com_authors)
                    print('Done.')
            print('Sorting data...')
            for char in sub_char_count:
                if is_emoji(char):
                    total_sub_emojis += 1
                    sub_emoji_count = count_occurances(
                        char, sub_emoji_count)
            for char in com_char_count:
                if is_emoji(char):
                    total_com_emojis += 1
                    com_emoji_count = count_occurances(
                        char, com_emoji_count)
            sub_emoji_count = sort_dict(sub_emoji_count, False)
            com_emoji_count = sort_dict(com_emoji_count, False)
            sub_char_count = sort_dict(sub_char_count)
            com_char_count = sort_dict(com_char_count)
            sub_word_count = sort_dict(sub_word_count)
            com_word_count = sort_dict(com_word_count)
            sub_authors = sort_dict(sub_authors)
            com_authors = sort_dict(com_authors)
            print('Done.\n\n')
    # Now that we've compiled the data, we now have to make it presentable:\
    print(
        f'Total Submissions:\t\t{total_subs} [Regular: {total_subs - nsfw_posts}|NSFW: {nsfw_posts}]')
    print(f'Total Comments:\t\t\t{total_coms} [Regular: {total_coms-removed_coms}|Removed: {removed_coms}]')
    print(
        f'Most active submitter:\t\t{get_first_item(sub_authors)[0][0]}\t| {get_first_item(sub_authors)[0][1]}')
    print(
        f'Most active commenter:\t\t{get_first_item(com_authors)[0][0]}\t| {get_first_item(com_authors)[0][1]}')
    print(
        f'\nEmoji count:\t\t\t[Submissions: {total_sub_emojis}\t| Comments: {total_com_emojis}\t| Total: {total_sub_emojis + total_com_emojis}]')
    print(
        f'Word count:\t\t\t[Submissions: {total_sub_words}\t| Comments: {total_com_words}\t| Total: {total_sub_words + total_com_words}]')
    print(
        f'Character count:\t\t[Submissions: {total_sub_chars}\t| Comments: {total_com_chars}\t| Total: {total_sub_chars + total_com_chars}]')
    # print(
    #     f'Most popular emoji:\t\t[Submissions: "{get_first_item(sub_emoji_count)[0][0]}": {get_first_item(sub_emoji_count)[0][1]}\t| Comments: "{get_first_item(com_emoji_count)[0][0]}": {get_first_item(com_emoji_count)[0][1]}]')
    # print(
    #     f'Most popular word:\t\t[Submissions: "{get_first_item(sub_word_count)[0][0]}": {get_first_item(sub_word_count)[0][1]}\t| Comments: "{get_first_item(com_word_count)[0][0]}": {get_first_item(com_word_count)[0][1]}]')
    # print(
    #     f'Most popular character:\t\t[Submissions: "{get_first_item(sub_char_count)[0][0]}": {get_first_item(sub_char_count)[0][1]}\t| Comments: "{get_first_item(com_char_count)[0][0]}": {get_first_item(com_char_count)[0][1]}]')
    print('\nSubmission breakdown:')
    high_score_karma = top_score['score']
    high_score_author = top_score['author']
    high_score_awards = len(top_score['all_awardings'])
    high_score_link = top_score['permalink']
    tier0 = len(sub_scoring_tier['<=0'])
    tier1 = len(sub_scoring_tier['==1'])
    tier2 = len(sub_scoring_tier['<=10'])
    tier3 = len(sub_scoring_tier['<=50'])
    tier4 = len(sub_scoring_tier['<=100'])
    tier5 = len(sub_scoring_tier['<=500'])
    tier6 = len(sub_scoring_tier['<=1000'])
    tier7 = len(sub_scoring_tier['<=5000'])
    tier8 = len(sub_scoring_tier['>5000'])
    print(f'Submissions scored <= 0:\t{tier0}')
    print(f'Submissions scored == 1:\t{tier1}')
    print(f'Submissions scored <= 10:\t{tier2}')
    print(f'Submissions scored <= 50:\t{tier3}')
    print(f'Submissions scored <= 100:\t{tier4}')
    print(f'Submissions scored <= 500:\t{tier5}')
    print(f'Submissions scored <= 1000:\t{tier6}')
    print(f'Submissions scored <= 5000:\t{tier7}')
    print(f'Submissions scored > 5000:\t{tier8}')
    print(f'Highest scoring submission: {high_score_karma} by {high_score_author} with {high_score_awards} awards here: https://www.reddit.com{high_score_link}')


def is_emoji(char):
    code = ord(char)
    return ((code >= 0x203c and code <= 0x3299) or (code >= 0x1f000 and code <= 0x1f64f))


def sort_dict(dict, rev = True):
    return {k: v for k, v in sorted(
        dict.items(), reverse=rev, key=lambda item: item[1])}


def get_first_item(dict, amount=1):
    top_items = []
    for n in range(amount):
        top_items.append([list(dict)[n], dict[list(dict)[n]]])
    return top_items


def count_occurances(item, array):
    if item in array:
        array[item] += 1
    else:
        array[item] = 1
    return array


def months(num):
    month = now.month
    year = now.year
    list_of_months = []
    for n in range(num):
        n += 1
        if month - n <= 0:
            month += 12
            year -= 1
        list_of_months.append(calendar.month_name[(month - n)].lower())
    return list_of_months


if __name__ == '__main__':
    main()
