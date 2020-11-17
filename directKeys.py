import ctypes
import time
import pynput

SendInput = ctypes.windll.user32.SendInput

W = 0x11
A = 0x1E
S = 0x1F
D = 0x20
M = 0x32
K = 0x25
SPACE = 0x39
ENTER = 0x0D
ESC = 0x1B

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


#
#
# class KeyBdInput(ctypes.Structure):
#     fields = [("wVk", ctypes.c_ushort),
#                 ("wScan", ctypes.c_ushort),
#                 ("dwFlags", ctypes.c_ulong),
#                 ("time", ctypes.c_ulong),
#                 ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    fields = [("uMsg", ctypes.c_ulong),
              ("wParamL", ctypes.c_short),
              ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    fields = [("dx", ctypes.c_long),
              ("dy", ctypes.c_long),
              ("mouseData", ctypes.c_ulong),
              ("dwFlags", ctypes.c_ulong),
              ("time", ctypes.c_ulong),
              ("dwExtraInfo", PUL)]


# class Input_I(ctypes.Union):
#     fields = [("ki", KeyBdInput),
#                 ("mi", MouseInput),
#                 ("hi", HardwareInput)]
#
#
# class Input(ctypes.Structure):
#     fields = [("type", ctypes.c_ulong),
#                 ("ii", Input_I)]


from ctypes import windll, Structure, c_long, byref


class POINT(Structure):
    fields = [("x", c_long), ("y", c_long)]


def queryMousePosition():
    pt = POINT()
    windll.user32.GetCursorPos(byref(pt))
    return pt
    # return { "x": pt.x, "y": pt.y}/


def left_click(x, y, sleep_time=0.3):
    # convert to ctypes pixels
    # x = int(x * 0.666)
    # y = int(y * 0.666)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(sleep_time)
    ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)  # left down
    ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)  # left up


def right_click(x, y):
    # convert to ctypes pixels
    # x = int(x * 0.666)
    # y = int(y * 0.666)
    ctypes.windll.user32.SetCursorPos(x, y)
    time.sleep(0.3)
    ctypes.windll.user32.mouse_event(0x0008, 0, 0, 0, 0)  # right down
    ctypes.windll.user32.mouse_event(0x0010, 0, 0, 0, 0)  # right up


def moveMouseTo(x, y):
    # convert to ctypes pixels
    # x = int(x * 0.666)
    # y = int(y * 0.666)
    ctypes.windll.user32.SetCursorPos(x, y)
    # ctypes.windll.user32.mouse_event(2, 0, 0, 0, 0)  # left down
    # ctypes.windll.user32.mouse_event(4, 0, 0, 0, 0)  # left up


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def PressKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008, 0,
                                           ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKeyPynput(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = pynput._util.win32.INPUT_union()
    ii_.ki = pynput._util.win32.KEYBDINPUT(0, hexKeyCode, 0x0008 | 0x0002, 0,
                                           ctypes.cast(ctypes.pointer(extra), ctypes.c_void_p))
    x = pynput._util.win32.INPUT(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
