class MLWorker:
    def __init__(self, server, ip: str, volume=None):
        self.server = server
        self.volume = volume
        self.ip = ip
