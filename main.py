from embeddings import *
from llm_utils import ask_llm, ask_llmSemantic
from utils import *
from iaFilter import *
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/")
def home():
	return render_template("index.html")


@app.route("/poc1", methods=["GET", "POST"])
def poc1():

	if request.method == "POST":
		data = {
			"nombre_bar": request.form.get("nombre"),
			"fecha_denuncia": request.form.get("fecha"),
			"poblacion": request.form.get("poblacion"),
			"observaciones": request.form.get("observaciones")
		}

		nueva_denuncia(data)

	return render_template("poc1.html")


@app.route("/poc1-browser", methods=["GET", "POST"])
def poc1_browser():
	messages = []

	if request.method == "POST":
		load_embeddings()
		
		query = request.form.get("question")
		datos_denuncia = similarity_search(query)
		ai_response = ask_llm(datos_denuncia)


		messages.append({
			"user": query,
			"ai": ai_response
		})

	return render_template("poc1-browser.html", messages=messages)


@app.route("/poc2", methods=["GET", "POST"])
def poc2():
    messages = []

    if request.method == "POST":
        query = request.form.get("question")

        query = normalize_query(query)

        if forbidden_filter(query):
            #return "No se permite hablar sobre el ilustrísimo Xavier."
            messages.append({
                "user": denormalize_output(query),
                "ai": "No se permite hablar sobre el ilustrísimo Xavier."
            })
            return render_template("poc2.html", messages=messages)

        if not football_domain_filter(query):
            #return: "Esta IA solo habla de fútbol"
            messages.append({
                "user": denormalize_output(query),
                "ai": "Esta IA solo habla de fútbol."
            })
            return render_template("poc2.html", messages=messages)

        ai_response = ask_llmSemantic(query)

        # Restaurar nombres antes de mostrar
        ai_response = denormalize_output(ai_response)

        messages.append({
            "user": query,
            "ai": ai_response
        })

    return render_template("poc2.html", messages=messages)


@app.route("/poc3", methods=["GET", "POST"])
def poc3():

	if request.method == "POST":
		data = {
			"password": request.form.get("password"),
			"question": request.form.get("question")
		}

		#nueva_denuncia(data)

	return render_template("poc3.html")


if __name__ == "__main__":
    
    # AQUI CARGAR LOS EMBEDDINGS DE LA POC2
    global index

    app.run(debug=True)
