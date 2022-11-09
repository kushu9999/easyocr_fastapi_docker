from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
import easyocr
from time import perf_counter
from PIL import Image


app = FastAPI(title="OCR", description="A Darwin Edge Product")

# adding middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


# homeurl
@app.get("/", tags=["Home"])
def index():
    return {"API": "Up & Running 200 OK"}

#OCR
@app.put("/ocr", tags=["OCR"])
async def detectFromImage(file: UploadFile = File(...)):
    time_start = perf_counter()

    # read images or video
    im = Image.open(file.file)
    if im.mode in ("RGBA", "P"): 
        im = im.convert("RGB")
    im.save('out.jpg', 'JPEG', quality=50) 
    IMAGE_PATH = "out.jpg"
    reader = easyocr.Reader(['en'], gpu=True)
    result = reader.readtext(IMAGE_PATH)
    time_stop = perf_counter()
    # print(result[0][1], result[1][1], result[2][1])
    total_time = time_stop-time_start
    return {"Heartrate" : result[0][1], "O2Saturation" : result[1][1], "Thirdvaue" : result[2][1], "time_taken" : f"{total_time} seconds"}