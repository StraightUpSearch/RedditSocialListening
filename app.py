from flask import Flask, request, jsonify
import praw
import logging

app = Flask(__name__)

# Configure Logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s %(levelname)s %(message)s')

# Configure Reddit API credentials
reddit = praw.Reddit(
    client_id='FSQYQli8O6HalmHROsOrKw',
    client_secret='CCDZBbffQOplorUKAaJtuYLVAlQGCg',
    user_agent='SocialListenerBot/0.1 by PossiblyAtWorkLOL'
)

@app.route('/')
def home():
    app.logger.debug('Home route accessed')
    return "Welcome to the Reddit Social Listening app!"

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    app.logger.debug(f'Search route accessed with query: {query}')
    if not query:
        app.logger.error('Query parameter is required')
        return jsonify({"error": "Query parameter is required"}), 400

    results = []
    try:
        for submission in reddit.subreddit('all').search(query, limit=10):
            results.append({
                'title': submission.title,
                'url': submission.url,
                'score': submission.score
            })
    except Exception as e:
        app.logger.error(f'Error during Reddit search: {e}')
        return jsonify({"error": "Internal server error"}), 500

    app.logger.debug(f'Search results: {results}')
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
