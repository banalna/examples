# -*- coding: utf-8 -*-
from abc import ABC

from pip_services3_commons.config import IConfigurable, ConfigParams
from pip_services3_commons.refer import IUnreferenceable, IReferenceable, References, Descriptor, DependencyResolver, \
    Referencer
from pip_services3_commons.refer.IReferences import IReferences

########################################################################################################################
class IReferences(ABC):

    def put(self, locator=None, reference=None):
        raise NotImplementedError('Method from interface definition')

    def remove(self, locator):
        raise NotImplementedError('Method from interface definition')

    def get_all_locators(self):
        raise NotImplementedError('Method from interface definition')

    def get_all(self):
        raise NotImplementedError('Method from interface definition')

    def get_optional(self, locator):
        raise NotImplementedError('Method from interface definition')

    def get_required(self, locator):
        raise NotImplementedError('Method from interface definition')

    def get_one_optional(self, locator):
        raise NotImplementedError('Method from interface definition')

    def get_one_required(self, locator):
        raise NotImplementedError('Method from interface definition')

    def get_one_before(self, reference, locator):
        raise NotImplementedError('Method from interface definition')

    def find(self, locator, required):
        raise NotImplementedError('Method from interface definition')


########################################################################################################################
class IUnreferenceable(ABC):
    def unset_references(self):
        raise NotImplementedError('Method from interface definition')


########################################################################################################################
class Worker1:
    def __init__(self, name=None):
        self._default_name = name or "Default name1"

    def do(self, level, message):
        print(f"Write to {self._default_name}.{level} message: {message}")


class Worker2:
    def __init__(self, name=None):
        self._default_name = name or "Default name2"

    def do(self, level, message):
        print(f"Write to {self._default_name}.{level} message: {message}")


########################################################################################################################
class SimpleController(IReferenceable, IUnreferenceable):
    _worker = None
    _references: References

    def set_references(self, references):
        self._worker = self._references.get_one_required(111)

    def unset_references(self):
        pass

    def greeting(self, name):
        self._worker.do('level', f"Hello, {name}!")


########################################################################################################################
references = References.from_tuples(
    111, Worker1(),
    222, Worker2()
)
controller = SimpleController()
controller.set_references(references)
print(controller.greeting("world"))
controller.unset_references()
controller = None

########################################################################################################################
class Descriptor(object):
    def __init__(self, group, type, kind, name, version)
    def get_group(self)
    def get_type(self)
    def get_kind(self)
    def get_name(self)
    def get_version(self)
    def _match_field(self, field1, field2)
    def match(self, descriptor)
    def _exact_match_field(self, field1, field2)
    def exact_match(self, descriptor)
    def is_complete(self)
    @staticmethod
    def from_string(value)->Descriptor


########################################################################################################################
class SimpleController(IReferenceable, IUnreferenceable):
    # ...
    def set_references(self, references):
        self._worker = self._references.get_one_required(
            Descriptor("*", "worker", "worker1", "*", "1.0")
        )
    # ...


references = References.from_tuples(
    Descriptor("sample", "worker", "worker1", "111", "1.0"), Worker1(),
    Descriptor("sample", "worker", "worker2", "222", "1.0"), Worker2()
)
controller = SimpleController()
controller.set_references(references)
print(controller.greeting("world"))
controller.unset_references()
controller = None

########################################################################################################################
class DependencyResolver(IReconfigurable, IReferenceable):
    _dependencies = None
    _references = None

    def __init__(self, config=None, references=None)
    def configure(self, config)
    def set_references(self, references)
    def put(self, name, locator)
    def _locate(self, name)
    def get_optional(self, name)
    def get_required(self, name)
    def get_one_optional(self, name)
    def get_one_required(self, name)
    def find(self, name, required)
    @staticmethod
    def from_tuples(*tuples)


########################################################################################################################
class SimpleController(IConfigurable, IReferenceable, IUnreferenceable):
    _depedency_resolver = DependencyResolver.fromTuples(
        "worker", Descriptor("*", "worker", "*", "*", 1.0)
    )

    def configure(self, config):
        self._depedency_resolver.configure(config)

    def set_references(self, references):
        self._depedency_resolver.set_references(references)
        self._worker = self._depedency_resolver.get_one_required("worker")

    def unset_references(self):
        self._depedency_resolver.unset_references()

    # ...


references = References.from_tuples(
    Descriptor("sample", "worker", "worker1", "111", "1.0"),
    Worker1(),
    Descriptor("sample", "worker", "worker2", "222", "1.0"),
    Worker2()
)

config = ConfigParams.from_tuples(
    "dependencies.worker", " *:worker: worker1:111: 1.0"
)

controller = SimpleController()
controller.configure(config)
controller.set_references(references)
print(controller.greeting("world"))
controller.unset_references()
controller = None

########################################################################################################################
class Referencer:

    @staticmethod
    def set_references_for_one(references, component)

    @staticmethod
    def set_references(references, components)

    @staticmethod
    def unset_references_for_one(component)

    @staticmethod
    def unset_references(components)