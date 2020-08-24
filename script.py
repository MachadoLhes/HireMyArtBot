import praw, requests
from googletrans import Translator

reddit = praw.Reddit(client_id = 'efGYc-LFh4aYow',
					 client_secret = 'qsQhjkiEKTGlEQQiXBYMEOViFCc',
					 username = 'hiremyartbot',
					 password = 'm35L^7NmNTtBtnYS',
					 user_agent = 'art_listener')

translator = Translator()

subreddit = reddit.subreddit('hungryartists')

def create_bot_message(submission):
	tittle_pt = translator.translate(submission.title, dest='pt', src='en')

	message = ""	
	message += tittle_pt.text + '\n'
	message += submission.url + '\n'

	return message

def telegram_bot_sendtext(bot_message):
    
    bot_token = '1226525498:AAGDP1-n91fRbSskv1lzL_9cUXLeeKadBrg'
    bot_chatID = '@hiremyartchannel'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def main():
	for submission in subreddit.stream.submissions():
		if submission.link_flair_text == 'Hiring':
			message = create_bot_message(submission)
			telegram_bot_sendtext(message)		

if __name__ == "__main__":
    main()