from game_engine import GameAction, GameEngine

steps = [
    {
        'step_name': u'战斗结束',
        'img': 'D:/workspace/python/game_script/langrisser/res/accounts.png',
        'actions': [GameAction.click, GameAction.sleep_2000ms, GameAction.click],
        'threshold': 0.9
    },
    # {
    #     'step_name': u'开宝箱',
    #     'img': 'D:/workspace/python/game_script/langrisser/res/treasure.png',
    #     'actions': [GameAction.click, GameAction.sleep_1000ms]
    # },
    {
        'step_name': u'再来一局',
        'img': 'D:/workspace/python/game_script/langrisser/res/again.png',
        'actions': [GameAction.click_padding_5],
        'threshold': 0.5
    },
    {
        'step_name': u'进入战斗',
        'img': 'D:/workspace/python/game_script/langrisser/res/attack.png',
        'actions': [GameAction.click_padding_5, GameAction.sleep_1000ms],
        'threshold': 0.5
    },
]

is_debug = False

if __name__ == '__main__':
    ge = GameEngine(steps=steps, client=3, is_debug=is_debug)
    counter = 0

    while True:
        if is_debug and counter > 0:
            break
        counter += 1

        ge.run()

