import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.model_selection import train_test_split
from catboost import CatBoostRegressor
import sklearn.metrics as metrics
from datetime import datetime
import numpy as np
from sklearn.model_selection import KFold
import torch
from sqlalchemy import create_engine

# Database connection configuration
db_config = {
    'host': '123.57.92.58',
    'port': 3306,
    'user': '租房数据',
    'password': 'Kingho325',
    'database': '租房数据',
    'charset': 'utf8'
}

# Create a database connection string
db_url = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# Connect to the MySQL database
engine = create_engine(db_url)
query = "SELECT * FROM rental_data_analysis"
data = pd.read_sql(query, engine)

# Print the first few lines of the data box
print(data.head())

# Delete the lines "Please Contact" in Price and "Not Available" in Size(sqft)
data = data[(data['Price'] != 'Please Contact') & (data['Size_sqft'] != 'Not Available')]


# Change the type of Price, Bedroom, Bathroom, Parking Included, Size(sqft) to float64
data['Price'] = data['Price'].replace('[\$,]', '', regex=True).astype(float)
data = data[(data['Bedroom'] != 'Studio')]
data['Bedroom'] = data['Bedroom'].replace('5+', '5').astype(float)
data['Type'] = data['Type'].replace('Apartments', 'Apartment')
data['Bathroom'] = data['Bathroom'].astype(float)
data['Parking_Included'] = data['Parking_Included'].replace('3+', '3').astype(float)
data['Size_sqft'] = data['Size_sqft'].replace('[\$,]', '', regex=True).astype(float)

today = datetime.now()
data['Move_In_Date'] = pd.to_datetime(data['Move_In_Date'], format='%B %d, %Y', errors='coerce')
data['Move_In_Date'] = data['Move_In_Date'].replace('Unknown', today)
# Calculate the number of days from today
data['Move_In_Date'] = (data['Move_In_Date'] - today).dt.days.astype(float)

# Pandas Tools view data
print(data.head())

# Statistics of missing data values
print(data.info())

# descriptive statistical analysis
data_desc = data[
    ['Latitude', 'Longitude', 'Type', 'Bedroom', 'Bathroom', 'Utilities_Included', 'Wi_Fi_and_More', 'Parking_Included', 'Agreement_Type',
     'Move_In_Date','Pet_Friendly', 'Size_sqft', 'Furnished', 'Appliances', 'Air_Conditioning',
     'Personal_Outdoor_Space', 'Smoking_Permitted']]
data_desc.to_excel('data.xlsx', index=False)
print(data_desc.describe())

# Price Feature distribution analysis
plt.rcParams['font.sans-serif'] = ['SimHei']  # Specify default font
plt.rcParams['axes.unicode_minus'] = False  # Fixed an issue where the save image is displayed as a square with the negative sign '-'
data['Price'].value_counts().plot(kind='bar', figsize=[5, 3])
plt.title("Price Feature bar chart")
print(data['Price'].value_counts())
plt.show()

# Size_sqft Feature distribution analysis
plt.rcParams['font.sans-serif'] = ['SimHei']  # Specify default font
plt.rcParams['axes.unicode_minus'] = False  # Fixed an issue where the save image is displayed as a square with the negative sign '-'
data['Size_sqft'].value_counts().plot(kind='bar', figsize=[5, 3])
plt.title("Size_sqft Feature bar chart")
print(data['Size_sqft'].value_counts())
plt.show()

# correlation analysis
df_tmp1 = data[
    ['Price', 'Bedroom', 'Bathroom', 'Parking_Included', 'Size_sqft']]
plt.rcParams['font.sans-serif'] = ['SimHei']  # Specify default font
plt.rcParams['axes.unicode_minus'] = False  # Fixed an issue where the save image is displayed as a square with the negative sign '-'
sns.heatmap(df_tmp1.corr(), cmap="YlGnBu", annot=True)
plt.show()

# The correlation of variables is shown
sns.pairplot(data[['Price', 'Size_sqft']])
plt.show()

# Plot a histogram of the Price variable
plt.hist(x=data['Price'],  # Assigned plot data
         bins=50,  # Specifies the number of bars in the histogram to be 50
         color='steelblue',
         edgecolor='black',  #
         )

plt.title('Price histogram')
plt.xlabel('Price')
plt.ylabel('quantity')
# Show Graph
plt.show()


