# NeuralBox 🧠📦

**Run, explore, and chat with state-of-the-art AI models in isolated “boxes.”**

NeuralBox provides a modular way to experiment with different AI models.
Each **box** is a self-contained environment (Docker-based) that includes everything you need to:

* ✅ Download and set up the model locally (via Hugging Face, with a valid token).
* ✅ Launch a **Jupyter server** for exploration.
* ✅ Run a **Gradio chat UI** to interact with the model.
* ✅ Automatically handle **chat history** until the model’s max input length is reached.
* ✅ Access equivalent functionality through **Python scripts** or **notebooks**.

Each model gets its **own folder**.

---

## 🚀 Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/YasminAwad/NeuralBox.git
cd NeuralBox
```

### 2. Create a Python Environment

It is highly suggested to create a python environment where the dependecies needed to download the model are going to be stored.

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Choose the model

Enter the folder of the model you want to play with, for example Llama3.1-8b-instruct:

```bash
cd ./llama3.1_8b_instruct
```

### 4. Add your Hugging Face token

Add a valid huggingface token in the config.yml file inside the config folder.

```yml
hugging_face:
  token: <your_token_here>
```

### 5. Setup and Model Download

Make the setup script executable and run it:

```bash
chmod +x ./scripts/setup.sh
./scripts/setup.sh
```

This will:

* Pull dependencies
* Download the model from Hugging Face using your token
* Change the model position from `~/.cache/huggingface/hub` to `./app/models`

### 6. Run the container!

Run the container with the following command:

```bash
sudo docker compose up
```

You will be able to access the Jupyter Server and play with the model running the cells of the `app/notebooks/main.ipynb`.

If you want to play with the model with the python file `app/python/chat.py` you can access the docker container on another terminal and run the python file.

- Open another terminal and search the container name with:

        docker ps

- Access the container:

        docker exec -it 4a4d4830c62f /bin/bash

- Run the python file:

        python3 ./app/python/chat.py

---

## 🌐 Accessing the Services

* **Jupyter Server:** [http://127.0.0.1:8888/lab](http://127.0.0.1:8888/lab)
* **Gradio Chat UI:** [http://localhost:7860](http://localhost:7860)

---

## 💬 Chat Features

* Interactive chat with the model
* Chat history is preserved until the model’s max input context length is reached
* When the limit is reached, the oldest messages are automatically dropped

You can experiment either via:

* **Notebook (`notebook.ipynb`)** in Jupyter
* **Script (`chat.py`)** from the terminal

---

## Notes

The project has been tested on a linux environment (Ubuntu 25.04), using a GPU RTX 5070ti.