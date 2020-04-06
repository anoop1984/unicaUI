from django.db import models
"""
class healthCheck(models.Model):
    date= models.DateField("Date Executed")
    test_id = models.CharField(max_length=100)
    desc = models.CharField(max_length=400)
    severity = models.CharField(max_length=50)
    ipaddr = models.GenericIPAddressField()
    hostname = models.CharField(max_length=100)
    command = models.CharField(max_length=400)
    verdict = models.CharField(max_length=50)
    remarks = models.CharField(max_length=1000)
"""
class healthCheck(models.Model):
    desc 	= models.CharField(max_length = 264)
    severity 	= models.CharField(max_length = 50)
    #ipaddress 	= models.CharField(max_length = 50)
    ipaddr      = models.GenericIPAddressField()  
    hostname 	= models.CharField(max_length = 100) 
    command 	= models.CharField(max_length = 264) 
    verdict 	= models.CharField(max_length = 264) 
    remarks  	= models.CharField(max_length = 1000) 
    test_id 	= models.CharField(max_length = 100) 
#   timestamp 	= models.DateTimeField(auto_now_add=True)
    date 	= models.DateField()
    site	= models.CharField(max_length = 100)


class Logfile_Testlab1(models.Model):
    logfile 	= models.FileField(upload_to='testlab1/')
    uploaded_at = models.DateField(primary_key=True)

class Logfile_Testlab2(models.Model):
    logfile 	= models.FileField(upload_to='testlab2/')
    uploaded_at = models.DateField(primary_key=True)

class Execute1(models.Model):
    user = models.CharField(max_length=50, blank=True)
    #logfile = models.FileField(upload_to='execute1/', blank=True)
    #jsonfile = models.FileField(upload_to='execute1/', blank=True)
    timestamp = models.CharField(max_length=50,primary_key=True)
    timestamp_str = models.CharField(max_length=50)
    status = models.CharField(max_length=50, blank=True)

