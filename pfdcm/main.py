str_description = """
    The main module for the service handler/system.

    This essentially creates the fastAPI app and adds
    route handlers.
"""

from    fastapi                 import FastAPI
from    fastapi.middleware.cors import CORSMiddleware
from    base.router             import helloRouter_create
from    routes.dicom            import router   as dicom_router
from    routes.listenerRouter   import router   as listener_router
from    routes.pacsSetupRouter  import router   as pacsSetup_router
from    routes.pacsQRrouter     import router   as pacsQR_router
from    routes.smdbSetupRouter  import router   as smdbSetup_router
from    routes.foobarRouter     import router   as foobar_router
from    os                      import path

import  pfstate
from    pfstate         import  S

with open(path.join(path.dirname(path.abspath(__file__)), 'ABOUT')) as f:
    str_about       = f.read()

with open(path.join(path.dirname(path.abspath(__file__)), 'VERSION')) as f:
    str_version     = f.read().strip()

tags_metadata = [
    {
        "name"          :   "PACS setup services",
        "description"   :
            """
            Configure various external PACS services to use.
            In most cases you will need to configure some valid
            PACS. Usually this will be a PUT to a `PACSobjName`
            endpoint.
            """
    },
    {
        "name"          :   "PACS QR services",
        "description"   :
            """
            Perform PACS Queries and Retrieve operations.
            """
    },
    {
        "name"          :   "pfdcm environmental detail",
        "description"   :
            """
            Pop on in and say hello. You can even ask me about myself!
            """
    },
    {
        "name"          :   "listener subsystem services",
        "description"   :
            """
            Configure internal settings relating to the listener.
            Mostly all that is required is a POST to the `initialize`
            API endpoing.
            """
    },
    {
        "name"          :   "SMDB setup services",
        "description"   :
            """
            Configure resources for pypx -- typically detail about swift
            storage and CUBE itself.
            """
    }
]

app = FastAPI(
    title           = 'pfdcm',
    version         = str_version,
    openapi_tags    = tags_metadata
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        # "http://localhost",
        # "http://localhost:8080",
        "*"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "OPTIONS"],
    allow_headers=["*"],
)

hello_router = helloRouter_create(
    name            = 'pfdcm_hello',
    version         = str_version,
    about           = str_about
)

# app.include_router( foobar_router,
#                     prefix  = '/api/v1')

app.include_router( hello_router,
                    prefix  = '/api/v1')

# app.include_router( dicom_router,
#                     prefix  = '/api/v1')

app.include_router( listener_router,
                    prefix  = '/api/v1')

app.include_router( pacsSetup_router,
                    prefix  = '/api/v1')

app.include_router( pacsQR_router,
                    prefix  = '/api/v1')

app.include_router( smdbSetup_router,
                    prefix  = '/api/v1')
