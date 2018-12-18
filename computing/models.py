from django.db import models

# Create your models here.


# 存储日志信息
class Logging(models.Model):
    ip = models.CharField(max_length=24)
    request_time = models.CharField(max_length=24)
    request_type = models.CharField(max_length=10)
    request_url = models.CharField(max_length=64)
    status_code = models.CharField(max_length=10)

    def __str__(self):
        return self.ip
