import os
basedir = os.path.dirname(__file__)
abs_basedir = os.path.abspath(basedir)

MYSQL_USER = "revealer"
MYSQL_PASSWD = "revealer"
MYSQL_SERVER = "localhost:3306"
DATABASE_NAME = "data"
DEBUG = 'true'
UPLOADED_SLIDESHOWS_DEST = os.path.join(basedir, 'templates', 'slideshows')
UPLOADED_RESOURCES_DEST = UPLOADED_SLIDESHOWS_DEST
SECRET_KEY = 's0m3 53cr3t k3y'
SQLALCHEMY_DATABASE_URI = 'mysql://%s:%s@%s/%s' % (MYSQL_USER, MYSQL_PASSWD,
                                                   MYSQL_SERVER, DATABASE_NAME)
SQLALCHEMY_TRACK_MODIFICATIONS = True
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
