# Vivlio ebook reader utils

The objective of this project is to export various data from your Vivlio (PocketBook / Tea) ebook reader. 
Supported data include: 
- annotations
- notes
- bookmarks
- read progress
- last position

The data is accessed from the sqlite database stored in the device.

If you set no profile, this database is located at: 
`<Vivlio_mount_point>/system/config/books.db`

Otherwise, you can find it at:
`<Vivlio_mount_point>/system/profiles/<profile_name>/config/books.db`