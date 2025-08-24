from flask import Flask, request, jsonify, render_template
import pandas as pd
import pickle
import os
from flask_restx import Api,Resource,fields

app = Flask(__name__)

api=Api(app,title="FLASK API DOCUMENTATION",description="Test your APIs here",doc="/docs")


# namespace
hello_ns=api.namespace('Hello',description='Hello apis',path='/hello')
user_ns=api.namespace('user',description='CURD USER',path='/user')
pred_ns=api.namespace('Prediction',description='predection opn',path='/predict')


#create class
@hello_ns.route('/')
class hello(Resource):
    def get(self):
        return {'hello world!'}

# crud opn for user 
@user_ns.route('/')
class user(Resource):
    def get(self):
        pass
    def post(self):
        pass
    def put(self):
        pass
    def delete(self):
        pass


input_model=pred_ns.model("predection input",{

                "gestation":fields.List(fields.Float,required=True) ,
                "parity": fields.List(fields.Float,required=True),
                "age": fields.List(fields.Float,required=True),
                "height": fields.List(fields.Float,required=True),
                "weight": fields.List(fields.Float,required=True),
                "smoke":fields.List(fields.Float,required=True) 
                    })










@pred_ns.route('/')
class Predection(Resource):
    @pred_ns.expect(input_model)
    def post(self):


        """
            Predicts the baby's birth weight based on input parameters.

            **Request Body Format:**
            - `gestation` (List[int]): Number of gestation days
            - `parity` (List[int]): Parity value
            - `age` (List[int]): Mother's age
            - `height` (List[int]): Mother's height
            - `weight` (List[int]): Mother's weight
            - `smoke` (List[int]): Smoking status (0 or 1)

            **Returns:**
            - JSON response containing predicted outcome as a float.
        """
        baby_data_form = request.get_json()

        baby_df = pd.DataFrame(baby_data_form)
        baby_df=baby_df[EXPECTED_COLUMS]

        path= os.path.join(os.path.dirname(__file__),"model.pkl")
        with open(path, 'rb') as obj:
            model = pickle.load(obj)
        
        # make prediciton on user data
        prediction = model.predict(baby_df)
        prediction = round(float(prediction), 2)

    # return reponse in a json format
        response = {"Prediction":prediction}

    # return render_template("index.html", prediction=prediction)
        return response



EXPECTED_COLUMS=["gestation","parity","age","height","weight","smoke"]

def get_cleaned_data(form_data):
    gestation = float(form_data['gestation'])
    parity = int(form_data['parity'])
    age = float(form_data['age'])
    height = float(form_data['height'])
    weight = float(form_data['weight'])
    smoke = float(form_data['smoke'])

    cleaned_data = {"gestation":[gestation],
                    "parity":[parity],
                    "age":[age],
                    "height":[height],
                    "weight":[weight],
                    "smoke":[smoke]
                    }


    return cleaned_data


@app.route('/', methods=['GET'])
def home():
    return render_template("index.html")




@app.route('/hello',methods=['GET'])
def hello():
    return {'hello world!'}








## define your endpoint
@app.route("/predict", methods = ['POST'])
def get_prediction():
    # get data from user
    # baby_data_form = request.form
    baby_data_form = request.get_json()


    # baby_data_cleaned = get_cleaned_data(baby_data_form)

    # convert into dataframe
    baby_df = pd.DataFrame(baby_data_form)
    baby_df=baby_df[EXPECTED_COLUMS]

    # load machine leanring trained model 
    path= os.path.join(os.path.dirname(__file__),"model.pkl")
    with open(path, 'rb') as obj:
        model = pickle.load(obj)

    # make prediciton on user data
    prediction = model.predict(baby_df)
    prediction = round(float(prediction), 2)

    # return reponse in a json format
    response = {"Prediction":prediction}

    # return render_template("index.html", prediction=prediction)
    return response




if __name__ == '__main__':
    app.run(debug=True)