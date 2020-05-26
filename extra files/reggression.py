import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report

features = pd.read_csv('features/SongFeatures.csv')
features = features.drop(columns=['Tracks', 'Artist', 'type', 'id', 'uri', 'track_href', 'analysis_url'])
x_train, x_test, y_train, y_test = train_test_split(features.drop('Success', axis = 1), features['Success'], test_size=0.30, random_state=0)
x_train.fillna(x_train.mean())
logmodel = LogisticRegression()

for i in range(506060):
    print(x_train)
    logmodel.fit(x_train.iloc[i],y_train.iloc[i])
logmodel.fit(x_train.iloc[500000:], y_train.iloc[500000:])

predictions = logmodel.predict(x_test)
print(classification_report(y_test,predictions))
