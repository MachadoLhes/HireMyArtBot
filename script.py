import praw, requests, os
from googletrans import Translator

reddit = praw.Reddit(client_id = os.environ['REDDIT_CLIENT_ID'],
					 client_secret = os.environ['REDDIT_CLIENT_SECRET'],
					 username = 'hiremyartbot',
					 password = os.environ['REDDIT_PWD'],
					 user_agent = 'art_listener')

translator = Translator()

subreddit = reddit.subreddit('hungryartists+artcommissions+commissions+DrawForMe')

def filter_title(title):
	return title.replace('&','n')

def create_bot_message(submission):
	title = filter_title(submission.title)
	title_pt = translator.translate(title, dest='pt', src='en')

	message = ""	
	message += title_pt.text + '\n'
	message += 'https://reddit.com' + submission.permalink + '\n'

	return message

def telegram_bot_sendtext(bot_message):
    
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    bot_chatID = '@hiremyartchannel'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

	print("There has been a new post! > {}".format(title))

    return response.json()

def main():
	for submission in subreddit.stream.submissions():
		title = submission.title.lower()
		try:
			flair = submission.link_flair_text.lower()
		except:
			flair = ''
		if 'hiring' in title or 'paid request' in flair:
			message = create_bot_message(submission)
			telegram_bot_sendtext(message)	
			# print(message)
				

if __name__ == "__main__":
    main()