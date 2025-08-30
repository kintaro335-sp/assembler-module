import uvicorn
import os
from fastapi import FastAPI, Body, Query
from fastapi.routing import APIRouter
from fastapi.staticfiles import StaticFiles
# machine
from interpreter.parser import parser
from environment import Machine

# interpreter

machine = Machine(mode='WEB')

# fastapi
app = FastAPI()

public_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), "public")

lang_router = APIRouter(prefix="/lang")

@lang_router.post('/compile')
def compile(body: str = Body(media_type='text/plain')):
    global machine
    instructions = []
    code_lines = body.split('\n')
    for code_line in code_lines:
        result = parser.parse(code_line)
        if result != None:
            instructions.append(result)
    machine = Machine(instructions, mode='WEB')

    return { 'message': 'ok' }

@lang_router.post('/execute')
def execute():
    global machine
    machine.execute_instructions()
    return { 'message': 'ok' }

@lang_router.post('/next')
def next():
    global machine
    machine.next_tick()
    return { 'message': 'ok' }

@lang_router.get('/state')
def state():
    global machine
    return machine.get_state()

@lang_router.post('/set_input')
def set_input(module: str = Query(alias='module', regex='[a-z_]+'), value: int = Query(alias='value', regex='[0-9]+')):
    global machine
    machine.set_input_to_module(module, int(value))
    return { 'message': 'ok' }

app.include_router(lang_router)

app.mount("/", StaticFiles(directory=public_path, html=True), name='static')

def run_server():
    uvicorn.run(app=app, host="0.0.0.0", port=5050)

if __name__ == '__main__':
    run_server()
