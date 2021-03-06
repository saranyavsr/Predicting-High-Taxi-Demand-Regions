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
	nycmodel = pd.read_csv("allfinal.csv")

	print("loaded dataset")

	# nycmodel=nycmodel.groupby(['Month', 'Day', 'Hour', 'Weekday', 'Zipcode']).size().reset_index(name='count')

	# print("grouped the dataset")

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
    unique_zips =[7030,  7605, 10001, 10002, 10003, 10004, 10005, 10006, 10007,
       10009, 10010, 10011, 10012, 10013, 10014, 10016, 10017, 10019,
       10020, 10021, 10022, 10023, 10024, 10025, 10026, 10027, 10028,
       10029, 10030, 10031, 10032, 10033, 10034, 10035, 10036, 10037,
       10038, 10039, 10040, 10044, 10065, 10069, 10075, 10111, 10115,
       10119, 10128, 10154, 10165, 10167, 10170, 10173, 10174, 10199,
       10278, 10314, 10451, 10452, 10453, 10454, 10455, 10456, 10457,
       10458, 10459, 10460, 10461, 10462, 10463, 10465, 10466, 10467,
       10468, 10469, 10470, 10472, 10473, 10475, 10705, 10708, 11101,
       11102, 11103, 11104, 11105, 11106, 11109, 11201, 11203, 11204,
       11205, 11206, 11209, 11210, 11211, 11213, 11214, 11215, 11216,
       11217, 11218, 11219, 11220, 11221, 11222, 11223, 11224, 11225,
       11226, 11230, 11231, 11232, 11233, 11234, 11235, 11237, 11238,
       11351, 11354, 11355, 11357, 11358, 11360, 11361, 11366, 11367,
       11368, 11369, 11370, 11371, 11372, 11373, 11374, 11375, 11377,
       11378, 11379, 11385, 11411, 11412, 11413, 11415, 11416, 11417,
       11418, 11419, 11420, 11421, 11422, 11423, 11427, 11432, 11433,
       11434, 11435, 11436,  7024,  7201,  7310,  7631, 10018, 10103,
       10112, 10168, 10280, 10471, 10474, 10701, 10704, 11004, 11207,
       11208, 11212, 11228, 11229, 11236, 11239, 11364, 11365, 11429,
       11590, 11692,  7307,  7458, 10282, 10301, 10305, 10550, 10703,
       10801, 11005, 11356, 11359, 11414, 11428, 11430, 11558, 11559,
       10306, 11001, 11021, 11362, 11426, 11580,  7002,  7010, 10303,
       10502, 10803, 11003, 11042, 11581, 11596, 11694,  7302,  7650,
        7666, 10310, 10311, 10464, 10552, 10805, 11024, 11552, 11691,
       11742,  7105,  7114, 10302, 10601,  7093, 10804, 11363, 11697,
       11040, 10553,  7306, 11756, 11010, 11030,  7670,  7632, 10304,
       11020, 10522, 11553, 10710,  7208, 11023, 10309, 10606, 11554,
        6831, 11516, 10308, 10594, 10977, 11570,  7660,  7036,  7608,
       11563, 11575, 11803,  7604, 11514,  7601,  7643, 11548, 11788,
       11520, 11753, 11797, 10543,  7020, 11050, 11545, 11771,  7657,
        6901, 11798, 11576, 10573,  2903,  7305, 10312,  7205,  7087,
        7606, 10709, 10538,  7103,  7018, 11752,  7206, 11598, 10523,
       11577, 11724, 11743,  7094, 11729, 11550,  7086,  7603,  7070,
       11096, 11565, 11804, 11542,  8859, 10707, 10706,  7621, 10532,
       11704, 10520, 11530, 10577, 11801, 11961,  7423, 11706,  7006,
        7927,  7626, 11507, 11509, 10570, 10530,  7304,  7647, 10591,
        7032,  7050,  7047,  7075, 10931, 10528, 11501, 11693, 11579,
       11557,  7072,  7607, 11762,  7642,  7041, 11703,  7676,  8901,
       11768, 11717,  7078,  7081, 11518,  7055,  7630, 11747,  7102,
       10983, 10980, 11791, 11793,  7001, 10580,  8861,  7663, 11709,
       10562, 11746, 11561, 10506, 11735, 11901,  8512, 11757,  7042,
        6473, 11758,  7950,  6825,  6878,  6902,  6906,  6907,  6854,
       10533, 10960, 10941,  7432, 10952,  7202,  7701,  6890,  7662,
        7052, 12542,  7104,  6606, 10989, 11566,  7656,  7640,  7661,
        8105,  6604,  7107, 11776, 10583, 11710,  8880, 10605,  7017,
        7014,  7444,  7644,  7022,  7046, 11787,  7452,  7026,  7029,
       11741,  7652,  7054, 11790, 11714, 11796,  7073, 11763,  7009,
        7112, 11568,  7401, 10510, 10603, 11556, 11725, 10962, 11572,
       11967, 11510, 10307, 10930,  6820,  7960,  7011,  6360, 11718,
        7003,  6460,  7064,  7501,  8542, 18202,  7012,  7410,  8648,
        7090, 11779,  7981, 10607,  8863,  7502,  7203, 10994, 11751,
        8734,  7512,  7071,  6335,  7407, 18102,  6830,  6477,  8850,
        7008,  8406,  6510, 11769, 11726,  7524, 12550, 19142,  7508,
        6897,  7504,  7503, 11721, 11783, 10917,  7039,  7108,  7079,
        8830,  6704,  7505,  8401,  8840, 18103,  7111,  7043, 19141,
       11740,  7106, 11722, 18661, 10964,  7722,  7901,  6880,  7677,
        8750, 10920,  7450,  7470,  7013, 10976, 11702,  6853, 10950,
       10504,  8823,  7040, 10970,  6811, 10956, 10507, 18930,  7495,
        6851, 19601,  7747,  7109,  7065, 10566, 10549,  7721, 10595,
        7095,  7074, 12534,  7062,  8817,  7446, 11749, 11767, 11754,
       19136,  7027, 18017, 11701,  6757,  7077, 12792,  7430,  7712,
        7311,  8832,  7885,  7935, 10604, 10913,  7028, 11715,  6903,
        7627, 11720,  8837,  8807,  7649, 10514, 95110,  7083, 19125,
        8514, 11560, 11950, 10511, 11732,  7522,  7080, 12151, 12540,
       24328, 12533,  8003, 12528,  7031,  7733,  8742,  2907,  8620,
       10509,  6032,  7514,  8812,  6605, 10536, 32137, 32164,  7738,
        7513,  7044, 11941,  7088,  7204, 11795, 11738,  7016, 19147,
        1521, 11948, 10954,  7628, 12508,  7641, 10527,  7110,  8610,
        8536, 19373,  7920,  8724,  8869, 10990, 10992,  8609,  7974,
       11944, 11937,  2126, 10973, 11731, 19020, 11716,  7060, 21229,
       11940,  2908, 11755,  7004,  7825,  6870,  7921,  7646,  7932,
        7740, 19406,  6403,  8201, 12442,  7928,  6905, 12601, 11782,
        7832, 11942,  8078, 11978, 22311, 17402,  7758, 10578, 11968,
       11954,  7728,  7405, 18302,  7645, 19713, 11733,  8904,  7648,
       11772,  7624, 12524, 12531,  6607,  6451,  8852,  8820, 10965,
       12110, 11980,  8550, 12207, 12205, 10535,  7021, 19090,  6043,
       20166,  6840, 12563, 10993,  6481, 12414, 48184,  7035,  2895,
       10516, 11778,  8831,  8854,  7424,  8054, 11933, 27616, 12768,
       10923,  7069,  7940,  6786,  6779,  6787,  1524,  1082,  6067,
       11976, 19149,  7457, 19109, 45203,  7066, 11949, 19107,  8629,
       10968,  7724, 10921, 22401,  7924, 11784, 19111,  6339, 12520,
       18635, 10598, 18104,  7939,  8012, 11946, 10928,  7506, 10996,
        7730,  6516,  7851,  8701,  8048, 19446,  6883,  7748,  7442,
       19522,  7045,  7092,  7068,  7702,  7417, 18460,  6498,  6357,
        6379,  2886, 12577,  8882,  6461,  7023,  7057,  6371,  6850,
       19104,  6450,  6475, 11713,  7726,  7711,  6801, 10505, 11786,
        7719, 12015,  7753, 22015,  7033, 11765, 11951, 19148,  1062,
        8033, 10567, 20005, 20006, 20037,  7481, 20004,  7005,  6103,
        7731, 10924,  8835, 10526, 10927,  7936,  6614,  7403, 10541,
        7871, 11789, 10597, 19153, 85034,  8857, 12561, 89103, 89119,
       12477, 18015, 18372,  1843, 11727, 11780,  8733,  8520, 18512,
       18321, 18509, 10974, 10975, 14212, 19116,  8902,  7834, 48126,
        8628, 17046,  2467, 48212,  8036,  8518,  7847,  6042,  6519,
       10501, 19507, 19120,  2119,  2118, 12204, 12077,  8879,  7756,
       18706,  7746, 12210,  7463,  7822,  8103, 10546, 13032]
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
