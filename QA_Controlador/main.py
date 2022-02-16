from farm.data_handler.inputs import Question
from fastapi import FastAPI
from pydantic import BaseModel

from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
import os
from haystack.pipeline import ExtractiveQAPipeline
from haystack.reader.farm import FARMReader
from haystack.retriever.sparse import ElasticsearchRetriever

ELASTIC_SEARCH_HOST = os.environ.get('es_ip', 'localhost')
ELASTIC_SEARCH_PORT = os.environ.get('es_port', 9200)

document_store = ElasticsearchDocumentStore(
    host=ELASTIC_SEARCH_HOST,
    port=ELASTIC_SEARCH_PORT,
    username="", password="",
    index="document"
)

retriever = ElasticsearchRetriever(document_store=document_store)
reader = FARMReader(model_name_or_path="deepset/roberta-base-squad2-covid", use_gpu=False)
# reader = TransformersReader(model="deepset/roberta-base-squad2",tokenizer="deepset/roberta-base-squad2-covid")
# https://huggingface.co/graviraja/covidbert_squad
pipe = ExtractiveQAPipeline(reader, retriever)

app = FastAPI()

# Se toma como entrada una pregunta
class Queobj(BaseModel):
    question: str
    num_answers: int
    num_docs: int


@app.post('/query')
async def query(que_obj: Queobj):
    question = que_obj.question
    k_retriver = que_obj.num_docs
    k_reader = que_obj.num_answers
    prediction = pipe.run(query=question, top_k_retriever=k_retriver, top_k_reader=k_reader)
    return {'answer': prediction}


# python -m uvicorn main:app --host 0.0.0.0 --port 8080
# python -m uvicorn main:app --host 0.0.0.0 --port 8200