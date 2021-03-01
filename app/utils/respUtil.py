from fastapi import status
from fastapi.responses import JSONResponse,Response

def resp_200(*,message='success',payload=None):
    return JSONResponse(
        status_code=status.HTTP_200_OK,
        content={
            'state':200,
            'message':message,
            'data':payload
        }
    )

def resp_500(*,message='Server Internal Error',payload=None):
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            'state':500,
            'message':message,
            'data':payload
        }
    )

def resp_401(*,message='UnAuthourize',payload=None):
    return JSONResponse(
        status_code=status.HTTP_401_UNAUTHORIZED,
        content={
            'state':401,
            'message':message,
            'data':payload
        }
    )

def resp_404(*,message='Not Found',payload=None):
    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content={
            'state':404,
            'message':message,
            'data':payload
        }
    )