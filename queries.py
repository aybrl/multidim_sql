import psycopg2 as psycopg2


def db_conn():
    conn = psycopg2.connect(
        user="citizens",
        password="citizens",
        host="172.31.253.182",
        port="5432",
        database="postgres"
    )
    return conn


db_connect = db_conn()


# Helper
def execute_select_query(query):
    try:
        cursor = db_connect.cursor()
        cursor.execute(query)
        row = cursor.fetchall()
        cursor.close()
        return row
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return None

    finally:
        if db_connect is not None:
            db_connect.close()


# Execute function
def get_query_5():
    query = get_seuil_passage_tour_2()
    result = execute_select_query(query)
    if result is not None:
        return result

def get_query_6():
    query = get_laguiller_ranking_by_region_query()
    result = execute_select_query(query)
    if result is not None:
        return result


# Queries
def get_seuil_passage_tour_2():
    return """SELECT departement, AVG(smp.seuil) as seuil_moyenne FROM 
                (SELECT MIN(prop_voix) as seuil, rf.id_lieu 
                    FROM resultat_fait rf
                    INNER JOIN (SELECT id_date, annee FROM date_dim WHERE tour='2') dd
                    ON dd.id_date = rf.id_date
                    GROUP BY rf.id_lieu
                    ) as smp
        INNER JOIN lieu_dim as ld ON ld.id_lieu = smp.id_lieu
        GROUP BY departement
        ORDER BY departement"""


def get_laguiller_ranking_by_region_query():
    return """SELECT l.region, SUM(res.moyenne) as cumul_moyenne
                    FROM (SELECT id_lieu as idl, sum(prop_voix) as moyenne
                            FROM resultat_fait as rf
                WHERE id_candidat = (SELECT id_candidat
                                    FROM candidat_dim
                                    WHERE nom = 'LAGUILLER ' LIMIT 1)
                GROUP BY id_lieu) res, lieu_dim l
                WHERE l.id_lieu = res.idl
                GROUP BY (l.region)
                ORDER BY cumul_moyenne DESC"""
