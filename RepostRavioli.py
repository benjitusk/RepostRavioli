#!/usr/bin/python3
import os
import sys
import math
import time
import praw
import json
import bot_strings
import signal
from nltk.tokenize import word_tokenize
PUBLIC = True
ratelimit_active = False
threshhold = 0.86


def main():
    try:
        # raw = []
        # log('Loading the last 90 days of submissions...')
        # for file in os.listdir("pushshift"):
        #     if file.endswith(".json"):
        #         with open(f'pushshift/{file}') as f:
        #             month_data = json.load(f)
        #             for sub in month_data:
        #                 raw.append(sub)
        # previous_submissions = []
        # for sub in raw:
        #     sub = sub[len(sub)-1]
        #     url = attr(sub, 'url')
        #     text = attr(sub, 'selftext')
        #     previous_submissions.append({'url':url,'text':text})
        # raw = []
        #
        # log('Done.')
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
                # if check_for_repost(submission):
                #     mark_repost(submission)
                #     continue
                if not submission.over_18 and scan_for_nsfw(submission):
                    mark_nsfw(submission)
                    nsfw += 1
                else:
                    reg += 1
        # spam_status = scan_for_spam(submission)
                # if spam_status is not False:
                #     mark_spam(submission, spam_status)
    except KeyboardInterrupt:
        return
    except Exception as e:
        print(e)
        main()


def scan_for_nsfw(submission):
    tokens = get_tokens(submission)
    return any(word in tokens for word in bot_strings.NSFW_STRINGS)


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
            reply = submission.author.message(
                'Evil NSFW Filter Muahahaha', bot_strings.NSFW_FLAG_MESSAGE)
            print(f'https://www.reddit.com{submission.permalink}')
            write_to_log(submission.id)
            show_stats()
        except praw.exceptions.RedditAPIException:
            delete_last_line()
            log(f'Ratelimited! Not alerting user.')
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


def check_for_repost(submission):
    return False
    for sub in previous_submissions:
        text = sub['text']
        if text is not None:
            if attr(sub, 'selftext') in text:
                return True
        return False


def mark_repost(submission):
    pass


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
            f'Regular: 0\t|NSFW: 0\t|Average NSFW: 0%\t|Total: 0\t|RateLimit Active: False')
#################################
##      FORMAT FUNCTIONS       ##
#################################


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


#################################
##      DRIVING FUNCTION       ##
#################################
if __name__ == "__main__":
    signal.signal(signal.SIGHUP, acknowledgeSIGHUP)
    main()

#
#
# def mark_spam(submission, stats):
#     if PUBLIC:
#         try:
#             reply = submission.reply(
#                 bot_strings.SPAM_FLAG_MESSAGE.format(submission.author.name))
#         except Exception as e:
#             print(f'{e.__class__} occurred. Not alerting user.')
#         finally:
#             print(
#                 f'Flagged a post by u/{submission.author.name} as SPAM here: https://www.reddit.com{reply.permalink}')
#         submission.mod.nsfw()
#         with open('sumbissions_flagged_as_spam.txt', 'a') as file:
#             file.write(f'https://www.reddit.com{submission.permalink}')
#     else:
#         print(
#             f'https://www.reddit.com{submission.permalink} by {submission.author.name} was a {round(stats[0]*10000)/100}% match with {stats[1]}')
#
#
# def scan_for_spam(master):
#     start = time()
#     sub_count = 0
#     total = len(september) - 1
#     print()
#     for sub in september:
#         end = time()
#         delete_last_line()
#         print(
#             f'Evaluting september[{sub_count}/{total}]: {round((sub_count/total)*100)}%... {math.floor(end-start)} seconds')
#         sub_count += 1
#         sim = get_similarity(master, sub)
#         if sim > threshhold:
#             print(f'\n\n{sim} > {threshhold}')
#             print(
#                 f'Time elapsed to get True result: {round(end-start)} seconds')
#             return [sim, 'https://www.reddit.com' + attr(sub, 'permalink')]
#     end = time()
#     print(f'Time elapsed to get False result: {(end-start)} seconds')
#     return False
#
#
# def get_similarity(sub1, sub2):
#     if attr(sub1, 'id') == attr(sub2, 'id'):
#         return 0.0
#     if attr(sub1, 'author') in ['[deleted]', '[removed]'] or attr(sub2, 'author') in ['[deleted]', '[removed]']:
#         return 0.0
#     if not abs(len(attr(sub1, 'selftext')) - len(attr(sub2, 'selftext'))) < len(attr(sub1, 'selftext')) * 1.5:
#         return 0.0
#     tokens1 = get_tokens(sub1)
#     tokens2 = get_tokens(sub2)
#     if tokens1 == False or tokens2 == False:
#         return 0.0
#     if abs(len(tokens1) - len(tokens2)) < len(tokens1) * 0.15:
#         return 0.0
#     processed1 = process_text(tokens1)
#     processed2 = process_text(tokens2)
#     return compare(processed1, processed2)
#
#
# def process_text(tokens):
#     words = [w.lower() for w in tokens]
#     porter = nltk.PorterStemmer()
#     stemmed_tokens = [porter.stem(t) for t in words]
#     stop_words = set(stopwords.words('english'))
#     filtered_tokens = [w for w in stemmed_tokens if not w in stop_words]
#     count = nltk.defaultdict(int)
#     for word in filtered_tokens:
#         count[word] += 1
#     return count
#
#
# def cos_sim(a, b):
#     dot_product = np.dot(a, b)
#     norm_a = np.linalg.norm(a)
#     norm_b = np.linalg.norm(b)
#     return dot_product / (norm_a * norm_b)
#
#
# def compare(dict1, dict2):
#     if not (dict1 and dict2):
#         return 0.0
#     all_words_list = []
#     for key in dict1:
#         all_words_list.append(key)
#     for key in dict2:
#         all_words_list.append(key)
#     all_words_list_size = len(all_words_list)
#     v1 = np.zeros(all_words_list_size, dtype=np.int)
#     v2 = np.zeros(all_words_list_size, dtype=np.int)
#     i = 0
#     for (key) in all_words_list:
#         v1[i] = dict1.get(key, 0)
#         v2[i] = dict2.get(key, 0)
#         i += 1
#     return cos_sim(v1, v2)
#
#


def test_nsfw_string(test_string):  # Manual testing
    from nltk.tokenize import word_tokenize
    NSFW_STRINGS = ['cum', 'sex', 'cock', 'nigger', 'cunt', 'dick',
                    'vagina', 'boobs', 'tits', 'penis', 'hentai', 'sex toy',
                    'kinky', 'bdsm', 'butt plug', 'dildo', 'strap on', 'slut']
    tokens = word_tokenize(test_string)
    return any(word in tokens for word in NSFW_STRINGS)
