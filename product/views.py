from msilib.schema import ListView

from django.contrib.auth.decorators import login_required
from django.views.generic import DetailView, TemplateView
from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from product.models import Product, OrderItem, Category, FeaturedProducts, Like, OfferProducts, Brande



class ProductDetailView(DetailView):
    template_name = 'product/detail1.html'
    model = Product

    def get_context_data(self, **kwargs):
        context = super(ProductDetailView, self).get_context_data()
        if self.request.user.is_authenticated:  # بررسی احراز هویت کاربر
            if self.request.user.likes.filter(product__slug=self.object.slug).exists():
                context['is_liked'] = True
            else:
                context['is_liked'] = False
        else:

            context['is_liked'] = False  # در صورتی که کاربر وارد نشده باشد، ایس_لایک را به False تنظیم کنید
        return context


def order_item_list(request):
    order_items = OrderItem.objects.all()
    return render(request, 'product/detail1.html', {'order_items': order_items})


class NavbarPartialView(TemplateView):
    template_name = 'home/include/nav_bar.html'

    def get_context_data(self, **kwargs):
        context = super(NavbarPartialView, self).get_context_data()
        context['categories'] = Category.objects.all()
        return context


class ProductListView(TemplateView):
    template_name = 'products_list.html'

    def get_context_data(self, **kwargs):
        request = self.request
        context = super().get_context_data(**kwargs)
        # form = ProductFilterForm(self.request.GET)
        sort_by = self.request.GET.get('sort')
        show_count = self.request.GET.get('show')

        queryset = Product.objects.all()

        if sort_by == 'latest':
            queryset = queryset.order_by('-created_at')
        elif sort_by == 'best_rating':
            queryset = queryset.order_by('likes')

        if show_count:
            paginator = Paginator(queryset, int(show_count))
        else:
            paginator = Paginator(queryset, 3)

        page_number = self.request.GET.get('page')
        object_list = paginator.get_page(page_number)
        context['object_list'] = object_list

        # context['form'] = form
        return context


class CategoryPartialView(TemplateView):
    template_name = 'home/include/category.html'

    def get_context_data(self, **kwargs):
        context = super(CategoryPartialView, self).get_context_data()
        context['category_object'] = Category.objects.all()
        return context


class FeaturedProductsPartialView(TemplateView):
    template_name = 'home/include/product.html'
    model = FeaturedProducts

    def get_context_data(self, **kwargs):
        queryset = FeaturedProducts.objects.all()
        context = super(FeaturedProductsPartialView, self).get_context_data()
        context['feature'] = queryset
        return context


class RecentProductsPartialView(TemplateView):
    template_name = 'home/include/products_list.html'
    queryset = Product.objects.all()

    def get_context_data(self, **kwargs):
        request = self.request
        queryset = Product.objects.all().order_by('-created_at')[:4]
        context = super(RecentProductsPartialView, self).get_context_data()
        context['recent'] = queryset
        return context


def like(request, pk, slug):
    if request.user.is_authenticated:
        try:
            like = Like.objects.get(product__slug=slug, user_id=request.user.id)
            like.delete()
        except Like.DoesNotExist:
            Like.objects.create(product_id=pk, user_id=request.user.id)

        # پس از لایک یا آنلایک، کاربر را به صفحه محصول هدایت کنید.
        return redirect('product:product_detail', pk=pk)


class OfferPartialView(TemplateView):
    template_name = 'home/include/offer.html'
    queryset = OfferProducts.objects.all()

    def get_context_data(self, **kwargs):
        request = self.request
        queryset = OfferProducts.objects.all()
        context = super(OfferPartialView, self).get_context_data()
        context['offer'] = queryset
        return context


class OfferBrand(TemplateView):
    template_name = 'home/include/carousel.html'
    queryset = OfferProducts.objects.all()

    def get_context_data(self, **kwargs):
        request = self.request
        queryset = OfferProducts.objects.all()
        context = super(OfferBrand, self).get_context_data()
        context['offer_brand'] = queryset
        return context


class BrandePartialView(TemplateView):
    template_name = 'home/include/vendor.html'
    queryset = Brande.objects.all()

    def get_context_data(self, **kwargs):
        request = self.request
        queryset = Brande.objects.all()
        context = super(BrandePartialView, self).get_context_data()
        context['all_brand'] = queryset
        return context


@login_required
def liked_products_count_view(request):
    liked_product_count = Like.objects.filter(user=request.user).count()
    return render(request, 'home/include/nav_bar.html', {'liked_product_count': liked_product_count})


class LikedProductsPartialView(TemplateView):
    model = Like
    template_name = 'home/include/liked.html'  # نام تمپلیت مورد استفاده

    def get_context_data(self, **kwargs):
        request = self.request
        queryset = Like.objects.all()
        context = super(LikedProductsPartialView, self).get_context_data()
        context['all_like'] = queryset
        return context


class LikedProductsCountView(TemplateView):
    template_name = 'home/include/nav_bar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        liked_product_count = Like.objects.filter(user=self.request.user).count()
        context['liked_product_count'] = liked_product_count
        return context


def search(request):
    q = request.GET.get('q')
    product = Product.objects.filter(title__icontains=q)
    return render(request, 'products_list.html', context={'object_list': product})


def product_list_category(request, category_slug):
    category = Category.objects.filter(slug=category_slug).first()

    products = category.products.all()

    return render(request, 'home/include/cat_list.html', {'cat_list': products})

