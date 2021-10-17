from django.db import models

# Create your models here.

class Customer(models.Model):
    id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=100, null=True)
    phone = models.CharField(max_length=10, null=True)
    email = models.CharField(max_length=50, null=True)
    state = models.CharField(max_length=20, null=True)
    postal_code = models.IntegerField(null=True)
    city = models.CharField(max_length=20, null=True)
    address = models.CharField(max_length=100, null=True)
    business_name = models.CharField(max_length=50,null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
	    return str(self.name)


class Post(models.Model):
    p_id = models.IntegerField(primary_key=True, null=False)
    name = models.CharField(max_length=50,null=True)
    description = models.CharField(max_length=1000, null=True)
    photo = models.ImageField(upload_to="images/",null=True,verbose_name="")
    owner = models.ForeignKey(Customer, null=True, on_delete= models.CASCADE)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    category = models.CharField(max_length=100, null=True)
    availability = models.CharField(max_length=20, null=True)
    location = models.CharField(max_length=50, null=True)
    business_name = models.CharField(max_length=50,null=True)
    price = models.IntegerField(null=True)
   

    def __str__(self):
	    return str(self.name)

    @property
    def imageURL(self):
        try:
            url = self.photo.url
        except :
            url = ''
        return url


class Comment(models.Model):
    c_id = models.IntegerField(primary_key = True, null = False)
    text = models.CharField(max_length=200, null=True)
    p_id = models.ForeignKey(Post, null =True, on_delete = models.CASCADE)
    c_by = models.ForeignKey(Customer, null=True, on_delete = models.SET_NULL)
    timestamp = models.DateTimeField(auto_now_add=True, null=True) 

    def __str__(self):
	    return self.c_id

    



