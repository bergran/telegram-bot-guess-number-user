# coding: utf-8

from bernard.engine import (
    Tr,
    triggers as trg,
)

from bernard.platforms.telegram import layers

from .state import S001xWelcome, S002xGuessANumber, S003xGuessAgain, S004xCongrats
from .trigger import Number

transitions = [
    Tr(
        dest=S001xWelcome,
        factory=trg.Equal.builder(layers.BotCommand('/start')),
    ),
    Tr(
        dest=S002xGuessANumber,
        origin=S001xWelcome,
        factory=trg.Action.builder('play'),
    ),
    Tr(
        dest=S003xGuessAgain,
        origin=S002xGuessANumber,
        factory=Number.builder(is_right=False),
    ),
    Tr(
        dest=S003xGuessAgain,
        origin=S003xGuessAgain,
        factory=Number.builder(is_right=False),
    ),
    Tr(
        dest=S004xCongrats,
        origin=S003xGuessAgain,
        factory=Number.builder(is_right=True),
    ),
    Tr(
        dest=S004xCongrats,
        origin=S002xGuessANumber,
        factory=Number.builder(is_right=True),
    ),
    Tr(
        dest=S002xGuessANumber,
        origin=S004xCongrats,
        factory=trg.Action.builder('again'),
    ),
]
