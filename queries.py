from this import d
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


# Helper
def execute_select_query(query):
    db_connect = db_conn()
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
def get_query_4():
    query_droite = get_droite_evolution_by_date()
    query_gauche = get_gauche_evolution_by_date()
    result_droite = execute_select_query(query_droite)
    result_gauche = execute_select_query(query_gauche)

    if result_droite is not None and result_gauche is not None:
        result = [result_gauche, result_droite]
        return result


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
def get_droite_evolution_by_date():
    return """
        SELECT AVG(rf.nb_voix)::INT as evolution, dd.annee FROM resultat_fait rf 
	    INNER JOIN (SELECT id_candidat FROM candidat_dim WHERE gauche = false) droite
	    ON droite.id_candidat = rf.id_candidat
	    INNER JOIN date_dim dd ON dd.id_date = rf.id_date
	    GROUP BY dd.annee
	    ORDER BY dd.annee
    """

def get_gauche_evolution_by_date():
    return """
        SELECT AVG(rf.nb_voix)::INT as evolution, dd.annee FROM resultat_fait rf 
	    INNER JOIN (SELECT id_candidat FROM candidat_dim WHERE gauche = true) gauche
	    ON gauche.id_candidat = rf.id_candidat
	    INNER JOIN date_dim dd ON dd.id_date = rf.id_date
	    GROUP BY dd.annee
	    ORDER BY dd.annee
    """

def get_droite_evolution_by_date_and_region() :
    return """
        SELECT AVG(rf.nb_voix)::INT as evolution, dd.annee, ll.region FROM resultat_fait rf 
        INNER JOIN (SELECT id_candidat FROM candidat_dim WHERE gauche = false) droite
        ON droite.id_candidat = rf.id_candidat
        INNER JOIN date_dim dd ON dd.id_date = rf.id_date
        INNER JOIN lieu_dim ll ON ll.id_lieu = rf.id_lieu
        GROUP BY dd.annee, ll.region
        ORDER BY dd.annee
    """

def get_gauche_evolution_by_date_and_region() :
    return """
        SELECT AVG(rf.nb_voix)::INT as evolution, dd.annee, ll.region FROM resultat_fait rf 
        INNER JOIN (SELECT id_candidat FROM candidat_dim WHERE gauche = true) gauche
        ON gauche.id_candidat = rf.id_candidat
        INNER JOIN date_dim dd ON dd.id_date = rf.id_date
        INNER JOIN lieu_dim ll ON ll.id_lieu = rf.id_lieu
        GROUP BY dd.annee, ll.region
        ORDER BY dd.annee
    """

def get_seuil_passage_tour_2():
    return """
        SELECT departement, AVG(smp.seuil)::INT as seuil_moyenne FROM 
                (SELECT MIN(nb_voix) as seuil, rf.id_lieu 
                    FROM resultat_fait rf
				 	INNER JOIN (SELECT id_date, annee FROM date_dim WHERE tour='1') dd
                    ON dd.id_date = rf.id_date
                    INNER JOIN 
				 		(SELECT firstTour.id_candidat FROM 
							(SELECT id_candidat FROM resultat_fait rf
							INNER JOIN (SELECT id_date, annee FROM date_dim WHERE tour='1') dd
							ON dd.id_date = rf.id_date
							GROUP BY id_candidat) as firstTour
							INNER JOIN
							(SELECT id_candidat FROM resultat_fait rf
							INNER JOIN (SELECT id_date, annee FROM date_dim WHERE tour='2') dd
							ON dd.id_date = rf.id_date
							GROUP BY id_candidat) as secondTour
						ON secondTour.id_candidat = firstTour.id_candidat) cand
                    ON cand.id_candidat = rf.id_candidat
                    GROUP BY rf.id_lieu
                    ) as smp
        INNER JOIN lieu_dim as ld ON ld.id_lieu = smp.id_lieu
        GROUP BY departement
        ORDER BY seuil_moyenne DESC	
    """


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
