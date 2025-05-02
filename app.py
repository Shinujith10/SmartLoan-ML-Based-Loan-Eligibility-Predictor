from flask import Flask, request, render_template
import joblib
import numpy as np

app = Flask(__name__)

model  = joblib.load('model')

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/predict', methods=['GET', 'POST'])
def predict():
    if request.method ==  'POST':
        gender = request.form['gender']
        married = request.form['married']
        dependents = request.form['dependents']
        education = request.form['education']
        employed = request.form['employed']
        credit = float(request.form['credit'])
        area = request.form['area']
        ApplicantIncome = float(request.form['ApplicantIncome'])
        CoapplicantIncome = float(request.form['CoapplicantIncome'])
        LoanAmount = float(request.form['LoanAmount'])
        Loan_Amount_Term = float(request.form['Loan_Amount_Term'])

        # Gender
        male = 1 if gender == "Male" else 0
        
        # Marital Status
        married_yes = 1 if married == "Yes" else 0

        # Dependents
        dependents_1, dependents_2, dependents_3 = 0, 0, 0
        if dependents == '1':
            dependents_1 = 1
        elif dependents == '2':
            dependents_2 = 1
        elif dependents == '3+':
            dependents_3 = 1

        # Education
        not_graduate = 1 if education == "Not Graduate" else 0

        # Employment
        employed_yes = 1 if employed == "Yes" else 0

        # Property Area
        semiurban, urban = 0, 0
        if area == "Semiurban":
            semiurban = 1
        elif area == "Urban":
            urban = 1

        # Safe Log Transformations
        ApplicantIncomelog = np.log(ApplicantIncome + 1)  # Avoid log(0)
        totalincomelog = np.log(ApplicantIncome + CoapplicantIncome + 1)  # Avoid log(0)
        LoanAmountlog = np.log(LoanAmount + 1)  # Avoid log(0)
        Loan_Amount_Termlog = np.log(Loan_Amount_Term + 1)  # Avoid log(0)

        prediction = model.predict([[credit, ApplicantIncomelog, LoanAmountlog, Loan_Amount_Termlog, 
                                     totalincomelog, male, married_yes, dependents_1, dependents_2, 
                                     dependents_3, not_graduate, employed_yes, semiurban, urban]])

        prediction_text = "Congratulations, You are Eligible for loan services" if prediction == "Y" else "Sorry, You are not Eligible to avail loan services"

        return render_template("prediction.html", prediction_text=prediction_text)

    else:
        return render_template("prediction.html")

if __name__ == "__main__":
    app.run(debug=True , host='0.0.0.0')
