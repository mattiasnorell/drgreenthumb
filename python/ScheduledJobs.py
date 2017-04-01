#!/usr/bin/env python
# -*- coding: utf-8 -*- 
import sqlite3
from Logger import Logger
import time

conn = sqlite3.connect("/data/websites/greenhouse.local/db/greenhouse.db")
curs=conn.cursor()

logger = Logger(conn)

def runScheduledJobs():
    print "Running scheduled jobs"

runScheduledJobs()
conn.close()
