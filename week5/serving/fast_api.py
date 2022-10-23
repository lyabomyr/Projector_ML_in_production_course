from fastapi import FastAPI, File, UploadFile
from fastapi.responses import StreamingResponse
import pandas as pd
import os
from io import BytesIO, StringIO
from serving.ml_decision_tree_sample.prepare_data import prepare_data_for_train, common_prepare, prepare_data_for_predict
from serving.ml_decision_tree_sample.predictor import model_for_predict
from serving.ml_decision_tree_sample.load_model import model_loader
from serving.ml_decision_tree_sample.train import grid_train_model
from serving.ml_decision_tree_sample.cleaner import clean_all
from serving.config import model_file_name
import uvicorn




def request_csv_to_df(file: UploadFile) -> pd.DataFrame:
    contents = file.file.read()
    buffer = BytesIO(contents)
    df = pd.read_csv(buffer)
    buffer.close()
    file.file.close()
    return df


def return_df_like_csv_file_in_response(df: pd.DataFrame):
    stream = StringIO()
    df.to_csv(stream, index=False)
    response = StreamingResponse(iter([stream.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=predict.csv"
    return response


app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "please add \'/docs\' to ur url and u will be transferred to swagger page with list of request "
                     "example url http://127.0.0.1:8000/docs"}


@app.post("/train_model_and_push_to_wandb/")
async def train_model_and_push_to_wandb(file: UploadFile = File(...)):
    if not file:
        return {"message": "No upload file sent"}
    else:
        df = request_csv_to_df(file)
        train = grid_train_model(prepare_data_for_train(df)[0]['x'], prepare_data_for_train(df)[0]['y'],
                                 model_file_name)
        model_loader('upload', model_file_name)
        clean_all(model_file_name)
        return {"Complete train and sent to wandb with model_name": train}


@app.post("/batch_predict_csv_file/")
async def predict_exel_file(file: UploadFile = File(...)):
    if not file:
        return {"message": "No upload file sent"}
    else:
        input_df = request_csv_to_df(file)
        model_loader('download', model_file_name)
        print(prepare_data_for_predict(input_df))
        print('sddddddddddddddddd',prepare_data_for_predict(input_df).columns)
        output_df = model_for_predict(prepare_data_for_predict(input_df), model_file_name)
        input_df['Exited'] = output_df
        result = input_df
        clean_all(model_file_name)
        return return_df_like_csv_file_in_response(result)


if __name__ == "__main__":
    uvicorn.run("fast_api:app", port=8000, host="0.0.0.0", reload=True)
