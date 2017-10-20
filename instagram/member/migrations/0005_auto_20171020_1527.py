# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-10-20 06:27
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('post', '0003_auto_20171019_1541'),
        ('member', '0004_auto_20171019_1540'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '사용자', 'verbose_name_plural': '사용자 목록'},
        ),
        migrations.AddField(
            model_name='user',
            name='like_posts',
            field=models.ManyToManyField(to='post.Post', verbose_name='좋아요 누른 포스트 목록'),
        ),
        migrations.AlterField(
            model_name='user',
            name='age',
            field=models.IntegerField(verbose_name='나이'),
        ),
        migrations.AlterField(
            model_name='user',
            name='img_profile',
            field=models.ImageField(blank=True, upload_to='user', verbose_name='프로필 이미지'),
        ),
    ]
