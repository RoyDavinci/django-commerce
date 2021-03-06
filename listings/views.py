from django.shortcuts import render, get_object_or_404, redirect
from .models import Products, Category, Review
from .forms import ReviewForm

# Create your views here.


def product_list(request, category_slug=None):
    categories = Category.objects.all()
    if category_slug:
        requested_category = get_object_or_404(Category, slug=category_slug)
        products = Products.objects.filter(category=requested_category)
    else:
        requested_category = None
        products = Products.objects.all()

    return render(request, 'products/list.html', {'products': products, 'categories': categories, 'requested_category': requested_category})


def product_detail(request, category_slug, product_slug):
    category = get_object_or_404(Category, slug=category_slug)
    product = get_object_or_404(
        Products, category_id=category.id, slug=product_slug)
    if request.method == "POST":
        review_form = ReviewForm(request.POST)
        if review_form.is_valid():
            cd = review_form.cleaned_data
            author_name = 'Anonymous'
            Review.objects.create(
                product=product, author=author_name, rating=cd['rating'], text=cd['text'])
        return redirect('listings:product_detail', category_slug=category_slug, product_slug=product_slug)
    else:
        review_form = ReviewForm()

    return render(request, 'products/detail.html', {'product': product, 'review_form': review_form})
