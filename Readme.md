# Automatic Question Generation and Evaluation System
This system is about saving directly to firebase again with the sources you upload to firebase;
* 7 models (“gemini-1.5-flash”, “nvidia/nemotron-4-340b-instruct”, “gemma2:27b”, “aya-expanse:32b”, “mistral-small”, “llama3.1:70b”, “qwen2.5:32b”) over 
* 6 question types (“Multiple Choice”, “True False”, “Fill in the Blank”, “Open Question”, “Matching”, “Short Answer”)
* 3 levels of difficulty(“easy”, “medium”, “hard”) 
you can generate questions.

Sources are shared as source.json.
You can create firebase realtime db and import it into it. 
I used *“question-gen-sources”* as the db name for sources. 
I used *“generated-question-list”* as the db name to save generated questions.

After importing the source as above and entering the envs for the apikeys, you can start generating questions as below.

### required envs
GOOGLE_API_KEY=
NVIDIA_API_KEY=
FIREBASE_DB_URL=

After entering the envs, you can work either locally or with docker with or without deployment.
### with virtual environment

```
pip install virtualenv
python -m venv .venv
source env/bin/activate

python -m pip install -r requirements.txt
```

### You can run them in the docker image.

```
docker buildx build --platform linux/amd64 -t question-generation-and-evaluation .
docker run question-generation-and-evaluation
```

## Question Generation Project
`python q_gen_task_list.py`

## Question Evaluation Project
`python correct_to_generated_questions.py`

## models
#### local models ()
How to install and run ollama models ?
https://github.com/ollama/ollama

<!-- MODELS=("gemma2" "aya-expanse" "mistral-nemo" "llama3.1" "qwen2.5", "mistral") -->
<!-- MODELS=("gemma2:27b" "aya-expanse:32b" "mistral-small" "llama3.1:70b" "qwen2.5:32b") -->

    - ollama run gemma2:27b    (27GB)
    - ollama run aya-expanse:32b    (20GB)
    - ollama run llama3.1:70b     (40GB)
    - ollama run qwen2.5:32b      (20GB)
    - ollama run mistral-small   (13GB)
<!-- Total 120 GB -->

#### api models ()
* "GOOGLE (gemini-1.5-flash)": "gemini-1.5-flash"
* "NVIDIA (nvidia/nemotron-4-340b-instruct)": "nvidia/nemotron-4-340b-instruct"

How to create api key for google gemini ?
https://ai.google.dev/gemini-api/docs/api-key


How to create api key for nvidia/nemotron ?
https://docs.nvidia.com/nim/large-language-models/latest/getting-started.html




### firebase admin
https://firebase.google.com/docs/reference/admin/python
