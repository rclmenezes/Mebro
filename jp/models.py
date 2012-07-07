from django.db import models

class RainbowEntry(models.Model):
    baseID = models.AutoField(primary_key=True)
    base = models.CharField("Base", max_length=15, null=True, blank=True)
    hashes = models.TextField("Hashes", null=True, blank=True)
    added = models.DateTimeField("Added", auto_now_add=True)
    
class Client(models.Model):
    client_id = models.AutoField(primary_key=True)
    preferred_project = models.ForeignKey('Project', null=True, blank=True)

class Project(models.Model):
    project_id = models.AutoField(primary_key=True)
    name = models.CharField("Name", max_length=50)
    code = models.URLField("Code", max_length=200)
    
    def __unicode__(self):
        return self.name
    
class InputData(models.Model):
    input_data_id = models.AutoField(primary_key=True)
    data = models.CharField(max_length=100)
    project = models.ForeignKey("Project")
    num_dealt = models.IntegerField(default=0)
    
class Job(models.Model):
    job_id = models.AutoField(primary_key=True)
    client = models.ForeignKey('Client')
    input_data = models.ForeignKey('InputData')
    result = models.CharField(max_length=65, null=True, blank=True)
    checkpoint = models.IntegerField(default=0)
    
'''

For projects:
add\_input(input\_id, input, project\_id)
clients(input\_id)
result(input\_id)
kill(input\_id)

For browser:
new()
get\_input(input\_id)
return\_result(input\_id, result)
checkpoint(percentage)

project
project\_id
name
code
jobs

input
input\_id
project\_id
value

job
job\_id
input\_id
ip
last\_checkpoint\_time
checkpoint

user
user\_id
project\_preference


'''