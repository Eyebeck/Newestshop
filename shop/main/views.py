from django.shortcuts import render, get_object_or_404
from .models import Category, Product
from cart.forms import CartAddProductForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import redirect, render


def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("dashboard")
    else:
        form = UserCreationForm()

    return render(request, "blog/register.html", {"form": form})


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            login(request, form.get_user())
            return redirect("dashboard")
    else:
        form = AuthenticationForm()

    return render(request, "blog/login.html", {"form": form})


def logout_view(request):
    logout(request)
    return redirect("login")


@login_required(login_url="login")
def dashboard_view(request):
    return render(request, "blog/dashboard.html")

def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    return render(request, 'main/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    related_products = Product.objects.filter(category=product.category,
                                              available=True).exclude(id=product.id)[:4]

    cart_product_form = CartAddProductForm()

    return render(request, 'main/product/detail.html', {'product': product,
                                                        'related_products' : related_products,
                                                        'cart_product_form': cart_product_form})

def product_list(request, category_slug=None):
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)

    category = None
    if category_slug:
        category = get_object_or_404(Category, slug=category_slug)
        products = products.filter(category=category)

    # ✅ Добавь сортировку
    sort = request.GET.get('sort', 'name')
    allowed_sorts = ['name', '-name', 'price', '-price']
    if sort in allowed_sorts:
        products = products.order_by(sort)

    return render(request, 'main/product/list.html',
                  {'category': category,
                   'categories': categories,
                   'products': products})