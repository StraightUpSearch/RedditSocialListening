from flask import Flask, request, jsonify
import praw

app = Flask(__name__)

# Configure Reddit API credentials
reddit = praw.Reddit(
    client_id='FSQYQli8O6HalmHROsOrKw',
    client_secret='CCDZBbffQOplorUKAaJtuYLVAlQGCg',
    user_agent='SocialListenerBot/0.1 by PossiblyAtWorkLOL'
)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({"error": "Query parameter is required"}), 400

    results = []
    for submission in reddit.subreddit('all').search(query, limit=10):
        results.append({
            'title': submission.title,
            'url': submission.url,
            'score': submission.score
        })

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
