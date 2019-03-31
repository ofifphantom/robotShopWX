# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AccessTokenTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startTime', models.DateTimeField(null=True, verbose_name=b'startTime')),
                ('endTime', models.DateTimeField(null=True, verbose_name=b'endTime')),
                ('access_token', models.CharField(max_length=600, null=True, verbose_name=b'access_token')),
            ],
            options={
                'db_table': 'accessTokenTable',
                'verbose_name': 'accessTokenTable',
                'verbose_name_plural': 'accessTokenTable',
            },
        ),
        migrations.CreateModel(
            name='DoorInfoTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('doorCode', models.CharField(max_length=50, null=True, verbose_name=b'ticket')),
                ('doorID', models.CharField(max_length=50, null=True, verbose_name=b'url')),
            ],
            options={
                'db_table': 'doorInfo',
                'verbose_name': 'doorInfo',
                'verbose_name_plural': 'doorInfo',
            },
        ),
        migrations.CreateModel(
            name='JsapiTicketTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('startTime', models.DateTimeField(null=True, verbose_name=b'startTime')),
                ('endTime', models.DateTimeField(null=True, verbose_name=b'endTime')),
                ('jsapi_ticket', models.CharField(max_length=600, null=True, verbose_name=b'jsapi_ticket')),
            ],
            options={
                'db_table': 'jsapiTicketTable',
                'verbose_name': 'jsapiTicketTable',
                'verbose_name_plural': 'jsapiTicketTable',
            },
        ),
        migrations.CreateModel(
            name='MessageTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('identityCode', models.CharField(max_length=10, null=True, verbose_name=b'identityCode')),
                ('phoneNumber', models.CharField(max_length=20, unique=True, null=True, verbose_name=b'phoneNumber')),
                ('startTime', models.DateTimeField(null=True, verbose_name=b'startTime')),
                ('endTime', models.DateTimeField(null=True, verbose_name=b'endTime')),
            ],
            options={
                'db_table': 'message',
                'verbose_name': 'message',
                'verbose_name_plural': 'message',
            },
        ),
        migrations.CreateModel(
            name='QRCodeTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('ticket', models.CharField(max_length=600, null=True, verbose_name=b'ticket')),
                ('url', models.CharField(max_length=100, null=True, verbose_name=b'url')),
            ],
            options={
                'db_table': 'qrCode',
                'verbose_name': 'qrCode',
                'verbose_name_plural': 'qrCode',
            },
        ),
        migrations.CreateModel(
            name='UserAuthTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openID', models.CharField(max_length=50, null=True, verbose_name=b'openID')),
                ('identityType', models.CharField(max_length=50, null=True, verbose_name=b'identityType')),
                ('identitfier', models.CharField(max_length=100, null=True, verbose_name=b'identitfier')),
                ('credential', models.CharField(max_length=50, null=True, verbose_name=b'credential')),
                ('registerTime', models.DateTimeField(null=True, verbose_name=b'registerTime')),
                ('access_token', models.CharField(max_length=600, null=True, verbose_name=b'access_token')),
                ('tokenEndTime', models.DateTimeField(null=True, verbose_name=b'tokenEndTime')),
                ('refresh_token', models.CharField(max_length=600, null=True, verbose_name=b'refresh_token')),
                ('refreshTime', models.DateTimeField(null=True, verbose_name=b'refreshTime')),
            ],
            options={
                'db_table': 'userAuth',
                'verbose_name': 'userAuth',
                'verbose_name_plural': 'userAuth',
            },
        ),
        migrations.CreateModel(
            name='UserTable',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('openID', models.CharField(max_length=50, null=True, verbose_name=b'openID')),
                ('nickName', models.CharField(max_length=100, null=True, verbose_name=b'nickName')),
                ('avatar', models.CharField(max_length=200, null=True, verbose_name=b'avatar')),
                ('picture', models.CharField(max_length=200, null=True, verbose_name=b'picture')),
            ],
            options={
                'db_table': 'user',
                'verbose_name': 'user',
                'verbose_name_plural': 'user',
            },
        ),
    ]
