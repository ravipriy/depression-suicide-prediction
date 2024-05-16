import mysql.connector

mysql_config = {
    'host': 'localhost', 
    'user': 'root',
    'password': 'admin',
    'database': 'amanProject', 
}

def conn():
    try:
        connection = mysql.connector.connect(**mysql_config)
        return connection
    
    except mysql.connector.Error as e:
        print(f"Error: {e}")


connection=conn()




def registerUserIntoDb(fullname,email,password,gender,dob):
    if connection.is_connected():
                cursor = connection.cursor()
                insert_query = "INSERT INTO patientDetails (fullname, email, password,gender,dob) VALUES (%s, %s, %s, %s, %s)"
                data = (fullname, email, password,gender,dob)

                cursor.execute(insert_query, data)
                connection.commit()
                return True
    return False
                

def login_user(email, password):
    try:
            # Create a cursor object to execute SQL queries
            cursor = connection.cursor()

            # Check if the user exists in the 'users' table
            select_query = "SELECT * FROM patientdetails WHERE email = %s AND password = %s"
            data = (email, password)

            cursor.execute(select_query, data)

            # Fetch the result
            user = cursor.fetchone()

            if user:
                return user[1]
            else:
                print("Login failed. Invalid email or password.")

    except mysql.connector.Error as e:
        print(f"Error: {e}")



def insertBasicOnPredict(data):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO suicidetext (email, fullname, input_text, date, output_number) VALUES (%s, %s, %s,%s, %s)"
        
        print("Insert Query:", insert_query)
        print("Data:", data)
        
        cursor.execute(insert_query, data)
        connection.commit()
        print("Data inserted successfully!")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()  # Close cursor after execution



def fetchDetails(email):
    cursor = connection.cursor()
    try:
        select_query = "SELECT fullname FROM patientdetails WHERE email = %s "
        data = [email]
        cursor.execute(select_query, data)
        r1 = cursor.fetchone()
        
        select_query = "SELECT phq, gad, epworth,date, output_text FROM anxiety WHERE email = %s "
        data = [email]
        cursor.execute(select_query, data)
        r2 = cursor.fetchall()

        select_query = "SELECT input_text,date, output_number FROM suicidetext WHERE email = %s "
        data = [email]
        cursor.execute(select_query, data)
        r3 = cursor.fetchall()

        

       
        print("<==========================>")
        print("R1 ",r1)
        print("R2 ",r2)
        print("R3 ",r3)
        print("<==========================>")


        data = [r1, r2, r3]



        return data, r1[0].split()[0]
    
    except mysql.connector.Error as err:
        print(f"Error Fetching  data: {err}....")



def insertAnxietyOnPredict(data):
    try:
        cursor = connection.cursor()
        insert_query = "INSERT INTO anxiety (email, fullname,phq, gad, epworth, date, output_text) VALUES (%s, %s, %s,%s, %s, %s, %s)"
        
        print("Insert Query:", insert_query)
        print("Data:", data)
        
        cursor.execute(insert_query, data)
        connection.commit()
        print("Data inserted successfully!")
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    finally:
        cursor.close()  # Close cursor after execution
