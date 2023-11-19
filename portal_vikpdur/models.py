from django.db import models


class Structure(models.Model):
    sp_name = models.CharField(max_length= 100,blank = False)

    def __str__(self):
        return self.sp_name

class Cdng(models.Model):
    structure = models.ForeignKey(Structure, null = True, on_delete = models.CASCADE)
    # structure_id = models.IntegerField(blank = False)
    cdng_name = models.CharField(max_length= 100,blank = False)
    kust_count = models.IntegerField(blank = False, default=0)
    cdng_uuid = models.CharField(max_length=50, blank = False, unique=True)
    master_name = models.CharField(max_length= 100,blank = False)
    master_phone = models.IntegerField(blank = False)

    def __str__(self):
        return self.cdng_name


class Debits(models.Model):
    cdng = models.ForeignKey(Cdng, null = True, on_delete = models.CASCADE)
    # cdng_id = models.IntegerField(blank = False)
    date_time = models.CharField(max_length=50, blank = False)
    debit = models.FloatField(blank = False)

    def __str__(self):
        return f"{self.cdng.cdng_name} {str(self.date_time)}"

class History_plan(models.Model):
    cdng = models.ForeignKey(Cdng, null= True, on_delete=models.CASCADE)
    # cdng_id = models.IntegerField(blank = False)
    editor_name = models.CharField(max_length= 100,blank = False)
    date_time = models.CharField(max_length= 100, blank = False)
    new_score_plan = models.FloatField(blank = False)

    def __str__(self):
        return f"{self.editor_name} {str(self.date_time)}"