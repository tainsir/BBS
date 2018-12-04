from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.
# UserInfo这个表,继承AbstractUser,因为要用auth组件

class UserInfo(AbstractUser):
    nid = models.AutoField(primary_key=True)

    # username=models.CharField(max_length=32,unique=True)
    # 该字段可以为空,为该字段设置默认值,default='123455666'
    # blank=True  只是admin中表单提交的时候,做校验,如果设置成True,就是不校验了
    phone = models.CharField(max_length=32,null=True,blank=True)
    # upload_to需要传一个路径(avatar文件夹会自动创建)
    avatar = models.FileField(upload_to='avatar/', default='avatar/default.png')
    # 如果avatar用charfield,如何处理?
    #  一对一关联blog表,to_field如果不写,默认主键
    # blog_id字段存的数据是什么?blog表的---nid这个字段
    blog = models.OneToOneField(to='Blog', to_field='nid',null=True)

    class Meta:
        # admin中显示表名
        verbose_name='用户表'
        # admin中表名s去掉
        verbose_name_plural = verbose_name

    # user表
    #     id name  blog_id
    #     1  111    1
    #     2  111    1
class Blog(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    site_name = models.CharField(max_length=32)
    theme = models.CharField(max_length=64)
    def __str__(self):
        return self.site_name


class Category(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    # ForeignKey跟OneToOneField的区别?
    #OneToOneField unique=True
    blog = models.ForeignKey(to='Blog', to_field='nid', null=True)
    def __str__(self):
        return self.title


class Tag(models.Model):
    nid = models.AutoField(primary_key=True)
    title = models.CharField(max_length=64)
    blog = models.ForeignKey(to='Blog', to_field='nid', null=True)
    def __str__(self):
        return self.title



class Article(models.Model):
    nid = models.AutoField(primary_key=True)
    # verbose_name='文章标题'  修改admin中表单的文字显示
    title = models.CharField(max_length=64,verbose_name='文章标题')
    # 摘要,简单描述
    desc = models.CharField(max_length=255)
    # 大文本TextField()
    content = models.TextField()
    # 存时间类型,auto_now_add每插入一条数据,时间自动写入当前时间,
    # auto_now,这条数据修改的时候,会更新成当前时间
    create_time = models.DateTimeField(auto_now_add=True)

    # 因为查询多,写入少,所以加这三个字段,以后不需要再连表查询了
    commit_num=models.IntegerField(default=0)
    up_num=models.IntegerField(default=0)
    down_num=models.IntegerField(default=0)

    blog = models.ForeignKey(to='Blog', to_field='nid', null=True)

    category = models.ForeignKey(to='Category', to_field='nid', null=True)
    # through_fields应该怎么写?
    # 中介模型,手动创建第三张表,through是通过哪个表跟Tag建立关系,through_fields为了查询用的
    tag = models.ManyToManyField(to='Tag', through='ArticleTOTag', through_fields=('article', 'tag'))
    # 这样写,会自动创建第三张表
    # tag = models.ManyToManyField(to='Tag')
    def __str__(self):
        return self.title+'----'+self.blog.userinfo.username


# 手动创建第三张表
class ArticleTOTag(models.Model):
    nid = models.AutoField(primary_key=True)
    article = models.ForeignKey(to='Article', to_field='nid')
    tag = models.ForeignKey(to='Tag', to_field='nid')
    # article和tag应不应该联合唯一?

    # article_id  1
    # tag_id     1


class Commit(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='nid')
    article = models.ForeignKey(to='Article', to_field='nid')
    content = models.CharField(max_length=255)
    create_time = models.DateTimeField(auto_now_add=True)
    # 这样写是可以的
    # parent_id=models.IntegerField()
    # 自关联
    # parent_id=models.ForeignKey(to='Commit',to_field='nid')
    parent = models.ForeignKey(to='self', to_field='nid',null=True,blank=True)


class UpAndDown(models.Model):
    nid = models.AutoField(primary_key=True)
    user = models.ForeignKey(to='UserInfo', to_field='nid')
    article = models.ForeignKey(to='Article', to_field='nid')
    is_up = models.BooleanField()

    class Meta:
        # 写这些,只是为了不写脏数据,联合唯一
        unique_together = (('user', 'article'),)
