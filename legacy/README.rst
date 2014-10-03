Changelog
=========

2013-10-5 marshalc :: @rassie / Nikolai has been busy :-) 

After a few months away from this project, I've come back to see that he's been 
nicely patching things up far more neatly than I had done. My thanks to him and 
the other contributors!

* Determined some missing packages for requirements, added requirements.txt (I deploy this as part of other projects, so this makes it easier for me)

ToDo

* Fix bug where adding a URL causes the newsletter creation to fail.
* Most of what was on my last todo list...
* UPDATE THE DOCUMENTATION! I've been making notes in my own wiki, need to combine those with a review of the below and try to make this into something more formal and useful. Don't hold your breath though ;-)

2013-6-28 rassie :: Changelog since @marshalc's version...

* Restored migrations
* Added missing dependencies, thrown out unnecessary ones
* Reverted Contact.owner field (based on discussion with original author)
* Changed slug handling to AutoSlugField
* Merged Contact.first_name and Contact.last_name to Contact.full_name
* Enabled and extended automatical subscription to mailing lists
* General cleanup
* Converted verification mail to template

ToDos

* It might make sense to revert the namespace flattening. There was
  little sense in that other than avoiding Django's incomplete
  namespace package support and other than that, **emencia** is a
  bigger project than just newsletters, which we don't own. Either we
  are going to bring the original **emencia-django-newsletter** up to
  speed or we'll need to rename, either way the namespace will change,
  but having the project under the original name would make merging
  back to Emencia easier.
* Subscriber verification should be more obvious
* Extend templating
* Make overriding default 4templates possible

2013-5-28 marshalc :: My notes on work done so far, and work to be done... mostly to be done ;-)

* Combined the verification process into the basic subscription form.
 * Still needs the normal subscribe form modifying and the urls unmangling.
 * Also needs to be able to sign up for specific mailing lists (public and private?)
* Need to update and consolidate the documentation from the various merged branches
* Have removed all the previous merged migrations, since this is effectively a clean install with too much of a mixed heritage for past upgrades to work easily.
* Need to finish the code inspection and cleanup. PyCharm has identified 1312 issues (admittedly 1003 of them are spelling concerns!) for me to look through.
* HTML Link as content isn't presently working...
* What are Workgroups? How do they differ/compare with Segments?
* What does the Premailer do? Answer: Seems to be responsible for parsing html pages into content for the newsletter.
 * Needs some work!
 * Go look at https://github.com/kapt/emencia-django-newsletter/commit/837a3a35c0bdb5bda1ec6e9c73db35cf8156496c for some inspiration
