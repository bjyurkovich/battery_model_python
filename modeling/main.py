import tensorflow as tf
import numpy as np

# Load in the data
training_set = tf.contrib.learn.datasets.base.load_csv_without_header(
    filename='./data/training.csv', features_dtype=np.float32, target_dtype=np.float32, target_column=2)

test_set = tf.contrib.learn.datasets.base.load_csv_without_header(
    filename='./data/test.csv', features_dtype=np.float32, target_dtype=np.float32, target_column=2)

# Set your Features
feature_columns = [tf.contrib.layers.real_valued_column("", dimension=2)]
classifier = tf.contrib.learn.DNNClassifier(feature_columns=feature_columns,
                                            hidden_units=[10, 20],
                                            n_classes=2,
                                            model_dir="./battery_model")

# Fit model
classifier.fit(x=training_set.data, y=training_set.target, steps=2000)

# Or this is equivalent:
# classifier.fit(x=training_set.data, y=training_set.target, steps=1000)
# classifier.fit(x=training_set.data, y=training_set.target, steps=1000)

# Not enough data, so a really bad accuracy rating!!
accuracy_score = classifier.evaluate(
    x=training_set.data, y=training_set.target)["accuracy"]
print('Accuracy: {0:f}'.format(accuracy_score))

# An extremely poor prediction because there is not enough data, and the #
# of nodes is not optimized
samples = np.array([[-2., 0.55]], dtype=np.float)
y = classifier.predict(samples)
print('Predictions: {}'.format(list(y)))
