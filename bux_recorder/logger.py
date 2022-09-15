import sys
import logging
import colorlog

# Create a custom logger
def create_logger(__name__, filename, out=sys.stdout):
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.DEBUG)
    

    # Create handlers
    stream_handler = logging.StreamHandler(out)
    file_handler = logging.FileHandler(filename)

    # Create formatters and add it to handlers
    stream_format = colorlog.ColoredFormatter('%(log_color)s %(asctime)s.%(msecs)03d | %(name)s | %(levelname)s | %(message)s', '%Y-%m-%d %H:%M:%S')
    stream_handler.setFormatter(stream_format)
    stream_handler.setLevel(logging.DEBUG)

    file_format = logging.Formatter('%(asctime)s.%(msecs)03d | %(name)s | %(levelname)s | %(message)s', '%Y-%m-%d %H:%M:%S')
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(file_format)

    # Add handlers to the logger
    logger.addHandler(stream_handler)
    logger.addHandler(file_handler)
    return(logger)

# Define loggers
create_logger('debugger', 'file.log')
create_logger('camera_log', 'cam.log')