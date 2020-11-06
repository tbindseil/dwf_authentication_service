import logging

def get_log(tag=""):
    #this line is important
    logging.basicConfig()
    log = logging.getLogger("LOG")
    return log;

def WARN(msg, tag=""):
    get_log(tag).warning(msg)
