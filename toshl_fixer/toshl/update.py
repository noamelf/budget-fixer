from toshl import Entry
from .labels import LabelMapping
from toshl_fixer.settings import client


def update_toshl(entry_id, **updates):
    entry = Entry(client)
    mapping = LabelMapping.create_from_local_copy()
    if "tag" in updates:
        tag_id = mapping.get_tag_id(updates["tag"])
        updates["tag"] = [tag_id] if tag_id else []
    if "category" in updates:
        updates["category"] = mapping.get_category_id(updates["category"])

    entry.update_entry(entry_id, **updates)
