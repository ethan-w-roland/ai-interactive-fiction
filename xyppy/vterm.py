from collections import deque
import sys

class NeedInput(Exception):
    pass

class Screen(object):
    def __init__(self, env):
        self.env = env
        self.buffer = deque()
        self.eol = True
        self.output = []

    def blank_top_win(self):
        return

    def blank_bottom_win(self):
        return

    def write(self, text):
        if self.eol and text == '>':
            return
        self.output.append(text)
        self.eol = text.endswith('\n')

    # for when it's useful to make a hole in the scroll text
    # e.g. moving already written text around to make room for
    # what's about to become a new split window
    def scroll_top_line_only(self):
        return

    def finish_wrapping(self):
        return

    def flush(self):
        return

    def get_line_of_input(self, prompt='', prefilled=''):
        if len(self.buffer) == 0:
            self.write(prompt)
            raise NeedInput(prompt)
        return self.buffer.popleft()

    def first_draw(self):
        return

    def getch_or_esc_seq(self):
        if len(self.buffer) == 0:
            raise NeedInput('GETCH')
        return self.buffer.popleft()

    # for save game error messages and such
    # TODO: better formatting here (?)
    def msg(self, text):
        self.output.extend((text, '\n'))