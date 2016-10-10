from psycopg2 import connect
from csv import reader
# Daniel Hoerauf, dah4pe


PG_USER = 'postgres'
PG_USER_PASS = 'wombat'
PG_DATABASE = 'course1'
PG_HOST_INFO = ''


def load_course_database(db_name, csv_filename):
    conn = connect('dbname={} user={} password={} {}'.format(
        db_name, PG_USER, PG_USER_PASS, PG_HOST_INFO))
    cur = conn.cursor()
    with open(csv_filename, 'rU') as csv_file:
        csv = reader(csv_file)
        for row in csv:
            cur.execute('INSERT INTO coursedata (deptID, courseNum, semester, '\
                        'meetingType, seatsTaken, seatsOffered, instructor) ' \
                        'VALUES (%s, %s, %s, %s, %s, %s, %s)', tuple(row))

    conn.commit()
    cur.close()
    conn.close()


def main():
    load_course_database(PG_DATABASE, 'seas-courses-5years.csv')


if __name__ == '__main__':
    main()
