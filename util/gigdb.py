#!/usr/bin/env python
import settings
import mysql.connector

def db_connect():
    return mysql.connector.connect(
            host="localhost",
            user=settings.db_user,
            password=settings.db_password,
            database=settings.database,
            charset='utf8mb4'
            )

def db_execute_sql(sql, fetch, **kwargs):
    mydb = db_connect()

    mycursor = mydb.cursor(buffered=True)

    mycursor.execute(sql, tuple(kwargs.values()))

    rows = None
    if fetch:
        rows = mycursor.fetchall()

    mydb.commit()
    mycursor.close()
    mydb.disconnect()

    return rows

def add_mute_member(guild_id, member_id, member_name):
    db_execute_sql("INSERT INTO mute_members VALUES ( %s, %s, %s ) ON DUPLICATE KEY UPDATE member_name = %s", False, guild_id=guild_id, member_id=member_id, member_name=member_name, member_name2=member_name )

def delete_mute_member(guild_id, member_id):
    db_execute_sql("DELETE FROM mute_members WHERE guild_id = %s AND member_id = %s", False, guild_id=guild_id, member_id=member_id)

def get_all(table):
    return db_execute_sql(f"SELECT * FROM {table}", True)

def save_guild(id, mod_log_channel_id):
    db_execute_sql("INSERT INTO guilds VALUES ( %s, %s ) ON DUPLICATE KEY UPDATE mod_log_channel_id = %s", False, id=id, mod_log_channel_id=mod_log_channel_id, mod_log_channel_id_2=mod_log_channel_id)
