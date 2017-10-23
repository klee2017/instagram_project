from django.contrib.auth.models import AbstractUser, UserManager as DjangoUserManager
from django.db import models


class UserManager(DjangoUserManager):
    def create_superuser(self, *args, **kwargs):
        return super().create_superuser(age=30, *args, **kwargs)


class User(AbstractUser):
    img_profile = models.ImageField('프로필 이미지', upload_to='user', blank=True)
    age = models.IntegerField('나이')
    like_posts = models.ManyToManyField('post.Post', verbose_name='좋아요 누른 포스트 목록')
    # 내가 팔로우 하고 있는 유저 목록
    # 내가 A를 follow한다
    #   나는 A의 follower
    #   A는 나의 followed_user
    # 나를 follow한 사람
    #   followers
    # 내가 follow한 사람
    #   followed_users
    followed_users = models.ManyToManyField('self', symmetrical=False, through='Relation', related_name='followers')

    objects = UserManager()

    class Meta:
        verbose_name = '사용자'
        verbose_name_plural = f'{verbose_name} 목록'


# REQUIRED_FIELDS = AbstractUser.REQUIRED_FIELDS + ['age']

class Relation(models.Model):
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followed_user_relations',)
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='follower_relations')
    created_at = models.DateTimeField(auto_now_add=True)