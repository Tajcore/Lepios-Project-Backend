import nltk
import random
import numpy as np

class Lepios:
    def __init__(self, model, ERR_THRESHOLD, stemmer, words, classes, intents):
        self.model = model
        self.ERR_THRESHOLD = ERR_THRESHOLD
        self.stemmer = stemmer
        self.classes = classes
        self.intents = intents
        self.words = words

    def clean_up_sentence(self, sentence):
        # It Tokenize or Break it into the constituents parts of Sentense.
        sentence_words = nltk.word_tokenize(sentence)
        # Stemming means to find the root of the word.
        sentence_words = [self.stemmer.stem(word.lower())
                          for word in sentence_words]
        return sentence_words
        # Return the Array of Bag of Words: True or False and 0 or 1 for each word of bag that exists in the Sentence

    def bow(self, sentence, words, show_details=False):
        print(sentence)
        sentence_words = self.clean_up_sentence(sentence)
        bag = [0]*len(words)
        for s in sentence_words:
            for i, w in enumerate(words):
                if w == s:
                    bag[i] = 1
                    if show_details:
                        print("found in bag: %s" % w)
        return(np.array(bag))

    def classify(self, sentence):
        # Prediction or To Get the Posibility or Probability from the Model

        bow = self.bow(sentence, self.words)
        results = self.model.predict([bow])[0]
        # Exclude those results which are Below Threshold
        results = [[i, r]
                   for i, r in enumerate(results) if r > self.ERR_THRESHOLD]
        # Sorting is Done because heigher Confidence Answer comes first.
        results.sort(key=lambda x: x[1], reverse=True)
        return_list = []
        for r in results:
            # Tuppl -> Intent and Probability
            return_list.append((self.classes[r[0]], r[1]))
        return return_list

    def response(self, sentence, userID, show_details=False):
        results = self.classify(sentence)
        # That Means if Classification is Done then Find the Matching Tag.
        if results:
            # Long Loop to get the Result.
            while results:
                for i in self.intents['intents']:
                    # Tag Finding
                    if i['tag'] == results[0][0]:
                        # Random Response from High Order Probabilities
                        return print(random.choice(i['responses']))
                results.pop(0)
