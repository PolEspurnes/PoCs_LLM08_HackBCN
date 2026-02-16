from embeddings import *
from llm_utils import ask_llm
from llm_semanticUtils import ask_llmSemantic
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

@app.route("/poc2-browser", methods=["GET", "POST"])
def poc2_browser():
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
            return render_template("poc2-browser.html", messages=messages)

        #if not football_domain_filter(query):
        #    return "Esta IA solo habla de fútbol."

        ai_response = ask_llmSemantic(query)

        # Restaurar nombres antes de mostrar
        ai_response = denormalize_output(ai_response)

        messages.append({
            "user": query,
            "ai": ai_response
        })

    return render_template("poc2-browser.html", messages=messages)



if __name__ == "__main__":
	app.run(debug=True)
