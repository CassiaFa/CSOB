import mysql.connector as msc

class Connexion:
    __user = "root"
    __password = "root"
    __host = "localhost"
    __port = "8081"
    __database = None
    __cursor = None

    @classmethod
    def creation(cls, db_name, sql_file):
        if cls.__cursor == None:
            cls.__bdd = msc.connect(user = cls.__user, password = cls.__password, host = cls.__host, port = cls.__port, database = cls.__database)
            cls.__cursor = cls.__bdd.cursor()
            cls.__database = db_name
            # f = open(sql_file, 'r').read()
            # cls.__cursor.execute(f, multi=True)
        
            with open(sql_file, 'r') as sql_file:
                result_iterator = cls.__cursor.execute(sql_file.read(), multi=True)
                for res in result_iterator:
                    print("Running query: ", res)  # Will print out a short representation of the query
                    print(f"Affected {res.rowcount} rows" )

                cls.__bdd.commit()  # Remember to commit all your changes!
            

    @classmethod
    def ouvrir(cls):
        if cls.__cursor == None:
            cls.__bdd = msc.connect(user = cls.__user, password = cls.__password, host = cls.__host, port = cls.__port, database = cls.__database)
            cls.__cursor = cls.__bdd.cursor()


    @classmethod
    def execute(cls, query):
        cls.__cursor.execute(query)
        if query.split(" ")[0] != "SELECT":
            cls.__bdd.commit()
            
        return cls.__cursor.fetchall()

    @classmethod
    def execute_file(cls, file):
        f = open(file, 'r').read()
        cls.__cursor.execute(f, multi=True)
        cls.__bdd.commit()

    @classmethod
    def fermer(cls):
        cls.__cursor.close()
        cls.__bdd.close()
        cls.__cursor = None
    
    @classmethod
    def drop_db(cls):
        query = f"DROP DATABASE IF EXISTS {cls.__database}"
        cls.__cursor.execute(query)
        cls.__bdd.commit()