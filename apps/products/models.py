from django.db import models
from django.db.models import Q
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _
import uuid
from apps.base_models import *
from django.utils.text import slugify
from ckeditor.fields import RichTextField
from djchoices import DjangoChoices, ChoiceItem
from django.utils import timezone
import random
from django.conf import settings

# INTERNALS
from .validators import validate_file_extension, validate_slug


class Categories(BaseModel):
    slug = models.SlugField(max_length=120, primary_key=True, unique=True, verbose_name=_('Slug'), editable=False, validators=[validate_slug])
    title = models.CharField(max_length=120, verbose_name=_('title'), validators=[validate_slug])
    image = models.ImageField(upload_to='categories', null=True, blank=True)
    @property
    def imageURL(self):
        return '%s%s'%(
                settings.BASE_SITE_DOMAIN, self.image.url
                )  if (self.image and hasattr(self.image, 'url')) else None
    # category = models.ForeignKey('self', on_delete=models.SET_NULL, null=True)

    class Meta:
        ordering = ("-modified_at", "-created_at")
        verbose_name = _('Category')
        verbose_name_plural = _('Categories')
    
    def __str__(self):
        return self.title
    

    @property
    def subcategories(self):
        return self.subcategories_set.all()

    @property
    def products(self):
        return self.products_set.all()

    @property
    def count_products(self):
        return self.products.count()


    def save(self, *args, **kwargs):
        print(self.title, self.slug)
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title_en)
            k = 1
            while self.check_existance_of_slug():
                self.slug = slugify(
                    '%s-%d'%(self.slug, k))
                k += 1
        return super(Categories, self).save(*args, **kwargs)

    def check_existance_of_slug(self):
        print(self.slug)
        return self.__class__.objects.filter(slug=self.slug).count()


class SubCategories(BaseModel):
    slug = models.SlugField(max_length=120, primary_key=True, unique=True, verbose_name=_('Slug'), editable=False, validators=[validate_slug])
    title = models.CharField(max_length=120, verbose_name=_('title'), validators=[validate_slug])
    category = models.ForeignKey(
        Categories, models.SET_NULL, null=True, verbose_name=_('Category')
    )
    image = models.ImageField(upload_to='subcategories', null=True, blank=True)
    @property
    def imageURL(self):
        return '%s%s'%(
                settings.BASE_SITE_DOMAIN, self.image.url
                )  if (self.image and hasattr(self.image, 'url')) else None

    @property
    def products(self):
        return self.products_set.all()

    class Meta:
        ordering = ("-modified_at", "-created_at")
        verbose_name = _('Sub Category')
        verbose_name_plural = _('Sub Categories')

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '':
            self.slug = slugify(self.title_en)
            k = 1
            while self.check_existance_of_slug():
                self.slug = slugify(
                    '%s-%d'%(self.slug, k))
                k += 1
        return super(SubCategories, self).save(*args, **kwargs)

    def check_existance_of_slug(self):
        print(self.slug)
        return self.__class__.objects.filter(slug=self.slug).count()

class Products(BaseModel):

    class STATUS(DjangoChoices):
        not_in_stock = ChoiceItem('default', 'Not In Stock')
        in_stock = ChoiceItem('in_stock', 'In Stock')
        archived = ChoiceItem('archived', 'Archived')

    slug = models.SlugField(max_length=120, primary_key=True, unique=True, verbose_name=_('Slug'), validators=[validate_slug])
    title = models.CharField(max_length=120, verbose_name=_('title'), validators=[validate_slug])
    category = models.ForeignKey(
        Categories, models.SET_NULL, null=True, verbose_name=_('Category')
    )
    sub_category = models.ForeignKey(
        SubCategories, models.SET_NULL, related_name='products', null=True, verbose_name=_('Sub category')
    )
    description = RichTextField(config_name='default')
    characteristics = RichTextField(config_name='default')

    status = models.CharField(
        max_length=20,
        choices=STATUS.choices,
        default=STATUS.not_in_stock
    )

    price = models.FloatField(
        verbose_name=_('Price in stock'),
        default=0.0,
        help_text=_('Price needs to be input in USD')
    )

    quantity = models.PositiveBigIntegerField(verbose_name=_('Quantity'), help_text=_('How many/much is there on base?'), null=True, blank=True)
    seen = models.PositiveBigIntegerField(default=0)
    # @property
    # def price_in_soum(self):
    
    @property
    def comments(self):
        return self.productcomments_set.all()
    
    @property
    def comments_count(self):
        return self.comments.count()


    @property
    def in_promotion(self):
        now = timezone.now()

        return self.promotions_set.filter(date_from__lte=now, date_till__gte=now).first()

    @property
    def similar_products(self):
        return Products.objects.filter(
            Q(category=self.category) |
            Q(sub_category=self.sub_category)
            ).exclude(
                Q(slug=self.slug)|
                Q(status=Products.STATUS.archived)
            )[:20]

    @property
    def images(self):
        return self.productimages_set.all()


    @property
    def thumbnail(self):
        return self.images.first()

    @property
    def price_UZS(self):
        active_currency = Currency.objects.last()
        if active_currency is None:
            return 0
        return self.price * active_currency.value

    def __str__(self):
        return '%s'%(self.slug)


    class Meta:
        ordering = ("-modified_at", "-created_at")
        verbose_name = _('Product')
        verbose_name_plural = _('Products')

    def save(self, *args, **kwargs):
        if self.slug is None or self.slug == '': 
            self.slug = slugify(self.title_en)
            k = 1
            while self.check_existance_of_slug():
                self.slug = slugify(
                    '%s-%d'%(self.slug, k))
                k += 1
        return super(Products, self).save(*args, **kwargs)

    def check_existance_of_slug(self):
        print(self.slug)
        return self.__class__.objects.filter(slug=self.slug).count()

