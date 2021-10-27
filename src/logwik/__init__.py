class ExitException(Exception):
    def __init__(self, code):
        self._code = code

    @property
    def code(self):
        return self._code
