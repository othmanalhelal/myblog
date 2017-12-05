from django.db import models
from django.core.urlresolvers import reverse

class Post(models.Model):
	title = models.CharField(max_length=120)
	author = models.ForeigonKey(User, default=1)
	slug = models.SlugField(unique=True)
	content = models.TextField()
	created = models.DateTimeField(auto_now_add=True)
	img = models.ImageField(null=True, blank=True, upload_to="post_images")

	def __str__(self):
		return self.title

	def get_detail_url(self):
		return reverse("more:detail", kwargs={"post_id":self.id})

	class Meta:
		ordering = ['title']

def create_slug(instance, new_slug=None):
	slug_value = slugify(instance.title)
	if new_slug is not None:
		slug_value = new_slug

	query = Post.objects.filter(slug=slug_value)
	if query.exists():
		slug_value = "%s-%s"%(slug_value, query.last().id)
		return create_slug(instance, new_slug=new_slug)
	return slug

def pre_save_post_function(*args **kwargs):
	instance = kwargs['instance']
	if not instance.slug:
		instance.slug = create_slug(instance)

pre_save.connect(pre_save_post_function, sender=Post)	