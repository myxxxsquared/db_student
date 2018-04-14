
# Copyright (C) 2018 Wenjie Zhang (https://github.com/myxxxsquared) - All Rights Reserved

import time

__all__ = ['emptyshell', 'timer']


class emptyshell:
    def __init__(self):
        self.value = None

    def set_return_value(self, value):
        self.value = value

    def __getattr__(self, obj):
        def myrunobj(*arg, **args):
            return self.value
        return myrunobj


class timer:
    def __init__(self):
        self.t0 = None

    def tic(self):
        self.t0 = time.time()

    def toc(self, result, factor=1):
        result.append(0.0 if self.t0 is None else (
            time.time() - self.t0)/factor)
        self.t0 = None


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
