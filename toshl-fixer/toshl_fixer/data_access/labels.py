import json

from ..settings import DATA_DIR

MAPPING_PATH = DATA_DIR / 'mapping.json'


def dump(categories, tags):
    mapping = {
        "tags": tags,
        "categories": categories,
    }
    with open(MAPPING_PATH, 'w') as f:
        json.dump(mapping, f, indent=4, sort_keys=True)


def load():
    with open(MAPPING_PATH) as f:
        mapping = json.load(f)
    return mapping["categories"], mapping["tags"]