class ProductImages(BaseModel):
    id = models.UUIDField(unique=True, primary_key=True, default=uuid.uuid1, editable=False)
    image = models.FileField( upload_to="products", validators=[validate_file_extension])
    product = models.ForeignKey(
        Products, models.CASCADE, 
        verbose_name=_("Product")
    )

    @property
    def imageURL(self):
        return '%s%s'%(
                settings.BASE_SITE_DOMAIN, self.image.url
                )  if (self.image and hasattr(self.image, 'url')) else None

    class Meta:
        ordering = ('-modified_at', '-created_at', )
        verbose_name = _('Product Image')
        verbose_name_plural = _('Product Images')

    def __str__(self):
        return '%s'%(self.id)

class Promotions(BaseModel):
    id = models.UUIDField(default=uuid.uuid1, unique=True, primary_key=True, editable=False)
    title = models.CharField(max_length=120, verbose_name=_('title'))
    
    date_from = models.DateField(verbose_name=_('date from'), null=True,blank=True)
    date_till = models.DateField(verbose_name=_('date till'), null=True,blank=True)

    description = RichTextField(null=True,blank=True)

    products = models.ManyToManyField(
        Products, null=True, blank=True
    )

    percentage = models.FloatField(
        verbose_name=_('Percentage')
    )

    image = models.ImageField(_('Promotion image'), upload_to='promotions', null=True, blank=True)
    
    @property
    def imageURL(self):
        return '%s%s'%(
                settings.BASE_SITE_DOMAIN, self.image.url
                )  if (self.image and hasattr(self.image, 'url')) else None

    
    @property
    def is_active(self):
        now = timezone.now().date()
        return (now >= self.date_from and now <= self.date_till ) if self.date_from and self.date_till else False 


    class Meta:
        ordering = ('-id', '-modified_at', '-created_at')
        verbose_name = _('Promotion')
        verbose_name_plural = _('Promotions')


class ProductComments(BaseModel):
    created = None
    modified = None
    name = models.CharField(max_length=120)
    review = models.PositiveIntegerField()
    comment = models.TextField(max_length=5000)
    product = models.ForeignKey(
        Products, models.CASCADE
    )
    def __str__(self):
        return self.name

    class Meta:
        ordering = ("-id", )
        verbose_name = _('Comment')
        verbose_name_plural = _('Comments')


class Contacts(models.Model):
    SEEN = 'seen'
    NOT_SEEN = 'not-seen'
    CHOICES = (
        (SEEN, 'ADMIN k\'rdi'),
        (NOT_SEEN, 'ADMIN ko\'rmadi'),
    )
    name = models.CharField(_('User name'), max_length=200)
    text = models.CharField(max_length=5000)
    date_created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=CHOICES)
    file = models.FileField(null=True, blank=True, upload_to='contacts')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = _('Contacts')
        verbose_name_plural = _('Contacts')

    @property
    def fileURL(self):
        return '%s%s'%(
                settings.BASE_SITE_DOMAIN, self.file.url
                )  if (self.file and hasattr(self.file, 'url')) else None


class Currency(models.Model):

    value = models.IntegerField(_("dollar value"))

    def __str__(self):
        return str(self.value)