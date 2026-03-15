from fastapi import FastAPI,UploadFile,File,Depends
from pypdf import PdfReader
import database
from database import engine,Sessionlocal,notetable
from sqlalchemy.orm import Session
from models import Note
import os
from openai import OpenAI


database.base.metadata.create_all(bind=engine)
app=FastAPI()

def db_get():
    db=Sessionlocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/get")
def greet():
    return "hello"

dt=""
@app.post("/upload")
async def uploadfile(file:UploadFile=File(...),db:Session=Depends(db_get)):
    text=""
    global dt
    pdf=PdfReader(file.file)
    for p in pdf.pages:
        text+=p.extract_text()
    dt=text
    dbtext=notetable(content=dt)
    db.add(dbtext)
    db.commit()

    return {"Succesfully added to database"}

# @app.get("/ask/{id}")
# def askquestion(id:int,question:str,db:Session=Depends(db_get)):
#     newtext=db.query(notetable).filter(notetable.id==id).first()
    
#     if question.lower() in newtext.content:
#         return{"answer may exist"}
#     return{"answer is not present"}



client = OpenAI(
    api_key=os.environ["GROQ_API_KEY"],
    base_url="https://api.groq.com/openai/v1"
)

@app.get("/aiask/{id}")
def ai_question(id: int, question: str, db: Session = Depends(db_get)):

    doc = db.query(notetable).filter(notetable.id == id).first()
    if not doc:
        return {"error": "Document not found"}

    content = doc.content

    prompt = f"""
        Use the following document to answer the question.

        Document:
        {content[:1500]}

        Question:
        {question}
        """

    response = client.chat.completions.create(
    model="llama-3.1-8b-instant",
    messages=[
        {"role": "system", "content": "Answer questions using the provided document."},
        {"role": "user", "content": prompt}
        ]
            )

    answer = response.choices[0].message.content


    return {"answer": answer}

    # content=await file.read()
    # return {"filename ":file.filename}
