'''
    Testing the recommender
'''
import unittest

from recommender import Recommender


class RecommenderTesting(unittest.TestCase):

    def setUp(self):
        self.x = [
            'Implement neural network',
            'Tweak nearest neighbours algorithm',
            'Make money with cryptocurrencies and blockchain',
        ]
        self.y = [
            ['aa11bcde'],
            ['aa11bcde', 'bb22cdef'],
            ['bb22cdef']
        ]
        self.rec = Recommender().fit(self.x, self.y)

    def test_predictions(self):
        self.assertEqual(
            self.rec.predict(['Tweak neural network implementation']),
            [self.y[0]])

    def test_multiple(self):
        x = [
            'Tweak neural network implementation',
            'Implement neural network',
        ]
        y = [
            self.y[0],
            self.y[2],
        ]
        self.assertEqual(self.rec.predict(x), y)

    def test_crash(self):
        with self.assertRaises(TypeError):
            self.rec.predict(None)

        with self.assertRaises(AttributeError):
            self.rec.predict([None])


if __name__ == '__main__':
    unittest.main()
