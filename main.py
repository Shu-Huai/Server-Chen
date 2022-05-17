from pinger import Pinger
from config import PingConfig

if __name__ == '__main__':
    pinger: Pinger = Pinger(PingConfig.host, PingConfig.timeout, PingConfig.count)
    pinger.loop_ping(PingConfig.interval)
