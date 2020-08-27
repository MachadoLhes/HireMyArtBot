import praw, requests, os
from googletrans import Translator

reddit = praw.Reddit(client_id = os.environ['REDDIT_CLIENT_ID'],
					 client_secret = os.environ['REDDIT_CLIENT_SECRET'],
					 username = 'hiremyartbot',
					 password = os.environ['REDDIT_PWD'],
					 user_agent = 'art_listener')

translator = Translator()

subreddit = reddit.subreddit('hungryartists+artcommissions')

def create_bot_message(submission):
	tittle_pt = translator.translate(submission.title, dest='pt', src='en')

	message = ""	
	message += tittle_pt.text + '\n'
	message += submission.url + '\n'

	return message

def telegram_bot_sendtext(bot_message):
    
    bot_token = os.environ['TELEGRAM_BOT_TOKEN']
    bot_chatID = '@hiremyartchannel'
    send_text = 'https://api.telegram.org/bot' + bot_token + '/sendMessage?chat_id=' + bot_chatID + '&parse_mode=Markdown&text=' + bot_message

    response = requests.get(send_text)

    return response.json()

def main():
	for submission in subreddit.stream.submissions():
		flair = submission.link_flair_text
		if flair == 'Hiring' or flair == '[Hiring]' :
			message = create_bot_message(submission)
			telegram_bot_sendtext(message)	
			print("There has been a new post!")	

if __name__ == "__main__":
    main()