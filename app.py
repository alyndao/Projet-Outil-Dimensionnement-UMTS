from flask import Flask, render_template, request, redirect, url_for
import math

app = Flask(__name__)

@app.route('/')
def accueil():
    return render_template('index1.html')

@app.route('/calcul')
def calcul():
    return render_template('index.html')

@app.route('/calculer', methods=['POST'])
def calculer():
    try:
        nombre_habitants = int(request.form.get('nombre_abonnes', 0))
        taux_penetration = float(request.form.get('taux_penetration', 0.0))
        taux_trafic = float(request.form.get('taux_trafic', 0.0))
        motif_reutilisation = request.form.get('motif_reutilisation', '0/0')
        nombre_its_tch = int(request.form.get('nombre_its_tch', 0))
        taux_blocage = int(request.form.get('taux_blocage', 0))
        frequence = int(request.form.get('frequence', 0))

        # Extraction des valeurs a et b du motif de réutilisation
        a, b = map(int, motif_reutilisation.split('/'))

        # Données du tableau pour différents taux de blocage
        capacite_trafic = {
            1: {
                51: 38.8,
                52: 39.7,
                53: 40.6,
                54: 41.5,
                55: 42.4
            },
            2: {
                51: 41.2,
                52: 42.1,
                53: 43.1,
                54: 44.0,
                55: 44.9
            },
            3: {
                51: 42.9,
                52: 43.9,
                53: 44.8,
                54: 45.8,
                55: 46.7
            }
        }

        # Calculs
        nombre_abonnes = nombre_habitants * taux_penetration / 100
        trafic_total = nombre_abonnes * taux_trafic / 1000

        # Calcul du nombre de porteuses par cellule et du nombre total d'ITs TCH
        nombre_porteuses_par_cellule = frequence / b
        nombre_its_tch_total = int(nombre_porteuses_par_cellule * 8 - nombre_its_tch)

        # Débogage : imprimer les valeurs intermédiaires
        print(f"nombre_habitants: {nombre_habitants}")
        print(f"taux_penetration: {taux_penetration}")
        print(f"taux_trafic: {taux_trafic}")
        print(f"motif_reutilisation: {motif_reutilisation}")
        print(f"a: {a}, b: {b}")
        print(f"frequence: {frequence}")
        print(f"nombre_its_tch_total: {nombre_its_tch_total}")

        # Obtenir le trafic par cellule en fonction du taux de blocage
        if nombre_its_tch_total in capacite_trafic.get(taux_blocage, {}):
            trafic_par_cellule = capacite_trafic[taux_blocage][nombre_its_tch_total]
        else:
            return f"Nombre d'ITs TCH ({nombre_its_tch_total}) non supporté par les données fournies."

        # Calcul du nombre de cellules nécessaires
        nombre_cellules = math.ceil(trafic_total / trafic_par_cellule)

        # Calcul du nombre de sites nécessaires
        nombre_sites = math.ceil(nombre_cellules / a)

        return render_template('index.html', trafic_total=trafic_total, 
                               trafic_par_cellule=trafic_par_cellule, 
                               nombre_cellules=nombre_cellules, 
                               nombre_sites=nombre_sites)
    except Exception as e:
        return str(e)

if __name__ == '__main__':
    app.run(debug=True)
