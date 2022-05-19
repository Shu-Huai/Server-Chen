from we_com_sender import WeComSender
from config import WeComConfig
from utils import ImageReader

if __name__ == '__main__':
    sender = WeComSender(WeComConfig.company_id, WeComConfig.agent_id, WeComConfig.app_secret,
                         WeComConfig.duplicate_check_interval)
    sender.send_text('测试文本', '@all')
    image: ImageReader = ImageReader('images/阿尔梅里亚.png')
    sender.send_image(image.read(), '@all')
    sender.send_markdown('''# 测试Markdown\n''', '@all')