* Tidy up, understand and expand on what the Templates functionality does (or doesn't).
* I want to add:
 * Mezzanine support - tie it into the blog system elegantly
 * WYSIWYG editor made active - several of the merges suggest work has been done on this, but I need to active and test it.
 * Need to work out which packages have been used as the base for tinymce and ckeditor


A word of warning from @rassie
==============================

This fork is an attempt to clean up, in part rewrite and extend the
original **emencia-django-newsletter** with patches available in
multiple forks on GitHub and some original work. Currently, I'm
extending the project for my needs, trying to be as generic as
possible. I've originally started with @marshalc's fork and
re-applied the patches he selected.

**This code currently provides no proper upgrade path between
revisions!** It's possible I'd change migrations retroactively,
reorder them, etc. If you want to use this code, please contact me!

Future development
------------------

Since original repository seems to be dormant and still several people
are interested in **emencia-django-newsletter**, we'll certainly be
discussing taking over the maintenance from Emencia, in case they find
this acceptable. If not, we'll probably have to proper fork and rename
this project.


----------------------------------------------------------------------

And now, for the original documentation

=========================
Emencia Django Newsletter
=========================

The problematic was :

 * How to couple a contact base to a mailing list and sending newsletters through Django ? *

Imagine that we have an application containing some kind of profiles or something like the **django.contrib.auth** and you want to send newsletters to them and tracking the activity.

.. contents::

Features
========

More than a long speech, here the list of the main features :

  * Coupling capacities with another django model.
  * Variables can be used in the newsletter's templates.
  * Mailing list managements (merging, importing...).
  * Import/Export of the contact in VCard 3.0.
  * Configurable SMTP servers with flow limit management.
  * Working groups.
  * Can send newsletter previews.
  * Subscriptions and unsubscriptions to mailing list.
  * Attachments in newsletters.
  * Unique urls for an user.
  * Tracking statistics.
  * Email verification
  * Templates


Architecture
============

At the level of the application architecture, we can see 2 originalities who need to be explained.

Content types
-------------

The **content types** application is used to link any *Contact* model instance to another model instance.
This allow you to create different kinds of contact linked to different application, and retrieve the association at anytime.

This is particularly useful with the templates variables if certain information is located in the model instance linked.

Cronjob/Command
---------------

The emencia.django.newsletter application will never send the newsletters registered in the site until you launch the **send_newsletter** command. ::

  $ python manage.py send_newsletter

This command will launch the newsletters who need to be launched accordingly to the credits of the SMTP server of the newsletter.
That's mean that not all newsletters will be expedied at the end of the command because if you use a public SMTP server you can be banished temporarly if you reach the sending limit.
To avoid banishment all the newsletters are not sent at the same time or immediately.

So it is recommended to create a **cronjob** for launching this command every hours for example.

Installation
============

Dependencies
------------

Make sure to install these packages prior to installation :

 * Django >= 1.2
 * html2text
 * beautifulsoup4
 * django-tagging
 * vobject
 * xlwt
 * xlrd
 * inlinestyler

The package below is optionnal but handy for rendering a webpage in your newsletter.

 * lxml

Getting the code
----------------

You could retrieve the last sources from http://github.com/Fantomas42/emencia-django-newsletter and running the installation script ::

  $ python setup.py install

or use pip ::

  $ pip install -e git://github.com/Fantomas42/emencia-django-newsletter.git#egg=emencia.django.newsletter

For the latest stable version use easy_install ::

  $ easy_install emencia.django.newsletter

Applications
------------

Then register **emencia**, **south**, **admin** and **contenttypes** in the INSTALLED_APPS section of your project's settings. ::

  INSTALLED_APPS = (
    # Your favorites apps
    'django.contrib.contenttypes',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.sessions',
    'emencia',
    'south',)


Urls
----

In your project urls.py adding this following line to include the newsletter's urls for serving the newsletters in HTML. ::

  url(r'^newsletters/', include('emencia.urls')),

Note this urlset is provided for convenient usage, but you can do something like that if you want to customize your urls : ::

  url(r'^newsletters/', include('emencia.urls.newsletter')),
  url(r'^mailing/', include('emencia.urls.mailing_list')),
  url(r'^tracking/', include('emencia.urls.tracking')),
  url(r'^statistics/', include('emencia.urls.statistics')),

Media Files
-----------

You have to make a symbolic link from emencia/django/newsletter/media/edn/ directory to your media directory or make a copy named **edn**,
but if want to change this value, define NEWSLETTER_MEDIA_URL in the settings.py as appropriate.

Don't forget to serve this url.

Synchronization
---------------

Now you can run a *syncdb* for installing the models into your database.

Settings
--------

You have to add in your settings the email address used to send the newsletter : ::

  NEWSLETTER_DEFAULT_HEADER_SENDER = 'My NewsLetter <newsletter@myhost.com>'


DBMS considerations
===================

It's not recommended to use SQLite for production use. Because is limited to 999
variables into a SQL query, you can not create a Mailing List greater than this limitations
in the Django's admin modules. Prefer MySQL ou PgSQL.


HOWTO use WYSIWYG for editing the newsletters
=============================================

It can be usefull for the end user to have a WYSIWYG editor for the
creation of the newsletter. The choice of the WYSIWYG editor is free and
the described method can be applied for anything, but we will focus on
TinyMCE and CkEditor.

Either install the `django-tinymce <http://code.google.com/p/django-tinymce/>`_ application or the `django-ckeditor <https://github.com/shaunsephton/django-ckeditor/>`_ application into your project.

That's done, enjoy !


HOWTO couple your profile application with emencia.django.newsletter
====================================================================

If you wan to quickly import your contacts into a mailing list for example,
you can write an admin's action for your model.

We suppose that we have the fields *email*, *first_name* and *last_name* in a models name **Profile**.

In his AdminModel definition add this method and register it into the *actions* property. ::

  class ProfileAdmin(admin.ModelAdmin):

      def make_mailing_list(self, request, queryset):
          from emencia.django.newsletter.models import Contact
          from emencia.django.newsletter.models import MailingList

          subscribers = []
          for profile in queryset:
              contact, created = Contact.objects.get_or_create(email=profile.mail,
                                                               defaults={'first_name': profile.first_name,
                                                                         'last_name': profile.last_name,
                                                                         'content_object': profile})
              subscribers.append(contact)
          new_mailing = MailingList(name='New mailing list',
                                    description='New mailing list created from admin/profile')
          new_mailing.save()
          new_mailing.subscribers.add(*subscribers)
          new_mailing.save()
          self.message_user(request, '%s successfully created.' % new_mailing)
      make_mailing_list.short_description = 'Create a mailing list'

      actions = ['make_mailing_list']

This action will create or retrieve all the **Contact** instances needed for the mailing list creation.

After this you can send a newsletter to this mailing list.

Development
===========

A `Buildout
<http://pypi.python.org/pypi/zc.buildout>`_ script is provided to properly initialize the project
for anybody who wants to contribute.

First of all, please use `VirtualEnv
<http://pypi.python.org/pypi/virtualenv>`_ to protect your system.

Follow these steps to start the development : ::

  $ git clone git://github.com/Fantomas42/emencia-django-newsletter.git
  $ virtualenv --no-site-packages emencia-django-newsletter
  $ cd emencia-django-newsletter
  $ source ./bin/activate
  $ python bootstrap.py
  $ ./bin/buildout

The buildout script will resolve all the dependencies needed to develop the application.

Once these operations are done, you are ready to develop on the project.

Run this command to launch the tests. ::

  $ ./bin/test

Or you can also launch the demo. ::

  $ ./bin/demo syncdb
  $ ./bin/demo runserver

Pretty easy no ?

Translations
------------

If you want to contribute by updating a translation or adding a translation
in your language, it's simple: create a account on Transifex.net and you
will be able to edit the translations at this URL :

http://www.transifex.net/projects/p/emencia-django-newsletter/resource/djangopo/

.. image:: http://www.transifex.net/projects/p/emencia-django-newsletter/resource/djangopo/chart/image_png

The translations hosted on Transifex.net will be pulled periodically in the
repository, but if you are in a hurry, `send me a message
<https://github.com/inbox/new/Fantomas42>`_.

Database Representation
=======================

.. image:: https://github.com/Fantomas42/emencia-django-newsletter/raw/master/docs/graph_model.png


Tracking Ignore Anchors
=======================

How to use
----------
Simply set the option ``NEWSLETTER_TRACKING_IGNORE_ANCHOR = True`` to track no
ankers in your email.

The goal of this option is so send emails with a template that has anchors, but
if ``NEWSLETTER_TRACKING_LINKS`` is enabled, the anchors won't work.

Subscriber Verification
=======================
**!IMPORTANT! This modification has no backwards compatibility support.
!IMPORTANT!**

How to use
----------
After installation of the newsletter, subcriber verification is set to
``NEWSLETTER_SUBSCRIBER_VERIFICATION = True``. If there is no need for, set it
on ``False``.

To set an reply email adress, you will edit the option
``NEWSLETTER_DEFAULT_HEADER_REPLY`` in *settings.py* for example to
``Freshmilk NoReply<noreply@freshmilk.tv>``.

Functionality
-------------
The subscriber verification has a table called SubscriberVerifications. If an
user subscribes over the ``<host>/newsletters/subscribe`` page, the view will
create a **Contact** in the **contacts** table and will also generate a uuid
which is saved with the new **Contact** in SubscriberVerifications. After an
call of ``<host>/newsletters/subscribe/<uuid>`` the view will delete the row in
SubscriberVerifications and set the **Contact** in **contacts** as verified.

Thats all. :)

Urls
----
  * <host>/newsletters/subscribe > to subscribe the email
  * <host>/newsletters/subscribe/<uuid> > to verify the email

Templates
---------
  * subscriber_verification.html > to subscribe the email
  * uuid_verification.html > to verify the email

Notes
-----
  * if you had more than one mailing list, all will shown in the verification
    link
  * if you had only one mailing list, the user will add to this one
  * translations are made for en and de. Please run ``makemessages`` for other
    languages

Update
------
If you update from a prior version of this newsletter, please run ``dbshell``
and add the column verified to newsletter_contact.

sqlite command ::

    ALTER TABLE newsletter_contact ADD COLUMN verified bool;
