from mongoengine import Document, fields
import datetime


class Order(Document):
    order_id = fields.StringField(max_length=50, required=True)
    customer_name = fields.StringField(max_length=100, required=True)
    product_name = fields.StringField(max_length=100, required=True)
    quantity = fields.IntField(min_value=1, required=True)
    delivery_address=fields.StringField(max_length=100,required=True)
    order_status = fields.StringField(max_length=50, required=True)
    created_at = fields.DateTimeField(default=datetime.datetime)


def __str__(self):
    return self.order_id
