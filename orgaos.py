from database import DAO


def read():
    data = DAO.run()
    results = []
    for row in data:
        row_dict = {
            "CDORG": row[0],
            "CRAAI": row[1],
            "COMARCA": row[2],
            "FORO": row[3],
            "ORGAO": row[4],
            "TITULAR": row[5]
        }
        results.append(row_dict)
    return results
