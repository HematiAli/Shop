from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from products.models import Product, Category
from . import tasks
from django.contrib import messages
from utils import IsAdminUserMixin
from orders.forms import CartAddForm
import logging


logger = logging.getLogger(__name__)


class HomeView(View):
    def get(self, request, category_slug=None):
        logger.warning("Home activated")
        products = Product.objects.filter(available=True)
        categories = Category.objects.filter(is_sub=False)
        if category_slug:
            category = Category.objects.get(slug=category_slug)
            products = products.filter(category=category)
        return render (request, 'home/index.html', {'products':products, 'categories': categories})


class ProductDetailView(View):
    def get(self, request, slug):
        product = get_object_or_404(Product, slug=slug)
        form = CartAddForm()
        return render(request, 'home/detail.html', {'product':product, 'form':form})
    

class BucketHomeView(IsAdminUserMixin, View):
    template_name = 'home/bucket.html'

    def get(self, request):
        objects = tasks.get_all_bucket_objects()
        return render(request, self.template_name, {'objects':objects})
    
class DeleteBucketObjectView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.delete_object_task.delay(key)
        messages.success(request, "your object will be deleted soon", "info")
        return redirect('home:bucket')
        
class DownloadBucketObjectView(IsAdminUserMixin, View):
    def get(self, request, key):
        tasks.download_object_task.delay(key)
        messages.success(request, 'your object will be downloaded soon', 'info')
        return redirect('home:bucket')
        