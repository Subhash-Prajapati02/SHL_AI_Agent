import os

from fastapi import (
    FastAPI,
    UploadFile,
    File
)

from fastapi.responses import (
    FileResponse
)

from fastapi.staticfiles import (
    StaticFiles
)

from pydantic import BaseModel

from typing import List

from agent.shl_agent import SHLAgent

app = FastAPI()

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)


agent = None

def get_agent():

    global agent

    if agent is None:

        print(
            "Loading SHL Agent..."
        )

        agent = SHLAgent()

        print(
            "SHL Agent Ready"
        )

    return agent

class Message(BaseModel):

    role: str
    content: str


class ChatRequest(BaseModel):

    messages: List[Message]


class QueryRequest(BaseModel):

    question: str

from fastapi.responses import FileResponse
import os

from fastapi.responses import HTMLResponse

@app.get("/", response_class=HTMLResponse)
def home():

    with open(
        "templates/index.html",
        "r",
        encoding="utf-8"
    ) as f:

        return f.read()

@app.get("/health")

def health():

    return {
        "status": "ok"
    }

@app.post("/chat")

def chat(request: ChatRequest):

    full_conversation = ""

    for message in request.messages:

        full_conversation += (
            message.content + " "
        )

    result = get_agent().ask(
        full_conversation
    )

    end = False

    if len(
        result["recommendations"]
    ) > 0:

        end = True

    return {

        "reply":
            result["reply"],

        "recommendations":
            result["recommendations"],

        "end_of_conversation":
            end
    }


@app.post("/ask")

def ask(req: QueryRequest):

    result = get_agent().ask(
        req.question
    )

    return {

        "answer":
            result["reply"]
    }

@app.post("/upload")

async def upload(

    file: UploadFile = File(...)
):

    os.makedirs(
        "pdf",
        exist_ok=True
    )

    file_path = os.path.join(
        "pdf",
        file.filename
    )

    with open(file_path, "wb") as f:

        f.write(await file.read())

    return {

        "message":
            f"{file.filename} uploaded successfully"
    }