from django.db import models

# Create your models here.
class User(models.Model):

    gender = (
        ('1', "男"),
        ('0', "女"),
    )

    name = models.CharField(max_length=128, unique=True)
    password = models.CharField(max_length=256)
    email = models.EmailField(unique=True)
    sex = models.CharField(max_length=32, choices=gender, default="男")
    c_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ["-c_time"]
        verbose_name = "用户"
        verbose_name_plural = "用户"

class job_list(models.Model):
    jname = models.CharField(max_length=128,null=False,unique=True)
    jid = models.CharField(max_length=128,null=False,unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

class add_host(models.Model):
    hostname = models.CharField(max_length=128,null=False,unique=True)
    IP = models.CharField(max_length=128,null=False,unique=False)
    username = models.CharField(max_length=128, null=False, unique=False)
    port = models.CharField(max_length=128, null=False, unique=False)
    keyname=models.CharField(max_length=128,null=False,unique=False)
    infro = models.CharField(max_length=128,null=False,unique=False)

class job_history(models.Model):
    jname = models.CharField(max_length=128,null=False,unique=False)
    jid = models.CharField(max_length=128,null=False,unique=False)
    exec_host = models.CharField(max_length=128,null=False,unique=False)
    exec_history = models.CharField(max_length=128,null=False,unique=True)
    c_time = models.DateTimeField(auto_now_add=True)

class update_version(models.Model):
    up_name = models.CharField(max_length=254, null=False, unique=False)
    ser_name = models.CharField(max_length=254,null=True,unique=False)
    ios_cname = models.CharField(max_length=254,null=True,unique=False)
    aos_cname = models.CharField(max_length=254,null=True,unique=False)
    env = models.CharField(max_length=254,null=True,unique=False)
    up_info = models.TextField(max_length=254, null=True, unique=False)
    status = models.CharField(max_length=128, null=False, unique=False,default='label-info')
    c_time = models.DateTimeField(auto_now_add=True)
    progress = models.CharField(max_length=128, null=False, unique=False,default='进行中')