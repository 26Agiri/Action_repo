from flask import Flask, request, jsonify, render_template
from models import collection
from flask_cors import CORS
from datetime import datetime

app = Flask(__name__)
CORS(app)

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    event_type = request.headers.get('X-GitHub-Event')
    event = {}

    if event_type == 'push':
        event = {
            "type": "push",
            "author": data["pusher"]["name"],
            "to_branch": data["ref"].split("/")[-1],
            "timestamp": datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')
        }

    elif event_type == 'pull_request':
        pr = data["pull_request"]
        event = {
            "type": "pull_request",
            "author": pr["user"]["login"],
            "from_branch": pr["head"]["ref"],
            "to_branch": pr["base"]["ref"],
            "timestamp": datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')
        }

    elif event_type == 'merge_group':  # Optional Brownie Point
        event = {
            "type": "merge",
            "author": data["sender"]["login"],
            "from_branch": data["merge_group"]["head_ref"],
            "to_branch": data["merge_group"]["base_ref"],
            "timestamp": datetime.utcnow().strftime('%d %B %Y - %I:%M %p UTC')
        }

    if event:
        collection.insert_one(event)

    return '', 200

@app.route('/events', methods=['GET'])
def get_events():
    events = list(collection.find({}, {'_id': 0}))
    return jsonify(events)

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True, port=5000)
