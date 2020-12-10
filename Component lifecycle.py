# -*- coding: utf-8 -*-
from abc import abstractmethod, ABC

from pip_services3_commons.config import IConfigurable, ConfigParams, IReconfigurable
from pip_services3_commons.refer import IReferenceable, IReferences, References
from pip_services3_commons.run import IOpenable, IClosable, IExecutable, FixedRateTimer, Parameters, Opener, Closer
from pip_services3_components.log import CompositeLogger

import concurrent.futures


class IConfigurable:
    def configure(self, config: ConfigParams):
        raise NotImplementedError('Method from interface definition')


class IReferenceable:
    def set_references(self, references: IReferences):
        raise NotImplementedError('Method from interface definition')


class IOpenable(IClosable):
    def is_opened(self):
        raise NotImplementedError('Method from interface definition')

    def open(self, correlation_id):
        raise NotImplementedError('Method from interface definition')


class IClosable:
    def close(self, correlation_id):
        raise NotImplementedError('Method from interface definition')


class IExecutable:
    def execute(self, correlation_id, args):
        raise NotImplementedError('Method from interface definition')


########################################################################################################################
class CounterController(IReferenceable, IReconfigurable, IOpenable, IExecutable):
    __logger = CompositeLogger()
    __timer = FixedRateTimer()
    __parameters = Parameters()
    __counter = 0

    def configure(self, config):
        self.__parameters = Parameters.from_config(config)

    def set_references(self, references: IReferences):
        self.__logger.set_references(references)

    def is_opened(self):
        return self.__timer.started

    def open(self, correlation_id):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            self.__timer.task = executor.submit(self.execute, correlation_id, self.__parameters)
            self.__timer.interval = 1000
            self.__timer.delay = 1000
            self.__timer.start()
        self.__logger.trace(correlation_id, "Counter controller opened")

    def close(self, correlation_id):
        self.__timer.stop()
        self.__logger.trace(correlation_id, "Counter controller closed")

    def execute(self, correlation_id, args):
        self.__logger.info(correlation_id,
                           f"{self.__counter + 1} - \
                            {self.__parameters.get_as_string_with_default('message', 'Hello World!')}")
        return self.__counter


########################################################################################################################
Opener.open(correlation_id, _references.get_all())
Closer.close(correlation_id, _references.get_all())