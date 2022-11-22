from django.db import models

# Create your models here.
# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Admin(models.Model):
    name = models.CharField(unique=True, max_length=45,verbose_name="用户名")
    password = models.CharField(max_length=45,verbose_name="密码")
    class Meta:
        managed = False
        db_table = 'admin'


class Collect(models.Model):
    user_id = models.PositiveIntegerField()
    type = models.IntegerField()
    song_id = models.PositiveIntegerField(blank=True, null=True)
    song_list_id = models.PositiveIntegerField(blank=True, null=True)
    create_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'collect'


class Comment(models.Model):
    user_id = models.PositiveIntegerField()
    song_id = models.PositiveIntegerField(blank=True, null=True)
    song_list_id = models.PositiveIntegerField(blank=True, null=True)
    content = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField(blank=True, null=True)
    type = models.IntegerField()
    up = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'comment'


class Consumer(models.Model):
    username = models.CharField(unique=True, max_length=255)
    password = models.CharField(max_length=100)
    sex = models.IntegerField(blank=True, null=True)
    phone_num = models.CharField(unique=True, max_length=15, blank=True, null=True)
    email = models.CharField(unique=True, max_length=30, blank=True, null=True)
    birth = models.DateTimeField(blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    location = models.CharField(max_length=45, blank=True, null=True)
    avator = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'consumer'


class ListSong(models.Model):
    song_id = models.PositiveIntegerField()
    song_list_id = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'list_song'


class RankList(models.Model):
    id = models.BigAutoField(primary_key=True)
    songlistid = models.BigIntegerField(db_column='songListId')  # Field name made lowercase.
    consumerid = models.BigIntegerField(db_column='consumerId')  # Field name made lowercase.
    score = models.PositiveIntegerField()

    class Meta:
        managed = False
        db_table = 'rank_list'
        unique_together = (('consumerid', 'songlistid'),)


class Singer(models.Model):
    name = models.CharField(max_length=45)
    sex = models.IntegerField(blank=True, null=True)
    pic = models.CharField(max_length=255, blank=True, null=True)
    birth = models.DateTimeField(blank=True, null=True)
    location = models.CharField(max_length=45, blank=True, null=True)
    introduction = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'singer'


class Song(models.Model):
    singer_id = models.PositiveIntegerField()
    name = models.CharField(max_length=45)
    introduction = models.CharField(max_length=255, blank=True, null=True)
    create_time = models.DateTimeField()
    update_time = models.DateTimeField()
    pic = models.CharField(max_length=255, blank=True, null=True)
    lyric = models.TextField(blank=True, null=True)
    url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'song'


class SongList(models.Model):
    title = models.CharField(max_length=255)
    pic = models.CharField(max_length=255, blank=True, null=True)
    introduction = models.TextField(blank=True, null=True)
    style = models.CharField(max_length=10, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'song_list'
