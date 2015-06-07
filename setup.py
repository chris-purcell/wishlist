# perform required imports
import sqlite3
from contextlib import closing
from getpass import getpass

# set up database connection and create database if not existent
db = sqlite3.connect('wishlist.db')

# create required database tables
db.execute('create table if not exists wishlist (id integer primary key autoincrement, title text not null, text text not null, username integer not null)')
db.execute('create table if not exists users (id integer primary key autoincrement, username text not null, password text not null, email text not null)')

# Create default admin user
username = raw_input("Please create a default admin user: ")
password = getpass("Please set password for default admin user: ")
email = raw_input("Email address for password reset and notifications: ")

db.execute('insert into users (username, password, email) values (?, ?, ?)', (username, password, email))

# Commit changes and close database
db.commit()
db.close()
