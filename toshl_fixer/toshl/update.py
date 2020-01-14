from toshl import Entry
from .labels import LabelMapping
from ..settings import client


def update_toshl(entry_id, **updates):
    entry = Entry(client)
    mapping = LabelMapping.create_from_local_copy()
    if "tag" in updates:
        tag_id = mapping.get_tag_id(updates["tag"])
        updates["tags"] = [tag_id] if tag_id else []
        del updates['tag']
    if "category" in updates:
        updates["category"] = mapping.get_category_id(updates["category"])

    entry.update_entry(entry_id, **updates)
