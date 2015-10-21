import datetime


class ElapseMark():

    def __init__(self, label, elapsed):
        self.label = label
        self.elapsed = elapsed.__str__().lstrip('0:')


class ElapsedTime():

    def __init__(self, totals=False):
        self.totals = totals
        self.start = datetime.datetime.now()
        self.last = self.start
        self.mark = []
        if self.totals:
            self.mark.append(ElapseMark('started:', self.start))

    def mark_time(self, label):
        now = datetime.datetime.now()
        elapsed = now - self.last
        self.last = now
        self.mark.append(ElapseMark(label, elapsed))

    def list(self):
        if self.totals:
            self.mark.append(ElapseMark('ended:', self.last))
            self.mark.append(ElapseMark('total:', self.last - self.start))
        return self.mark
