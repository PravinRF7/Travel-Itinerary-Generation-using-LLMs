# Generated by Django 5.1 on 2024-09-25 15:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0006_rename_query_contactenquiry_delete_contact'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='contactEnquiry',
            new_name='Contact',
        ),
    ]
