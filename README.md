# COMP9900 group project

## X-o-Bot: A Generic Dialog Framework for Conversational Agents

This project focuses on the creation of a generic and modular architecture for conversational
agents which is based on three core components:

1. A knowledge extraction/building module (which includes search, ingestion and knowledge representation)
2. A dialog builder (which can leverage on existing APIs and theories about interaction)

This project is 

* A student-tutor support system (extracting all content from a specific course and answering key questions)

## Environment settings

### 1. change directory to the root directory of the project

### 2. recommend to use virtual environment for this chatbot

```bash
virtualenv -p python3 --no-site-packages venv
```

### 3. start this virtual environment (ignore this if not using virtualenv)

```bash
source venv/bin/activate
```

### 4. install modules based on requirements.txt

```bash
pip install -r requirements.txt
```


## Run Chat Part
### run chat_start.sh
This shell includes running python app, using ssh serveo.net to expose local service to the Internet

make sure all the modules in requirements.txt are installed or use virtual environment installed before
```bash
chmod a+x chat_start.sh
./chat_start.sh
```


## Run Server Part
### run server_start.sh
This shell includes adding authentication file for Dialogflow to environment, running server part for web page

make sure all the modules in requirements.txt are installed or use virtual environment installed before
```bash
chmod a+x server_start.sh
./server_start.sh
```




