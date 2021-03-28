"""Providers configuration.

See: https://bocadilloproject.github.io/guides/injection/
"""
from bocadillo import provider
from .chatbot import Lepios
from . import words, model, stemmer, classes, intents

# Define providers below.

@provider(scope="app")
def lepios():
    lepios = Lepios(model=model, ERR_THRESHOLD=0.2, stemmer=stemmer,
                    words=words, classes=classes, intents=intents)
    return lepios
