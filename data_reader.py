import sqlite3


def read(SELECT, FROM, WHERE=None, ORDER_BY=None):
    '''
    Returns data from a SQLite table

    Parameters
    ----------
    SELECT : str
        Which column(s) you want from a table using sqlite syntax
    FROM : str
        Which table you want data from
    WHERE : str
        Conditional statement ex. 'Time >= 11:00'
    ORDER_BY : str
        which column to order the output by
    
    Returns
    -------
    data : list
        SQLite rows in a list of tuples
    
        
    Change address in con to the address of the database on your own machine since this is for mine ~ jath
    '''
    con = sqlite3.connect("database.db")
    cur = con.cursor()
    request = f"SELECT {SELECT} FROM {FROM}"
    if WHERE != None:
        request += f" WHERE {WHERE}"
    if ORDER_BY != None:
        request += f" ORDER BY {ORDER_BY}"
    response = cur.execute(request)
    data = response.fetchall()
    con.close()
    return data
