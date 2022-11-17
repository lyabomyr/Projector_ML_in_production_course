import streamlit as st
import pandas as pd
from config import model_file_name
from ml_decision_tree.prepare_data import prepare_data_for_predict, prepare_data_for_train, prepare_alone
from ml_decision_tree.train import grid_train_model
from ml_decision_tree.predictor import model_for_predict
from ml_decision_tree.load_model import model_loader
from ml_decision_tree.cleaner import clean_all

st.title('App model for predict and train')


def train_model():
    uploaded_train_file = st.file_uploader("Choice a train_CSV file", type=["csv"])
    button_property=False
    st.info('upload ur training file and click Start train', icon=None)
    if st.button('start train',type="secondary",disabled=button_property):
        if uploaded_train_file:
            with st.spinner('Training...'):
                st.write('prepare data..')
                train_file = pd.read_csv(uploaded_train_file)
                st.write('train model..')
                train = grid_train_model(prepare_data_for_train(train_file)[0]['x'], prepare_data_for_train(train_file)[0]['y'],
                                        model_file_name)
                st.write('upload model...')
                model_loader('upload', model_file_name)
                clean_all(model_file_name)
                st.write('cleaning  after work ....')
        else:
            st.warning('upload correct train file')
        st.success(f"Complete train and sent model to wandb with model_name : {train}")
        


def batch_pred():
    uploaded_file = st.file_uploader("Put a CSV file", type=["csv"])
    if st.button('start predict'):
        st.info('Please input file for predict (csv without predict column)')
        if uploaded_file:
            st.write("Inputing datafile...")
            input_df = pd.read_csv(uploaded_file)
            model_loader('download', model_file_name)
            st.write('model loading ...')
            output_df = model_for_predict(prepare_data_for_predict(input_df), model_file_name)
            st.write("data prepared")
            input_df['Exited'] = output_df
            result = input_df
            clean_all(model_file_name)
            st.success("Result datafile")
            st.write(result)
            csv = result.to_csv().encode('utf-8')
            st.download_button(
                label="Download predict as CSV",
                data=csv,
                file_name='predict.csv',
                mime='text/csv',
            )

def alone_predict():
    credit_score, geography, gender,age,tenure,balance,num_of_products,has_cr_card, is_active_member, estimated_salary = st.columns(10)
    credit_score = credit_score.text_input("CreditScore")
    geography = geography.text_input("Geography")
    gender = gender.text_input("Gender")
    age = age.text_input("Age")
    tenure = tenure.text_input("Tenure")
    balance = balance.text_input("Balance")
    num_of_products = num_of_products.text_input("NumProd")
    has_cr_card = has_cr_card.text_input("HasCrCard")
    is_active_member = is_active_member.text_input("ActMember")   
    estimated_salary = estimated_salary.text_input("Salary")   
    if st.button('predict'):
        with st.spinner('pedicting'):
            st.write('download model...')
            model_loader('download', model_file_name)
            st.write('preparing data and do predict')
            input=[credit_score, geography, gender,age,tenure,balance,num_of_products,has_cr_card, is_active_member, estimated_salary]
            output_df = model_for_predict(prepare_alone(input), model_file_name)
            st.success('Done')
            if output_df.iloc[0, 0] == 1:
                st.warning('this user will exit')
            if output_df.iloc[0, 0] == 0:
                st.info('this user is will not exit')




def main():
    tab1, tab2, tab3 = st.tabs(["Train model on data", "Predict batch data", "Predict per user"])

    with tab1:
        st.header("Train model on data")
        st.image("https://uxwing.com/wp-content/themes/uxwing/download/education-school/training-icon.png", width=200)
        train_model()

    with tab2:
        st.header("Predict batch data")
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/3/3c/Predict_Logo.jpg/250px-Predict_Logo.jpg", width=200)

        batch_pred()

    with tab3:
        st.header("Predict per user")
        st.image("https://w7.pngwing.com/pngs/470/597/png-transparent-predictive-analytics-prediction-business-forecasting-others-face-weather-forecasting-head.png", width=200)
        alone_predict()


if __name__ == "__main__":
    main()