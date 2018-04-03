import MySQLdb

def check_admin(username,password):
    new_connection = MySQLdb.connect('localhost','root','akash198','Miniproject')
    new_cursor = new_connection.cursor()
    statement = "select username from admin where username='"+username+"' and password='"+password+"';"
    try:
        new_cursor.execute(statement)
    except:
        print("sorry")
    results = new_cursor.fetchone()
    if results!=None:
        return results
    print("no user")