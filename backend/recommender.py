from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np


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
        most_similar = np.argmax(similarity, axis=1)
        return [self._y[i] for i in most_similar]
