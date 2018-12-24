import sys
import json
import build_model
import data_helper
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import data_processing

def train_predict():
	"""Train and predict time series data"""

	# Load command line arguments 
	start_time = sys.argv[1]
	end_time = sys.argv[2]
	#filename = sys.argv[1]
	parameter_file = sys.argv[3]
	train_file=pd.DataFrame()
	train_file=data_processing.data_preprocessing(start_time,end_time)
	train_file.to_csv('out_temp1.csv' , index =False)
	x='out_temp1.csv'

	# Load training parameters
	params = json.loads(open(parameter_file).read())

	# Load time series dataset, and split it into train and test
	x_train, y_train, x_test, y_test, x_test_raw, y_test_raw,last_window_raw, last_window = data_helper.load_timeseries(x, params)

	# Build RNN (LSTM) model
	lstm_layer = [1, params['window_size'], params['hidden_unit'], 1]
	model = build_model.rnn_lstm(lstm_layer, params)
	
	# Train RNN (LSTM) model with train set
	model.fit(
		x_train,
		y_train,
		batch_size=params['batch_size'],
		epochs=params['epochs'],
		validation_split=params['validation_split'])

	# Check the model against test set
	predicted = build_model.predict_next_timestamp(model, x_test)        
	predicted_raw = []
	
	for i in range(len(x_test_raw)):
		predicted_raw.append((predicted[i] + 1) * x_test_raw[i][0])

	# Plot graph: predicted VS actual
	#plt.subplot(111)
	#plt.plot(predicted_raw, label='Actual')
	#plt.plot(y_test_raw, label='Predicted')	
	#plt.legend()
	#plt.show()
    #print(predicted_raw.dtype )
	# Predict next time stamp 
	np.savetxt("y_test_raw1.csv",y_test_raw,delimiter=',')
	np.savetxt("predicted_raw1.csv",predicted_raw,delimiter=',')
	data_new =[]
	for i in range(5) :
		next_timestamp = build_model.predict_next_timestamp(model, last_window)
		next_timestamp_raw = (next_timestamp[0] + 1) * last_window_raw[0][i]
		data_new.append(format(next_timestamp))
		print('The next time stamp forecasting is: {}'.format(next_timestamp_raw))
	plt.plot(data_new)
	plt.show()
if __name__ == '__main__':
	# python3 train_predict.py ./data/sales.csv ./training_config.json_
	train_predict()