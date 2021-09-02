import math

# from src.settings import settings


class PagePagination:

    def __init__(self, items, page, page_size, total, schema=None):
        self.page = page
        self.items: list = items
        self.previous_page = None
        self.next_page = None
        self.has_previous = page > 1
        if self.has_previous:
            self.previous_page = page - 1
        previous_items = (page - 1) * page_size
        self.total = total
        self.has_next = previous_items + len(items) < self.total
        if self.has_next:
            self.next_page = page + 1
        self.pages = int(math.ceil(self.total / float(page_size)))
        self.meta_info = self.create_meta()

        if schema:
            self.schema = schema
            self._cast_to_schema()

    def create_meta(self):
        return {
            'page': self.page,
            'pages': self.pages,
            'total': self.total,
            'has_next': self.has_next,
            'has_previous': self.has_previous
        }

    def _cast_to_schema(self):
        if self.items.count(None) != 0:
            self.items.remove(None)  # remove from response `null` element
        return [self.schema.from_orm(item) for item in self.items]

    @staticmethod
    def get_query(page, query, page_size):
        return (
            query
            .limit(page_size)
            .offset((page - 1) * page_size)
        )
