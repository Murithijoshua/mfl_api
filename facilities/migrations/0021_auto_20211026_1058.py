# -*- coding: utf-8 -*-
# Generated by Django 1.11.27 on 2021-10-26 10:58
from __future__ import unicode_literals

import common.fields
import common.models.base
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('facilities', '0020_auto_20200224_1845'),
    ]

    operations = [
        migrations.CreateModel(
            name='FacilityAdmissionStatus',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('name', models.CharField(help_text=b'A short name representing the admission status e.g NOT ADMITTING', max_length=100, unique=True)),
                ('description', models.TextField(blank=True, help_text=b'A short explanation of what the status entails.', null=True)),
                ('created_by', models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('updated_by', models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
                'verbose_name_plural': 'facility admission statuses',
            },
        ),
        migrations.CreateModel(
            name='FacilityInfrastructure',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, default=0, help_text=b'The actual number of infrastructure items in a facility.')),
                ('present', models.BooleanField(default=False, help_text=b'True if the listed infrastructure is present.')),
                ('created_by', models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='FacilitySpecialist',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('count', models.IntegerField(blank=True, default=0, help_text=b'The actual number of specialists for this speciality.')),
                ('created_by', models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Infrastructure',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('abbreviation', models.CharField(blank=True, help_text=b'A short form for the infrastructure', max_length=50, null=True)),
                ('numbers', models.NullBooleanField(default=True, help_text=b'A flag to indicate whether an infrastructure item can have count/numbers tracked ')),
                ('code', common.fields.SequenceField(blank=True, editable=False, unique=True)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
                'verbose_name_plural': 'infrastructure',
            },
            bases=(common.models.base.SequenceMixin, models.Model),
        ),
        migrations.CreateModel(
            name='InfrastructureCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('name', models.CharField(help_text=b'What is the name of the category? ', max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('abbreviation', models.CharField(blank=True, help_text=b'A short form of the category e.g ANC for antenatal', max_length=50, null=True)),
                ('created_by', models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, help_text=b'The parent category under which the category falls', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sub_categories', to='facilities.InfrastructureCategory')),
                ('updated_by', models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
                'verbose_name_plural': 'specialities categories',
            },
        ),
        migrations.CreateModel(
            name='Speciality',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('name', models.CharField(max_length=255, unique=True)),
                ('description', models.TextField(blank=True, null=True)),
                ('abbreviation', models.CharField(blank=True, help_text=b'A short form for the speciality', max_length=50, null=True)),
                ('code', common.fields.SequenceField(blank=True, editable=False, unique=True)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
                'verbose_name_plural': 'specialities',
            },
            bases=(common.models.base.SequenceMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SpecialityCategory',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('created', models.DateTimeField(default=django.utils.timezone.now)),
                ('updated', models.DateTimeField(default=django.utils.timezone.now)),
                ('deleted', models.BooleanField(default=False)),
                ('active', models.BooleanField(default=True, help_text=b'Indicates whether the record has been retired?')),
                ('search', models.CharField(blank=True, editable=False, max_length=255, null=True)),
                ('name', models.CharField(help_text=b'What is the name of the category? ', max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('abbreviation', models.CharField(blank=True, help_text=b'A short form of the category e.g ANC for antenatal', max_length=50, null=True)),
                ('created_by', models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('parent', models.ForeignKey(blank=True, help_text=b'The parent category under which the category falls', null=True, on_delete=django.db.models.deletion.PROTECT, related_name='sub_categories', to='facilities.SpecialityCategory')),
                ('updated_by', models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ('-updated', '-created'),
                'default_permissions': ('add', 'change', 'delete', 'view'),
                'abstract': False,
                'verbose_name_plural': 'specialities categories',
            },
        ),
        migrations.AddField(
            model_name='facility',
            name='accredited_lab_iso_15189',
            field=models.BooleanField(default=False, help_text=b'Indicate if facility is accredited Lab ISO 15189'),
        ),
        migrations.AddField(
            model_name='facility',
            name='admitting_maternity_general',
            field=models.NullBooleanField(help_text=b'A flag to indicate whether facility admits both maternity & general casualty patients'),
        ),
        migrations.AddField(
            model_name='facility',
            name='admitting_maternity_only',
            field=models.NullBooleanField(help_text=b'A flag to indicate whether facility admits only maternity patients'),
        ),
        migrations.AddField(
            model_name='facility',
            name='number_of_isolation_beds',
            field=models.PositiveIntegerField(default=0, help_text=b'The number of isolation beds that a facility has e.g 0'),
        ),
        migrations.AddField(
            model_name='facility',
            name='number_of_maternity_beds',
            field=models.PositiveIntegerField(default=0, help_text=b'The number of maternity beds that a facility has e.g 0'),
        ),
        migrations.AddField(
            model_name='facilityupdates',
            name='humanresources',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='facilityupdates',
            name='infrastructure',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='speciality',
            name='category',
            field=models.ForeignKey(help_text=b'The classification that the specialities lies in.', on_delete=django.db.models.deletion.PROTECT, related_name='category_specialities', to='facilities.SpecialityCategory'),
        ),
        migrations.AddField(
            model_name='speciality',
            name='created_by',
            field=models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='speciality',
            name='updated_by',
            field=models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='category',
            field=models.ForeignKey(help_text=b'The classification that the infrastructure item lies in.', on_delete=django.db.models.deletion.PROTECT, related_name='category_infrastructure', to='facilities.InfrastructureCategory'),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='created_by',
            field=models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='infrastructure',
            name='updated_by',
            field=models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityspecialist',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='facility_specialists', to='facilities.Facility'),
        ),
        migrations.AddField(
            model_name='facilityspecialist',
            name='speciality',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.Speciality'),
        ),
        migrations.AddField(
            model_name='facilityspecialist',
            name='updated_by',
            field=models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facilityinfrastructure',
            name='facility',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='facility_infrastructure', to='facilities.Facility'),
        ),
        migrations.AddField(
            model_name='facilityinfrastructure',
            name='infrastructure',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='facilities.Infrastructure'),
        ),
        migrations.AddField(
            model_name='facilityinfrastructure',
            name='updated_by',
            field=models.ForeignKey(default=common.models.base.get_default_system_user_id, on_delete=django.db.models.deletion.PROTECT, related_name='+', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='facility',
            name='admission_status',
            field=models.ForeignKey(blank=True, help_text=b'Indicates whether the facilityadmits patients, and the admission types offered', null=True, on_delete=django.db.models.deletion.PROTECT, to='facilities.FacilityAdmissionStatus'),
        ),
    ]