# Create feature data and label data
X = data[
    ['Latitude', 'Longitude', 'Type', 'Bedroom', 'Bathroom', 'Utilities_Included', 'Wi_Fi_and_More', 'Parking_Included', 'Agreement_Type',
     'Move_In_Date','Pet_Friendly', 'Size_sqft', 'Furnished', 'Appliances', 'Air_Conditioning',
     'Personal_Outdoor_Space', 'Smoking_Permitted']]
y = data['Price']

categorical_features_indices = np.where(X.dtypes != float)[0]

# Define k-fold cross-validation
k_folds = 5
kf = KFold(n_splits=k_folds, shuffle=True, random_state=5)

# Initializes the list to store training and validation loss values for each fold
train_losses = []
val_losses = []

# Initializes the list to store the predictions for each fold
all_y_test = []
all_y_pred = []

# Data set splitting
x_data, x_test, y_data, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Perform K-fold cross-validation
for train_index, test_index in kf.split(x_data):
    X_train, X_val = X.iloc[train_index], X.iloc[test_index]
    y_train, y_val = y.iloc[train_index], y.iloc[test_index]

    model = CatBoostRegressor(iterations=500,  # iterations
                               learning_rate=0.13,  # learning rate
                               depth=11,  # Depth of Tree
                               loss_function='RMSE',  # loss function
                               eval_metric='RMSE',  # evaluation index
                               random_seed=99,  # Seed
                               od_type='Iter',  # Type of overfitting detection
                               od_wait=20,  # The number of iterations that continue after the optimization goal is reached
                               verbose=False)  # Training process information is not displayed

    model.fit(X_train, y_train, eval_set=(X_val, y_val), use_best_model=True, cat_features=categorical_features_indices)

    # Record the loss value for each training cycle
    train_loss = model.evals_result_['learn']['RMSE']
    val_loss = model.evals_result_['validation']['RMSE']
    train_losses.append(train_loss)
    val_losses.append(val_loss)

    # Make predictions on the test set and record the results
    y_pred = model.predict(x_test)
    all_y_test.extend(y_test)
    all_y_pred.extend(y_pred)

# Visual loss value
plt.figure(figsize=(10, 5))
for i in range(k_folds):
    plt.plot(train_losses[i], label=f'Fold {i+1} Train Loss')
    plt.plot(val_losses[i], label=f'Fold {i+1} Validation Loss')

plt.xlabel('Iterations')
plt.ylabel('RMSE')
plt.title('Training and Validation Losses in each Fold')
plt.legend()
plt.show()

# model evaluation
print('Interpretable variance value：{}'.format(round(metrics.explained_variance_score(all_y_test, all_y_pred), 2)))
print('mean absolute error：{}'.format(round(metrics.mean_absolute_error(all_y_test, all_y_pred), 2)))
print('error of mean square：{}'.format(round(metrics.mean_squared_error(all_y_test, all_y_pred), 2)))
print('r-value method：{}'.format(round(metrics.r2_score(all_y_test, all_y_pred), 2)))

# Comparison graph between true value and predicted value
plt.plot(range(len(all_y_test)), all_y_test, color="green", linewidth=1.5, linestyle="-")
plt.plot(range(len(all_y_pred)), all_y_pred, color="red", linewidth=1.5, linestyle="-.")
plt.legend(['true value', 'predicted value'])
plt.title("Comparison graph between true value and predicted value")
plt.show()  # display picture

feature_importance = model.get_feature_importance(type='FeatureImportance')

# Get feature name
feature_names = model.feature_names_

# Visual feature importance
sorted_idx = np.argsort(feature_importance)
plt.figure(figsize=(10, 8))
plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx], align='center')
plt.yticks(range(len(sorted_idx)), np.array(feature_names)[sorted_idx])
plt.xlabel('Feature Importance')
plt.title('CatBoost Feature Importance')
plt.show()

# Conservation of resources model
torch.save(model, "full_model.pt")

# loading model
model_loaded = torch.load("full_model.pt")

