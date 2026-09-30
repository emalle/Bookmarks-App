import sqlite3
from bs4 import BeautifulSoup

def get_or_create_folder(conn, name, parent_id, user_id=1):
    cur = conn.execute(
        "SELECT id FROM folders WHERE user_id = ? AND parent_id IS ? AND name = ?",
        (user_id, parent_id, name)
    )
    row = cur.fetchone()
    if row:
        return row[0]
    cur = conn.execute(
        "INSERT INTO folders (user_id, parent_id, name) VALUES (?, ?, ?)",
        (user_id, parent_id, name)
    )
    return cur.lastrowid

def import_bookmark(conn, url, title, folder_id, user_id=1):
    try:
        conn.execute(
            "INSERT INTO bookmarks (user_id, folder_id, url, title) VALUES (?, ?, ?, ?)",
            (user_id, folder_id, url, title)
        )
        return True
    except sqlite3.IntegrityError:
        return False
    
def walk (conn, dl_tag, parent_folder_id, user_id=1):
    inserted = 0
    skipped = 0

    for child in dl_tag.find_all(["dt"], recursive=False):
        h3 = child.find("h3", recursive=False)
        a = child.find("a", recursive=False)

        if h3:
            folder_name = h3.text.strip()
            folder_id = get_or_create_folder(conn, folder_name, parent_folder_id, user_id)

            nested_dl =child.find("dl", recursive=False)
            if nested_dl:
                sub_inserted, sub_skipped = walk(conn, nested_dl, folder_id, user_id)
                inserted += sub_inserted
                skipped += sub_skipped
        elif a :
            url = a.get("href")
            title = a.text.strip()
            if url :
                if import_bookmark(conn, url, title, parent_folder_id, user_id):
                    inserted += 1
                else:
                    skipped +=1
    return inserted, skipped

    
def main():
    conn = sqlite3.connect("bookmarks.db") # I open the connection ONCE 
    
    with open("bookmarks.html", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html5lib")
    try:

        conn.execute("INSERT OR IGNORE INTO users(id, email) VALUES (?, ?)",
                     (1, "e.lucianille@gmail.com")
                     )

        top_level_dl = soup.find("dl")
        inserted, skipped = walk (conn, top_level_dl, parent_folder_id=None)

        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()

    print(f"Done! Imported {inserted} bookmarks, skipped {skipped} bookmarks")


if __name__=="__main__":
    main()