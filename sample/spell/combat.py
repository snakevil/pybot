# encoding: utf-8

from pybot import bot

class Ready(bot.Spell):
    def __init__(self):
        super(Ready, self).__init__(
            bot.action.Wait(
                1000, 1500
            ).then(
                bot.action.Fire(
                    ((596, 355), (708, 397)),
                    4
                )
            ),
            bot.expect.Fingerprint(
                ((596, 355), (708, 397)),
                '807f7f4d595b7f00',
                91
            ) & bot.expect.Colors(
                ((596, 355), (708, 397)),
                (((645, 0), (0, 0)), ((904, 0), (3143, 12)))
            )
        )

class Begin(bot.Spell):
    def __init__(self):
        super(Begin, self).__init__(
            bot.action.Wait(
                500, 1000
            ).then(
                bot.action.Fire(
                    (730, 346),
                    48
                )
            ),
            bot.expect.Fingerprint(
                ((685, 398), (777, 434)),
                '5d0080e37c3fcfe7',
                144
            )
        )

class MemberLoot(bot.Spell):
    def __init__(self, when = None):
        super(MemberLoot, self).__init__(
            bot.action.Fire(
                ((542, 222), (800, 450)),
                10
            ),
            when
        )

class Loot(MemberLoot):
    def __init__(self):
        super(Loot, self).__init__(
            bot.expect.Fingerprint(
                ((261, 84), (413, 137)),
                '2222aeaeb8f47604',
                105
            )
        )

class Over(bot.Spell):
    def __init__(self):
        super(Over, self).__init__(
            bot.action.Wait(
                500, 1000
            ).then(
                bot.action.Fire(
                    ((672, 32), (800, 450)),
                    10
                )
            ),
            bot.expect.Fingerprint(
                ((297, 370), (477, 394)),
                'cbb3b2e4e86040e0',
                28
            )
        )
