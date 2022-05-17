import json, requests, base64
import os
from config import WeComConfig
from utils import ImageReader, Logger


class WeComSender:
    def __init__(self, company_id: str, agent_id: str, app_secret: str, duplicate_check_interval: int = 1000,
                 bypass_proxies=True) -> None:
        self.company_id: str = company_id
        self.agent_id: str = agent_id
        self.app_secret: str = app_secret
        self.duplicate_check_interval: int = duplicate_check_interval
        if bypass_proxies:
            self.proxies: dict = {
                "http": None,
                "https": None
            }
        else:
            self.proxies: dict = {
                "http": os.environ.get('http_proxy', ''),
                "https": os.environ.get('https_proxy', '')
            }

    def get_token(self) -> str:
        get_token_url: str = f"https://qyapi.weixin.qq.com/cgi-bin/gettoken?corpid={self.company_id}&corpsecret={self.app_secret}"
        response: bytes = requests.get(get_token_url, proxies=self.proxies).content
        token: str = json.loads(response).get('access_token')
        if token and len(token) > 0:
            Logger.success(f'获取token成功。')
            return token
        else:
            Logger.error(f'Token获取失败。')
            return ''

    def send_text(self, text: str, to_user_id='@all') -> bytes:
        token: str = self.get_token()
        if token and len(token) > 0:
            send_url: str = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}'
            data: dict = {
                "touser": to_user_id,
                "agentid": self.agent_id,
                "msgtype": "text",
                "text": {
                    "content": text
                },
                "duplicate_check_interval": self.duplicate_check_interval
            }
            response = requests.post(send_url, data=json.dumps(data), proxies=self.proxies).content
            if len(response) > 0:
                Logger.success(f'文本发送成功。')
                return response
            else:
                Logger.error(f'文本发送失败。')
                return b''
        else:
            return b''

    def send_image(self, base64_content: bytes, to_user_id='@all') -> bytes:
        token: str = self.get_token()
        if token and len(token) > 0:
            upload_url: str = f'https://qyapi.weixin.qq.com/cgi-bin/media/upload?access_token={token}&type=image'
            upload_response: json = requests.post(upload_url, files={"picture": base64.b64decode(base64_content)},
                                                  proxies=self.proxies).json()
            if "media_id" in upload_response:
                media_id = upload_response['media_id']
            else:
                return b''
            send_url: str = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}'
            data: dict = {
                "touser": to_user_id,
                "agentid": self.agent_id,
                "msgtype": "image",
                "image": {
                    "media_id": media_id
                },
                "duplicate_check_interval": self.duplicate_check_interval
            }
            response = requests.post(send_url, data=json.dumps(data), proxies=self.proxies).content
            if len(response) > 0:
                Logger.success(f'图片发送成功。')
                return response
            else:
                Logger.error(f'图片发送失败。')
                return b''
        else:
            return b''

    def send_markdown(self, text: str, to_user_id='@all') -> bytes:
        token: str = self.get_token()
        if token and len(token) > 0:
            send_url = f'https://qyapi.weixin.qq.com/cgi-bin/message/send?access_token={token}'
            data = {
                "touser": to_user_id,
                "agentid": self.agent_id,
                "msgtype": "markdown",
                "markdown": {
                    "content": text
                },
                "duplicate_check_interval": self.duplicate_check_interval
            }
            response = requests.post(send_url, data=json.dumps(data), proxies=self.proxies).content
            if len(response) > 0:
                Logger.success(f'Markdown发送成功。')
                return response
            else:
                Logger.error(f'Markdown发送失败。')
                return b''
        else:
            return b''


if __name__ == '__main__':
    sender = WeComSender(WeComConfig.company_id, WeComConfig.agent_id, WeComConfig.app_secret,
                         WeComConfig.duplicate_check_interval)
    sender.send_text('测试文本', '@all')
    image: ImageReader = ImageReader('../images/阿尔梅里亚.png')
    sender.send_image(image.read(), '@all')
    sender.send_markdown('''# 测试Markdown\n''', '@all')
