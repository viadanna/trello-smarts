Trello Assistant
================

Bringing artificial intelligence to your boards and cards.

A proof of concept assistant that suggests labels based on card titles.

Notice that this is a work in progress, but is functional.

Usage:
------

This application can be deployed to Heroku.

Before building service, make sure to update `settings.py` with
the developer key and token to be used.
```
{
    "key": "your developer key"
}
```

The key must also be updated in `public/auth.html:13`

There's a live server that can be used for testing by creating a power-up
with url:
```
https://pure-wave-30477.herokuapp.com/index.html
```

Implementation:
---------------

The current proof of concept implementation takes a board id and card title
to generate a prediction. It then queries Trello restful API to fetch all cards
for the given board, storing their titles and labels. Finally, it find the
term frequency/inverse document frequency vectors for the titles and uses
cosine distance to find the most similar, returning its labels.

Contents:
---------

+ server.py
    Web service implementation.

+ recommender.py
    Label recommendation implementation.

+ requirements.txt
    List of python libraries needed.

+ settings.py
    Configuration.

+ tests.py
    Unit testing.

+ public/index.html
    Trello power-up main point of entry.

+ public/auth.html
    Power-up authentication.


Requirements:
-------------

+ Python, tested on v3.5.2.
+ Bottle, for web service.
+ requests, for querying Trello API.
+ scikit-learn, for text vectorizing and similarity metric.

Make sure to check the `requirements.txt` file for further information.