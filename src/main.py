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

while True:
    ec_index_name = "{}_{}".format(EC_INDEX_PREFIX, date.today().strftime("%Y%m%d"))
    ph_index_name = "{}_{}".format(PH_INDEX_PREFIX, date.today().strftime("%Y%m%d"))
    flow_index_name = "{}_{}".format(FLOW_INDEX_PREFIX, date.today().strftime("%Y%m%d"))
    wt_index_name = "{}_{}".format(WT_INDEX_PREFIX, date.today().strftime("%Y%m%d"))

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
                if "vp-io-0 : " in val:
                    log_msg(LOG_LEVEL, "INFO", "Received ec value of : {}".format(val.strip("vp-io-0 : ")))
                    timestamp = datetime.now()
                    ec_val = float(val.strip("vp-io-0 : ").strip("\r\n"))
                    es.index(index=ec_index_name, id=timestamp,
                             body={"ec_value": ec_val, "value_format": "ms/cm",
                                   "timestamp": timestamp})
                if "vp-io-1 : " in val:
                    log_msg(LOG_LEVEL, "INFO", "Received ph value of : {}".format(val.strip("vp-io-1 : ")))
                    timestamp = datetime.now()
                    ph_val = float(val.strip("vp-io-1 : ").strip("\r\n"))
                    ph_val += PH_CAL
                    es.index(index=ph_index_name, id=timestamp,
                             body={"ph_value": ph_val, "value_format": "raw",
                                   "calibration_offset": PH_CAL,
                                   "timestamp": timestamp})
                if "vp-io-2 : " in val:
                    log_msg(LOG_LEVEL, "INFO", "Received water temperature value of : {}".format(val.strip("vp-io-2 : ")))
                    timestamp = datetime.now()
                    wt_val = float(val.strip("vp-io-2 : ").strip("\r\n"))
                    es.index(index=wt_index_name, id=timestamp,
                             body={"temperature_value": wt_val, "value_format": "celsius",
                                   "timestamp": timestamp})
                if "vp-io-3 : " in val:
                    log_msg(LOG_LEVEL, "INFO", "Received flow meter value of : {}".format(val.strip("vp-io-3 : ")))
                    timestamp = datetime.now()
                    flow_val = float(val.strip("vp-io-3 : ").strip("\r\n"))
                    es.index(index=flow_index_name, id=timestamp,
                             body={"flow_value": flow_val, "value_format": "l/h",
                                   "timestamp": timestamp})

        else:
            log_msg(LOG_LEVEL, "ERROR", "Failed to retrieve values...")
    except:
        log_msg(LOG_LEVEL, "ERROR", "Something went wrong!")

    sleep(WAIT_TIME)
