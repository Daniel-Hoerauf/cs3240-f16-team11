from psycopg2 import connect
from collections import defaultdict
# Daniel Hoerauf, dah4pe

PG_USER = 'postgres'
PG_USER_PASS = 'wombat'
PG_DATABASE = 'course1'

def instructor_numbers(dept_id):
    conn = connect('dbname={} user={} password={}'.format(PG_DATABASE,
                                                          PG_USER, PG_USER_PASS))
    cur = conn.cursor()
    cur.execute('SELECT * FROM coursedata WHERE deptID=%s', (dept_id,))
    dept_courses = cur.fetchall()
    ret_dict = defaultdict(int)
    for course in dept_courses:
        ret_dict[course[6]] += course[4]

    cur.close()
    conn.close()
    return dict(ret_dict)


def main():
    print(instructor_numbers('APMA'))


if __name__ == '__main__':
    main()
