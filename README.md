Trello Assistant
================

Bringing artificial intelligence to your boards and cards.

A proof of concept assistant that suggests labels based on card titles.

Notice that this is a work in progress and contains just the backend for now.

Usage:
------

This application can be run using Docker composer and using the API endpoint
at port 8080.

Before building service, make sure to update `settings.py` with
the developer key and token to be used.
```
{
    "key": "your developer key",
    "token": "authorization token"
}
```

Starting the service:
```
$ docker-composer up
```

Predict labels for card based on the given board cards and labels
```
$ curl "localhost:8080/predict?board=<board_id>&text=<card_title>"
```


Implementation:
---------------

The current proof of concept implementation takes a board id and card title
to generate a prediction. It then queries Trello restful API to fetch all cards
for the given board, storing their titles and labels. Finally, it vectorizes
the titles and uses cosine distance to find the most similar, returning its
labels.

Contents:
---------

+ backend/main.py
    Web service implementation.

+ backend/recommender.py
    Label recommendation implementation.

+ backend/requirements.txt
    List of python libraries needed.

+ backend/settings.py
    Configuration variables.

+ backend/tests.py
    Unit testing.

+ docker-compose.yml
    Docker composer configuration to run service.

+ Dockerfile
    Docker configuration for container.

Requirements:
-------------

+ Python, tested on v3.5.2.
+ Bottle, for web service.
+ requests, for querying Trello API.
+ scikit-learn, for text vectorizing and similarity metric.

Make sure to check the `requirements.txt` file for further information.