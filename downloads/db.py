import pymysql
import config

conn = pymysql.connect(
    host=config.db_host,
    user=config.db_user,
    passwd=config.db_pass,
    db=config.db_name
)
