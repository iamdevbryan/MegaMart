from django.urls import path
from .views import (product_list, shop_list, login_view, register_view,get_category,
                     get_order, add_to_order,
    remove_from_order, clear_order
                    )
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path('api/products/', product_list, name="product-list"),
    path('api/shops/', shop_list, name="shop-list"),
     path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),

    path('api/category/<str:category_name>', get_category, name='get-category'),
    path('api/orders/user/<int:user_id>/', get_order, name="get-order"),
    path('api/orders/add/<int:user_id>/', add_to_order, name="add-to-order"),
    path('api/orders/remove/<int:item_id>/', remove_from_order, name="remove-from-order"),
    path('api/orders/clear/<int:user_id>/', clear_order, name="clear-order"),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
     
urlpatterns+= staticfiles_urlpatterns()