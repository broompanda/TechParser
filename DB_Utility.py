__author__ = 'christie'
import MySQLdb as mdb
import sys


def get_from_db(select_string):
    try:

        con = mdb.connect('172.28.161.199', 'parser_read', 'arastra123', 'platform_counters')
        cur = con.cursor()
        cur.execute(select_string)
        return cur.fetchall()



    except mdb.Error, e:

        print "Error %d: %s" % (e.args[0], e.args[1])
        sys.exit(1)

    finally:

        if con:
            con.close()

def main():

    result_lines = get_from_db("SELECT counter_name  FROM jericho_counters")
    for line in result_lines:
            print line



if __name__ == '__main__':
    main()

