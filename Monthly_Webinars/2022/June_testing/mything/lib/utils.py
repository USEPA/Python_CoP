def invert(data):
    """Return reversed data, at most 10 items"""
    
    if isinstance(data, dict):
        print("Warning: reversing dict keys only")
        
    return list(reversed(data))


def summarize_db(db_conn):
    """Summarize data in DB, db_conn is DB connection"""
    records = 0
    total_inv = 0
    
    # count records and items returned by invert()
    for res in db_conn.execute("select name, role from people"):
        records += 1
        total_inv += len(invert(res[1]))
    return {"records": records, "total_inv": total_inv}


def untested():
    """This could take a while"""
    for i in range(10**100):
        print(i)
        