from datetime import datetime as dt


# TODO: реализовать класс IP так, чтобы его можно было добавлять в ЧС и писать запросы.
class IP(object):

    def __init__(self, address: str, handshake_time=dt.utcnow()):
        self.address = address
        self.handshake_time = handshake_time

    def __eq__(self, other):
        return self.address == other.address


class Visitor:
    def __init__(self, ip, platform, agent):
        self.ip = ip
        self.datetime = dt.utcnow()
        self.platform = f"'{platform}'" if platform != "None" else "NULL"
        self.agent = f"'{agent}'" if agent != "None" else "NULL"
