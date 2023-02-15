import sys
import logging
import colorlog

# Create a custom logger
class Create_logger:
    def __init__(self, __name__):
        self.__name__ = __name__
        self.log = logging.getLogger(self.__name__)
        self.log.setLevel(logging.DEBUG)
        # print(self.__name__)

    def get_log(self):
        return self.log

    def add_stream_handler(self, out=sys.stdout):
        # Create handlers
        self.stream_handler = logging.StreamHandler(out)

        # Create formatters and add it to handlers
        self.stream_format = colorlog.ColoredFormatter(
            "%(log_color)s %(asctime)s.%(msecs)03d | %(name)s | %(levelname)s | %(message)s",
            "%Y-%m-%d %H:%M:%S",
        )
        self.stream_handler.setFormatter(self.stream_format)
        self.stream_handler.setLevel(logging.DEBUG)

        # Add handlers to the logger
        self.log.addHandler(self.stream_handler)
        # return(self.log)

    def add_file_handler(self, path, date):
        self.filename = path + "/" + date + "-" + self.__name__ + ".log"
        self.file_handler = logging.FileHandler(self.filename)

        # Create formatters and add it to handlers
        self.file_format = logging.Formatter(
            "%(asctime)s.%(msecs)03d | %(levelname)s | %(message)s", "%Y-%m-%d %H:%M:%S"
        )  # | %(name)s
        self.file_handler.setLevel(logging.DEBUG)
        self.file_handler.setFormatter(self.file_format)

        # Add handlers to the logger
        self.log.addHandler(self.file_handler)


# def create_logger(__name__, path, out=sys.stdout):

#     logger = logging.getLogger(__name__)
#     logger.setLevel(logging.DEBUG)

#     # Create handlers
#     stream_handler = logging.StreamHandler(out)
#     # Create dynamic filename
#     filename = path + "/" + __name__ + ".log"
#     print(filename)
#     file_handler = logging.FileHandler(filename)

#     # Create formatters and add it to handlers
#     stream_format = colorlog.ColoredFormatter('%(log_color)s %(asctime)s.%(msecs)03d | %(name)s | %(levelname)s | %(message)s', '%Y-%m-%d %H:%M:%S')
#     stream_handler.setFormatter(stream_format)
#     stream_handler.setLevel(logging.DEBUG)

#     file_format = logging.Formatter('%(asctime)s.%(msecs)03d | %(name)s | %(levelname)s | %(message)s', '%Y-%m-%d %H:%M:%S')
#     file_handler.setLevel(logging.DEBUG)
#     file_handler.setFormatter(file_format)

#     # Add handlers to the logger
#     logger.addHandler(stream_handler)
#     logger.addHandler(file_handler)
#     return(logger)

# Define loggers
# create_logger('camera_log', 'cam.log')

if __name__ == "__main__":
    a = Create_logger("debug")
    a.add_stream_handler()

    for item in range(10):
        a.log.debug(item)
