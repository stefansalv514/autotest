import psycopg2
from psycopg2 import sql
from sshtunnel import SSHTunnelForwarder

def startdb():
    server = SSHTunnelForwarder(
        ('192.168.77.116', 22),
        ssh_username="dkonovalov",
        ssh_password="123456aA",
        remote_bind_address=('localhost', 5432),
        local_bind_address=('localhost',6543),
        )

    server.start()
    conn = psycopg2.connect(
        database="api",
        user="dashboard_user",
        password="password",
        host=server.local_bind_host,
        port=server.local_bind_port,
    )
    return conn, server

#try:
#    cur.execute("SELECT * FROM call_results WHERE acronim = %s", ("test",))
#    x = cur.fetchone()
#    print(x)
#except Exception as ex:
#    print("hello")
def stopdb(conn, server):
    conn.close()
    server.stop()



