import threading
import sqlite3
import datetime
from NewSimpleSQL.SimpleSQLite import Database



# Example usage
update_thread = threading.Thread(target=update_user_info, args=(1250676888607789158, 'new_username', datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")))  # Replace with actual values
update_thread.start()
