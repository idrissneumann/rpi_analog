import sensors_pack.analog_pack.analog_reader as analog

from elasticsearch import Elasticsearch
from datetime import date
from datetime import datetime
import json
from time import sleep

from veggie_utils import *
from elastic_utils import es_connect

with open('analog_conf.json') as json_file:
    conf = json.load(json_file)

override_conf_from_env_array(conf, 'elastic_hosts')
override_conf_from_env(conf, 'log_level')
override_conf_from_env(conf, 'elastic_port')
override_conf_from_env(conf, 'elastic_scheme')
override_conf_from_env(conf, 'elastic_subpath')
override_conf_from_env(conf, 'elastic_username')
override_conf_from_env(conf, 'elastic_password')
override_conf_from_env(conf, 'wait_time')
override_conf_from_env(conf, 'index_prefix')
override_conf_from_env(conf, 'ph_calibration_offset')
override_conf_from_env(conf, 'ph_index_prefix')
override_conf_from_env(conf, 'ec_index_prefix')
override_conf_from_env(conf, 'flow_meter_index_prefix')
override_conf_from_env(conf, 'water_temp_index_prefix')
override_conf_from_env(conf, 'vp_sep')

LOG_LEVEL = conf['log_level']
ES_HOSTS = conf['elastic_host']
ES_PORT = cast_int(conf['elastic_port'])
ES_SCHEME = conf['elastic_scheme']
ES_USER = conf['elastic_username']
ES_PASS = conf['elastic_password']

PH_CAL = cast_int(conf['ph_calibration_offset'])
PH_INDEX_PREFIX = conf['ph_index_prefix']
EC_INDEX_PREFIX = conf['ec_index_prefix']
FLOW_INDEX_PREFIX = conf['flow_meter_index_prefix']
WT_INDEX_PREFIX = conf['water_temp_index_prefix']
VP_SEPARATOR = conf['vp_sep']
WAIT_TIME = cast_int(conf['wait_time'])

es = es_connect(LOG_LEVEL, ES_SCHEME, ES_HOSTS, ES_PORT, ES_USER, ES_PASS, ES_SUBPATH)

def index_val(match_prefix, val, index_name, field_name, field_format):
    if match_prefix in val:
        log_msg(LOG_LEVEL, "INFO", "Received ec value of : {}".format(val.strip(match_prefix)))
        timestamp = datetime.now().isoformat()
        vid = "{}_{}".format(field_name, timestamp)
        sval = float(val.strip(match_prefix).strip("\r\n"))
        record={field_name: sval, "value_format": field_format, "timestamp": timestamp}
        if "ph_value" == field_name:
            record['calibration_offset'] = PH_CAL
        es.index(index=index_name, id=vid, body=record)

while True:
    date_suffix = date.today().strftime("%Y%m%d")
    ec_index_name = "{}_{}".format(EC_INDEX_PREFIX, date_suffix)
    ph_index_name = "{}_{}".format(PH_INDEX_PREFIX, date_suffix)
    flow_index_name = "{}_{}".format(FLOW_INDEX_PREFIX, date_suffix)
    wt_index_name = "{}_{}".format(WT_INDEX_PREFIX, date_suffix)

    es.indices.create(index=ec_index_name, ignore=400)
    es.indices.create(index=ph_index_name, ignore=400)
    es.indices.create(index=flow_index_name, ignore=400)
    es.indices.create(index=wt_index_name, ignore=400)

    serial_value = analog.get_serial_input()
    log_msg(LOG_LEVEL, "INFO", "Received serial value is : {}".format(serial_value))
    try:
        if serial_value is not None:
            vals = serial_value.split(VP_SEPARATOR)
            for val in vals:
                index_val("vp-io-0 : ", val, ec_index_name, "ec_value", "ms/cm")
                index_val("vp-io-1 : ", val, ph_index_name, "ph_value", "raw")
                index_val("vp-io-2 : ", val, flow_index_name, "temperature_value", "celsius")
                index_val("vp-io-3 : ", val, wt_index_name, "flow_value", "l/h")
        else:
            log_msg(LOG_LEVEL, "ERROR", "Failed to retrieve values...")
    except:
        log_msg(LOG_LEVEL, "ERROR", "Something went wrong!")

    sleep(WAIT_TIME)
