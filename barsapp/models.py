from django.db import models
from django.contrib.auth.models import User


###############################################################################
# Global models
###

class GlobalUser(models.Model):
    '''Information shared by all user's bars

    auth_user : contains username, first_name, last_name, email, password
        is_staff (not used), is_active, is_superuser (not used), last_login,
        date_joined'''
    auth_user = models.OneToOneField(User)
    frankiz_id = models.CharField(max_length=100)
    
class Bar(models.Model):
    '''Information about a bar

    hrname : human readable name
    name : name used internally. Must be in regex class [a-z]+
    charges : percentage per day (0 for no charges)
    amount : bar current amount of money'''
    hrname = models.CharField(max_length=25)
    name = models.CharField(max_length=25)
    charges = models.FloatField()
    amount = models.FloatField()

class IP(models.Model):
    '''A user can have several IP adresses, or an IP can refer to a bar

    sort : the IP refer to a bar or to a user
    user : the user the IP belongs to
    bar : the bar the IP belongs to'''
    USER = 0
    BAR = 1
    ip = models.IPAddressField(unique=True)
    sort = models.IntegerField()
    user = models.ForeignKey(User, null=True)
    bar = models.ForeignKey(Bar, null=True)


###############################################################################
# Telemarket models
###

class Category(models.Model):
    '''Telemarket goods are sorted in a 3 level hierarchy.

    name_cat : name of the main category (eg Frais, Boissons...)
    name_sub : subcategory (eg Charcuterie, Poissonerie...)
    name_subsub : subsubcategory (eg Poissons frais, poissons fumés...)'''
    name_cat = models.CharField(max_length=200)
    name_sub = models.CharField(max_length=200)
    name_subsub = models.CharField(max_length=200)

class TelemarketItem(models.Model):
    '''Telemarket goods information

    name : human-readable name
    ref : telemarket reference
    cookie_ref : reference used for online ordering, normally same as ref
    price : telemarket price
    unit : may be one of the followings 'kg', 'L', 'unit'
    qty : quantity
    price_qty : price divided by quantity
    description : telemarket description of goods
    thumbnail : varying part of the thumbnail url (thumbnail : about 5ko)
    image : varying part of the image url (image : about 100ko)
    category : goods category
'''
    name = models.CharField(max_length=200)
    ref = models.IntegerField()
    cookie_ref = models.IntegerField()
    price = models.FloatField()
    unit = models.CharField(max_length=50)
    qty = models.FloatField()
    price_qty = models.CharField(max_length = 50)
    description = models.TextField()
    thumbnail = models.TextField(max_length = 200)
    image = models.TextField(max_length = 200)
    category = models.ManyToManyField(Category)


###############################################################################
# Bar models
###

class BarsUser(models.Model):
    '''Bar specific information about a user

    section : member of the section ?
    total : sum of all the money the user spent in the bar'''
    user = models.ForeignKey(User)
    bar = models.ForeignKey(Bar)
    pseudo = models.CharField(max_length = 100)
    section = models.BooleanField()
    respo = models.BooleanField()
    credit = models.FloatField()
    total = models.FloatField()


###############################################################################


class BarsTax(models.Model):
    '''Defines the tax policy for a bar food

    sort:
        NO_POLICY : Individual tax policy.
        AUTO_POLICY : Automatic tax policy (based on thefts...).
            BarsFood.tax_percentage is the tax percentage
        DEFINED_POLICY : param is the tax percentage'''
    POLICY_CHOICES = (
        (0, 'Taxe par produit'),
        (1, 'Taxe automatique'),
        (2, 'Taxation groupée')
    )
    name = models.CharField(max_length=200)
    sort = models.IntegerField(choices=POLICY_CHOICES)
    param = models.FloatField(null=True)

    class Meta:
        abstract = True

class JudoJoneTax(BarsTax):
    pass

class BadJoneTax(BarsTax):
    pass


###############################################################################

class BarsFood(models.Model):
    '''Can be logged by bar users
    
    name : name of the food
    tax_percentage : used if tax.sort is NO_POLICY
    amount : value of all goods related to the food'''
    name = models.CharField(max_length=200)
    tax_percentage = models.IntegerField()
    amount = models.FloatField()

    class Meta:
        abstract = True

class JudoJoneFood(BarsFood):
    tax = models.ForeignKey(JudoJoneTax)
    pass

class BadJoneFood(BarsFood):
    tax = models.ForeignKey(BadJoneTax)
    pass


###############################################################################

class BarsHistory(models.Model):
    '''History of all bar's transactions

    BUYING : user pays, logguer logs on IP
    DONATION : logguer pays, user recieves
    SUPPLYING : user supplies
    THEFT : logguer reports a theft
    PROVISION : user's amount is increased, 
    FINE : user receives a fine from logguer
    GARBAGE : logguer reports
    INVENTORY : logguer reports
    EVENT : logguer logs
    CHARGES : user receives charges'''
    BUYING = 0
    DONATION = 9
    SUPPLYING = 2
    THEFT = 3
    PROVISION = 4
    FINE = 5
    GARBAGE = 6
    INVENTORY = 7
    EVENT = 8
    CHARGES = 10
    sort = models.IntegerField()

    user = models.ForeignKey(BarsUser, null=True)
    logger = models.ForeignKey(
        BarsUser, related_name="%(class)s_as_logger_set", null=True)
    qty = models.FloatField(null=True)
    amount = models.FloatField()
    date = models.DateTimeField()
    ip = models.IPAddressField()
    # description : only for sort=EVENT
    description = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True

class JudoJoneHistory(BarsHistory):
    food = models.ForeignKey(JudoJoneFood)

class BadJoneHistory(BarsHistory):
    food = models.ForeignKey(BadJoneFood)


###############################################################################

class BarsItem(models.Model):
    '''Item a bar regularly buys

    order : ideal quantity of the item the bar has'''
    telemarket_item = models.ForeignKey(TelemarketItem)
    order = models.IntegerField()

    class Meta:
        abstract = True

class JudoJoneItem(BarsItem):
    judojone_item = models.ForeignKey(JudoJoneFood)

class BadJoneItem(BarsItem):
    badjone_item = models.ForeignKey(JudoJoneFood)

