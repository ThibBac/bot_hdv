from functions import *

with keyboard.Listener(on_press=on_press) as listener:
    keyboard = Controller()

    # On met l'amu bouf
    left_click(1242, 406, sleep_time=0.1)
    left_click(1242, 406, sleep_time=0.1)
    time.sleep(0.2)
    # go ressource
    left_click(1564, 310)
    time.sleep(0.2)

    while not break_program:

        # on met les runes fo
        left_click(1242, 406, sleep_time=0.1)
        left_click(1242, 406, sleep_time=0.1)
        time.sleep(0.2)

        for _ in range(15):
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            left_click(913, 777)
            time.sleep(0.1)

            left_click(913, 777)
            time.sleep(0.2)

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        # On enlève les fo
        time.sleep(0.3)
        left_click(912, 611, sleep_time=0.1)
        left_click(912, 611, sleep_time=0.1)
        time.sleep(0.2)
        # on met les runes ine
        left_click(1299, 405, sleep_time=0.1)
        left_click(1299, 405, sleep_time=0.1)
        time.sleep(0.2)

        for _ in range(15):
            keyboard.press(Key.enter)
            keyboard.release(Key.enter)
            left_click(913, 777)
            time.sleep(0.1)

            left_click(913, 777)
            time.sleep(0.2)

        keyboard.press(Key.enter)
        keyboard.release(Key.enter)
        # On enlève les ine
        time.sleep(0.3)
        left_click(912, 611, sleep_time=0.1)
        left_click(912, 611, sleep_time=0.1)
        time.sleep(0.2)
