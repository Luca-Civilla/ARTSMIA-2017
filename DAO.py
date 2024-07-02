from database.DB_connect import DBConnect
from model.connessione import Connessione
from model.object import ArtObject


class DAO():

    @staticmethod
    def getAllObjects():
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = "select * from objects o"

        cursor.execute(query, ())

        for row in cursor:
            result.append(ArtObject(**row))
            # result.append(ArtObject(object_id=row["object_id"], ... ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchiPeso(uID,vID):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select count(distinct eo2.exhibition_id) as peso 
                from exhibition_objects eo, exhibition_objects eo2 
                where eo2.exhibition_id = eo.exhibition_id and eo.object_id =%s and eo2.object_id =%s"""

        cursor.execute(query, (uID,vID,))

        for row in cursor:
            result.append(row["peso"])
            # result.append(ArtObject(object_id=row["object_id"], ... ))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def getArchi2(idMap):
        conn = DBConnect.get_connection()

        result = []

        cursor = conn.cursor(dictionary=True)
        query = """select eo.object_id as id1,eo2.object_id as id2,count(distinct eo2.exhibition_id) as peso
                from exhibition_objects eo, exhibition_objects eo2 
                where eo2.exhibition_id = eo.exhibition_id and eo.object_id != eo2.object_id
                group by eo.object_id, eo2.object_id """

        cursor.execute(query,)

        for row in cursor:
            result.append(Connessione(idMap[row["id1"]],idMap[row["id2"]],row["peso"]))
            # result.append(ArtObject(object_id=row["object_id"], ... ))

        cursor.close()
        conn.close()
        return result
