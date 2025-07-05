from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from recommend import get_recommendations

app = FastAPI()

# Enable CORS for Streamlit
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # can limit to localhost if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/recommend")
def recommend(district: str, mode: str = "walmart_only"):
    result = get_recommendations(district, mode)
    return result
