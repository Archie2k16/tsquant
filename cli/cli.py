hint_msg = '''usage:
python manage.py 
    [show]
        [data]
        [empty]
'''


class arg_proc(object):
    def __init__(self):
        super(arg_proc, self).__init__()

    def process(self, argv):
        proc_selector = {
            'show': self._show,
            'run': self._run
        }

        if len(argv) == 1:
            return self._empty_process()
        elif argv[1] in proc_selector.keys():
            return proc_selector[argv[1]](argv)

    def _empty_process(self):
        return hint_msg

    def _show(self, argv):
        return 'showing'

    def _run(self, argv):

        if len(argv) == 2:
            return self._empty_process()

        elif argv[2] == 'notebook':
            return 'running notebook'


arg_proc = arg_proc()
