#
# @author:Don Dennis (metastableB)
# featureExtractor.py
#


class FeatureExtractor():
    '''
    Extractor features from the current gameState
    using the getFeatures method.

    Exposes:
    getFeatureKeys(): Returns list of string keys to the features
        extracted.
    getFeatures(gameState): Returns a dict of {featueKey:value}

    '''

    def __init__(self):
        pass

    def getFeatures(self, gameState):
        pass

    def getFeatureKeys(self):
        return self.featureKeys


class SimpleFeatureExtractor(FeatureExtractor):
    '''
    A very simple feature extractor for approx Q-learning.
    '''

    def __init__(self):
        self.featureKeys = ['Circular Manhattan Index']

    def getFeatures(self, gameState):
        return 0.0


if __name__ == '__main__':
    sfe = SimpleFeatureExtractor()
    print(dir(sfe))
