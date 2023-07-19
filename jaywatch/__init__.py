import pymysql
from .celery import celery

pymysql.install_as_MySQLdb()
