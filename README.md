# MemGPT-obstacle-course
a simple obstacle course for MemGPT to traverse

### How to launch the server (on OSX)
It is ideal that you have an up to date version of python installed (3.11).
It is a good idea to have pip installed as well.

1. ```python -m venv .venv```
2. ```source .venv/bin/activate``` (This is different on windows)
3. ```pip install -r requirements.txt```
4. ```export OPENAI_API_KEY=sk-...``` (This is needed for the bad doctor bot to run on the server)

From the root project directory, run the following command
```uvicorn Backend.main:app --reload```
Please note, the server will also run if you cd into the *Backend* directroy and run the following
```uvicorn main:app --reload```
The --reload argument is not necessary but is nice for development purposes

### Whats the idea?
My fork of MemGPT has support for HTTP GET and POST calls with an optional Bearer token.
The goal of this obstacle course is to have MemGPT login to a server via human direction using a natural language interface.

the /chatbot URL takes in text as a query prompt and returns medical advice via a simple langchain REACT agent that queries WebMD. By default, this agent responds as incorrectly as possible. I am working to find a way to have MemGPT catch these errors and correct itself before responding to the user. This is an area for improvement. 

#### How to make it happen...
While this can be done with gpt-3.5-turbo, better results are achieved with gpt-4.

1. Launch my hacked version of MemGPT: https://github.com/jaquielajoie/MemGPT-hacked
- Note: you need to run MemGPT from the legacy CLI to have access the http_request method.
- I am working to fix this issue
2. Launch the server on http://localhost:8000
3. Give MemGPT-hacked the following prompts:
    ```make an http post request to http://localhost:8000/auth/register/ with a payload of username=abc123 password=abc123```
    ```make an http post request to http://localhost:8000/auth/login/ with a payload of username=abc123 password=abc123```
    ```format the bearer token```
    ```make an http post request to http://localhost:8000/chatbot/ with a payload of text=what is a sprained ankle with the bearer token in the appropriate argument```

In my tests, MemGPT with GPT-4 was able to catch the mistakes made by the bad doctor bot. 
