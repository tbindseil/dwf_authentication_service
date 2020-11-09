import logging

def get_log(tag=""):
    #this line is important
    logging.basicConfig()
    log = logging.getLogger(tag)
    log.setLevel('INFO')
    return log;

def WARN(msg, tag=""):
    get_log(tag).warning(msg)

def INFO(msg, tag=""):
    get_log(tag).info(msg)
