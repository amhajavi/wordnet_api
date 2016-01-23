import psycopg2

def connect():
	conn_string = "host='localhost' dbname='farsnet' user='amh' password='saeideh'"
	conn = psycopg2.connect(conn_string)
	return conn