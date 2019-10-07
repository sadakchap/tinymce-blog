from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from tinymce.models import HTMLField
from taggit.managers import TaggableManager
from PIL import Image
# Create your models here.

class Author(models.Model):
	user	= models.OneToOneField(User,on_delete=models.CASCADE)
	image 	= models.ImageField('profile_pics/',default='static/default_images/person.png')

	def __str__(self):
		return '{} author'.format(self.user.username)

	def save(self,*args,**kwargs):
		super(Author,self).save(*args,**kwargs)
		img = Image.open(self.image.path)
		if img.width>300 or img.height>300:
			output_size = (300,300)
			img.thumbnail(output_size)
			img.save(self.image.path)


class PublishManager(models.Manager):
	def get_queryset(self):
		return super(PublishManager,self).get_queryset().filter(feature=True)


class Post(models.Model):
	title		= models.CharField(max_length=255)
	slug		= models.SlugField(max_length=255,unique_for_date='pub_date')
	author 		= models.ForeignKey(Author,on_delete=models.CASCADE,related_name='author_posts')
	body		= HTMLField()
	thumbnail	= models.ImageField(upload_to='post_pics/',default='static/default_images/post_pic.jpg')
	created		= models.DateTimeField(auto_now_add=True)
	pub_date	= models.DateTimeField(default=timezone.now)
	updated		= models.DateTimeField(auto_now=True)
	feature		= models.BooleanField(default=True)
	tags 		= TaggableManager()

	objects 	= models.Manager()
	published 	= PublishManager()

	def __str__(self):
		return self.title

	def get_absolute_url(self):
		return reverse('blog:detail',kwargs={'slug':self.slug})

class Comment(models.Model):
	text		= models.TextField()
	active		= models.BooleanField(default=True)
	author 		= models.ForeignKey(Author,on_delete=models.CASCADE,related_name='author_comments')
	post 		= models.ForeignKey(Post,on_delete=models.CASCADE,related_name='comments')
	created		= models.DateTimeField(auto_now_add=True)
	updated		= models.DateTimeField(auto_now=True)

	def __str__(self):
		return '{} Commented on {}'.format(self.author,self.post.title)


from django.dispatch import receiver

@receiver(models.signals.post_save,sender=User)
def create_author(sender,instance,created,**kwargs):
	if created:
		Author.objects.create(user=instance)

@receiver(models.signals.post_save,sender=User)
def save_author(sender,**kwargs):
	kwargs['instance'].author.save()
