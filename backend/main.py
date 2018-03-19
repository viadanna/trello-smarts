import json

from bottle import Bottle, abort, debug, request
from requests import get

from recommender import Recommender

app = Bottle()
debug(True)
cards_url = "https://api.trello.com/1/boards/{}/cards"

with open('settings.json') as f:
    settings = json.load(f)


@app.get('/predict')
def predict():
    """
    Label predicting endpoint, requires query strings:
        + board: the id of the board for reference
        + text: card text for the prediction
    """
    board = request.query.board
    if not board:
        abort(400, 'Missing board')
    text = request.query.text
    if not text:
        abort(400, 'Missing card title')
    cards = get(
        cards_url.format(board),
        params={'key': settings['key'], 'token': settings['token']}
    ).json()
    x_train = [c['name'] for c in cards]
    y_train = [c['idLabels'] for c in cards]
    rec = Recommender().fit(x_train, y_train)
    labels = rec.predict([text])[0]
    return json.dumps(labels)


if __name__ == '__main__':
    app.run(host='0.0.0.0')
