import os

from common_utils import *

def override_conf_from_env( conf, key ):
    env_key = "VEGGIEPI_{}".format(key)
    if os.environ.get(env_key) is not None:
        conf[key] = os.environ[env_key]
    elif not key in conf:
        conf[key] = "nil"

def override_conf_from_env_array( conf, key ):
    env_key = "VEGGIEPI_{}".format(key)
    if os.environ.get(env_key) is not None:
        if is_empty(os.environ[env_key]):
            conf[key] = []
        else:
            conf[key] = os.environ[env_key].split(",")

def check_log_level ( conf_log_level, log_level ):
    if conf_log_level == "debug" or conf_log_level == "DEBUG":
        return True
    else:
        return log_level != "debug" and log_level != "DEBUG"

def log_msg ( conf_log_level, log_level, message ):
    if check_log_level(conf_log_level, log_level):
        print ("[{}] {}".format(log_level, message))
