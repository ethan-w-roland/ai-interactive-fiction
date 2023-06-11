# os-specific txt controls

from __future__ import print_function

import atexit
import ctypes
import sys
import time

from collections import deque
from threading import Thread

from xyppy.debug import err, warn

win_original_attributes = None
win_original_cursor_info = None

unix_in_tstp_signal = False
unix_screen_is_reset = False

stdin_is_tty = False # sys.stdin.isatty()
stdout_is_tty = False #sys.stdout.isatty()

def init(env):
    global win_original_attributes
    global win_original_cursor_info

    def on_exit_common():
        home_cursor()
        cursor_down(env.hdr.screen_height_units)
        reset_color()
        show_cursor()
    atexit.register(on_exit_common)
    hide_cursor()

def reset_color():
    return

def write_char_with_color(char, fg_col, bg_col):
    return

"""
class COORD(ctypes.Structure):
    _fields_ = [("X", ctypes.c_short), ("Y", ctypes.c_short)]

class SMALL_RECT(ctypes.Structure):
    _fields_ = [("Left", ctypes.c_short), ("Top", ctypes.c_short),
                ("Right", ctypes.c_short), ("Bottom", ctypes.c_short)]

class CONSOLE_SCREEN_BUFFER_INFO(ctypes.Structure):
    _fields_ = [("dwSize", COORD),
                ("dwCursorPosition", COORD),
                ("wAttributes", ctypes.c_ushort),
                ("srWindow", SMALL_RECT),
                ("dwMaximumWindowSize", COORD)]

class CONSOLE_CURSOR_INFO(ctypes.Structure):
    _fields_ = [("dwSize", ctypes.c_uint32),
                ("bVisible", ctypes.c_int)]

class char_union(ctypes.Union):
    _fields_ = [("UnicodeChar", ctypes.c_uint16),
                ("AsciiChar", ctypes.c_char)]
class CHAR_INFO(ctypes.Structure):
    _fields_ = [("Char", char_union),
                ("Attributes", ctypes.c_uint16)]
"""

def get_size():
    return 80, 40

def scroll_down():
    return


def fill_to_eol_with_bg_color():
    return


def cursor_to_left_side():
    return


def cursor_up(count=1):
    return


def cursor_down(count=1):
    return


def cursor_right(count=1):
    return


def cursor_left(count=1):
    return


def clear_line():
    return


def hide_cursor():
    return


def show_cursor():
    return


def clear_screen():
    pass


def home_cursor():
    return


def rgb3_to_bgr3(col):
    return ((col >> 2) & 1) | (col & 2) | ((col << 2) & 4)


def set_color(fg_col, bg_col):
    return


# TODO: any other encodings to check for?
def supports_unicode():
    return sys.stdout.encoding in ['UTF-8', 'UTF-16', 'UTF-32']


def getch_impl():
    raise RuntimeError("getch")


used_esc_char_list = [
    # arrow keys
    '[A', '[B', '[C', '[D',
    # fkeys
    'OP', 'OQ', 'OR', 'OS', '[15~', '[17~',
    '[18~', '[19~', '[20~', '[21~', '[23~', '[24~',
]
non_zscii_esc_char_list = [
    # home/end
    '[H', '[F',
    # ins/del, pgup/pgdn, alt home/end
    '[2~', '[3~', '[5~', '[6~', '[1~', '[4~',
]
esc_char_list = used_esc_char_list + non_zscii_esc_char_list
def could_be_escape(seq):
    return any(x.startswith(seq) for x in esc_char_list)
def is_zscii_special_key(seq):
    return seq[0] == '\x1b' and seq[1:] in used_esc_char_list

# only run these on the main thread
def getch_or_esc_seq():
    global stored_chars
    sys.stdout.flush()
    while len(stored_chars) == 0:
        time.sleep(0.005)

    # safe, b/c only one thread pops
    c = stored_chars.popleft()

    if ord(c) == 3:
        # 0x03 == ctrl-c is pressed on windows. checked here
        # to keep the raise on the main thread (avoid hang).
        raise KeyboardInterrupt

    if c == '\x1b':
        time.sleep(0.005)
        if peekch():
            seq = ''
            while peekch() and could_be_escape(seq + peekch()):
                seq += stored_chars.popleft()
                time.sleep(0.005)
            if seq not in esc_char_list:
                for s in seq[::-1]:
                    # hurray for threadsafe queues!
                    # preserves order because only this
                    # thread touches the lefthand side.
                    stored_chars.appendleft(s)
            else:
                c += seq

    # puts('\n' + repr(c) + '\n')

    return c

def peekch():
    if len(stored_chars):
        # safe, b/c only one thread peeks/pops
        return stored_chars[0]
    return ''

def puts(s):
    sys.stdout.write(s)
    sys.stdout.flush()

def flush():
    sys.stdout.flush()