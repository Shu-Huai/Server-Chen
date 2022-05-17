import time
from we_com_sender import WeComSender
from config import WeComConfig, PingConfig
from utils import Logger
from multiping import multi_ping


class Pinger:
    def __init__(self, host_list: list, timeout: int, count: int = 1) -> None:
        self.host_list: list = host_list
        self.timeout: int = timeout
        self.count: int = count
        self.sender: WeComSender = WeComSender(WeComConfig.company_id, WeComConfig.agent_id, WeComConfig.app_secret,
                                               WeComConfig.duplicate_check_interval)

    def __int__(self, host: str, timeout: int, count: int = 1) -> None:
        self.host_list: list = [host]
        self.timeout: int = timeout
        self.count: int = count
        self.sender: WeComSender = WeComSender(WeComConfig.company_id, WeComConfig.agent_id, WeComConfig.app_secret,
                                               WeComConfig.duplicate_check_interval)

    def ping(self) -> None:
        for host in self.host_list:
            responses, no_responses = multi_ping([host], timeout=self.timeout, retry=self.count)
            if responses:
                for _ in responses:
                    Logger.info(f"{host}正常。")
            if no_responses:
                for _ in no_responses:
                    Logger.error(f"{host}不可达。")
                    self.sender.send_text(f"{host}不可达。")

    def loop_ping(self, interval: int, count: int = 0) -> None:
        if count == 0:
            while True:
                self.ping()
                time.sleep(interval)
        else:
            for i in range(count):
                self.ping()
                time.sleep(interval)


if __name__ == "__main__":
    pinger: Pinger = Pinger(PingConfig.host, PingConfig.timeout, PingConfig.count)
    pinger.loop_ping(PingConfig.interval)
