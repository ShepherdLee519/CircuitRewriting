import time
from os.path import dirname, basename

from qcpm.statistics.create import create
from qcpm.statistics.addrow import addRow


class StatReporter:
    def __init__(self, path, **kwargs):
        if path == None:
            self._state = False
            return
        else:
            self._state = True

        # csv file's name:
        name = self.initCSVName(**kwargs)
        self.path = f'{path}{name}.csv'
        self.metric = kwargs.get('metric', 'cycle')

        create(self.path, self.metric)

    def initCSVName(self, *, metric, folder):
        # %d%m_dirname_[optimize]_[strategy]_[systems]_[metric]
        timestamp = time.strftime('%d%m', time.localtime(time.time()))

        name = basename(dirname(folder))

        return f'{timestamp}_{name}_{metric}'

    def add(self, filename, circuitInfos, time):
        if self._state == False:
            # no need to report: eg. solving single file.
            return

        addRow(self.path, filename, circuitInfos, self.metric, time)
        

        



        

        