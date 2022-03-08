import time

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
        # eg. 2022-03-07_20.50.50
        name = time.strftime('%Y-%m-%d_%H.%M.%S', time.localtime(time.time()))
        self.path = f'{path}{name}.csv'
        self.metric = kwargs.get('metric', 'cycle')

        create(self.path, self.metric)

    def add(self, filename, circuitInfos, time):
        if self._state == False:
            # no need to report: eg. solving single file.
            return

        addRow(self.path, filename, circuitInfos, self.metric, time)
        

        



        

        