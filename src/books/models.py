from django.db import models
from publishers.models import Publisher
from authors.models import Author
from django.utils.text import slugify
import uuid
from django.urls import reverse
#imports for qrcode generation
import qrcode
from io import BytesIO
from django.core.files import File
from PIL import Image
from rentals.rental_choices import STATUS_CHOICES
# Create your models here.


class BookTitle(models.Model):
    title = models.CharField(max_length=200, unique=True)
    #optional field
    slug=models.SlugField(blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    @property
    def books(self):
        return self.my_books.all()
    
    def get_absolute_url(self):
        letter = self.title[:1].lower()
        return reverse("books:detail", kwargs={"letter":letter,"slug": self.slug})
    

    def __str__(self):
        return f"Book position: {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=slugify(self.title)
        super().save(*args, **kwargs)



class Book(models.Model):
    isbn = models.CharField(max_length=24, blank=True)
    title= models.ForeignKey(BookTitle, on_delete=models.CASCADE , related_name='my_books')
    qr_code = models.ImageField(upload_to='qr_codes', blank=True, null=True)
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    def __str__(self) :
        return str(self.title)
    
    @property
    def status(self):
        if len(self.rental_set.all())>0:
            statuses = dict(STATUS_CHOICES)
            return statuses [self.rental_set.first().status]
        return False
    
    


    def save(self, *args, **kwargs):
        if not self.isbn:
            self.isbn = str(uuid.uuid4()).replace('-','')[:24].lower()
        qrcode_img = qrcode.make(self.isbn)
        canvas = Image.new('RGB', (qrcode_img.pixel_size, qrcode_img.pixel_size), 'white')
        canvas.paste(qrcode_img)
        fname=f'qr_code-{self.isbn}.png'
        buffer = BytesIO()
        canvas.save(buffer, 'PNG')
        self.qr_code.save(fname, File(buffer), save=False)
        canvas.close()

        super().save(*args, **kwargs)

    