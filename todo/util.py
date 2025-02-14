import logging

def setup_logging():
    logging.basicConfig(format=("[%(levelname)s\033[0m] "
                                "\033[1;31m%(module)s\033[0m: "
                                "%(message)s"),
                        level=logging.INFO)
    logging.addLevelName(logging.ERROR, '\033[1;31mE')
    logging.addLevelName(logging.INFO, '\033[1;32mI')
    logging.addLevelName(logging.WARNING, '\033[1;33mW')