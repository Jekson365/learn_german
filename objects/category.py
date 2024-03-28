class Category:
    def __init__(self,category_name,category_id):
        self.category_name = category_name
        self.category_id = category_id

    def to_dict(self):
        return {
            'category_name': self.category_name,
            'category_id': self.category_id
        }