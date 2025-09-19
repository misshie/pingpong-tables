import base64
import pickle
import secrets
from typing import Annotated, List, Optional
from lib.encode import *
from lib.evaluation import *
from pydantic import BaseModel
from lib.face_alignment import *
from contextlib import asynccontextmanager
from lib.utils_functions import readb64, encodeb64
from datetime import datetime
from lib.pubcasefinder import query_pubcasefinder

from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.staticfiles import StaticFiles
from starlette.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

import os

security = HTTPBasic()

with open('config.json', 'r') as config_file:
    print(1233445)
    config = json.load(config_file)

USERNAME = config.get('username')
PASSWORD = config.get('password')

def get_current_username(
        credentials: Annotated[HTTPBasicCredentials, Depends(security)]
    ):
    current_username_bytes = credentials.username.encode("utf8")
    correct_username_bytes = USERNAME.encode("utf8")
    is_correct_username = secrets.compare_digest(
        current_username_bytes, correct_username_bytes
    )
    current_password_bytes = credentials.password.encode("utf8")
    correct_password_bytes = PASSWORD.encode("utf8")
    is_correct_password = secrets.compare_digest(
        current_password_bytes, correct_password_bytes
    )
    if not (is_correct_username and is_correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username


@asynccontextmanager
async def lifespan(app: FastAPI):
    global _models
    global _device
    global _cropper_model
    global _gallery_df
    global _images_synds_dict
    global _images_genes_dict
    global _genes_metadata_dict
    global _synds_metadata_dict
    _models = get_models()
    _cropper_model, _device = load_cropper_model()
    # Load synd dict
    with open(os.path.join("data", "image_gene_and_syndrome_metadata_20082024.p"), "rb") as f:
        data = pickle.load(f)
    _images_synds_dict = data["disorder_level_metadata"]
    _images_genes_dict = data["gene_level_metadata"]
    _genes_metadata_dict = data["gene_metadata"]
    _synds_metadata_dict = data["disorder_metadata"]
    _gallery_df = get_gallery_encodings_set(_images_synds_dict)
    yield


app = FastAPI(lifespan=lifespan)

origins = [
    "http://localhost:3000", # Vue.js: npm run dev
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

api_router = APIRouter(prefix="/api")

# --- Pydantic Models for API Requests ---


# Renamed from Img for clarity, used by endpoints that only need an image
class ImageRequest(BaseModel):
    img: str


# model for the predict endpoint, including optional HPO IDs
class PredictRequest(BaseModel):
    img: str
    hpo_ids: Optional[List[str]] = None


@api_router.post("/predict")
async def predict_endpoint(username: Annotated[str, Depends(get_current_username)], request_data: PredictRequest):
    img = readb64(request_data.img)
    hpo_ids = request_data.hpo_ids # Access the optional HPO IDs

    # For verification, print the received HPO IDs
    if hpo_ids:
        print(f"Received HPO IDs: {hpo_ids}")
    else:
        print("No HPO IDs were provided.")

    start_time = time.time()
    timestamp = time.time()

    # Convert the timestamp to a datetime object
    datetime_obj = datetime.fromtimestamp(timestamp)

    # Format the datetime object as a readable string
    formatted_time = datetime_obj.strftime('%Y-%m-%d %H:%M:%S')

    print("Formatted Time:", formatted_time)
    try:
        aligned_img = face_align_crop(_cropper_model, img, _device)
    except Exception as e:
        return {"message": "Face alignment error."}
    align_time = time.time()
    try:
        encoding = encode(_models, 'cpu', aligned_img, False, False)
    except Exception as e:
        return {"message": "Encoding error."}
    encode_time = time.time()
 
    try:
        # Step 1: Run the original GestaltMatcher analysis
        gestaltmatcher_result = predict(encoding,
                                      _gallery_df,
                                      _images_synds_dict,
                                      _images_genes_dict,
                                      _genes_metadata_dict,
                                      _synds_metadata_dict)

        # Step 2: If HPO IDs are provided, query PubCaseFinder
        if hpo_ids:
            pubcasefinder_result = query_pubcasefinder(hpo_ids)

            # Step 3: Combine the results
            final_result = gestaltmatcher_result.copy()
            final_result['pubcasefinder'] = pubcasefinder_result
        else:
            final_result = gestaltmatcher_result

    except Exception as e:
        print(f"Evaluation or combination error: {e}")
        return {"message": "Evaluation error."}
    finished_time = time.time()

    print('Crop: {:.2f}s'.format(align_time-start_time))
    print('Encode: {:.2f}s'.format(encode_time-align_time))
    print('Predict: {:.2f}s'.format(finished_time-encode_time))
    print('Total: {:.2f}s'.format(finished_time-start_time))
    return final_result


@api_router.post("/encode")
async def encode_endpoint(image: ImageRequest):
    img = readb64(image.img)
    aligned_img = face_align_crop(_cropper_model, img, _device)
    return {"encodings": encode(_models, 'cpu', aligned_img).to_dict()}


@api_router.post("/crop")
async def crop_endpoint(image: ImageRequest):
    img = readb64(image.img)
    aligned_img = face_align_crop(_cropper_model, img, _device)
    img_en = cv2.imencode(".png", aligned_img)
    return {"crop": base64.b64encode(img_en[1])}


@api_router.get("/status")
async def status_endpoint():
    return {"status": "running"}


app.include_router(api_router)


# --- Configuration for serving the Vue.js frontend ---


STATIC_DIR = os.path.join(os.path.dirname(__file__), "static")
app.mount("/assets", 
          StaticFiles(directory=os.path.join(STATIC_DIR, "assets"))
          , name="static-assets",
          )
@app.get("/{full_path:path}")
async def serve_vue_app(full_path: str):
    """
    Serve the Vue app's index.html for any path that is not an API endpoint or a static file.
    """
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))


#if __name__ == "__main__":
#    global _models
#    # _models = []
#    #_models = get_models()
#    print(len(_models))
#    uvicorn.run("main:app", port=5000, log_level="info")
