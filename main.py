import datetime
import glob
import os
import numpy as np
import pandas as pd
import pathlib
import uuid

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


c_bg = 235
c_fg = 255
c_emphasize = 47


import random
def date_to_score(d):
    return random.randrange(0, 10)

def csqr(fg, bg=None):
    return cc('■', fg, bg)

class Task:
    def __init__(self, name, hash_str=None, begin=None, deadline=None, table=None):
        self.name = name

        if hash_str is not None:
            self.hash = hash_str
        else:
            self.hash = str(uuid.uuid4())

        self.begin = begin
        self.deadline = deadline
        self.table = table

def get_term(today, start=-14, end=7):
    return [ today + datetime.timedelta(days=i) for i in range(start, end+1) ]

def split_term(term, weekday=5, ys=None):
    ret = []
    buf = []
    if ys is None:
        for x in term:
            buf.append(x)
            if x.weekday() == weekday:
                ret.append(buf)
                buf = []
    else:
        for x, y in zip(term, ys):
            buf.append(y)
            if x.weekday() == weekday:
                ret.append(buf)
                buf = []

    if len(buf) != 0:
        ret.append(buf)

    return ret

log_dir = os.path.expanduser('~/.config/taskman/log')
hash_dir = os.path.expanduser('~/.config/taskman/hash')

class Calender:
    def __init__(self, start=-14, end=7):
        self._check_config()

        self.start = start
        self.end = end

        self.today = self._today()
        self.term = get_term(self.today, self.start, self.end)

        self.df = None
        self.buffer = []
        self.table = {}

    def _today(self):
        d = datetime.date.today()
        return datetime.datetime(d.year, d.month, d.day)

    def _check_config(self):
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)

        if not os.path.exists(hash_dir):
            os.makedirs(hash_dir)

    def load(self):
        self.table = {}

        path = pathlib.Path(log_dir)
        fname = list(path.iterdir())[-1]

        self.hash_df = pd.read_csv(os.path.join(hash_dir, 'table.csv'), index_col=0)
        self.df = pd.read_csv(fname, index_col=0, parse_dates=True)

        self.term_df = self.df.loc[self.term]

        for h, row in self.hash_df.iterrows():
            self.table[h] = (row, self.term_df[h])



    def save(self, term):
        hashes = [ str(uuid.uuid4()) for i in range(4) ]
        names = ['task1', 'task2', 'task3', 'task4']

        hash_df = pd.DataFrame(index=hashes, columns=['name', 'begin', 'deadline'])
        hash_df['name'] = names
        hash_df.to_csv(os.path.join(hash_dir, 'table.csv'))

        df = pd.DataFrame(index=term, columns=hashes)
        for d in term:
            df.loc[d] = np.random.randint(0, 10, 4)
        fname = datetime.datetime.now().isoformat() + '.csv'
        df.to_csv(os.path.join(log_dir, fname))
        return df

    def get_table(self, term):
        return self.df.loc[term]

    def make_header(self):
        self.b('-------------------\n')
        self.b(f' {datetime.date.today()}\n')
        self.b('-------------------\n')

    def make_date_header(self, sdl):
        buf = ['|']
        for xs in sdl:
            date = xs[0].strftime('%-m/%-d')
            s = f'{date:<5}        '
            buf.append(' ' + s + ' |')
        buf.append('\n')
        self.b(''.join(buf))

    def make_weekdays(self, sdl):
        buf = ['|']
        for xs in sdl:
            buf.append(' S M T W T F S |')
        buf.append('\n')
        self.b(''.join(buf))

        weekday = ['S', 'M', 'T', 'W', 'T', 'F', 'S']
        t = []
        for x in self.term:
            if x == self.today:
                t.append(cc(weekday[x.weekday()], c_emphasize))
            else:
                t.append(weekday[x.weekday()])
        self.t = t
        splitted = split_term(self.term, ys=self.t)
        print(splitted)

    def make_score_row(self, sdl):
        buf = ['|']
        for xs in sdl:
            scores = [ date_to_score(x) for x in xs ]
            squares = one_week(scores)
            buf.append(' ' + squares + ' |')
        buf.append('\n')
        self.b(''.join(buf))

    def make_scores(self, sdl):
        pass

    def clear(self):
        self.buffer = []

    def flush(self):
        for s in self.buffer:
            print(s, end='')

    def b(self, s):
        self.buffer.append(s)

    def show(self):
        self.clear()

        sdl = split_term(self.term, weekday=5)

        self.make_header()
        self.make_date_header(sdl)
        self.make_weekdays(sdl)
        self.make_scores(sdl)
        self.flush()

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
#df = c.save(c.term)
#print(df)
#import sys
#sys.exit(0)

c.color_sample()
c.sample()

print('')

for k, v in c.table.items():
    print(k)
    print(type(v[0]))
    print(type(v[1]))

for x in c.t:
    print(x)
