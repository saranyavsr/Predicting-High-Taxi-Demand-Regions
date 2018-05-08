print("importing")
# from forms import predictForm
from flask import Flask, render_template, request
from flask_script import Manager
import numpy as np
import pandas as pd
import os
from sklearn.ensemble import RandomForestRegressor
from uszipcode import ZipcodeSearchEngine
    
print("imported")

app = Flask(__name__)
app.secret_key = 's3cr3t'
manager = Manager(app)


def createModel():
	os.chdir("/Users/whiplash/SJSU/Semester 2/Github/Predicting-High-Taxi-Demand-Regions/Data")
	nycmodel = pd.read_csv("nycmodeldatajan.csv")

	print("loaded dataset")

	nycmodel=nycmodel.groupby(['Month', 'Day', 'Hour', 'Weekday', 'Zipcode']).size().reset_index(name='count')

	print("grouped the dataset")

	just_dummies = pd.get_dummies(nycmodel['Zipcode'])
	just_dummies1=just_dummies.applymap(np.int)

	print("created dummies")

	step_1 = pd.concat([nycmodel, just_dummies1], axis=1)
	step_1.drop(['Zipcode'], inplace=True, axis=1)
	target=step_1[['count']]
	data=step_1[[col for col in step_1.columns if col not in ['count']]]

	RFR=RandomForestRegressor(max_features=14,n_estimators=300)
	print("Creating model")
	RFR.fit(data, target)
	print("model created")
	app.config['model'] = RFR
	print("Model Created")
    # return vec, reg


@manager.command
def runserver():
    createModel()
    app.run(debug=False)
    app.run(host='0.0.0.0', port=4000, debug=False)


@app.route('/', methods=['GET', 'POST'])
def index():
  # form = predictForm()
  if request.method == 'POST':
    print(request.form)
    RFR = app.config['model']
    unique_zips =  [7030,  7605, 10001, 10002, 10003, 10004, 10005, 10006, 10007,10009, 10010, 10011, 10012, 10013, 10014, 10016, 10017, 10019,10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028,10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037,10038, 10039, 10040, 10044, 10065, 10069, 10075, 10111, 10115,10119, 10128, 10154, 10165, 10167, 10170, 10173, 10174, 10199,10278, 10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457,10458, 10459, 10460, 10461, 10462, 10463, 10465, 10466, 10467,10468, 10469, 10470, 10472, 10473, 10475, 10705, 10708, 11101,11102, 11103, 11104, 11105, 11106, 11109, 11201, 11203, 11204,11205, 11206, 11209, 11210, 11211, 11213, 11214, 11215, 11216,11217, 11218, 11219, 11220, 11221, 11222, 11223, 11224, 11225,11226, 11230, 11231, 11232, 11233, 11234, 11235, 11237, 11238,11351, 11354, 11355, 11357, 11358, 11360, 11361, 11366, 11367,11368, 11369, 11370, 11371, 11372, 11373, 11374, 11375, 11377,11378, 11379, 11385, 11411, 11412, 11413, 11415, 11416, 11417,11418, 11419, 11420, 11421, 11422, 11423, 11427, 11432, 11433,11434, 11435, 11436,  7024,  7201,  7310,  7631, 10018, 10103,10112, 10168, 10280, 10471, 10474, 10701, 10704, 11004, 11207,11208, 11212, 11228, 11229, 11236, 11239, 11364, 11365, 11429,11590, 11692,  7307,  7458, 10282, 10301, 10305, 10550, 10703,10801, 11005, 11356, 11359, 11414, 11428, 11430, 11558, 11559,10306, 11001, 11021, 11362, 11426, 11580,  7002,  7010, 10303,10502, 10803, 11003, 11042, 11581, 11596, 11694,  7302,  7650, 7666, 10310, 10311, 10464, 10552, 10805, 11024, 11552, 11691,11742,  7105,  7114, 10302, 10601,  7093, 10804, 11363, 11697,11040, 10553,  7306, 11756, 11010, 11030,  7670,  7632, 10304,11020, 10522, 11553, 10710,  7208, 11023, 10309, 10606, 11554, 6831, 11516, 10308, 10594, 10977, 11570,  7660,  7036,  7608,11563, 11575, 11803,  7604, 11514,  7601,  7643, 11548, 11788,11520, 11753, 11797, 10543,  7020, 11050, 11545, 11771,  7657, 6901, 11798, 11576, 10573,  2903,  7305, 10312,  7205,  7087, 7606, 10709, 10538,  7103,  7018, 11752,  7206, 11598, 10523,11577, 11724, 11743,  7094, 11729, 11550,  7086,  7603,  7070,11096, 11565, 11804, 11542,  8859, 10707, 10706,  7621, 10532,11704, 10520, 11530, 10577, 11801, 11961,  7423, 11706,  7006, 7927,  7626, 11507, 11509, 10570, 10530,  7304,  7647, 10591, 7032,  7050,  7047,  7075, 10931, 10528, 11501, 11693, 11579,11557,  7072,  7607, 11762,  7642,  7041, 11703,  7676,  8901,11768, 11717,  7078,  7081, 11518,  7055,  7630, 11747,  7102,10983, 10980, 11791, 11793,  7001, 10580,  8861,  7663, 11709,10562, 11746, 11561, 10506, 11735, 11901,  8512, 11757,  7042, 6473, 11758,  7950,  6825,  6878,  6902,  6906,  6907,  6854,10533, 10960, 10941,  7432, 10952,  7202,  7701,  6890,  7662, 7052, 12542,  7104,  6606, 10989, 11566,  7656,  7640,  7661, 8105,  6604,  7107, 11776, 10583, 11710,  8880, 10605,  7017, 7014,  7444,  7644,  7022]
    print("predicting")
    col_names =["Month", "Day", "Hour", "Weekday"]
    col = col_names + unique_zips

    testdummy1 = pd.DataFrame(columns = col)

    testdummy1.loc[0] = [0 for n in range(422)]

    testdummy1["Month"][0] = request.form["month"]
    testdummy1["Day"][0] = request.form["day"]
    testdummy1["Hour"][0] = request.form["hour"]
    testdummy1["Weekday"][0] = request.form["weekday"]
    search = ZipcodeSearchEngine()
    print("finding zip")
    res = search.by_coordinate(float(request.form["lat"]), float(request.form["lon"]), radius=30, returns=1)
    ziptry = res[0]["Zipcode"]
    print(ziptry)
    testdummy1[int(ziptry)][0] = 1
    testing = RFR.predict(testdummy1)

    print ("output is")
    print(testing)
    return str(testing)
    # return render_template('predict.html', count=testing)
    
    
    
  elif request.method == 'GET':
    print("Rendering home page")
    return render_template('home.html')



@app.route('/crime')
def crime():
    return render_template('crime.html')


if __name__ == '__main__':
    manager.run()


