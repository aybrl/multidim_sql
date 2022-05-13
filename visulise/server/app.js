const express    = require('express');
const dotenv     = require('dotenv');
const bodyParser = require('body-parser');
const path       = require('path');
const cors       = require('cors');
const { Pool, Client } = require("pg");

// DB Connection
const pool = new Pool({
    user: "citizens",
    host: "172.31.250.25",
    database: "postgres",
    password: "citizens",
    port: "5432"
  });

//Config
const app = express()
dotenv.config()
app.use(cors())


app.get('/result-per-year-region', (req, res) => {
    let query = `
        SELECT AVG(rf.nb_voix)::INT as evolution, dd.annee, ll.region FROM resultat_fait rf 
        INNER JOIN (SELECT id_candidat FROM candidat_dim WHERE gauche = ${req.query.parti}) gauche
        ON gauche.id_candidat = rf.id_candidat
        INNER JOIN (SELECT id_date, annee FROM date_dim WHERE tour='1' AND annee=${req.query.year}) dd ON dd.id_date = rf.id_date
        INNER JOIN lieu_dim ll ON ll.id_lieu = rf.id_lieu
        GROUP BY dd.annee, ll.region
    `
    pool.query(query, (err, result) => {
        //res.send(result)
        if(result) res.send(result.rows)
        else res.end({'code' : 'error'})
        //pool.end();
      });

});

app.get('/result-per-year', (req, res) => {
    let query = `
        SELECT ((SUM(pf.votants) / CAST(SUM(pf.inscrits) as float)) * 100) as taux_paticip, dd.annee, ld.region 
        FROM participation_fait pf
        INNER JOIN (SELECT id_date, annee FROM date_dim WHERE annee=${req.query.year}) dd ON dd.id_date = pf.id_date
        INNER JOIN lieu_dim ld ON ld.id_lieu = pf.id_lieu
        GROUP BY dd.annee, ld.region
        ORDER BY dd.annee
    `
    pool.query(query, (err, result) => {
        //res.send(result)
        if(result) res.send(result.rows)
        else res.end({'code' : 'error'})
        //pool.end();
      });

});


//Listen
app.listen(4042, () => {console.log(`app listening at port : ${4042}`)})