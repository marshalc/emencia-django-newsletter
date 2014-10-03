import os
from setuptools import setup
from setuptools import find_packages

import emencia


setup(name='emencia',
      version=emencia.__version__,
      description='A Django app for sending emencia by email to a contact list.',
      long_description=open('README.rst').read() + '\n' +
                       open(os.path.join('docs', 'HISTORY.txt')).read(),
      keywords='django, emencia, mailing',
      classifiers=[
          'Framework :: Django',
          'Programming Language :: Python',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'Operating System :: OS Independent',
          'License :: OSI Approved :: BSD License',
          'Development Status :: 5 - Production/Stable',
          'Topic :: Software Development :: Libraries :: Python Modules', ],

      author=emencia.__author__,
      author_email=emencia.__email__,
      url=emencia.__url__,

      license=emencia.__license__,
      packages=find_packages(exclude=['demo']),
      #namespace_packages=['emencia',],
      include_package_data=True,
      zip_safe=False,
      install_requires=['setuptools',
                        'html2text',
                        'python-dateutil==1.5',
                        'beautifulsoup4',
                        'django-tagging',
                        'vobject',
                        'xlwt',
                        'xlrd',
                        'premailer',
                        'django-filebrowser-no-grappelli',
                        'django-tinymce',
                        'django-uuidfield',
                        'South',
                        'django-autoslug==1.6.1'])
