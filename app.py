from __future__ import annotations
from typing import List, Optional, Dict, Any

import os
from flask import Flask, request, jsonify, send_from_directory
from pyproj import Transformer

from graph import Graph
from makeGraph import makeGraph

from a_star import astar

app = Flask(__name__, static_folder="web/static", static_url_path="/")

transformer = Transformer.from_crs("EPSG:2180", "EPSG:4326", always_xy=True)


STATE: Dict[str, Any] = {
    "graph": None,   # type: Optional[Graph]
    "shp_path": None # ostatnie źródło
}


def graph_to_geojson(graph: Graph) -> Dict[str, Any]:
    features: List[Dict[str, Any]] = []
    # Edges
    for from_id, edges in graph.edges.items():
        for e in edges:
            n1 = graph.get_node(e.from_node)
            n2 = graph.get_node(e.to_node)
            if not n1 or not n2:
                continue
            
            lon1, lat1 = transformer.transform(n1.x, n1.y)
            lon2, lat2 = transformer.transform(n2.x, n2.y)

            features.append({
                "type": "Feature",
                "geometry": {"type": "LineString", "coordinates": [[lon1, lat1], [lon2, lat2]]},
                "properties": {"from": e.from_node, "to": e.to_node, "weight": getattr(e, "weight", None)},
            })
    # Nodes
    for nid, n in graph.nodes.items():
        lon, lat = transformer.transform(n.x, n.y)
        features.append({
            "type": "Feature",
            "geometry": {"type": "Point", "coordinates": [lon, lat]},
            "properties": {"id": nid},
        })
    return {"type": "FeatureCollection", "features": features}


@app.route("/")
def index():
    return send_from_directory(app.static_folder, "index.html")


@app.route("/api/load", methods=["POST"])
def api_load():
    data = request.get_json(silent=True) or {}
    shp_path = data.get("shp_path")
    if not shp_path or not os.path.exists(shp_path):
        return jsonify({"ok": False, "error": "Podaj prawidłową ścieżkę."}), 400

    g = makeGraph(shp_path)
    if g is None:
        return jsonify({"ok": False, "error": "nie udało się zbudować grafu."}), 400

    STATE["graph"] = g
    STATE["shp_path"] = shp_path

    return jsonify({
        "ok": True,
        "nodes": len(g.nodes),
        "edges": sum(len(v) for v in g.edges.values()),
        "message": f"graf załądowany z {shp_path}"
    })


@app.route("/api/nodes")
def api_nodes():
    g: Optional[Graph] = STATE.get("graph")
    if not g:
        return jsonify({"ok": False, "error": "Graf nie załadowany. Najpierw POST /api/load."}), 400
    ids = list(g.nodes.keys())
    return jsonify({"ok": True, "ids": ids, "total": len(ids)})

@app.route("/api/nodes_all")
def api_nodes_all():
    g: Optional[Graph] = STATE.get("graph")
    if not g:
        return jsonify({"ok": False, "error": "Graf nie załadowany. Najpierw POST /api/load."}), 400
    
    data = []
    for nid, n in g.nodes.items():
        lon, lat = transformer.transform(n.x, n.y)
        data.append({"id": nid, "x": lon, "y": lat}) # x=lon, y=lat 

    return jsonify({"ok": True, "nodes": data, "total": len(data)})


@app.route("/api/path", methods=["POST"])
def api_path():
    data = request.get_json(silent=True) or {}
    start = data.get("start_id")
    end = data.get("end_id")
    criteria = data.get("criteria", "shortest")  # "shortest" albo "fastest"
    use_dijkstra = data.get("use_dijkstra", False)

    if not start or not end:
        return jsonify({"ok": False, "error": "Podaj 'start_id' i 'end_id'"}), 400
    
    g: Optional[Graph] = STATE.get("graph")
    if not g:
        return jsonify({"ok": False, "error": "Graf nie załadowany. Najpierw POST /api/load."}), 400

    use_shortest = (criteria == "shortest")

    # astar zwraca listę tupli (node_id,edge_id)
    # edge_id to None dla pierwszego węzła
    path_data = astar(start, end, g, shortest=use_shortest, dijkstra=use_dijkstra)
    
    if not path_data:
        return jsonify({"ok": False, "error": "Nie znaleziono ścieżki."}), 404

    path_ids = [item[0] for item in path_data]
    full_coords: List[List[float]] = []
    total_dist = 0.0

    # Rekonstrukcja geometrii ścieżki
    for i in range(1, len(path_data)):
        prev_node_id = path_data[i-1][0]
        # curr_node_id = path_data[i][0]
        edge_id = path_data[i][1]

        points = g.get_edge_geometry(edge_id)
        if not points:
            continue
            
        p_start = points[0]
        p_end = points[-1]
        
        n_prev = g.get_node(prev_node_id)
        
        # dystans
        dist_start = (p_start[0] - n_prev.x)**2 + (p_start[1] - n_prev.y)**2
        dist_end = (p_end[0] - n_prev.x)**2 + (p_end[1] - n_prev.y)**2
        
        # Jeśli bliżej końca odwróć punkty
        segment_coords = list(points)
        if dist_end < dist_start:
            segment_coords = segment_coords[::-1]
            
        # Dłługość 
        for k in range(len(segment_coords) - 1):
            p1 = segment_coords[k]
            p2 = segment_coords[k+1]
            d = ((p1[0]-p2[0])**2 + (p1[1]-p2[1])**2)**0.5
            total_dist += d

        transformed_segment = []
        for pt in segment_coords:
            lon, lat = transformer.transform(pt[0], pt[1]) # transformacja do lat lon
            transformed_segment.append([lon, lat])

        if not full_coords:
            full_coords.extend(transformed_segment)
        else:
            # duplikacje
            full_coords.extend(transformed_segment[1:])

    feature = {
        "type": "Feature",
        "geometry": {"type": "LineString", "coordinates": full_coords},
        "properties": {"distance": total_dist, "nodes": path_ids},
    }
    return jsonify({"ok": True, "path": path_ids, "distance": total_dist, "feature": feature})


@app.route("/api/graph")
def api_graph():
    g: Optional[Graph] = STATE.get("graph")
    if not g:
        return jsonify({"ok": False, "error": "Graf nie załadowany. Najpierw POST /api/load."}), 400
    return jsonify(graph_to_geojson(g))


if __name__ == "__main__":
    port = int(os.environ.get("PORT", "8000"))
    app.run(host="0.0.0.0", port=port, debug=True)
