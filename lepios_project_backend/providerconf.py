"""Providers configuration.

See: https://bocadilloproject.github.io/guides/injection/
"""
from bocadillo import provider
from .chatbot import Lepios
from .symptom_prediction import SymptomPrediction
from . import words, model, stemmer, classes, intents, words_symptoms, model_symptoms, classes_symptoms, symptoms

# Define providers below.


@provider(scope="app")
def lepios():
    lepios = Lepios(model=model, ERR_THRESHOLD=0, stemmer=stemmer,
                    words=words, classes=classes, intents=intents)
    return lepios


@provider(scope="app")
def symptom_prediction():
    symptom_prediction = SymptomPrediction(model=model_symptoms, ERR_THRESHOLD=0,
                                           stemmer=stemmer, words=words_symptoms, classes=classes_symptoms, intents=symptoms)
    return symptom_prediction
