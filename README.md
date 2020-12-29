# Confusion_matrix_classifier
These scripts will help you generate a confusion matrix to help determine your model performance
Model performance for classification models is usually debatable in terms of which model performance is most relevant, especially when the dataset is imbalanced. The usual model performance measures for evaluating a classification model are accuracy, sensitivity or recall, specificity, precision, KS statistic and Area under the curve (AUC).


Let us understand some model performance measures based on an example of predicting loan default. A loan default dataset is a typical example of an imbalanced dataset where the two classes are Loan default Y and Loan default N. The number of loan defaulters is usually a very small fraction of the total dataset — not more than 7–8%. This provides a classical imbalanced dataset to understand why cost functions are critical is deciding on which model to use.


What is a confusion matrix?
The confusion matrix is a table that contains the output of a binary classifier. Let us look at the confusion matrix of a binary classifier that predicts loan default — 0 indicates that the customer will pay the loan and 1 indicates that the customer will default. The positive class for our further discussions is 1 (a customer who will default).


This is my attempt to implement a confusion matrix to test a supervised file level classifier that I implemented using CNNs.
- This code cannot be replicated exactly and it only provides the bare structure for a confusion matrix.
- The user is expected to use their own csv file and generate the confusion matrix using the original and predicted value 