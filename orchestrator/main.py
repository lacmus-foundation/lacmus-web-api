import processing
from commons import logging
import project_config


if __name__ == '__main__':
    logging.init_logging(project_config.PROJECT_SYMBOL)
    processor = processing.Processing()
    processor.run()


