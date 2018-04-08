import json
import os
import re

from bottle import Bottle, abort, debug, request, static_file
from requests import get, post

from recommender import Recommender

app = Bottle()
debug(True)

card_url = "https://api.trello.com/1/cards/{}"
cards_url = "https://api.trello.com/1/boards/{}/cards"
label_url = "https://api.trello.com/1/cards/{}/idLabels"

with open('.env') as f:
    settings = dict(line.split('=', 1) for line in f.readlines())


def get_text(card):
    name = card['name']
    desc = card['desc'].replace('\n', ' ')
    text = '{} {}'.format(name, desc)
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text


@app.get('/predict/<card_id>')
def predict(card_id):
    """
    Label predicting endpoint, requires query strings:
        + board: the id of the board for reference
        + text: card text for the prediction
    """
    token = request.query.token  # pylint disable=E1101
    if not token:
        abort(400, 'Missing token')

    # Fetch card name and full description
    card = get(
        card_url.format(card_id),
        params={'key': settings['KEY'], 'token': token}
    ).json()

    # Fetch all cards in board
    board = card['idBoard']
    cards = get(
        cards_url.format(board),
        params={'key': settings['KEY'], 'token': token}
    ).json()

    # Train model with board cards
    x_train = [get_text(c) for c in cards if c['id'] != card]
    y_train = [c['idLabels'] for c in cards]
    rec = Recommender().fit(x_train, y_train)

    # Predict labels for given card
    labels = rec.predict([get_text(card)])[0]
    for label in labels:
        post(
            label_url.format(card_id),
            params={'value': label, 'key': settings['KEY'], 'token': token}
        )
    return json.dumps(labels)


@app.route('/<filepath:path>')
def serve_public(filepath):
    return static_file(filepath, root='public/')


if __name__ == '__main__':
    port = os.getenv('PORT', 8080)
    app.run(host='0.0.0.0', port=port)
