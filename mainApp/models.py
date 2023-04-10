from django.db import models

class Maincategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name

class Subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Brand(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Seller(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=10)
    phone = models.CharField(max_length=15,default=None, null=True, blank=True)
    email = models.EmailField(max_length=30,default=None, null=True, blank=True)
    addressline1 = models.CharField(max_length=50,default=None, null=True, blank=True)
    addressline2 = models.CharField(max_length=50,default=None, null=True, blank=True)
    pincode = models.CharField(max_length=8,default=None, null=True, blank=True)
    city = models.CharField(max_length=20,default=None, null=True, blank=True)
    state = models.CharField(max_length=20,default=None, null=True, blank=True)
    pic = models.FileField(upload_to="image",default=None, null=True, blank=True)

    def __str__(self):
        return str(self.id)+"   "+self.username+"  "+str(self.phone)
    

class Product(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    maincategory = models.ForeignKey(Maincategory, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE)
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=None)
    baseprice = models.IntegerField()
    discount = models.IntegerField()
    finalprice = models.IntegerField()
    size = models.CharField(max_length=100)
    color = models.CharField(max_length=100)
    discription = models.TextField()
    stock = models.CharField(max_length=30, default="In Stock")
    pic1 = models.ImageField(upload_to="image",default=None, null=True, blank=True)
    pic2 = models.ImageField(upload_to="image", default=None, null=True, blank=True)
    pic3 = models.ImageField(upload_to="image", default=None, null=True, blank=True)
    pic4 = models.ImageField(upload_to="image", default=None, null=True, blank=True)

    def __str__(self):
        return str(self.id)+" "+self.name
    
class Buyer(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    username = models.CharField(max_length=10)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=30)
    addressline1 = models.CharField(max_length=50, default=None, null=True, blank=True)
    addressline2 = models.CharField(max_length=50, default=None, null=True, blank=True)
    pincode = models.CharField(max_length=8, default=None, null=True, blank=True)
    city = models.CharField(max_length=20, default=None, null=True, blank=True)
    state = models.CharField(max_length=20, default=None, null=True, blank=True)
    pic = models.FileField(upload_to="image", default=None, null=True, blank=True)

    def __str__(self):
        return str(self.id)+" "+self.username
    
class Wishlist(models.Model):
    id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)

    def __str__(self):
        return str(self.id)+" "+self.buyer.username
    
order = ((0,"Cancel"),(1,"Not Packed"),(2,"Packed"),(3,"Out For Delivery"),(4,"Deliverd"))
payment = ((1,"Pending"),(2,"Done"))
class Checkout(models.Model):
    id = models.AutoField(primary_key=True)
    total = models.IntegerField()
    shopping = models.IntegerField()
    final = models.IntegerField()
    buyer = models.ForeignKey(Buyer,on_delete=models.CASCADE)
    mode = models.CharField(max_length=20,default="COD")
    orderstatus = models.IntegerField(choices=order,default=0)
    paymentstatus = models.IntegerField(choices=payment,default=1)
    rpid = models.CharField(max_length=50,default="",null=True,blank=True)
    roid = models.CharField(max_length=50,default="",null=True,blank=True)
    rsid = models.CharField(max_length=50, default="",null=True,blank=None)
    date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return str(self.id)+" "+self.buyer.username
    
class CheckOutProduct(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    size = models.CharField(max_length=20)
    color = models.CharField(max_length=20)
    price = models.IntegerField()
    qty = models.IntegerField()
    total = models.IntegerField()
    pic = models.ImageField(upload_to="image", default=None, null=True, blank=True)
    checkout = models.ForeignKey(Checkout, on_delete=models.CASCADE)

    def __str__(self):
        return "pid: "+str(self.id)+"CheckOut Id: "+str(self.checkout)

class NewsLatter(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=30,unique=True)

    def __str__(self):
        return self.email
    

contacatStatusChoice = ((1,"Active"),(2,"Done"))
class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=30)
    phone = models.CharField(max_length=15)
    email = models.EmailField(max_length=20)
    subject = models.TextField(max_length=50)
    message = models.TextField(max_length=50)
    status = models.IntegerField(choices=contacatStatusChoice,default=1)

    def __str__(self):
        return str(self.id)+" "+ self.name+" "+self.email
