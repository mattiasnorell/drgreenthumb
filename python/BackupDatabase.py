import datetime
from shutil import copyfile
import sys
from os.path import isfile, join
import glob
import os
import sqlite3
from Logger import Logger

conn = sqlite3.connect("/data/websites/greenhouse.local/db/greenhouse.db")
curs=conn.cursor()

logger = Logger(conn)

maxBackups = 7
backupDir = '/data/websites/greenhouse.local/backup/'
source = '/data/websites/greenhouse.local/db/greenhouse.db'
dateTime = datetime.datetime.now().strftime('%Y-%m-%d')
dest = backupDir + 'greenhouse_backup_' + dateTime + '.db'

def deleteOldBackups():
	# Delete old backups
	files = glob.glob(backupDir + "*.db")
	files.sort(key=os.path.getmtime, reverse=True)

	for num in range(maxBackups, len(files)):
		os.remove(files[num])

def copyBackup():
	# Copy new backup
	copyfile(source, dest)
	logger.log("Database backup created")

deleteOldBackups()
copyBackup()