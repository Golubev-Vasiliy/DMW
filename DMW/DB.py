import sys 
import mysql.connector
from mysql.connector import Error



con_mysql = 0
id = ""
steg = ""

#connect for DB
def connect():
    try:
        """ Connect to MySQL database """
        global con_mysql
        con_mysql = mysql.connector.connect(user='ssp', password='sspPassword', host='10.208.2.0', database='ssp')

        if con_mysql.is_connected():
            print('Connected to MySQL database')
    except Error as e:
        print(e)

#select user
def select_user(user, password):
    try:
        connect()
        cursor = con_mysql.cursor()
        query = "SELECT id FROM user WHERE user=%s AND password=%s"
        cursor.execute(query, (user, password))
        row = cursor.fetchone()
        while row is not None:
            print(row[0])
            global id
            id = row[0]
            row = cursor.fetchone()
    except Error as e:
        print(e)

    finally:
        cursor.close()
        con_mysql.close()

#select_dwm_user function have a mistake in the select query
def select_dwm(id):
    query = "SELECT stegocode FROM symbolSteg WHERE id_u = 94"
    try:
        connect()
        cursor = con_mysql.cursor()
        cursor.execute(query)
        row = cursor.fetchone()
        while row is not None:
            print(row[0])
            global steg
            steg = row[0]
            row = cursor.fetchone()
    except Error as e:
        print(e)

    finally:
        cursor.close()
        con_mysql.close()


#insert query
def insert_user(user, password, email):
    query = "INSERT INTO user(user,password,email) VALUES(%s,%s,%s)"
    args = (user, password, email)

    try:
        connect()
        cursor = con_mysql.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        con_mysql.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        con_mysql.close()

#insert_dmg
def insert_dmg(id_u, stegocode):
    query = "INSERT INTO symbolSteg(id_u, stegocode) VALUES (%s, %s)"
    args = (id_u, stegocode)

    try:
        connect()
        cursor = con_mysql.cursor()
        cursor.execute(query, args)

        if cursor.lastrowid:
            print('last insert id', cursor.lastrowid)
        else:
            print('last insert id not found')

        con_mysql.commit()
    except Error as error:
        print(error)

    finally:
        cursor.close()
        con_mysql.close()



#call function
if __name__ == '__main__':
    #connect
    #connect();
    #select
    #select_user('user', 'password')
    #insert
    #insert_user('user', 'password', 'email')
    print 'very good'