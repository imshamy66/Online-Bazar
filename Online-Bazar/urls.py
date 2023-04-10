from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from mainApp import views

admin.site.site_header="Online Bazar"
admin.site.site_header="Online Bazar"
urlpatterns = [
    path('admin/', admin.site.urls),
    path('',views.home_page),
    path('login/',views.login_page),
    path('signup/',views.sign_up),
    path('profile/',views.seller_profile),
    path('updateprofile/',views.update_profile),
    path('addproduct/',views.addProduct),
    path('delete-product/<int:num>/',views.deleteProduct),
    path('edit-product/<int:num>/',views.editProduct),
    path('logout/',views.logout),
    path('shop/<str:mc>/<str:sc>/<str:br>/',views.shop_page),
    path('single-product/<int:num>/',views.singleProduct),
    path('wishlist/<int:num>/',views.wishlist),
    path('delete-wishlist/<int:num>/',views.deleteWishlist),
    path('add-to-cart/',views.addToCart),
    path('cart/',views.cartPage),
    path('update-cart/<str:id>/<str:num>/',views.updateCart),
    path('delete-cart/<str:id>/',views.deleteCart),
    path('checkout/',views.checkPage),
    path('confirmation/',views.confirmationPage),
    path('paymentSuccess/<str:rpid>/<str:roid>/<str:rsid>/',views.paymentSuccess),
    path('paynow/<int:num>/',views.paynow),
    path('contact/',views.contact),
    path('forget-username/',views.forgetUsername),
    path('forget-otp/',views.forgetOtp),
    path('forget-password/',views.forgetPassword),

]+static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
