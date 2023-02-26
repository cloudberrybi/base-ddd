class Error(Exception):
    pass


class StubError(Error):
    pass


class StubSaveError(StubError):
    pass


class StubFindError(StubError):
    pass


class StubDeleteError(StubError):
    pass


class InitStorageError(Error):
    pass
