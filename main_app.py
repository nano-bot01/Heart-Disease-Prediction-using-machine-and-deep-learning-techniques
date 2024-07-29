import numpy as np
import pickle
import streamlit as st
from datetime import date

# loading the saved model

# loaded_model = pickle.load(open("D:/FinalProject/trained_model.pkl", 'rb'))
loaded_model = pickle.load(open('model/trained_model.pkl', 'rb'))


# creating a function for prediction
def heart_prediction(input_data):
    # changing data to numpy array
    input_data_array = np.asarray(input_data, dtype=np.float64)

    # reshape the array as we are predicting for one instance
    input_data_reshaped = input_data_array.reshape(1, -1)

    result = loaded_model.predict(input_data_reshaped)
    print("The prediction is : ", result)

    if result[0] == 1:
        return 1
    else:
        return 0


def main():
    # giving a title
    st.markdown("<h1 style='text-align: center; color: red;'>Heart Disease Prediction Application</h1>",
                unsafe_allow_html=True)
    st.write('\n')
    # User Information
    st.sidebar.markdown("""
    About the data to be filled : 
                
        1. Name
        2. Date Of Birth
        3. Sex
        4. Chest Pain Type (4 Values : 0-3)
        5. Resting Blood Pressure
        6. Serum Cholestoral In Mg/dl
        7. Fasting Blood Sugar > 120 Mg/dl
        8. Exercise Induced Angina
        9. Resting Electrocardiographic Results (values 0,1,2)
        10. Maximum Heart Rate Achieved
        11. Oldpeak = St Depression Induced By Exercise Relative To Rest
        12. The Slope Of The Peak Exercise St Segment
        13. Number Of Major Vessels (0-3) Colored By Flourosopy
        14. Thal: 0 = Normal; 1 = Fixed Defect; 2 = Reversable Defect

        """)

    st.sidebar.markdown("""

    Sample data to fill:  

        52 1 2 172 199 1 1 162 0 0.5 2 0 3	  =>  has Heart Disease """)

    # useful Methods
    def calculateAge(birthDate):
        today = date.today()
        age = today.year - birthDate.year - ((today.month, today.day) < (birthDate.month, birthDate.day))
        return age

    def chestPainType(cPain):
        if cPain == 'Microvascular':
            return 0
        elif cPain == 'Stable':
            return 1
        elif cPain == 'Unstable':
            return 2
        else:
            return 3

    def restEcgSelect(ecg):
        if ecg == 'Resting ECG':
            return 0
        elif ecg == 'Ambulatory ECG':
            return 1
        else:
            return 2

    def slopeSelect(slope):
        if slope == 'Up Sloping':
            return 0
        elif slope == 'Flat':
            return 1
        else:
            return 2

    def thalValue(value):
        if value == 'Normal':
            return 0
        elif value == 'Fixed':
            return 1
        else:
            return 2

    # getting the input data from input user

    name = st.text_input('Full Name')

    age = calculateAge(st.date_input('D. O. B.', value=date.today(),
                                     min_value=date(date.today().year - 100, date.today().month, date.today().day)))

    sex = st.radio("SEX", ['Male', 'Female'], horizontal=True)
    if sex == 'Male':
        sex = 1
    else:
        sex = 0

    cp = chestPainType(st.select_slider("Chest pain type : ", ['Microvascular', 'Stable', 'Unstable', 'Variant']))

    restbps = st.text_input("Resting BP : ")

    chol = st.text_input("Serum Cholesterol (mg/dl) : ")

    fbs = st.checkbox("Fasting blood sugar > 120 mg/dl : ")
    if fbs:
        fbs = 1
    else:
        fbs = 0

    exang = st.checkbox("Exercise induced angina : ")
    if exang:
        exang = 1
    else:
        exang = 0

    # restecg = restEcgSelect(
    #     st.selectbox("Resting Electrocardiograph Result  : ", ['Resting ECG', 'Ambulatory ECG', 'Exercise Stress test'], index=None,
    #                  placeholder="Select rest ecg type"))

    restecg = restEcgSelect(
    st.selectbox("Resting Electrocardiograph Result  : ", ['Resting ECG', 'Ambulatory ECG', 'Exercise Stress test'],
                 index=0, placeholder="Select rest ecg type"))

    
    thalach = st.text_input("Maximum heart rate achieved : ")

    oldpeak = st.number_input("Old peak : ")

    slope = slopeSelect(
        st.selectbox("Slope of the peak exercise ST segment : ", ['Up Sloping', 'Flat', 'Down Sloping'], index=None,
                     placeholder="Select slope type"))

    ca = st.number_input("Number of major vessels (0-3) : ", min_value=1, max_value=4) - 1

    thal = thalValue(st.selectbox('Thal Value : ', ['Normal', 'Fixed', 'Reversible'], index=None,
                                  placeholder="Select thal type"))


    # performing diagnosis

    if st.button('Diagnosis Test Result'):
        report = heart_prediction(
            [float(age), float(sex), float(cp), float(restbps), float(chol), float(fbs), float(restecg), float(thalach),
             float(exang), float(oldpeak), float(slope), float(ca), float(thal)])
        if report:
            st.error(name + ' has heart disease')
        else:
            st.success(name + ' has no heart disease')

    st.write('\n\n')
    st.write("\n© 2024 Heart Disease Prediction System. All rights reserved.")


if __name__ == '__main__':
    main()
