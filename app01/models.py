from django.db import models


# Create your models here.
class UserInfo(models.Model):
    user_type_choice = (
        (1, '普通用户'),
        (2, 'vip用户'),
        (3, 'svip用户')
    )
    user_type = models.IntegerField(choices=user_type_choice)
    username = models.CharField(max_length=32, unique=True)
    password = models.CharField(max_length=64)
    group = models.ForeignKey('UserGroup', on_delete=models.DO_NOTHING, default=1)
    roles = models.ManyToManyField('UserRoles')


class UserToken(models.Model):
    user = models.OneToOneField(to='UserInfo', on_delete=models.DO_NOTHING)
    token = models.CharField(max_length=64)


class UserRoles(models.Model):
    title = models.CharField(max_length=32)


class UserGroup(models.Model):
    choice = (
        (1, '前端小组'),
        (2, 'android小组'),
        (3, 'java小组')
    )
    title = models.IntegerField(choices=choice)
