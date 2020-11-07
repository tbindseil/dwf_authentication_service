import logging

def get_log(tag=""):
    #this line is important
    logging.basicConfig()
    log = logging.getLogger(tag)
    return log;

def WARN(msg, tag=""):
    get_log(tag).warning(msg)
