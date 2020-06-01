import psycopg2
try:
    conn = psycopg2.connect("host=localhost dbname=postgres")
    conn.close();
except psycopg2.OperationalError as ex:
    print("Connection failed: {0}".format(ex))