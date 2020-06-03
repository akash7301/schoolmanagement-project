from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.db.models.signals import post_save

# Create your models here.

class Genre(models.Model):
    name = models.CharField(max_length = 200,help_text="Enter a book genre (e.g Science Fiction, French Poetry etc.)")

    def __str__(self):
        return self.name

class Language(models.Model):
    name = models.CharField(max_length=200,help_text="Enter the book's natural language (e.g English,Hindi,Chinese etc.)")

    def __str__(self):
        return self.name

#book relation that has 2 foreign kry auther Language
#book relation can contain multiple genre so we have used manytomanyfield

class Book(models.Model):
    title = models.CharField(max_length=200)
    auther = models.CharField(max_length=100)
    summary = models.TextField(max_length=1000,help_text='Enter a brief description of the book')
    isbn = models.CharField('ISBN',max_length=13,help_text='13 character <a href="https://www.isbn-international.org/content/what-isbn">ISBN number</a>')
    genre = models.ManyToManyField(Genre,help_text='Select a genre for this book')
    language = models.ForeignKey('Language',on_delete=models.SET_NULL,null=True)
    total_copies = models.IntegerField()
    available_copies = models.IntegerField()
    pic = models.ImageField(blank=True,null=True)

    def get_absolute_url(self):
        return reverse('book-detail',args=[str(self.id)])

    def __str__(self):
        return self.title

def create_user(sender, *args, **kwargs):
    if kwargs['created']:
        user = User.objects.create(username=kwargs['instance'],password="dummypass")


class Student(models.Model):
    roll_no = models.CharField(max_length=12,unique=True)
    name = models.CharField(max_length=30)
    branch = models.CharField(max_length=20)
    contact_no = models.CharField(max_length=10)
    total_book_due = models.IntegerField(default=0)
    email = models.EmailField(unique=True)
    pic = models.ImageField(blank=True)

    def __str__(self):
        return str(self.roll_no)

post_save.connect(create_user,sender=Student)


class Borrower(models.Model):
    student = models.ForeignKey('Student',on_delete=models.CASCADE)
    book = models.ForeignKey('Book',on_delete=models.CASCADE)
    issue_date = models.DateTimeField(null=True,blank=True)
    return_date = models.DateTimeField(null=True,blank=True)

    def __str__(self):
        return self.student.name+" borrowed "+self.book.title


class Reviews(models.Model):
    review = models.CharField(max_length=100,default='none')
    book = models.ForeignKey('Book',on_delete=models.CASCADE)
    student = models.ForeignKey('Student',on_delete=models.CASCADE)
    CHOICES = (
        ('0','0'),
        ('.5','.5'),
        ('1','1'),
        ('1.5','1.5'),
        ('2','2'),
        ('2.5','2.5'),
        ('3','3'),
        ('3.5','3.5'),
        ('4','4'),
        ('4.5','4.5'),
        ('5','5'),
    )
    rating = models.CharField(max_length=3,choices=CHOICES,default='2')
