from embeddings import *
from llm_utils import ask_llm
from utils import nueva_denuncia
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



if __name__ == "__main__":
	app.run(debug=True)
