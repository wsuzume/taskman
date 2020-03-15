import datetime
import glob
import os
import numpy as np
import pandas as pd
import pathlib

    #parser.add_argument('--colors')
    #parser.add_argument('--begin')
    #parser.add_argument('--deadline')
    #parser.add_argument('--task') #TODO
    #parser.add_argument('--show-task') #TODOの一覧
    #parser.add_argument('--schedule') #予定
    #parser.add_argument('--show-schedule') #予定の一覧
    #parser.add_argument('--issue') # GitHub の issue
    #parser.add_argument('--show-issue') # 


# color scheme (0 - 10)
def cs(n):
    if n < 0:
        n = 0
    if n > 10:
        n = 10
    default = list(range(c_bg, c_fg + 1, 2))
    return default[n]

# colored character
def cc(s, fg, bg=None):
    pbg = '\x1b[48;5;'
    pfg = '\x1b[38;5;'
    rs = '\x1b[0m'
    if bg is None:
        return f'{pfg}{fg}m{s}{rs}'
    return f'{pbg}{bg}m{pfg}{fg}m{s}{rs}'

def one_week(xs):
    ys = []
    for x in xs[:7]:
        ys.append(cc('■', cs(x)))
    return ' '.join(ys)

def split_datelist(xs):
    ret = []
    buf = []
    for x in xs:
        buf.append(x)
        if x.weekday() == 5:
            ret.append(buf)
            buf = []

    if len(buf) != 0:
        ret.append(buf)

    return ret


log_dir = os.path.expanduser('~/.config/taskman/log')

c_bg = 235
c_fg = 255
c_emphasize = 47


import random
def date_to_score(d):
    return random.randrange(0, 10)

def csqr(fg, bg=None):
    return cc('■', fg, bg)

class Calender:
    def __init__(self):
        self.df = None
        self.buffer = []

    def today(self):
        return datetime.date.today()

    def get_term(self):
        return [ self.today() + datetime.timedelta(days=i) for i in range(-14,8) ]

    def get_splitted_term(self):
        return split_datelist(self.get_term())

    def load(self):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        path = pathlib.Path(log_dir)
        fname = list(path.iterdir())[-1]

        self.df = pd.read_csv(fname, index_col=0)

    def save(self):
        fname = datetime.datetime.now().isoformat() + '.csv'
        df.to_csv(os.path.join(log_dir, fname))

    def print_header(self):
        print('-------------------')
        print(f' {datetime.date.today()}')
        print('-------------------')

    def print_date(self, sdl):
        print('|', end='')
        for xs in sdl:
            date = xs[0].strftime('%-m/%-d')
            s = f'{date:<5}        '
            print(' ' + s + ' |', end='')
        print('')

    def print_weekdays(self, sdl):
        print('|', end='')
        for xs in sdl:
            print(' S M T W T F S |', end='')
        print('')

    def print_scores(self, sdl):
        print('|', end='')
        for xs in sdl:
            scores = [ date_to_score(x) for x in xs ]
            squares = one_week(scores)
            print(' ' + squares + ' |', end='')
        print('')


    def show(self):
        self.buffer = []

        sdl = self.get_splitted_term()

        self.print_header()
        self.print_date(sdl)
        self.print_weekdays(sdl)
        self.print_scores(sdl)

    def color_sample(self):
        for i in range(11):
            print(cc("hoge", cs(i)))
        print(cc("hoge", c_emphasize))

    def sample(self):
        print('')
        print('-------------------')
        print(f' {datetime.date.today()}')
        print('-------------------')
        print('|        | 2/29          | 3/7           | 3/14          | 3/21          |        |')
        print('|        | S M T W T F S | S M T W T F S | S M T W T F S | S M T W T F S |        |')
        print('| 12/26- | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ | -3/19  | ■ task1')
        print('|        | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ |        | ■ task2')
        print('|        | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ |        | ■ task3')
        print('|        | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ | □ ■ □ ■ □ ■ □ |        | ■ task4')
        print('')


c = Calender()
c.load()
c.show()

c.color_sample()
c.sample()

print('')

