import psycopg2

import excel

conn = psycopg2.connect(host="localhost", database="postgres", user="root", password="991155")
cur = conn.cursor()


def write_unas_data(data):
    sql = "INSERT INTO unas_positions (position, name, photo, type, position_seller, seller_photo, status, seller_name) SELECT %s, %s, %s, %s, %s, %s, %s, %s WHERE NOT EXISTS (SELECT 1 FROM unas_positions WHERE position = %s);"
    for d in data:
        cur.execute(
            sql,
            (
                d[0],
                d[1],
                d[2],
                "",
                "",
                "",
                "created",
                "",
                d[0],
            ),
        )
    conn.commit()


def get_new_article():
    cur.execute(
        "SELECT id, position, name, photo FROM unas_positions WHERE status = 'created' LIMIT 1"
    )
    return cur.fetchone()


def write_row(
    position, name, photo, type, position_seller, seller_photo, status, names
):
    for i in range(len(seller_photo)):
        try:
            cur.execute(
                "INSERT INTO unas_positions (position, name, photo, type, position_seller, seller_photo, status, seller_name) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    position,
                    name,
                    photo,
                    type,
                    position_seller[i],
                    seller_photo[i],
                    status,
                    names[i],
                ),
            )
            print(
                position,
                name,
                photo,
                type,
                position_seller[i],
                seller_photo[i],
                status,
                names[i],
            )
        except Exception as e:
            print(e)
    conn.commit()


def delete_row_by_id(id):
    cur.execute("DELETE FROM unas_positions WHERE id = %s", (id,))
    conn.commit()


def get_unchecked_position():
    cur.execute("SELECT * FROM unas_positions WHERE status = 'parsed' LIMIT 1")
    return cur.fetchone()


def get_stats():
    cur.execute(
        "SELECT COUNT(*) as total_positions, SUM(CASE WHEN status = 'created' THEN 1 ELSE 0 END) as created_positions, SUM(CASE WHEN status = 'parsed' THEN 1 ELSE 0 END) as parsed_positions, SUM(CASE WHEN status = 'approved' THEN 1 ELSE 0 END) as approved_positions, SUM(CASE WHEN status = 'disliked' THEN 1 ELSE 0 END) as disliked_positions FROM unas_positions;"
    )
    return cur.fetchone()


def update_status(id, status):
    cur.execute(f"UPDATE unas_positions SET status='{status}' WHERE id={id}")
    conn.commit()


def get_approved():
    cur.execute("SELECT * FROM unas_positions WHERE status = 'approved'")
    return cur.fetchall()
