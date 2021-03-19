def annotationExporter(annotation):
    s = "page {0}: {1}\n".format(annotation.page, annotation.citation)
    if len(annotation.note) > 0:
        s += "Note: %s\n" % annotation.note
    return s


def bookExporter(book):
    s = "{0} -- {1}\n\n".format(book.author, book.title)
    for annotation in book.annotations:
        s += annotationExporter(annotation) + "\n"
    return s


def bookDictsExporter(books):
    for book in books.values():
        if len(book.annotations) > 0:
            print(bookExporter(book) + "------------------\n")
