from toshl import Category, Tag
from ..data import labels
from ..settings import client


class LabelMapping:
    def __init__(self, categories, tags):
        self.tags = tags
        self.categories = categories

    @staticmethod
    def _fetch():
        categories = {category['name']: category['id'] for category in Category(client).list()}
        tags = {tag['name']: tag['id'] for tag in Tag(client).list()}
        return categories, tags

    @classmethod
    def create_from_toshl(cls):
        categories, tags = cls._fetch()
        labels.dump(categories, tags)
        return cls(categories, tags)

    @classmethod
    def create_from_local_copy(cls):
        categories, tags = labels.load()
        return cls(categories, tags)

    def get_tag_id(self, tag):
        return self.tags.get(tag)

    def get_category_id(self, category):
        return self.categories[category]

    def get_category_name_from_id(self, category_id):
        for name, id_ in self.categories.items():
            if id_ == category_id:
                return name

    def get_tag_name_from_id(self, tag_id):
        for name, id_ in self.tags.items():
            if id_ == tag_id:
                return name
