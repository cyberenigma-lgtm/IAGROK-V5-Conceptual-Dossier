import json
import urllib.request
import urllib.error
from flask import Flask, request, Response, jsonify

app = Flask(__name__)

# Configuración

@app.route("/sse", methods=["GET", "POST"])
def sse():
    if request.method == "POST":
        return handle_message(request.get_json())
        
    # GET: Event Stream
    def event_stream():
        endpoint_url = "http://127.0.0.1:11436/sse"
        yield f"event: endpoint\ndata: {endpoint_url}\n\n"
        while True:
            import time
            time.sleep(1)
            yield ": ping\n\n"
            
    return Response(event_stream(), mimetype="text/event-stream")

@app.route("/message", methods=["POST"])
def message():
    return handle_message(request.get_json())

def handle_message(req_data):
    if not req_data:
        return jsonify({"error": "Invalid request"}), 400
        
    method = req_data.get("method")
    req_id = req_data.get("id")
    
    if method == "initialize":
        # Responder con las capacidades del servidor
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "protocolVersion": "2024-11-05",
                "capabilities": {
                    "tools": {}
                },
                "serverInfo": {
                    "name": "Noxferion-Proxy",
                    "version": "1.0.0"
                }
            }
        }
        return jsonify(response)
        
    elif method == "tools/list":
        # Listar herramientas
        response = {
            "jsonrpc": "2.0",
            "id": req_id,
            "result": {
                "tools": [
                    {
                        "name": "ask_noxferion",
                        "description": "Pregunta al cerebro local soberano de Noxferion.",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "prompt": {
                                    "type": "string",
                                    "description": "La consulta o instrucción para el modelo local."
                                },
                                "model": {
                                    "type": "string",
                                    "description": "El modelo a utilizar (opcional). Por defecto usa 'noxferion' o el mejor modelo disponible."
                                }
                            },
                            "required": ["prompt"]
                        }
                    }
                ]
            }
        }
        return jsonify(response)
        
    elif method == "tools/call":
        params = req_data.get("params", {})
        tool_name = params.get("name")
        tool_args = params.get("arguments", {})
        
        if tool_name == "ask_noxferion":
            prompt = tool_args.get("prompt")
            model = tool_args.get("model", "Noxferion: Evolution AI (Aprendiz)")
            
            # Intentar llamar al backend local de IAGROK primero (puerto 5000)
            try:
                data = json.dumps({"query": prompt, "model": model}).encode("utf-8")
                req = urllib.request.Request("http://127.0.0.1:5000/api/chat", data=data, headers={"Content-Type": "application/json"})
                with urllib.request.urlopen(req, timeout=30) as response:
                    res = json.loads(response.read().decode("utf-8"))
                    answer = res.get("result", {}).get("answer", "No se obtuvo respuesta.")
            except Exception as e:
                answer = f"Error al conectar con el backend soberano IAGROK (5000): {e}"
            
            response = {
                "jsonrpc": "2.0",
                "id": req_id,
                "result": {
                    "content": [
                        {
                            "type": "text",
                            "text": answer
                        }
                    ]
                }
            }
            return jsonify(response)
            
    # Para cualquier otro método no implementado
    return jsonify({
        "jsonrpc": "2.0",
        "id": req_id,
        "result": {}
    })

if __name__ == "__main__":
    import sys
    port = 11436
    print(f"Iniciando Noxferion Proxy en puerto {port}...")
    app.run(host="127.0.0.1", port=port, debug=False)