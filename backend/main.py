from fastapi import FastAPI, UploadFile, File, HTTPException, Form
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd
import io
import logging
from models.data_processor import DataProcessor

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI()

# Konfigurasi CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/upload")
async def upload_file(
    before_file: UploadFile = File(...),
    after_file: UploadFile = File(...),
    data_type: str = Form(...)
):
    try:
        if not before_file.filename.endswith('.csv') or not after_file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="Only CSV files are allowed")
        
        # Read files
        before_contents = await before_file.read()
        before_df = pd.read_csv(io.StringIO(before_contents.decode('utf-8')))
        
        after_contents = await after_file.read()
        after_df = pd.read_csv(io.StringIO(after_contents.decode('utf-8')))

        processor = DataProcessor(before_df, after_df, data_type)
        result = {
            "statistics": processor.get_data_stats(),
            "visualizations": processor.generate_plots()
        }
        
        logger.info("Data processed successfully")
        return result

    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 