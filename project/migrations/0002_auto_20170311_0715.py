# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2017-03-10 23:15
from __future__ import unicode_literals

from django.db import migrations


'''
	Status:
		Active
			Hold
			Assigned
		Completed
			QC
			Submitted
			Assigned
		Cancelled			
			Assigned
'''


def set_default_misc_values(apps,schema_editor):
	Order_type = apps.get_model("project","Order_type")
	Status = apps.get_model("project","Status")

	order_types = ["Exterior","Interior","Data Entry","Rental"]
	statuses = ["Active","Completed","Cancelled"]

	Order_type.objects.all().delete()
	for order_type in order_types:
		Order_type(name = order_type).save()

	Status.objects.all().delete()
	for status in statuses:
		Status(name = status).save()



class Migration(migrations.Migration):

    dependencies = [
        ('project', '0001_initial'),
    ]

    operations = [
    	migrations.RunPython(set_default_misc_values)
    ]
