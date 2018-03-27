import json
import os

from bottle import Bottle, abort, debug, request, static_file
from requests import get, post

from recommender import Recommender

app = Bottle()
debug(True)

cards_url = "https://api.trello.com/1/boards/{}/cards"
label_url = "https://api.trello.com/1/cards/{}/idLabels"

with open('settings.json') as f:
    settings = json.load(f)


@app.get('/predict')
def predict():
    """
    Label predicting endpoint, requires query strings:
        + board: the id of the board for reference
        + text: card text for the prediction
    """
    token = request.query.token
    if not token:
        abort(400, 'Missing token')
    board = request.query.board
    if not board:
        abort(400, 'Missing board')
    card = request.query.card
    if not card:
        abort(400, 'Missing card')
    text = request.query.text
    if not text:
        abort(400, 'Missing card title')
    cards = get(
        cards_url.format(board),
        params={'key': settings['key'], 'token': token}
    ).json()
    x_train = [c['name'] for c in cards if c['id'] != card]
    y_train = [c['idLabels'] for c in cards]
    rec = Recommender().fit(x_train, y_train)
    labels = rec.predict([text])[0]
    for label in labels:
        res = post(
            label_url.format(card),
            params={'value': label, 'key': settings['key'], 'token': token}
        )
        print(res.text)
    return json.dumps(labels)


@app.route('/<filepath:path>')
def serve_public(filepath):
    return static_file(filepath, root='public/')


if __name__ == '__main__':
    port = os.getenv('PORT', 8080)
    app.run(host='0.0.0.0', port=port)
