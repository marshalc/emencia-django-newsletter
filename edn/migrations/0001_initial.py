# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import autoslug.fields
import datetime
import uuidfield.fields


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('email', models.EmailField(unique=True, max_length=75, verbose_name='email')),
                ('full_name', models.CharField(max_length=255, null=True, verbose_name='full name', blank=True)),
                ('verified', models.BooleanField(default=False, verbose_name=b'verified')),
                ('verified_on', models.DateTimeField(null=True, verbose_name=b'verified on', blank=True)),
                ('tester', models.BooleanField(default=False, verbose_name='contact tester')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='modification date')),
            ],
            options={
                'ordering': ('creation_date',),
                'verbose_name': 'contact',
                'verbose_name_plural': 'contacts',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ContactMailingStatus',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('status', models.IntegerField(verbose_name='status', choices=[(-1, 'sent in test'), (0, 'sent'), (1, 'error'), (2, 'invalid email'), (4, 'opened'), (5, 'opened on site'), (6, 'link opened'), (7, 'unsubscription')])),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('contact', models.ForeignKey(verbose_name='contact', to='edn.Contact')),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'contact mailing status',
                'verbose_name_plural': 'contact mailing statuses',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Link',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=255, verbose_name='title')),
                ('url', models.CharField(max_length=255, verbose_name='url')),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'link',
                'verbose_name_plural': 'links',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='MailingList',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255, verbose_name='name')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='modification date')),
                ('subscribers', models.ManyToManyField(related_name=b'mailinglist_subscriber', null=True, verbose_name='subscribers', to='edn.Contact', blank=True)),
                ('unsubscribers', models.ManyToManyField(related_name=b'mailinglist_unsubscriber', null=True, verbose_name='unsubscribers', to='edn.Contact', blank=True)),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'mailing list',
                'verbose_name_plural': 'mailing lists',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Newsletter',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(help_text='Project-Id-Version: Django\nReport-Msgid-Bugs-To: \nPOT-Creation-Date: 2013-05-02 16:18+0200\nPO-Revision-Date: 2010-05-13 15:35+0200\nLast-Translator: Django team\nLanguage-Team: English <en@li.org>\nLanguage: en\nMIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n', max_length=255, verbose_name='title')),
                ('content', models.TextField(default='<!-- Edit your newsletter here -->', help_text='Project-Id-Version: Django\nReport-Msgid-Bugs-To: \nPOT-Creation-Date: 2013-05-02 16:18+0200\nPO-Revision-Date: 2010-05-13 15:35+0200\nLast-Translator: Django team\nLanguage-Team: English <en@li.org>\nLanguage: en\nMIME-Version: 1.0\nContent-Type: text/plain; charset=UTF-8\nContent-Transfer-Encoding: 8bit\n', verbose_name='content')),
                ('template', models.CharField(max_length=200, verbose_name='template', choices=[(b'default', b'default')])),
                ('base_url', models.CharField(max_length=200, null=True, verbose_name='base URL', blank=True)),
                ('header_sender', models.CharField(max_length=255, verbose_name='sender')),
                ('header_reply', models.CharField(max_length=255, verbose_name='reply to')),
                ('status', models.IntegerField(default=0, verbose_name='status', choices=[(0, 'draft'), (1, 'waiting sending'), (2, 'sending'), (4, 'sent'), (5, 'canceled')])),
                ('sending_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='sending date')),
                ('slug', autoslug.fields.AutoSlugField(help_text='Used for displaying the newsletter on the site.', unique=True, editable=False)),
                ('creation_date', models.DateTimeField(auto_now_add=True, verbose_name='creation date')),
                ('modification_date', models.DateTimeField(auto_now=True, verbose_name='modification date')),
                ('mailing_list', models.ForeignKey(verbose_name='mailing list', to='edn.MailingList', null=True)),
                ('test_contacts', models.ManyToManyField(to='edn.Contact', null=True, verbose_name='test contacts', blank=True)),
            ],
            options={
                'ordering': ('-creation_date',),
                'verbose_name': 'newsletter',
                'verbose_name_plural': 'newsletters',
                'permissions': (('can_change_status', 'Can change status'),),
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='SubscriberVerification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('link_id', uuidfield.fields.UUIDField(unique=True, max_length=32, editable=False, blank=True)),
                ('contact', models.ForeignKey(to='edn.Contact')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='contactmailingstatus',
            name='link',
            field=models.ForeignKey(verbose_name='link', blank=True, to='edn.Link', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='contactmailingstatus',
            name='newsletter',
            field=models.ForeignKey(verbose_name='newsletter', to='edn.Newsletter'),
            preserve_default=True,
        ),
    ]
