from django.urls import path
from . import views
from .views import dashboard_view, login_view, logout_view, register_view
from django.conf import settings
from django.conf.urls.static import static

app_name = 'main'

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path("register/", register_view, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("dashboard/", dashboard_view, name="dashboard"),
    path('<slug:category_slug>/', views.product_list, name='product_list_by_category'),
    path('<int:id>/<slug:slug>', views.product_detail, name='product_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)