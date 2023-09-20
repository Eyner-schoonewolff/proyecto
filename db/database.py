import psycopg2

class DataBaseConnector:
    def __init__(self, host, user, password, database,port):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port=port
        self.connection = None

    def connect(self):
        self.connection = psycopg2.connect(
            host=self.host,
            user=self.user,
            password=self.password,
            database=self.database,
            port=self.port,
            keepalives=1,
            keepalives_idle=30,
            keepalives_interval=10,
            keepalives_count=5,
            connect_timeout=10 
        )

    def disconnect(self):
        self.connection.close()



try:
    db = DataBaseConnector(user = "postgres",
                                  password = "1001781662proyect",
                                  host = "db.nbdocmgfggiqmjxxwred.supabase.co",
                                  port = "5432",
                                  database = "postgres",)
    
    db.connect()

    cursor = db.connection.cursor()
    # Print PostgreSQL Connection properties
    print (db.connection.get_dsn_parameters(),"\n")

    # Print PostgreSQL version
    cursor.execute("SELECT version();")
    record = cursor.fetchone()
    print("You are connected to - ", record,"\n")


except (Exception, psycopg2.Error) as error :
    print ("Error while connecting to PostgreSQL", error)
