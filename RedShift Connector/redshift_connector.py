import psycopg2
from getpass import getpass
from pandas import read_sql



def create_conn(*args,**kwargs):
    config = kwargs['config']
    try:
        con=psycopg2.connect(dbname=config['dbname'], host=config['host'], 
                              port=config['port'], user=config['user'], 
                              password=config['pwd'])
        return con
    except Exception as err:
        print(err)


con = create_conn(config=config)
df = read_sql("select * from item limit 50", con=con)
df.info()
print df.head()
con.close()