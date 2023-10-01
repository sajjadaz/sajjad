from autoslug.settings import slugify
from django.db import models
from django.db.models import ExpressionWrapper, Count


from account.models import User


class Size(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Color(models.Model):
    title = models.CharField(max_length=10)

    def __str__(self):
        return self.title


class Category(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True, related_name='subs', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='category/images', blank=True, null=True)
    title = models.CharField(max_length=50)
    slug = models.SlugField()

    def __str__(self):
        return self.title


class Type(models.Model):
    title = models.CharField(max_length=30)

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=30)
    slug = models.SlugField(unique=True, blank=True)
    description = models.TextField()
    price = models.IntegerField()
    discount = models.SmallIntegerField()
    size = models.ManyToManyField(Size, related_name='products', blank=True, null=True)
    color = models.ManyToManyField(Color, related_name='products', blank=True, null=True)
    type = models.ManyToManyField(Type, related_name="products", blank=True, null=True)
    category = models.ManyToManyField(Category, related_name='products', blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    def get_comment_count(self):
        return self.comments.annotate(reply_count=Count('replys')).count()

    # class Meta:
    #     ordering = ('-created',)


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='product_images/')  # آدرس ذخیره‌سازی تصاویر

    def __str__(self):
        return f"Image for {self.product.title}"


class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes', verbose_name='کاربر')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='likes', verbose_name='محصول')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}-{self.product.title}"

    class Meta:
        verbose_name = 'لایک'
        verbose_name_plural = 'لایک ها'
        ordering = ('-created_at',)


class OrderItem(models.Model):
    item = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"order of {self.item.title}"

    def get_total_item_price(self):
        """calculate price by quantity ,ex 4 phone of 100$ would be 400$ """
        return self.quantity * self.item.price

    def get_item_price_after_discount(self):
        """calculate price with discount ,ex 1 phone of 100$ with 25% would be 100*0.25 = 75$ """
        return self.item.price * self.item.discount

    def get_total_discount_item_price(self):
        """calculate price by quantity with discount ,ex 4 phone of 100$ with 25% would be 400*0.25 = 300$ """
        return self.quantity * self.get_item_price_after_discount()

    def get_difference_price_after_discount(self):
        """,ex 4 phone of 100$ with 25% would be (400$ - 400*0.25 = 100$) """
        return self.get_total_item_price() - self.get_total_discount_item_price()


class Information(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="information", null=True, blank=True)
    text = models.TextField()

    def __str__(self):
        return self.text[:30]


class FeaturedProducts(models.Model):
    image = models.ImageField(blank=True, null=True, upload_to='FeaturedProducts/images')
    title = models.CharField(max_length=50, blank=True, null=True)
    price = models.FloatField()
    slug = models.SlugField()
    description = models.TextField()
    discount = models.SmallIntegerField()
    size = models.ManyToManyField(Size, related_name='fproducts', blank=True, null=True)
    color = models.ManyToManyField(Color, related_name='fproducts', blank=True, null=True)
    type = models.ManyToManyField(Type, related_name="fproducts", blank=True, null=True)

    def __str__(self):
        return self.title


class OfferProducts(models.Model):
    product = models.ForeignKey(Product, blank=True, null=True, on_delete=models.CASCADE, related_name='products')
    image = models.ImageField(upload_to='offer/image')
    price = models.IntegerField()
    discount = models.IntegerField()

    @property
    def total_price(self):
        return int(self.price - (self.price * self.discount / 100))

    def __str__(self):
        if self.product:
            return self.product.title
        return f"Offer #{self.id}"


class Brande(models.Model):
    brande = models.CharField(max_length=30, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True)
    image = models.ImageField(upload_to='image/brande')

    def __str__(self):
        return self.brande


class Comments(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, blank=True, null=True, related_name='comments')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replys', blank=True, null=True,
                               default=None)

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', null=True, blank=True)
    body = models.TextField(max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body[:50]
