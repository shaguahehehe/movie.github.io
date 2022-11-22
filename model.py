# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=80)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.PositiveSmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey('UsersUserprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class FilmComment(models.Model):
    content = models.TextField()
    add_time = models.DateTimeField()
    movie = models.ForeignKey('FilmMovie', models.DO_NOTHING)
    user = models.ForeignKey('UsersUserprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'film_comment'


class FilmMovie(models.Model):
    title = models.CharField(max_length=200)
    info = models.TextField()
    logo = models.CharField(max_length=100)
    star = models.IntegerField()
    play_nums = models.IntegerField()
    comment_nums = models.IntegerField()
    area = models.CharField(max_length=200)
    release_time = models.DateField()
    length = models.CharField(max_length=200)
    add_time = models.DateTimeField()
    tag = models.ForeignKey('FilmTag', models.DO_NOTHING)
    download_url = models.CharField(max_length=300)
    movie_file = models.CharField(max_length=200)

    class Meta:
        managed = False
        db_table = 'film_movie'


class FilmMoviecol(models.Model):
    add_time = models.DateTimeField()
    movie = models.ForeignKey(FilmMovie, models.DO_NOTHING)
    user = models.ForeignKey('UsersUserprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'film_moviecol'


class FilmPreview(models.Model):
    title = models.CharField(max_length=200)
    logo = models.CharField(max_length=100)
    add_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'film_preview'


class FilmTag(models.Model):
    name = models.CharField(max_length=100)
    add_time = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'film_tag'


class MovieMessage(models.Model):
    title = models.CharField(max_length=255, blank=True, null=True)
    info = models.CharField(max_length=1024, blank=True, null=True)
    img = models.CharField(max_length=255, blank=True, null=True)
    play_num = models.IntegerField(blank=True, null=True)
    area = models.CharField(max_length=255, blank=True, null=True)
    length = models.CharField(max_length=255, blank=True, null=True)
    addtime = models.DateTimeField(blank=True, null=True)
    updatetime = models.DateTimeField(blank=True, null=True)
    movie_file = models.CharField(max_length=255, blank=True, null=True)
    download_url = models.CharField(max_length=255, blank=True, null=True)
    type = models.CharField(max_length=255, blank=True, null=True)
    star = models.CharField(max_length=255, blank=True, null=True)
    alias = models.CharField(max_length=255, blank=True, null=True)
    director = models.CharField(max_length=255, blank=True, null=True)
    score = models.CharField(max_length=255, blank=True, null=True)
    language = models.CharField(max_length=255, blank=True, null=True)
    year = models.CharField(max_length=255, blank=True, null=True)
    moive_id = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'movie_message'


class UsersUserlog(models.Model):
    ip = models.CharField(max_length=50)
    add_time = models.DateTimeField()
    user = models.ForeignKey('UsersUserprofile', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_userlog'


class UsersUserprofile(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.IntegerField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.CharField(max_length=254)
    is_staff = models.IntegerField()
    is_active = models.IntegerField()
    date_joined = models.DateTimeField()
    name = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    gender = models.CharField(max_length=6)
    info = models.TextField()
    image = models.CharField(max_length=100)
    add_time = models.DateTimeField()
    uuid = models.CharField(max_length=50)
    phone = models.CharField(max_length=11, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_userprofile'


class UsersUserprofileGroups(models.Model):
    userprofile = models.ForeignKey(UsersUserprofile, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_userprofile_groups'
        unique_together = (('userprofile', 'group'),)


class UsersUserprofileUserPermissions(models.Model):
    userprofile = models.ForeignKey(UsersUserprofile, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'users_userprofile_user_permissions'
        unique_together = (('userprofile', 'permission'),)


class XadminBookmark(models.Model):
    title = models.CharField(max_length=128)
    url_name = models.CharField(max_length=64)
    query = models.CharField(max_length=1000)
    is_share = models.IntegerField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING)
    user = models.ForeignKey(UsersUserprofile, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'xadmin_bookmark'


class XadminLog(models.Model):
    action_time = models.DateTimeField()
    ip_addr = models.CharField(max_length=39, blank=True, null=True)
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.CharField(max_length=32)
    message = models.TextField()
    content_type = models.ForeignKey(DjangoContentType, models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(UsersUserprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'xadmin_log'


class XadminUsersettings(models.Model):
    key = models.CharField(max_length=256)
    value = models.TextField()
    user = models.ForeignKey(UsersUserprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'xadmin_usersettings'


class XadminUserwidget(models.Model):
    page_id = models.CharField(max_length=256)
    widget_type = models.CharField(max_length=50)
    value = models.TextField()
    user = models.ForeignKey(UsersUserprofile, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'xadmin_userwidget'
