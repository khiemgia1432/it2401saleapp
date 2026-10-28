from eapp.models import Category, Product
from eapp import app

def load_categories():
    return Category.query.order_by('id').all()

def load_product(kw=None, cate_id=None, page=1):
    query = Product.query

    if kw:
        query = query.filter(Product.name.contains(kw))

    if cate_id:
        query = query.filter(Product.category_id==int(cate_id))

    page_size = app.config['PAGE_SIZE']
    start = (page - 1 ) * page_size
    query = query.slice(start,start*page_size)

    return query.all()