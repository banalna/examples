# -*- coding: utf-8 -*-
import os
from datetime import datetime

from pip_services3_commons.config import ConfigParams, NameResolver, OptionsResolver
from pip_services3_commons.config.IConfigurable import IConfigurable
from abc import ABC, abstractmethod

from pip_services3_commons.data import FilterParams, PagingParams
from pip_services3_components.config import IConfigReader, MemoryConfigReader, JsonConfigReader, YamlConfigReader


class IConfigurable:
    def configure(self, config: ConfigParams):
        raise NotImplementedError('Method from interface definition')


########################################################################################################################
config = ConfigParams.from_tuples(
    "param1", 123,
    "param2’, ‘2020-01-01T11:00:00.0Z"
)

########################################################################################################################
param1 = config.get_as_integer("param1")
param2 = config.get_as_datetime_with_default("param2", datetime.now())

########################################################################################################################
configWithSections = ConfigParams.from_tuples(
    "param1", 123,
    "options.param1", "ABC",
    "options.param2", "XYZ"
)
options = configWithSections.get_section("options")

########################################################################################################################
default_config = ConfigParams.from_tuples(
    "param1", 1,
    "param2", "Default Value"
)
config = config.set_defaults(default_config)

########################################################################################################################
anotherConfig = ConfigParams.from_string("param1=123;param2=ABC")


########################################################################################################################
class DataController(IConfigurable):
    _max_page_size: int = 5

    def configure(self, config):
        self._max_page_size = config.get_as_integer_with_default('max_page_size', self._max_page_size)

    def get_data(self, correlation_id: str, filter: FilterParams, paging: PagingParams):
        paging.take = min(paging.take, self._max_page_size)
        # Get data using max page size constraint.


########################################################################################################################
component = DataController()
config = ConfigParams.from_tuples("max_page_size", 100)
component.configure(config)

########################################################################################################################
# ...
# Controller
# - descriptor: "beacons:controller:default:default:1.0"
#  max_page_size: 10
# ...

########################################################################################################################
config = ConfigParams.from_tuples(
    "descriptor", "myservice:connector:aws:connector1:1.0",
    "param1", "ABC",
    "param2", 123
)
name = NameResolver.resolve(config)  # Result: connector1

########################################################################################################################
config = ConfigParams.from_tuples(
    # ...
    "options.param1", "ABC",
    "options.param2", 123
)
options = OptionsResolver.resolve(config)  # Result: param1=ABC;param2=123


########################################################################################################################
class IConfigReader(ABC):
    def _read_config(self, correlation_id: str, parameters: ConfigParams):
        raise NotImplementedError('Method from interface definition')


########################################################################################################################
config = ConfigParams.from_tuples(
    "connection.host", "localhost",
    "connection.port", "8080"
)
config_reader = MemoryConfigReader()
config_reader.configure(config)
parameters = ConfigParams.from_value(os.environ)
result = config_reader.read_config("123", parameters)
# Result: connection.host=localhost;connection.port=8080

########################################################################################################################
# ======== config.json ======
# { "key1": "1234", "key2": "ABCD" }
# ===========================

########################################################################################################################
config_reader = JsonConfigReader("config.json")
parameters = ConfigParams.from_tuples("KEY1_VALUE", 123, "KEY2_VALUE", "ABC")
result = config_reader._read_config("correlationId", parameters)
# Result: key1=1234;key2=ABCD

########################################################################################################################
# ======== config.yml ======
# key1: "1234"
# key2: "ABCD"
# ==========================

########################################################################################################################
config_reader = YamlConfigReader("config.yml")
parameters = ConfigParams.from_tuples("KEY1_VALUE", 123, "KEY2_VALUE", "ABC")
result = config_reader._read_config("correlationId", parameters)
# Result: key1=1234;key2=ABCD


