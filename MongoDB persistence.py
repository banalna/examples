# -*- coding: utf-8 -*-
import pymongo
from pip_services3_commons.config import ConfigParams
from pip_services3_commons.data import FilterParams
from pip_services3_commons.refer import Descriptor
from pip_services3_components.build import Factory
from pip_services3_container import ProcessContainer
from pip_services3_mongodb.persistence import MongoDbPersistence, IdentifiableMongoDbPersistence


class BeaconMongoDbPersistence(MongoDbPersistence):

    def __init__(self):
        super(BeaconMongoDbPersistence, self).__init__("beacons")

    def get_by_name(self, correlation_id, name):
        item = self._collection.find_one({'name': name})
        return item

    def set(self, correlation_id, item):
        item = self._collection.find_one_and_update(
            {'_id': item.id}, {'$set': item},
            return_document=pymongo.ReturnDocument.AFTER,
            upsert=True
        )
        return item


########################################################################################################################
persistence = BeaconMongoDbPersistence()
persistence.open("test")
beacon = BeaconV1(name="Super Beacon")
persistence.set("test", beacon)
item = persistence.get_by_name("test", "Super Beacon")
persistence.close("test")
print(item)  # Result: { name: "Super Beacon" }

########################################################################################################################
persistence = BeaconMongoDbPersistence()
# Let's say we need to connect to a local MongoDb, but on a non-standard port - 30000

persistence.configure(ConfigParams.from_tuples(
    "connection.host", "localhost",
    "connection.port", "30000"
))
persistence.open()  # While opening, it will try to establish a connection with the locally hosted MongoDb on port 30000


########################################################################################################################
class BeaconsFactory(Factory):
    beacons_mongodb_persistnece_descriptor = Descriptor("beacons", "persistence", "mongodb", "default", "1.0")

    def __init__(self):
        self.register_as_type(self.beacons_mongodb_persistnece_descriptor, BeaconMongoDbPersistence)


########################################################################################################################
class BeaconsProcess(ProcessContainer):
    def __init__(self):
        super(BeaconsProcess, self).__init__("beacons", "Beacons microservice")
        self._factories.add(DefaultMongoDbFactory())
        self._factories.add(BeaconsFactory())


########################################################################################################################
class IIdentifiable:
    id: Any
    pass


########################################################################################################################
class IdentifiableMongoDbPersistence(MongoDbPersistence):
    _max_page_size = 100

    def __init__(self, collection=None)
    def configure(self, config)
    def get_list_by_filter(self, correlation_id, filter, sort=None, select=None)
    def get_list_by_ids(self, correlation_id, ids)
    def get_one_random(self, correlation_id, filter)
    def get_one_by_id(self, correlation_id, id)
    def create(self, correlation_id, item)
    def set(self, correlation_id, item)
    def update(self, correlation_id, new_item)
    def update_partially(self, correlation_id, id, data)
    def delete_by_id(self, correlation_id, id)
    def delete_by_filter(self, correlation_id, filter)
    def delete_by_ids(self, correlation_id, ids)


########################################################################################################################
class BeaconsMongoDbPersistence(IdentifiableMongoDbPersistence):
    def __init__(self):
        super(BeaconsMongoDbPersistence, self).__init__("beacons")

    def composite_filter(self, filter):
        filter = filter or FilterParams()
        name = filter.get_as_nullable_string("name")
        return self._collection.find_one({"name": name})

    def get(self, correlation_id, filter, paging):
        return self.get_page_by_filter(correlation_id, ComposeFilter(filter), paging, None, None)


########################################################################################################################
filter = FilterParams.from_tuples('name', 'ABC')
result = persistence.get_page_filter(None, filter, None)


########################################################################################################################
def FilterDefinition(filter):
    filter = filter or FilterParams()
    name = filter.get_as_nullable_string("name")

    return self._collection.find_one({"name": name})


########################################################################################################################
# skip = 25, take = 50, total = false
paging = PagingParams(25, 50, False)
result = persistence.get_page_filter(None, None, paging)


########################################################################################################################
def get_one_by_name(self, correlation_id, name):
    item = self._collection.find_one({"name": name})

    if item is not None:
        self._logger.trace(correlation_id, f"Retrieved from {self._collectionName} with name = {name}")
    else:
        self._logger.trace(correlation_id, f"Nothing found from {self._collectionName} with name = {name}")


########################################################################################################################
class BeaconsMongoDbPersistence(IdentifiableMongoDbPersistence):
    def __init__(self):
        super(BeaconsMongoDbPersistence, self).__init__("beacons")

    def FilterDefinition(filter):
        filter = filter or FilterParams()
        name = filter.get_as_nullable_string("name")

        return self._collection.find_one({"name": name})

    def get(self, correlation_id, filter, paging):
        return self.get_page_by_filter(correlation_id, ComposeFilter(filter), paging, None, None)

    def get_one_by_name(self, correlation_id, name):
        item = self._collection.find_one({"name": name})

        if item is not None:
            self._logger.trace(correlation_id, f"Retrieved from {self._collectionName} with name = {name}")
        else:
            self._logger.trace(correlation_id, f"Nothing found from {self._collectionName} with name = {name}")


########################################################################################################################
persistence = BeaconMongoDbPersistence()
persistence.open("test_open")
beacon = BeaconV1(name="Super Beacon")
persistence.set("test", beacon)
item = persistence.get_by_name("test", "Super Beacon")
print(item)  # Result: { name: "Super Beacon" }
itemsPage = persistence.get_page_by_filter("test", FilterParams.from_tuples(
    "name", "Super Beacon"
), None)
print(itemsPage.Data.Count)  # Result: 1
print(itemsPage.Data[0])  # Result: { name: "Super Beacon" }
persistence.close("test");
