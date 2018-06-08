import csv
import time
import json
import time
import random
import inspect
import datetime as D
import threading

from datetime import datetime, timedelta
from io import StringIO


def today():
    now = D.datetime.now()
    # return now.strftime("%Y-%m-%d %H:%M")
    return now.strftime("%Y-%m-%d")


def lastweek():
    return (datetime.now() + timedelta(weeks=-1)).strftime("%Y-%m-%d")


def todate(t):
    return t.strftime("%Y-%m-%d")


def tojstime(d):
    return time.mktime(time.strptime(str(d), '%Y-%m-%d')) * 1000


def dumpjson(data, fn):
    with open(fn, 'w') as outfile:
        json.dump(data, outfile)


def toCsvString(title, dates, series):
    stream = StringIO()
    writer = csv.writer(stream, delimiter=',', skipinitialspace=True)
    writer.writerow(title)
    for i in range(len(dates)):
        r = []
        r.append(dates[i])
        for j in range(len(series)):
            r.append(series[j][i])

        writer.writerow(r)
    return stream


class TaskManager:
    def __init__(self):
        self.__pool = {}

    def run(self, f, args):
        t = threading.Thread(target=f, args=args)
        t.start()
        key = str(t.ident)
        self.__pool[key] = t
        return t.ident

    def is_alive(self, tid):
        ret = False
        key = str(tid)
        if key in self.__pool:
            ret = self.__pool[key].is_alive()
            if ret is False:
                del self.__pool[key]
        return ret

    def trim(self):
        for k in self._pool:
            if not self.pool[k].is_alive():
                del self.__pool[k]


def assign(objfrom, objto):
    # for n, v in inspect.getmembers(objfrom):
    #     setattr(objto, n, v)
    for k in objfrom:
        objto.__dict__[k] = objfrom[k]


def hasNumbers(inputString):
    return any(c.isdigit() for c in inputString)


def toFloat(s):
    ret = 0.0
    try:
        ret = float(s)
    except:
        pass
    return ret
