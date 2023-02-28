class Error(Exception):
    pass


class StorageError(Error):
    pass


class SaveError(StorageError):
    pass


class FindError(StorageError):
    pass


class DeleteError(StorageError):
    pass


class StubError(Error):
    pass


class StubSaveError(StubError, SaveError):
    pass


class StubFindError(StubError, FindError):
    pass


class StubDeleteError(StubError, DeleteError):
    pass


class InitStorageError(StorageError):
    pass
