from mongoengine import Document, fields


class Products(Document):
    product_id = fields.StringField(max_length=30, required=True)
    product_name = fields.StringField(max_length=100, required=True)
    stock_quantity = fields.IntField(min_value=1, required=True)

    def __str__(self):
        return self.product_id
