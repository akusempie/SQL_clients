import psycopg2

conn = psycopg2.connect(host="localhost", database="netology_db", user="postgres", password="postgres", port="5432")
c = conn.cursor()


def create_table():
    c.execute("""
    CREATE TABLE IF NOT EXISTS clients
        (id SERIAL PRIMARY KEY,
        first_name TEXT,
        last_name TEXT,
        email TEXT
    );
    """)
    c.execute("""
    CREATE TABLE IF NOT EXISTS phones
        (id SERIAL PRIMARY KEY,
        phone_number TEXT,
        client_id INTEGER,
        FOREIGN KEY(client_id) REFERENCES clients(id)
    );
    """)


def add_client(first_name, last_name, email):
    c.execute("""
    INSERT INTO clients (first_name, last_name, email)
    VALUES (%s, %s, %s);
    """,
              (first_name, last_name, email))
    conn.commit()


def add_phone(client_id, phone_number):
    c.execute("""
    INSERT INTO phones (client_id, phone_number) 
    VALUES (%s, %s);
    """,
              (client_id, phone_number))
    conn.commit()


def update_client(client_id, first_name=None, last_name=None, email=None):
    if first_name:
        c.execute("""
            UPDATE clients SET first_name=%s WHERE id=%s;
            """,
                  (first_name, client_id))
    if last_name:
        c.execute("""
            UPDATE clients SET last_name=%s WHERE id=%s;
            """,
                  (last_name, client_id))
    if email:
        c.execute("""
            UPDATE clients SET email=%s WHERE id=%s;
            """,
                  (email, client_id))
    conn.commit()


def delete_phone(phone_id):
    c.execute("""
        DELETE FROM phones WHERE id=%s;
        """,
              (phone_id,))
    conn.commit()


def delete_client(client_id):
    c.execute("""
        DELETE FROM clients WHERE id=%s;
        """,
              (client_id,))
    conn.commit()


def search_clients(search_string):
    c.execute("""
        SELECT * FROM clients
        WHERE first_name LIKE %s OR last_name LIKE %s OR id IN 
        (SELECT client_id FROM phones WHERE phone_number LIKE %s);
        """,
              ("%"+search_string+"%", "%"+ search_string+"%", "%"+search_string+"%"))
    return c.fetchall()


# create_table()
#
# add_client("Иоганн", "Бах", "jsbach@kunst.de")
# add_client("Вольфганг", "Моцарт", "wamozart@kunst.at")
#
# add_phone(1, "+49-150-2518590")
# add_phone(1, "+49-171-4241223")
# add_phone(2, "+49-151-4445343")

# update_client(1, first_name="Василий")
# update_client(2, email="salieri@kunst.at")

print(search_clients("Иоганн"))

# delete_phone(2)
# delete_client(1)

conn.close()
