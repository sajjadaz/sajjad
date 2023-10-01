from django.urls import path
from . import views
from .views import NavbarPartialView, CategoryPartialView, FeaturedProductsPartialView, RecentProductsPartialView, \
    OfferPartialView, OfferBrand, BrandePartialView, LikedProductsPartialView, LikedProductsCountView

app_name = "product"
urlpatterns = [
    path('all', views.ProductListView.as_view(), name='product_list'),
    path('search', views.search, name='search'),
    path('<int:pk>', views.ProductDetailView.as_view(), name='product_detail'),# az inja bayad benevisam havaset bashe vaseye category list
    # path('feature/<int:pk>', views.FeatureProductDetailView.as_view(), name='feature_detail'),# az inja bayad benevisam havaset bashe vaseye category list
    path('navbar', NavbarPartialView.as_view(), name='navbar'),
    path('Cat', CategoryPartialView.as_view(), name='cat'),
    path('Feature', FeaturedProductsPartialView.as_view(), name='Feature'),
    path('category/<slug:category_slug>/', views.product_list_category, name='product_list_by_category'),
    path('recent', RecentProductsPartialView.as_view(), name='recent'),
    path('offer', OfferPartialView.as_view(), name='offer'),
    path('offer_brand', OfferBrand.as_view(), name='offer_brand'),
    path('brande', BrandePartialView.as_view(), name='brande'),
    path('liked-products-count', LikedProductsCountView.as_view(), name='liked-products-count'),
    path('ob', LikedProductsPartialView.as_view(), name='liked-products'),
    path('like/<slug:slug>/<int:pk>', views.like, name='like'),
]
