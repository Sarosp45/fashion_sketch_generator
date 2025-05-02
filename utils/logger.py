
import logging

def setup_logger(name, log_file, level=logging.INFO):
    """Function to setup a logger with specified name and file."""
    handler = logging.FileHandler(log_file)        
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    logger = logging.getLogger(name)
    logger.setLevel(level)
    logger.addHandler(handler)
    logger.propagate = False
    return logger

# Create loggers for each part
data_logger = setup_logger('data', 'logs/data.log')
train_logger = setup_logger('train', 'logs/train.log')
eval_logger = setup_logger('eval', 'logs/eval.log')