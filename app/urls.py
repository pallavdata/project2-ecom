from django.urls import path
from . import views

urlpatterns = [
    path("", views.home,name="home"),
    path("cart/", views.cart_data,name="cart_data"),
    path("signup/", views.signup, name="signup"),
    path("add-to-cart/<int:id>/", views.add_to_cart, name="add_to_cart"),
    path("data-delete/<int:id>/", views.add_to_cart_delete, name="add_to_cart_delete"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("data-add/<int:id>/",views.add_to_cart_main),
    # path("address/edit/<int:id>/",views.address_edit.as_view()),
    path("address/edit/<int:id>/",views.address_edit),
    path("address/delete/<int:id>/",views.address_delete,name="address_delete"),
    path("address/",views.address_view),
    path("buy_now/",views.buy_now, name="buy_now"),
    path("order/",views.order_view, name="order"),
    path("order/delete/<int:id>/",views.order_delete, name="order_delete"),
]