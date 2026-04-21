# PoCs_LLM08_HackBCN
PoCs creadas para la presentación **Más allá del Prompt Injection: LLM08 contra Sistemas de Embeddings** de la [HackBCN 2026](https://hackbcn.org/).


## Tech Stack
### LLM Model
El proyecto utiliza actualmente un modelo gratuito a través de **OpenRouter**.


**Pasos para la configuración:**

1. Crear una cuenta en [openrouter.ai](https://openrouter.ai/).
2. Generar una **API Key**.
3. Seleccionar el modelo de tu preferencia y definirlo en `.env`


* **Modelo de ejemplo:** `openai/gpt-oss-20b:free`

Este modelo es suficiente para los propósitos de estas PoCs, aunque es posible intercambiarlo por cualquier otro modelo reciente y de características similares.


### Embedding Model
Para la generación de vectores, se utiliza el siguiente modelo ejecutado de forma **local**:

* **Modelo:** [sentence-transformers/all-MiniLM-L6-v2](https://huggingface.co/sentence-transformers/all-MiniLM-L6-v2)


## Install & Run

1. Configurar `.env`
2. Instalar dependencias
3. Ejecutar

```shell
pip install -m requirements.txt
python3 main.py
```

http://127.0.0.1:5000