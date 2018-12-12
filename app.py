
import Python_Project_1
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def main():
	return render_template('main.html')

@app.route('/forecast', methods=['POST'])
def home():
	if request.method == 'POST':
		bedrooms = request.form.get('bedrooms')
		bathrooms = request.form.get('bathrooms')
		sqft_lot = request.form.get('sqft-lot')
		sqft_basement = request.form.get('sqft-basement')
		floors = request.form.get('floors')
		waterfront = request.form.get('waterfront')
		age = request.form.get('age')
		grade = request.form.get('grade')
		zip_code = request.form.get('zip-code')
		output = Python_Project_1.prediction_model(bedrooms, bathrooms, sqft_lot, sqft_basement, floors, waterfront, age, grade, zip_code)
		return '<title>Housing Price Prediction - Forecast</title><strong>Forecast = {}</strong>'.format(int(round(output)))

if __name__ == '__main__':
	app.run(debug=True)