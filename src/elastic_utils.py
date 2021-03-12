from elasticsearch import Elasticsearch
from common_utils import *
from veggie_utils import *

def es_connect(conf_log_level, es_scheme, es_hosts, es_port, es_user, es_password, es_subpath):
    if is_not_empty(es_user) and is_not_empty(es_password) and is_not_empty(es_subpath):
        es_url_tpl = "{}://{}:{}@{}:{}/{}"
        es_url = es_url_tpl.format(es_scheme, es_user, "{}", es_hosts[0], es_port, es_subpath)
        log_msg(conf_log_level, "debug", "Connect to elastic search with url = {}".format(es_url.format("XXXXXX")))
        return Elasticsearch([es_url.format(es_password)], http_auth=(es_user, es_password))
    elif is_not_empty(es_user) and is_not_empty(es_password):
        es_url_tpl = "{}://{}:{}"
        es_url = es_url_tpl.format(es_scheme, es_hosts[0], es_port)
        log_msg(conf_log_level, "debug", "Connect to elastic search with url = {} and username = {}".format(es_url, es_user))
        return Elasticsearch(es_hosts, http_auth=(es_user, es_password), scheme = es_scheme, port = es_port)
    elif is_not_empty(es_subpath):
        es_url_tpl = "{}://{}:{}/{}"
        es_url = es_url_tpl.format(es_scheme, es_hosts[0], es_port, es_subpath)
        log_msg("debug", "Connect to elastic search with url = {}".format(es_url))
        return Elasticsearch([es_url])
    else:
        es_url_tpl = "{}://{}:{}"
        es_url = es_url_tpl.format(es_scheme, es_hosts[0], es_port)
        log_msg(conf_log_level, "debug", "Connect to elastic search with url = {}".format(es_url))
        return Elasticsearch(es_hosts, scheme = es_scheme, port = es_port)
