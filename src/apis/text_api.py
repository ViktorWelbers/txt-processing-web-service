from fastapi import APIRouter, File, UploadFile, Request,HTTPException
from fastapi.responses import Response, PlainTextResponse
from src.controllers.textfile_controller import random_line_controller,multiple_line_controller
from src.controllers.util.file_util import gen_file
from uuid import uuid4, UUID
from src.models.textline_models import TwentyLongestLines, LongestHundredLines

""" API for text manipulation """

router = APIRouter()

@router.post("/file", status_code=201, response_class=PlainTextResponse)
async def create_file(file: UploadFile = File(None, description="")) -> UUID:
    """Upload a text file and store it."""
    if file is None:
        raise HTTPException(status_code=400, detail="No File was selected for Upload")
    if file.content_type != 'text/plain':
        raise HTTPException(status_code=400, detail="File needs to have a .txt extension")
    uuid = uuid4()
    with open(gen_file(uuid,file), "wb") as f:
        f.write(file.file.read())
    return uuid


@router.get("/onerandomline", responses={
    200: {
        "content": {"text/plain": {}, "application/json": {}, "application/xml": {}, "application/*": {}},
    }
})
async def one_random_line(request: Request):
    """ Return one random line of a previously uploaded file via http as text/plain, application/json or application/xml depending on the request accept header. All three headers must be supported.

        If the request is application/* please include following details in the response:

        line number
        file name
        the letter which occurs most often in this line
    """
    accept = request.headers.get('accept')
    return Response(content= random_line_controller.one_random_line_logic(accept=accept), media_type=accept)



@router.get("/backwardsline", responses={
    200: {
        "content": {"text/plain": {}, "application/json": {}, "application/xml": {}, "application/*": {}},
    }
})
async def  one_random_line_backwards(request: Request):
    """Return the requested line backwards"""
    accept = request.headers.get('accept')
    return Response(content= random_line_controller.one_random_line_logic(accept=accept, backwards=True), media_type=accept)


@router.get("/hundredlongest", response_model= LongestHundredLines)
async def longest_hundred_lines() -> LongestHundredLines:
    """ Return the 100 longest lines of all files uploaded """
    return multiple_line_controller.longest_hundred_lines()


@router.get("/twenty_longest", response_model= TwentyLongestLines)
async def twenty_longest_lines_of_one_file() -> TwentyLongestLines:
    """ Return the 20 longest lines of one file uploaded """
    return multiple_line_controller.twenty_longest_one_file()
