import json

# ---- Data Model

class Book:
    def __init__(self, oid, title, author):
        self.oid = oid
        self.title = title
        self.author = author
        self.annotations = []
        self.bookmarks = []
        self.read_progress = 0
        self.last_read_position = None

    def __repr__(self):
        return "Book(oid={0}, title={1}, author={2}, read_progress={3}, last_read_position={4}, annotations={5}, bookmarks={6})".format(self.oid, self.title, self.author, self.read_progress, self.last_read_position, self.annotations, self.bookmarks)

class Annotation:
    def __init__(self, oid, book_oid, edit_time, value):
        self.oid = oid
        self.book_oid = book_oid
        self.edit_time = edit_time
        val = json.loads(value)
        self.begin = val["begin"]
        self.end = val["end"]
        self.citation = val["text"]
        self.note = ""

    def __repr__(self):
        return "Annotation(oid={0}, book_oid={1}, citation={2}, note={3})".format(self.oid, self.book_oid, self.citation, self.note)

class Note:
    def __init__(self, oid, book_oid, edit_time, value):
        self.oid = oid
        self.book_oid = book_oid
        self.edit_time = edit_time
        self.text = json.loads(value)["text"]

class Bookmark:
    def __init__(self, oid, book_oid, edit_time, value):
        self.oid = oid
        self.book_oid = book_oid
        self.edit_time = edit_time
        self.anchor = json.loads(value)["anchor"]

class ReadProgress:
    def __init__(self, book_oid, edit_time, progress):
        self.book_oid = book_oid
        self.edit_time = edit_time
        self.progress = float(progress)

class LastReadPosition:
    def __init__(self, book_oid, edit_time, read_position):
        self.book_oid = book_oid
        self.edit_time = edit_time
        self.read_position = read_position

# ---- DB Queries

def fetch_items(conn, query, class_def):
    res = {}
    for row in conn.execute(query):
        obj = class_def(*row)
        res[obj.oid] = obj
    return res

def get_all_open_books(conn):
    get_all_books_query = "SELECT OID, Title, Authors FROM books;"
    return fetch_items(conn, get_all_books_query, Book)

## All annotations

def get_all_annotations(conn):
    get_all_annotations_query = """SELECT Items.OID, Items.ParentID AS BookId, Tags.TimeEdt, Tags.Val FROM Tags
    JOIN Items on Tags.ItemID = Items.OID
    WHERE Tags.TagID = 104 AND Items.State = 0;"""
    return fetch_items(conn, get_all_annotations_query, Annotation)

    # CFI (define 'start' and 'end' of the annotation)
    #
    # PDF case: 
    # 89|88||computer_vision_models|1572701208|{"begin":"pbr:/word?page=20&offs=1171##pdfloc(b128,20)","end":"pbr:/word?page=20&over=1269##pdfloc(b128,20)","text":"the  solution will  be  posted  on\n the  main  book  website  (http://\nwww.computervisionmodels.com"}
    #
    # EPUB case
    # 12|6|Hawkins|Une brève histoire du temps|1569180993|{"begin":"pbr:/word?page=26&offs=663##epubcfi(/6/12!/4/28/1:655)","end":"pbr:/word?page=26&over=737##epubcfi(/6/12!/4/28/1:732)","text":"Les arguments d’Einstein étant de nature plus physique que ceux de Poincaré"}


def get_all_notes(conn):
    ## The notes are linked to an annotation with the same Items.OID
    get_all_notes_query = """SELECT Items.OID, Items.ParentID AS BookId, Tags.TimeEdt, Tags.Val FROM Tags
    JOIN Items on Tags.ItemID = Items.OID
    WHERE Tags.TagID = 105 AND Items.State = 0;"""
    return fetch_items(conn, get_all_notes_query, Note)


def get_all_bookmarks(conn):
    get_all_bookmarks_query = """SELECT Items.OID, Items.ParentID AS BookId, Tags.TimeEdt, Tags.Val FROM Tags
    JOIN Items on Tags.ItemID = Items.OID
    WHERE Tags.TagID = 101 AND Items.State = 0;"""
    return fetch_items(conn, get_all_bookmarks_query, Bookmark)

def get_all_progresses(conn):
    get_all_read_progress_query = """SELECT Items.OID, Tags.TimeEdt, Tags.Val FROM Tags
    JOIN Items on Tags.ItemID = Items.OID
    WHERE Tags.TagID = 80 AND Items.State = 0;"""
    return map(lambda o : ReadProgress(*o), conn.execute(get_all_read_progress_query))


def get_all_last_read_position(conn):
    get_all_read_position_query = """
    SELECT Items.OID, Tags.TimeEdt, Tags.Val FROM Tags
    JOIN Items on Tags.ItemID = Items.OID
    WHERE Tags.TagID = 81 AND Items.State = 0;"""
    return map(lambda o : LastReadPosition(*o), conn.execute(get_all_read_position_query))



def build_books_objects_database(conn):
    books = get_all_open_books(conn)
    annotations = get_all_annotations(conn)
    notes = get_all_notes(conn)
    bookmarks = get_all_bookmarks(conn)
    read_progresses = get_all_progresses(conn)
    last_read_positions = get_all_last_read_position(conn)

    for oid, note in notes.items():
        annotations[oid].note = note.text
    for annotation in annotations.values():
        if annotation.book_oid in books:
            books[annotation.book_oid].annotations.append(annotation)
        else:
            print("Orphan {0}".format(annotation))
    for bookmark in bookmarks.values():
        books[bookmark.book_oid].bookmarks.append(bookmark)
    for read_progress in read_progresses:
        books[read_progress.book_oid].read_progress = read_progress.progress
    for last_read_position in last_read_positions:
        books[last_read_position.book_oid].last_read_position = last_read_position

    return books




import sqlite3

db_path = "/Users/Telequid/Documents/vivlio/books.db"

conn = sqlite3.connect(db_path)
books = build_books_objects_database(conn)






