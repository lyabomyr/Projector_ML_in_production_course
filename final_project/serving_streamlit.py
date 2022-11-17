import streamlit as st
import pandas as pd
from config import model_file_name
from ml_decision_tree.prepare_data import prepare_data_for_predict, prepare_data_for_train
from ml_decision_tree.train import grid_train_model
from ml_decision_tree.predictor import model_for_predict
from ml_decision_tree.load_model import model_loader
from ml_decision_tree.cleaner import clean_all

st.title('App model for predict and train')


def train_model():
    uploaded_train_file = st.file_uploader("Choice a train_CSV file", type=["csv"])
    st.info('Just upload ur training file and upload will started', icon=None)

    if uploaded_train_file:
        train_file = pd.read_csv(uploaded_train_file)
        train = grid_train_model(prepare_data_for_train(train_file)[0]['x'], prepare_data_for_train(train_file)[0]['y'],
                                 model_file_name)
        model_loader('upload', model_file_name)
        clean_all(model_file_name)
        st.write(f"Complete train and sent to wandb with model_name : {train}")


def batch_pred():
    uploaded_file = st.file_uploader("Put a CSV file", type=["csv"])
    if st.button('start predict'):
        st.text('Please input file for predict (csv without predict column)')
        if uploaded_file:
            st.write("Inputing datafile...")
            input_df = pd.read_csv(uploaded_file)
            model_loader('download', model_file_name)
            st.write('model loading ...')
            output_df = model_for_predict(prepare_data_for_predict(input_df), model_file_name)
            input_df['Exited'] = output_df
            result = input_df
            clean_all(model_file_name)
            st.write("Result datafile")
            st.write(result)
            csv = result.to_csv().encode('utf-8')
            st.download_button(
                label="Download predict as CSV",
                data=csv,
                file_name='predict.csv',
                mime='text/csv',
            )


def main():
    tab1, tab2 = st.tabs(["Train model on data", "prediction data"])

    with tab1:
        train_model()

    with tab2:
        batch_pred()


if __name__ == "__main__":
    main()