from .cart import Cart
#every templates has receive context_processors
#add to settings => templates => context_processors


def cart(request):
    return {'cart': Cart(request)}