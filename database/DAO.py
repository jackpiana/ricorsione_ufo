from database.DB_connect import DBConnect
from model.state import State
from model.sighting import Sighting


class DAO():
    def __init__(self):
        pass

    @staticmethod
    def get_years():
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT YEAR(datetime) as anno 
                    FROM sighting s 
                    ORDER BY anno DESC"""
            cursor.execute(query)

            for row in cursor:
                result.append(row["anno"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_shapes_year(anno: int):
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """SELECT DISTINCT s.shape
                        FROM sighting s 
                        WHERE YEAR(s.datetime)=%s
                        ORDER BY shape ASC"""
            cursor.execute(query, (anno,))

            for row in cursor:
                if row["shape"] != "":
                    result.append(row["shape"])

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def getAllShapes():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select distinct shape from sighting s 
                   where shape != "" """

        cursor.execute(query)

        for row in cursor:
            result.append(row['shape'])

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def get_nodes(year, shape):
        cnx = DBConnect.get_connection()
        result = {}
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor(dictionary=True)
            query = """
                select *
                from sighting s 
                where year(s.datetime) = %s and 
                s.shape = %s
            """

            cursor.execute(query, (year, shape))

            for row in cursor:
                s = Sighting(**row)
                result[s.id] = s

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_edges(year, shape):
        """
        restituisce lista di tuple (nodo partenza id, nodo arrivo id, peso)
        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """
                    select 
                    s1.id, s1.longitude,
                    s2.id, s2.longitude,
                    (greatest(s1.longitude, s2.longitude) - least(s1.longitude, s2.longitude)) as 'weight'
                    from sighting s1, sighting s2 
                    where year(s1.datetime) = %s 
                    and s1.shape = %s
                    and year(s2.datetime) = %s 
                    and s2.shape = %s
                    and s1.state = s2.state
                    and (greatest(s1.longitude, s2.longitude) - least(s1.longitude, s2.longitude)) != 0
                    """

            cursor.execute(query, (year, shape, year, shape))

            for row in cursor:
                if row[1] < row[3]:
                    edge = (row[0], row[2], row[4])
                    result.append(edge)
                else:
                    edge = (row[2], row[0], row[4])
                    result.append(edge)

            cursor.close()
            cnx.close()
        return result

    @staticmethod
    def get_top5_edges(year, shape):
        """
        inutile jack, usa sorted edges

        """
        cnx = DBConnect.get_connection()
        result = []
        if cnx is None:
            print("Connessione fallita")
        else:
            cursor = cnx.cursor()
            query = """
                    select
                    s1.id, s1.longitude,
                    s2.id, s2.longitude,
                    (greatest(s1.longitude, s2.longitude) - least(s1.longitude, s2.longitude)) as 'weight'
                    from sighting s1, sighting s2 
                    where year(s1.datetime) = %s 
                    and s1.shape = %s
                    and year(s2.datetime) = %s 
                    and s2.shape = %s
                    and s1.state = s2.state
                    and (greatest(s1.longitude, s2.longitude) - least(s1.longitude, s2.longitude)) != 0
                    order by (greatest(s1.longitude, s2.longitude) - least(s1.longitude, s2.longitude)) desc
                    limit 5
                            """

            cursor.execute(query, (year, shape, year, shape))

            for row in cursor:
                if row[1] < row[3]:
                    edge = (row[0], row[2], row[4])
                    result.append(edge)
                else:
                    edge = (row[2], row[0], row[4])
                    result.append(edge)

            cursor.close()
            cnx.close()
        return result

if __name__ == '__main__':
    for edge in DAO.get_edges(1995, "triangle"):
        print(edge)
