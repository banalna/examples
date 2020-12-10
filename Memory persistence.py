# -*- coding: utf-8 -*-
from pip_services3_commons.data import IIdentifiable, FilterParams, PagingParams
from pip_services3_data.persistence import IdentifiableMemoryPersistence, MemoryPersistence, JsonFilePersister

class IIdentifiable:
    id: Any
    pass

class IdentifiableMemoryPersistence(MemoryPersistence, IWriter, IGetter, ISetter):
    def __init__(self, loader=None, saver=None)
    def get_list_by_ids(self, correlation_id, ids)
    def get_one_by_id(self, correlation_id, id)
    def create(self, correlation_id, item)
    def set(self, correlation_id, item)
    def update(self, correlation_id, new_item)
    def update_partially(self, correlation_id, id, data)
    def delete_by_id(self, correlation_id, id)


########################################################################################################################
filter = FilterParams.from_tuples(
    "name", 'ABC'
)

persistence.get_page_by_filter(None, filter, None)


########################################################################################################################
def composite_filter(self, filter):
    filter = filter or FilterParams()
    name = filter.get_as_nullable_string("name")
    return lambda item: False if (name is not None and item.name != name) else True


def get_page_by_filter(self, correlation_id, filter, paging, sort=None, select=None):
    super().get_page_by_filter(correlation_id, filter, paging, sort, select)


########################################################################################################################
# skip = 25, take = 50, total = false
paging = PagingParams(25, 50, False)
persistence.get_page_by_filter(None, None, paging)


########################################################################################################################
def get_one_by_name(self, correlation_id, name):
    item = None
    for _item in self.items:
        if _item.name == name:
            item = _item
            break
    if item is not None:
        self._logger.trace(correlation_id, "Found by %s", name)
    else:
        self._logger.trace(correlation_id, "Cannot find by %s", name)


########################################################################################################################
class MyMemoryPersistence(IdentifiableMemoryPersistence):
    def composite_filter(self, filter):
        filter = filter or FilterParams()
        name = filter.get_as_nullable_string("name")
        return lambda item: False if (name is not None and item.name != name) else True

    def get_page_by_filter(self, correlation_id, filter, paging, sort=None, select=None):
        super().get_page_by_filter(correlation_id, filter, paging, sort, select)

    def get_one_by_name(self, correlation_id, name):
        item = None
        for _item in self.items:
            if _item.name == name:
                item = _item
                break
        if item is not None:
            self._logger.trace(correlation_id, "Found by %s", name)
        else:
            self._logger.trace(correlation_id, "Cannot find by %s", name)


########################################################################################################################
def use_memory_persistence():
    # arrange
    persistence = MyMemoryPersistence()
    item = persistence.create("123", MyData("1", "ABC"))

    # filter by id
    filter = FilterParams.from_tuples("name", "ABC")

    # act
    result = persistence.get_page_by_filter(None, filter, PagingParams(0, 100, False))

    # clean
    persistence.delete_by_id("123", "1")


########################################################################################################################
class MyFilePersistence(MyMemoryPersistence):
    _persister: JsonFilePersister

    def __init__(self):
        self._persister = JsonFilePersister()
        self._loader = self._persister
        self._saver = self._persister
        super(MyFilePersistence, self).__init__(self._loader, self._saver)

    def configure(self, config):
        super().configure(config)
        self._persister.configure(config)

