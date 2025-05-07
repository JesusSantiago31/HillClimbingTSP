from flask import Flask, request, jsonify, render_template
import math
import random

app = Flask(__name__)

def distancia(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    return math.sqrt((lat1 - lat2)**2 + (lon1 - lon2)**2)

def evalua_ruta(ruta, coord):
    total = 0
    for i in range(len(ruta) - 1):
        ciudad1 = ruta[i]
        ciudad2 = ruta[i + 1]
        total += distancia(coord[ciudad1], coord[ciudad2])
    total += distancia(coord[ruta[-1]], coord[ruta[0]])
    return total

def i_hill_climbing(coord):
    ciudades = list(coord.keys())
    mejor_ruta = ciudades[:]
    mejor_distancia = evalua_ruta(mejor_ruta, coord)
    
    max_iteraciones = 10
    for _ in range(max_iteraciones):
        ruta = ciudades[:]
        random.shuffle(ruta)
        mejora = True
        while mejora:
            mejora = False
            dist_actual = evalua_ruta(ruta, coord)
            for i in range(len(ruta)):
                for j in range(len(ruta)):
                    if i != j:
                        ruta_tmp = ruta[:]
                        ruta_tmp[i], ruta_tmp[j] = ruta_tmp[j], ruta_tmp[i]
                        dist = evalua_ruta(ruta_tmp, coord)
                        if dist < dist_actual:
                            ruta = ruta_tmp[:]
                            dist_actual = dist
                            mejora = True
                            break
                if mejora:
                    break
        if evalua_ruta(ruta, coord) < mejor_distancia:
            mejor_ruta = ruta[:]
            mejor_distancia = evalua_ruta(ruta, coord)
    return mejor_ruta, mejor_distancia

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ruta-optima', methods=['POST'])
def ruta_optima():
    data = request.get_json()
    coord = data.get('coordenadas')
    seleccionadas = data.get('seleccionadas')

    if not coord or not seleccionadas:
        return jsonify({'error': 'Faltan coordenadas o selección de ciudades.'}), 400

    try:
        coord_filtradas = {ciudad: coord[ciudad] for ciudad in seleccionadas}
        mejor_ruta, mejor_distancia = i_hill_climbing(coord_filtradas)
        return jsonify({
            'mejor_ruta': mejor_ruta,
            'distancia_total': mejor_distancia
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
