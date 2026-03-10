from pydantic import BaseModel


class Note(BaseModel):
    ques:str

# class Content(BaseModel):
#     id:int
#     content=dt
#     name:str