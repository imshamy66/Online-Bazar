from django.contrib import admin
from .models import*

@admin.register(Maincategory)
class MaincategoryAdmin(admin.ModelAdmin):
    list_display = ["id","name"]


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    list_display = ["id","name"]


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ["id","name"]


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ["id","name","maincategory","subcategory","brand","seller","baseprice","discount","finalprice","size","color","discription","stock","pic1","pic2","pic3"]


@admin.register(Seller)
class SellerAdmin(admin.ModelAdmin):
    list_display = ["id","name","username","phone","email","addressline1","addressline2","pincode","city","state","pic"]


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = ["id","name","username","phone","email","addressline1","addressline2","pincode","city","state","pic"]


@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ["id","buyer","product"]


@admin.register(Checkout)
class CheckoutAdmin(admin.ModelAdmin):
    list_display = ["id","total","shopping","final","buyer","mode","orderstatus",'paymentstatus',"rpid","roid","rsid",'date']


@admin.register(CheckOutProduct)
class CheckOutProductAdmin(admin.ModelAdmin):
    list_display = ["id","name","size","color","qty","price","total","checkout","pic"]


@admin.register(NewsLatter)
class NewsLatterAdmin(admin.ModelAdmin):
    list_display = ["id","email"]
 
@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ["id","name","phone","email","subject","message","status"]

