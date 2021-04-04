#!/usr/bin/python3
import os
import sys
import math
import time
import praw
import bot_strings
import signal
from nltk.tokenize import word_tokenize
PUBLIC = True
ratelimit_active = False
threshhold = 0.86


def main():
    global submissions_examined
    global reg
    global nsfw
    log('\nLogging in to Reddit as /u/RepostRavioli...')
    reddit = praw.Reddit("CopyPasta")
    log('Login successful.')

    log('Loading examined submissions...')
    if not os.path.isfile('submissions_examined.txt'):  # If file does not exist
        submissions_examined = []   # create an empty list (A.K.A. array)
    else:   # But if the file does exist
        with open('submissions_examined.txt') as f:  # open it
            submissions_examined = f.read()  # read it and store it as 'f'
            # Seperate items by newline and store as list
            submissions_examined = submissions_examined.split('\n')
            # Remove empty values
            submissions_examined = list(filter(None, submissions_examined))
    log('Done.')
    subreddit = reddit.subreddit("copypasta")
    log('Awating submissions...')
    print()
    reg = 0
    nsfw = 0
    show_stats()
    for submission in subreddit.stream.submissions(pause_after=0):
        if submission is None:
            continue
        if submission.id not in submissions_examined:
            examine_submission(submission)
            if not submission.over_18 and scan_for_nsfw(submission):
                mark_nsfw(submission)
                nsfw += 1
            else:
                reg += 1


def scan_for_nsfw(submission):
    return any(word in get_tokens(submission) for word in bot_strings.NSFW_STRINGS)


def examine_submission(submission):
    if PUBLIC:
        global submissions_examined
        submissions_examined.append(submission.id)
        with open('submissions_examined.txt', 'a') as file:
            file.write(submission.id + '\n')


def mark_nsfw(submission):
    if PUBLIC:
        global ratelimit_active
        try:
            delete_last_line()
            submission.author.message(
                'Evil NSFW Filter Muahahaha', bot_strings.NSFW_FLAG_MESSAGE)
            print(f'https://www.reddit.com{submission.permalink}')
            write_to_log(submission.id)
            show_stats()
        except praw.exceptions.RedditAPIException:
            delete_last_line()
            log('Ratelimited! Not alerting user.')
            show_stats()
            ratelimit_active = True
        else:
            ratelimit_active = False
        finally:
            submission.mod.nsfw()
            with open('sumbissions_flagged.txt', 'a') as file:
                file.write(f'https://www.reddit.com{submission.permalink}\n')
    else:
        delete_last_line()
        print(f'{submission.author.name}')
        show_stats()


def get_tokens(submission):
    return word_tokenize(submission.selftext + ' ' + submission.title)


def attr(object, attribute):
    if hasattr(object, attribute):
        return getattr(object, attribute)
    else:
        try:
            return object[attribute]
        except:
            return None


def show_stats():
    global ratelimit_active
    global reg
    global nsfw
    try:
        print(
            f'Regular: {reg}\t|NSFW: {nsfw}\t|Average NSFW: {math.floor(nsfw/(nsfw+reg)*100)}%\t|Total: {reg+nsfw}\t|RateLimit Active: {ratelimit_active}')
    except ZeroDivisionError:
        print(
            'Regular: 0\t|NSFW: 0\t|Average NSFW: 0%\t|Total: 0\t|RateLimit Active: False')


def delete_last_line(n=1):
    for _ in range(n):
        sys.stdout.write('\x1b[1A')  # CURSOR UP ONE LINE
        sys.stdout.write('\x1b[2K')  # ERASE LINE


def log(data):
    print(data)
    write_to_log(data)


def write_to_log(data):
    with open('bot_log.txt', 'a') as log_file:
        log_file.write(f'[{time.ctime()}]:\t{data}\n')


def acknowledgeSIGHUP(a, b):
    log('Registered SSH session disconnect, process still running in the background')


if __name__ == "__main__":
    signal.signal(signal.SIGHUP, acknowledgeSIGHUP)
    main()
