#!/usr/bin/env python3

import sqlite3
import sys
from db import build_books_objects_database
from text_exporter import bookDictsExporter


if len(sys.argv) == 1:
    print("Usage: %s vivlio_db_path" % sys.argv[0])
    sys.exit(-1)

conn = sqlite3.connect(sys.argv[1])
books = build_books_objects_database(conn)
bookDictsExporter(books)
