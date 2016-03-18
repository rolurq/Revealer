import os
basedir = os.path.dirname(__file__)
abs_basedir = os.path.abspath(basedir)

DEBUG = 'true'
UPLOADED_SLIDESHOWS_DEST = os.path.join(basedir, 'templates', 'slideshows')
SECRET_KEY = 's0m3 53cr3t k3y'
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % os.path.join(abs_basedir, 'data',
                                                        'data.sqlite')
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
