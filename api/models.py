import uuid
from .helpers import url_path
from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, Group, Permission)

class MyUserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError('Users must have an email address')
        user = self.model(
            email=self.normalize_email(email),
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(
            email,
            password=password,
        )
        user.is_admin = True
        user.save(using=self._db)
        return user

class MyUser(AbstractBaseUser):
    email = models.EmailField(
        verbose_name='email address',
        max_length=255,
        unique=True,
    )
    USERNAME_FIELD = 'email'
    name = models.CharField(max_length=255, null=True, blank=True)
    reset_password = models.CharField(max_length=50, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    permissions = models.ManyToManyField(Permission, related_name='+', blank=True)
    groups = models.ManyToManyField(Group, related_name='+', blank=True)
    favorite_store = models.ForeignKey('api.Store', related_name="favorite_users", on_delete=models.SET_NULL, null=True, blank=True)
    objects = MyUserManager()

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

class MetadataManager(models.Manager):
    def get_queryset(self):
        return super().get_queryset().filter(deleted__isnull=True)

class MetaData(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created = models.DateTimeField(auto_now_add=True, blank=True, null=True)
    created_user = models.ForeignKey('api.MyUser', related_name='+', blank=True, null=True, on_delete=models.SET_NULL)
    updated = models.DateTimeField(auto_now=True, blank=True, null=True)
    updated_user = models.ForeignKey('api.MyUser', related_name='+', blank=True, null=True, on_delete=models.SET_NULL)
    deleted = models.DateTimeField(blank=True, null=True)
    deleted_user = models.ForeignKey('api.MyUser', related_name='+', blank=True, null=True, on_delete=models.SET_NULL)
    deleted_reason = models.TextField(blank=True, null=True)
    objects = MetadataManager()

    @property
    def uuid(self):
        return self.id

    class Meta:
        abstract = True

class Brand(MetaData): 
    name = models.CharField(max_length=50)
    logo = models.ImageField(upload_to=url_path, blank=True, null=True)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']
        verbose_name = 'Brand'
        verbose_name_plural = 'Brands' 

class Store(MetaData):
    name = models.CharField(max_length=50)
    identifier = models.CharField(max_length=50)
    address = models.TextField(blank=True, null=True)
    brand = models.ForeignKey('api.Brand', related_name='stores', on_delete=models.CASCADE)

    class Meta:
        ordering = ['name']
        verbose_name = 'Store'
        verbose_name_plural = 'Stores'

class Deal(MetaData):
    name = models.CharField(max_length=50)
    store = models.ForeignKey('api.Store', related_name='deals', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=url_path, blank=True, null=True)
    price = models.DecimalField(max_digits=10, decimal_places=3)

    class Meta:
        ordering = ['name']
        verbose_name = 'Deal'
        verbose_name_plural = 'Deals'

class StoreSuscription(MetaData):
    store = models.ForeignKey('api.Store', related_name='suscriptions', on_delete=models.CASCADE)
    user = models.ForeignKey('api.MyUser', related_name='suscriptions', on_delete=models.CASCADE)
    active = models.BooleanField(default=True)
    class Meta:
        ordering = ['store']
        verbose_name = 'Store Suscription'
        verbose_name_plural = 'Store Suscriptions'