from sensor.configuration.mongo_db_connection import MongoDBClient
from sensor.constant import training_pipeline
from sensor.exception import SensorException
import os , sys
from sensor.logger import logging
#from  sensor.utils import dump_csv_file_to_mongodb_collecton
#from sensor.entity.config_entity  import TrainingPipelineConfig,DataIngestionConfig

from sensor.pipeline.training_pipeline import TrainPipeline
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

from fastapi import FastAPI
from sensor.constant.application import APP_HOST, APP_PORT
from starlette.responses import RedirectResponse
from uvicorn import run as app_run
from sensor.ml.model.estimator import ModelResolver, TargetValueMapping
from sensor.utils.main_utils import load_object
from fastapi.middleware.cors import CORSMiddleware
import os
from fastapi import FastAPI, File, UploadFile, Response
import pandas as pd

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins = origins,
    allow_credentials = True,
    allow_methods = ["*"],
    allow_headers = ["*"]
)

@app.get("/", tags=["authentication"])
async def index():
    return RedirectResponse(url = "/docs")

@app.get("/train")
async def train():
        try:
            training_pipeline = TrainPipeline()
            if training_pipeline.is_pipeline_running:
                return Response("Training pipeline is already running")
            training_pipeline.run_pipeline()
            return Response("Training Successfully Completed")
        except Exception as e:
             return Response(f"error occured {e}")

@app.get("/predict")
async def predict():
     # get data from the csv file
     # convert it into dataframe
    try:
        df = pd.read_csv("input_file.csv")

        # ✅ Drop label column if present
        if "class" in df.columns:
            df = df.drop(columns=["class"])

        model_resolver = ModelResolver(model_dir=training_pipeline.SAVED_MODEL_DIR)
        if not model_resolver.is_model_exists():
              return Response("Model is not available")
        
        best_model_path = model_resolver.get_bast_model_path()
        model = load_object(file_path=best_model_path)
        y_pred = model.predict(df)
        df["predicted_column"] = y_pred
        df["predicted_column"] = df["predicted_column"].replace(TargetValueMapping().reverse_mapping())


        result = df.replace({float('nan'): None, float('inf'): None, float('-inf'): None})
        return {"status": "success", "predictions": result.to_dict(orient="records")}



    except Exception as e:
         raise SensorException(e, sys)
    


def main():
    try:
        training_pipeline = TrainPipeline()
        training_pipeline.run_pipeline()
    except Exception as e:
        print(e)
        logging.exception(e)



if __name__ == "__main__":

    app_run(app, host=APP_HOST, port=APP_PORT)


