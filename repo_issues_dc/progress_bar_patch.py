def getpatchedprogress():
    import progress

    from functools import wraps

    from sys import platform

    if platform.startswith("win"):
        progress.HIDE_CURSOR = ''
        progress.SHOW_CURSOR = ''

    @wraps(progress.Infinite.clearln)
    def patchedclearln(self):
        from sys import platform
        if self.file and self.is_tty():
            if platform.startswith("win"):
                print('\r', end='', file=self.file)
            else:
                print('\r\x1b[K', end='', file=self.file)

    progress.Infinite.clearln = patchedclearln

    return progress
