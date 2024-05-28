import logging

def setup_logger(name, log_file='app.log', level=logging.DEBUG):
    # Create a custom logger
    logger = logging.getLogger(name)
    
    # Prevent logging messages from being propagated to the root logger
    logger.propagate = False
    
    # Check if handlers already exist to avoid adding multiple handlers
    if not logger.handlers:
        # Set the logging level
        logger.setLevel(level)

        # Create handlers
        console_handler = logging.StreamHandler()
        file_handler = logging.FileHandler(log_file)

        # Set the logging level for handlers
        console_handler.setLevel(logging.DEBUG)
        file_handler.setLevel(logging.INFO)

        # Create formatters and add them to handlers
        console_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_format = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

        console_handler.setFormatter(console_format)
        file_handler.setFormatter(file_format)

        # Add handlers to the logger
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger