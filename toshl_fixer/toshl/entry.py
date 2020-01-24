import threading
from functools import partial

from toshl import Entry
from toshl_fixer.settings import client
from toshl_fixer.toshl.labels import LabelMapping


def update_entry(entry_id, **updates):
    entry = Entry(client)
    mapping = LabelMapping.create_from_local_copy()
    if "tag" in updates:
        tag_id = mapping.get_tag_id(updates["tag"])
        updates["tags"] = [tag_id] if tag_id else []
        del updates['tag']
    if "category" in updates:
        updates["category"] = mapping.get_category_id(updates["category"])

    entry.update_entry(entry_id, **updates)


def delete_entry(entry_id):
    entry = Entry(client)
    entry.delete(entry_id)


def send_request_async(fn, *args, **kwargs):
    x = threading.Thread(target=fn, args=args, kwargs=kwargs)
    x.start()


delete_entry_async = partial(send_request_async, delete_entry)
update_entry_async = partial(send_request_async, update_entry)
