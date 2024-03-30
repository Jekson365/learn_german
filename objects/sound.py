class Sound:
    def __init__(self,id,text,category_id,meaning):
        self.text = text
        self.meaning = meaning
        self.category_id = category_id
        self.id = id

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "category_id": self.category_id,
            "meaning": self.meaning,
        }