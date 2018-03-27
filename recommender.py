from collections import defaultdict
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


class Recommender(object):
    """
    A simple recommender based on text similarity
    """

    def __init__(self):
        """
        Just create the Tf-Idf vectorizer for reuse
        """
        self.__vec__ = TfidfVectorizer()
        self._tfidf = None
        self._y = None

    def fit(self, x, y):
        """
        Store given documents and labels
        """
        self._tfidf = self.__vec__.fit_transform(x)
        self._y = y
        return self

    def predict(self, x):
        """
        Find the most similar document and return labels
        """
        query = self.__vec__.transform(x)
        similarity = cosine_similarity(query, self._tfidf)
        results = []
        for result in similarity:
            # Make all results vote instead of just the best one
            votes = defaultdict(float)
            for labels, sim in zip(self._y, result):
                if not labels:
                    # Always return a label
                    continue
                key = tuple(labels)
                votes[key] += sim
            most_similar = max(votes.items(), key=lambda x: x[1])
            results.append(list(most_similar[0]))
        return results
