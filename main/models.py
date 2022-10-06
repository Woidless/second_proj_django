from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=150)
    parent = models.ForeignKey('self',
                                on_delete=models.CASCADE,
                                related_name='subclass',
                                blank=True,
                                null=True,)

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self) -> str:
        return f'{self.name} --> {self.parent}'


class Post(models.Model):
    title = models.CharField(max_length=150, unique=True)
    body = models.TextField(blank=True)
    owner = models.ForeignKey('auth.User',
                                related_name='posts',
                                on_delete=models.CASCADE,)
    category = models.ForeignKey(Category,
                                    on_delete=models.SET_NULL,
                                    null=True,
                                    related_name='posts',)

    preview = models.ImageField(upload_to='images/',
                                null=True,
                                blank=True,)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('create_at',)
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'

    def __str__(self) -> str:
        return f'{self.owner} _ {self.body}'


class Comment(models.Model):
    owner = models.ForeignKey('auth.User',
                                related_name='comments',
                                on_delete=models.CASCADE)
    post = models.ForeignKey(Post,
                                related_name='comments',
                                on_delete=models.CASCADE)
    body = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.owner} -> {self.post} -> {self.created_at}'

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class PostImage(models.Model):
    title = models.CharField(max_length=150,
                                blank=True,)
    image = models.ImageField(upload_to='images/')
    post = models.ForeignKey(Post,
                                on_delete=models.CASCADE,
                                related_name='images')

    @staticmethod
    def generate_name():
        from random import randint
        return 'image' + str(randint(1, 1000000))

    def save(self, *args, **kwargs) -> None:
        self.title = self.generate_name()
        return super(PostImage, self).save(*args, **kwargs)