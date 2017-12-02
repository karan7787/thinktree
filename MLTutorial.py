import urllib3, requests, json, os
from flask import Flask, render_template, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, FloatField, IntegerField
from wtforms.validators import Required, Length, NumberRange
url = 'https://ibm-watson-ml.mybluemix.net'
username = 'c1ef4b80-2ee2-458e-ab92-e9ca97ec657d'
password = '030528d4-5a3e-4d4c-9258-5d553513be6f'
scoring_endpoint = 'https://ibm-watson-ml.mybluemix.net/v3/wml_instances/219bfaf6-37c6-43cb-a362-a3d87c1c9d12/published_models/66e8b1c4-419e-4282-a66b-36ccada64d32/deployments/dea20870-a7cc-4425-bab5-e9caf31abd8e/online'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secretpassw0rd'
bootstrap = Bootstrap(app)
class TentForm(FlaskForm):
  DATE = Stringfield('DATE OF JOURNEY')
  DISTANCE = FloatField('DISTANCE')
  DRIVER = RadioField('Nature of driver', coerce=str, choices=[('active','active'),('lazy','lazy'),('active','active')])
  matric_tone = FloatField('MATRIC TONE')
  cost_per_tone = FloatField('COST PER TONE')
  no_of_travellers = IntegerField('NO OF TRAVELLERS')

  submit = SubmitField('Submit')
@app.route('/', methods=['GET', 'POST'])
def index():
  form = TentForm()
  if form.validate_on_submit():
    DATE = form.DATE.data
    form.DATE.data = ''
    DISTANCE = form.DISTANCE.data
    form.DISTANCE.data = ''
    DRIVER = form.DRIVER.data
    form.DRIVER.data = ''
    matric_tone = form.matric_tone.data
    form.matric_tone.data = ''
    cost_per_tone = form.cost_per_tone.data
    form.cost_per_tone.data = ''
    no_of_travellers = form.no_of_travellers.data
    form.no_of_travellers.data = ''
    headers = urllib3.util.make_headers(basic_auth='{}:{}'.format(username, password))
    path = '{}/v3/identity/token'.format(url)
    response = requests.get(path, headers=headers)
    mltoken = json.loads(response.text).get('token')
    scoring_header = {'Content-Type': 'application/json', 'Authorization': mltoken}
    payload = {"fields": ["DATE", "DISTANCE", "DRIVER", "tranport type", "matric tone", "cost per tone", "No. Of travellers"], "values": [["01-01-2017",1166.17,"active","carriage",2,12,0]]}
    scoring = requests.post(scoring_endpoint, json=payload, headers=scoring_header)
    return render_template('score.html', form=form, scoring=scoring)
  return render_template('index.html', form=form)
port = os.getenv('PORT', '5000')
if __name__ == "__main__":
  app.run(host='0.0.0.0', port=int(port))