# Test whether client input and prediction are possible
def predict_price():
    # Receive user input feature parameters
    # User input feature value

    global latitude, longitude, move_in_date, air_conditioning, personal_outdoor_space, smoking_permitted, utilities_included, wi_fi_and_more, parking_included, agreement_type, pet_friendly, size_sqft, furnished, post_time, Type, bedroom, bathroom, appliances
    try:
        latitude = float(input("Enter Latitude: "))
        longitude = float(input("Enter Longitude: "))
        Type = input(
            "Enter the Type of home ('Apartment' or 'House' or 'Condo' or 'Duplex/Triplex' or 'Basement' or 'Townhouse'): ")
        bedroom = float(input("Enter the number of bedrooms: "))
        bathroom = float(input("Enter the number of bathrooms: "))

        # Question by question
        hydro = input("Is hydro included? (Yes/No): ").capitalize()
        heat = input("Is heat included? (Yes/No): ").capitalize()
        water = input("Is water included? (Yes/No): ").capitalize()
        # Converts user input into a specified format
        utilities_included = ", ".join([f"Yes: {hydro}" if hydro == 'Yes' else "No: Hydro",
                                        f"Yes: {heat}" if heat == 'Yes' else "No: Heat",
                                        f"Yes: {water}" if water == 'Yes' else "No: Water"])

        wi_fi_and_more = input(
            "Enter Wi-Fi and more ('Not included' or 'Internet' or 'Cable / TV, Internet'): ")
        parking_included = int(input("Enter parking included (3+ all imputed as 3, range is 0-3): "))
        agreement_type = input("Enter agreement type ('1 Year' or 'Month-to-month' or 'Not Available'): ")
        pet_friendly = input("Enter pet friendly ('No' or 'Yes' or 'Limited'): ")
        move_in_date = input("Enter the number of days until the delivery date (If you don't know, enter 'NaN'): ")
        size_sqft = float(input("Enter size in square feet: "))
        furnished = input("Enter furnished ('No' or 'Yes'): ")

        laundry_in_unit = input("Is 'Laundry (In Unit)' included? (Yes/No): ").lower()
        laundry_in_building = input("Is 'Laundry (In Building)' included? (Yes/No): ").lower()
        dishwasher = input("Is 'Dishwasher' included? (Yes/No): ").lower()
        # Check the user's input to determine the output string
        if laundry_in_unit == 'yes' and laundry_in_building == 'no' and dishwasher == 'no':
            appliances = 'Laundry (In Unit)'
        elif laundry_in_unit == 'no' and laundry_in_building == 'yes' and dishwasher == 'no':
            appliances = 'Laundry (In Building)'
        elif laundry_in_unit == 'no' and laundry_in_building == 'no' and dishwasher == 'yes':
            appliances = 'Dishwasher'
        elif laundry_in_unit == 'yes' and laundry_in_building == 'yes' and dishwasher == 'no':
            appliances = 'Laundry (In Unit), Laundry (In Building)'
        elif laundry_in_unit == 'yes' and laundry_in_building == 'no' and dishwasher == 'yes':
            appliances = 'Laundry (In Unit), Dishwasher'
        elif laundry_in_unit == 'no' and laundry_in_building == 'yes' and dishwasher == 'yes':
            appliances = 'Laundry (In Building), Dishwasher'
        elif laundry_in_unit == 'yes' and laundry_in_building == 'yes' and dishwasher == 'yes':
            appliances = 'Laundry (In Unit), Laundry (In Building), Dishwasher'
        else:
            appliances = 'Not included'

        air_conditioning = input("Enter air conditioning ('No' or 'Yes'): ")
        personal_outdoor_space = input("Enter personal outdoor space ('Balcony' or 'Yard' or 'Yard Balcony' or 'Not included'): ")
        smoking_permitted = input("Enter smoking permitted ('No' or 'Yes' or 'Outdoors only'): ")
    except ValueError:
        print("The entered data format is incorrect. Please try again.")
        exit()

    # Construct feature vector
    input_data = {
        'Latitude': latitude,
        'Longitude': longitude,
        'Type': Type,
        'Bedroom': bedroom,
        'Bathroom': bathroom,
        'Utilities_Included': utilities_included,
        'Wi_Fi_and_More': wi_fi_and_more,
        'Parking_Included': parking_included,
        'Agreement_Type': agreement_type,
        'Move_In_Date': move_in_date,
        'Pet_Friendly': pet_friendly,
        'Size_sqft': size_sqft,
        'Furnished': furnished,
        'Appliances': appliances,
        'Air_Conditioning': air_conditioning,
        'Personal_Outdoor_Space': personal_outdoor_space,
        'Smoking_Permitted': smoking_permitted
    }

    # Price forecasting
    X = pd.DataFrame(input_data, index=[0])
    predicted_price = model_loaded.predict(X)

    return predicted_price


# Call the function for price prediction
predicted_price = predict_price()
print("Predicted price:", predicted_price)
