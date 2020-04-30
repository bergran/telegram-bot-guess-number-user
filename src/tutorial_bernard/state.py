from random import (
    SystemRandom,
)

from bernard import (
    layers as lyr,
)
from bernard.analytics import (
    page_view,
)
from bernard.engine import (
    BaseState,
)
from bernard.i18n import (
    intents as its,
    translate as t,
)
from bernard.media import UrlMedia

from .store import (
    cs,
)

from bernard.platforms.telegram import (
    layers as tll,
)

random = SystemRandom()


class NumberBotState(BaseState):
    """
    Root class for Number Bot.
    """

    @page_view('/bot/error')
    async def error(self) -> None:
        """
        This happens when something goes wrong (it's the equivalent of the
        HTTP error 500).
        """

        self.send(lyr.Text(t.ERROR))

    @page_view('/bot/confused')
    async def confused(self) -> None:
        """
        This is called when the user sends a message that triggers no
        transitions.
        """

        self.send(lyr.Text(t.CONFUSED))

    async def handle(self) -> None:
        raise NotImplementedError


class S001xWelcome(NumberBotState):
    """
    Welcome the user
    """

    @page_view('/bot/welcome')
    async def handle(self) -> None:
        name = await self.request.user.get_friendly_name()

        self.send(
            lyr.Text('Play?'),
            tll.InlineKeyboard([
                [tll.InlineKeyboardCallbackButton(
                    text=t.LETS_PLAY,
                    payload={'action': 'play'},
                )]
            ]),
            lyr.Image(UrlMedia('https://domain/image.jpg'))
            # tll.AnswerInlineQuery(
            #     results=[1, 2, 3],
            #     cache_time=0,
            #     is_personal=True,
            # )
        )


class S002xGuessANumber(NumberBotState):
    """
    Define the number to guess behind the scenes and tell the user to guess it.
    """

    # noinspection PyMethodOverriding
    @page_view('/bot/guess-a-number')
    @cs.inject()
    async def handle(self, context) -> None:
        context['number'] = random.randint(1, 10)
        self.send(lyr.Text(t.GUESS_A_NUMBER))


class S003xGuessAgain(NumberBotState):
    """
    If the user gave a number that is wrong, we give an indication whether that
    guess is too low or too high.
    """

    # noinspection PyMethodOverriding
    @page_view('/bot/guess-again')
    @cs.inject()
    async def handle(self, context) -> None:
        user_number = self.trigger.user_number

        self.send(lyr.Text(t.WRONG))

        if user_number < context['number']:
            self.send(lyr.Text(t.HIGHER))
        else:
            self.send(lyr.Text(t.LOWER))


class S004xCongrats(NumberBotState):
    """
    Congratulate the user for finding the number and propose to find another
    one.
    """

    @page_view('/bot/congrats')
    async def handle(self) -> None:
        self.send(
            lyr.Text(t.CONGRATULATIONS),
            lyr.Text('Wanna play again?'),
            tll.InlineKeyboard([
                [tll.InlineKeyboardCallbackButton(
                    text=t.LETS_PLAY,
                    payload={'action': 'again'},
                )]
            ])
        )
