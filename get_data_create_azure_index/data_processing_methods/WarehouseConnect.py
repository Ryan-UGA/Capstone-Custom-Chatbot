import pyodbc

def convert_rows_to_json(cursor: pyodbc.Cursor, rows):
    columns = [column[0] for column in cursor.description]
    # 'name', 'description'
    # 'something', 'something'
    data = [dict(zip(columns, row)) for row in rows]

    return data

def ssms_connect_and_extract(query_string:str, connection_string:str, ssms_format): # SQL Server Management Studio
    try:
        conn = pyodbc.connect(connection_string)
        print("Successfully Connected to the DB")
    except Exception as e:
        print("Something went wrong connecting: ", e)

    try:
        cursor = conn.cursor()
        cursor.execute(query_string)
        records = cursor.fetchall()
        data = convert_rows_to_json(cursor, records)
    except Exception as e:
        print("Something went wrong querying the DB: ", e)

    try:
        conn.close()
        print("Closed connection")
    except Exception as e:
        print("Could not close exception: ", e)
    return data