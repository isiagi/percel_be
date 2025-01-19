"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.conf.urls import include
from customer import urls as customer_urls
from sale import urls as sale_urls
from product import urls as product_urls
from category import urls as category_urls
from expense import urls as expense_urls
from supplier import urls as supplier_urls
from users import urls as users_urls

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/users/', include(users_urls)),
    path('api/customer/', include(customer_urls)),
    path('api/sale/', include(sale_urls)),
    path('api/product/', include(product_urls)),
    path('api/category/', include(category_urls)),
    path('api/expense/', include(expense_urls)),
    path('api/supplier/', include(supplier_urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
