from django.core.exceptions import ValidationError
from django.db.models.enums import Choices
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from django.forms.widgets import TextInput


states = ["Andhra Pradesh", "Arunachal Pradesh", "Assam","Bihar","Chhattisgarh","Goa","Gujarat","Haryana",
			"Himachal Pradesh","Jammu and Kashmir","Jharkhand","Karnataka","Kerala","Madhya Pradesh",
			"Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Punjab","Rajasthan",
			"Sikkim","Tamil Nadu","Telangana","Tripura","Uttar Pradesh","Uttarakhand","West Bengal",
			"Andaman and Nicobar Islands","Chandigarh","Dadra and Nagar Haveli","Daman and Diu",
			"Lakshwadeep","National Capital Territory of Delhi","Puducherry"]

shipping_opt = ["Local","Span-India","Global"]
category_opt = ["Accessories","Art","Clothing","Electronics","Food Items","Handicraft","Home Decor",
				"Others"]


state_choices =tuple([(x,x) for x in states])  
shipping = tuple([(x,x) for x in shipping_opt])
category = tuple([(x,x) for x in category_opt])

# state_choices = (("Andhra Pradesh", "Andhra Pradesh"), ("Arunachal Pradesh ", "Arunachal Pradesh "), 
# 				 ("Assam", "Assam"), ("Bihar", "Bihar"),("Chhattisgarh", "Chhattisgarh"), 
# 				 ("Goa", "Goa"), ("Gujarat","Gujarat"), ("Haryana", "Haryana"), ("Himachal Pradesh", "Himachal Pradesh"),
#                  ("Jammu and Kashmir ", "Jammu and Kashmir "), ("Jharkhand", "Jharkhand"), ("Karnataka", "Karnataka"), 
# 				 ("Kerala", "Kerala"), ("Madhya Pradesh", "Madhya Pradesh"), ("Maharashtra", "Maharashtra"),
# 				 ("Manipur", "Manipur"), ("Meghalaya", "Meghalaya"), ("Mizoram", "Mizoram"), ("Nagaland", "Nagaland"), ("Odisha", "Odisha"), ("Punjab", "Punjab"), ("Rajasthan", "Rajasthan"), 
# 				 ("Sikkim", "Sikkim"), ("Tamil Nadu", "Tamil Nadu"), ("Telangana", "Telangana"), 
# 				 ("Tripura", "Tripura"), ("Uttar Pradesh", "Uttar Pradesh"), ("Uttarakhand", "Uttarakhand"), 
# 				 ("West Bengal", "West Bengal"), ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"), 
# 				 ("Chandigarh", "Chandigarh"), ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"), 
# 				 ("Daman and Diu", "Daman and Diu"), ("Lakshadweep", "Lakshadweep"), 
# 				 ("National Capital Territory of Delhi", "National Capital Territory of Delhi"), 
# 				 ("Puducherry", "Puducherry"))

# shipping = (("Local", "Local"), ("Span-India",
#                                  "Span-India"), ("Global", "Global"),)

# category = (("Accessories", "Accessories"), ("Art", "Art"), ("Clothing", "Clothing"), ("Electronics", "Electronics"),
#             ("Food Items", "Food Items"), ("Handicraft", "Handicraft"), ("Home Decor", "Home Decor"), ("Others", "Others"))


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email']


# def validate_positive(value):
#     try:
#     if value <= 0:
#         raise ValidationError("Only Positive Numbers Accepted!")

class CreatePost(forms.Form):
    name = forms.CharField(label="Name", max_length=200)
    category = forms.CharField(
        label="Category", widget=forms.Select(choices=category))
    description = forms.CharField(
        label="Description", widget=forms.Textarea(attrs={"rows": 2, "cols": 40}))
    image = forms.FileField(widget=forms.ClearableFileInput(
        attrs={'id': 'image-upload', 'onchange': 'readURL(this);','style': 'border: none; background: none; color:white '}))
    availability = forms.CharField(
        label="Shipping...", widget=forms.Select(choices=shipping))
    price = forms.IntegerField(label="Price &#8377;", required=True,min_value=1,initial=1)


class ProfileForm(forms.Form):
    u_name = forms.CharField(label='Name', max_length=100,
                             widget=forms.TextInput(attrs={'placeholder': ''}))
    phone = forms.CharField(label='Phone', required=True, max_length=10,
                            widget=forms.TextInput(attrs={'placeholder': ''}))
    email = forms.EmailField(label='Business Email',widget=forms.EmailInput(attrs={'placeholder': '', 'style': 'background-color: white'}))
    business_name = forms.CharField(
        label='Business Name', max_length=100, widget=forms.TextInput(attrs={'placeholder': ' '}))
    state = forms.CharField(
        label="State", widget=forms.Select(choices=state_choices))
    city = forms.CharField(label='City', max_length=20,
                           widget=forms.TextInput(attrs={'placeholder': ''}))
    postal_code = forms.CharField(
        label="Postal Code", max_length=6, widget=forms.TextInput(attrs={'placeholder': ''}))
    address = forms.CharField(label="Address", max_length=100,
                              widget=forms.TextInput(attrs={'placeholder': ''}))
