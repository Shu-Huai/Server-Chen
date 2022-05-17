import base64
from typing import IO
from utils.logger import Logger


class ImageReader:
    def __init__(self, path: str) -> None:
        self.path: str = path

    def read(self) -> bytes:
        file: IO = open(self.path, 'rb')
        result: bytes = base64.b64encode(file.read())
        file.close()
        return result


if __name__ == '__main__':
    image_reader: ImageReader = ImageReader('../images/阿尔梅里亚.png')
    Logger.info(str(image_reader.read()))
