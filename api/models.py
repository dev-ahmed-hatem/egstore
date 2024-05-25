from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db.models.signals import pre_delete
from django.dispatch import receiver
from django.utils import timezone
from django.contrib import auth


# Create custom user manger
class CustomUserManager(BaseUserManager):
    def create_user(self, phone_number, first_name, last_name, password=None, **kwargs):
        """
        Creates and saves a User with the given phone_number, first name,
        last name, and password.
        """
        if not phone_number:
            raise ValueError("Users must have a phone number")

        user = self.model(
            phone_number=phone_number,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, first_name, last_name, password=None, **kwargs):
        """
        Creates and saves a superuser with the given phone_number, first name,
        last name, and password.
        """
        user = self.create_user(
            phone_number,
            password=password,
            first_name=first_name,
            last_name=last_name,
            **kwargs
        )
        user.is_admin = True
        user.save(using=self._db)
        return user


class UserProfile(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    username = models.CharField(max_length=30, unique=True)
    phone_number = models.CharField(max_length=15, unique=True)
    picture = models.ImageField(upload_to="profile_pictures/", blank=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "phone_number"
    REQUIRED_FIELDS = ["first_name", "last_name", "username", ]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        if not self.is_active or self.is_anonymous:
            return False

        if self.is_superuser:
            return True

        if obj is not None:
            return _user_has_perm(self, perm, obj)

        for backend in auth.get_backends():
            if backend.has_perm(self, perm):
                return True

        return False

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


class Category(models.Model):
    title = models.CharField(max_length=100)
    picture = models.ImageField(upload_to="categories_pictures/", blank=True)

    class Meta:
        verbose_name_plural = "Categories"

    def __str__(self):
        return self.title


class Sale(models.Model):
    discount_percentage = models.DecimalField(max_digits=5, decimal_places=2)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f"{self.discount_percentage}% off"


# delete a sale after end time
@receiver(pre_delete, sender=Sale)
def delete_expired_sale(sender, instance, **kwargs):
    if instance.end_date < timezone.now().date():
        instance.delete()


class Product(models.Model):
    title = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    sale = models.ForeignKey(Sale, null=True, blank=True, on_delete=models.SET_NULL, related_name='products')

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_pictures/')


class Order(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name="order_history")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date_created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order #{self.id} - {self.date_created.strftime('%Y-%m-%d')}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.count} of {self.product.title} in Order #{self.order.id}"


class Cart(models.Model):
    user = models.OneToOneField(UserProfile, on_delete=models.CASCADE)

    def __str__(self):
        return f"Cart for {self.user.username}"


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="cart_items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    count = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.count} of {self.product.title}"
