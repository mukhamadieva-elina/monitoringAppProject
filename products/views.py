from django.shortcuts import render

from marketplaces.wildberries.wildberries import Wildberries
from products.models import Product


def product(request, **kwargs):
    article = kwargs['article']
    product_info = Product.objects.filter(article=article).first()
    img_link = Wildberries.get_image(product_info.article)
    context = {'product_info': product_info, 'img_link': img_link}
    return render(request, 'product.html', context)
