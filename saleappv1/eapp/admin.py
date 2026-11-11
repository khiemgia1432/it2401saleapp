from flask_admin.contrib.sqla import ModelView

from eapp.models import Category, Product
from flask_admin import Admin
from eapp import app, db

admin = Admin(app=app, name="E-commerce's Admin")

class ProductView(ModelView):
    column_list = ['id', 'name', 'price', 'category_id']
    column_searchable_list = ['name']
    can_export = True
    column_filters = ['name', 'price']
    edit_modal = True
    column_editable_list = ['name']

admin.add_view(ModelView(Category, db.session))
admin.add_view(ProductView(Product, db.session))