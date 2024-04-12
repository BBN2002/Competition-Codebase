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

# 数据库连接配置
db_config = {
    'host': '123.57.92.58',
    'port': 3306,
    'user': '租房数据',
    'password': 'Kingho325',
    'database': '租房数据',
    'charset': 'utf8'
}

# 创建数据库连接字符串
db_url = f"mysql+mysqlconnector://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['database']}"

# 连接到MySQL数据库
engine = create_engine(db_url)
query = "SELECT * FROM rental_data_analysis"
data = pd.read_sql(query, engine)

# 打印数据框的前几行
print(data.head())
# 删除Price中为“Please Contact”和Size(sqft)中为“Not Available”的行
data = data[(data['Price'] != 'Please Contact') & (data['Size_sqft'] != 'Not Available')]


# 将Price, Bedroom, Bathroom, Parking Included, Size(sqft)的类型改为float64
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
# 计算日期距今天的天数
data['Move_In_Date'] = (data['Move_In_Date'] - today).dt.days.astype(float)
# 用Pandas工具查看数据
print(data.head())

# 数据缺失值统计
print(data.info())


# 描述性统计分析
data_desc = data[
    ['Latitude', 'Longitude', 'Type', 'Bedroom', 'Bathroom', 'Utilities_Included', 'Wi_Fi_and_More', 'Parking_Included', 'Agreement_Type',
     'Move_In_Date','Pet_Friendly', 'Size_sqft', 'Furnished', 'Appliances', 'Air_Conditioning',
     'Personal_Outdoor_Space', 'Smoking_Permitted']]
data_desc.to_excel('data.xlsx', index=False)
print(data_desc.describe())

# Price特征分布分析
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
data['Price'].value_counts().plot(kind='bar', figsize=[5, 3])
plt.title("Price特征柱状图")
print(data['Price'].value_counts())
plt.show()

# Size_sqft特征分布分析
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
data['Size_sqft'].value_counts().plot(kind='bar', figsize=[5, 3])
plt.title("Size_sqft特征柱状图")
print(data['Size_sqft'].value_counts())
plt.show()

# 相关性分析
df_tmp1 = data[
    ['Price', 'Bedroom', 'Bathroom', 'Parking_Included', 'Size_sqft']]
plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题
sns.heatmap(df_tmp1.corr(), cmap="YlGnBu", annot=True)
plt.show()

# 变量的相关关系展示
sns.pairplot(data[['Price', 'Size_sqft']])
plt.show()

# 绘制Price变量直方图
plt.hist(x=data['Price'],  # 指定绘图数据
         bins=50,  # 指定直方图中条形的数量为50个
         color='steelblue',
         edgecolor='black',  #
         )

plt.title('Price直方图')
plt.xlabel('Price')
plt.ylabel('数量')
# 显示图形
plt.show()


# 建立特征数据和标签数据
X = data[
    ['Latitude', 'Longitude', 'Type', 'Bedroom', 'Bathroom', 'Utilities_Included', 'Wi_Fi_and_More', 'Parking_Included', 'Agreement_Type',
     'Move_In_Date','Pet_Friendly', 'Size_sqft', 'Furnished', 'Appliances', 'Air_Conditioning',
     'Personal_Outdoor_Space', 'Smoking_Permitted']]
y = data['Price']

categorical_features_indices = np.where(X.dtypes != float)[0]

# 定义 k 折交叉验证
k_folds = 5
kf = KFold(n_splits=k_folds, shuffle=True, random_state=5)

# 初始化列表来存储每个折叠的训练和验证损失值
train_losses = []
val_losses = []

# 初始化列表来存储每个折叠的预测结果
all_y_test = []
all_y_pred = []

# 数据集拆分
x_data, x_test, y_data, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 执行 k 折交叉验证
for train_index, test_index in kf.split(x_data):
    X_train, X_val = X.iloc[train_index], X.iloc[test_index]
    y_train, y_val = y.iloc[train_index], y.iloc[test_index]

    model = CatBoostRegressor(iterations=500,  # 迭代次数
                               learning_rate=0.39,  # 学习率
                               depth=8,  # 树的深度
                               loss_function='RMSE',  # 损失函数
                               eval_metric='RMSE',  # 评估指标
                               random_seed=99,  # 随机种子
                               od_type='Iter',  # 过拟合检测类型
                               od_wait=20,  # 达到优化目标后继续迭代的次数
                               verbose=False)  # 不显示训练过程信息

    model.fit(X_train, y_train, eval_set=(X_val, y_val), use_best_model=True, cat_features=categorical_features_indices)

    # 记录每个训练周期的损失值
    train_loss = model.evals_result_['learn']['RMSE']
    val_loss = model.evals_result_['validation']['RMSE']
    train_losses.append(train_loss)
    val_losses.append(val_loss)

    # 在测试集上进行预测并记录结果
    y_pred = model.predict(x_test)
    all_y_test.extend(y_test)
    all_y_pred.extend(y_pred)

# 可视化损失值
plt.figure(figsize=(10, 5))
for i in range(k_folds):
    plt.plot(train_losses[i], label=f'Fold {i+1} Train Loss')
    plt.plot(val_losses[i], label=f'Fold {i+1} Validation Loss')

plt.xlabel('Iterations')
plt.ylabel('RMSE')
plt.title('Training and Validation Losses in each Fold')
plt.legend()
plt.show()

# 模型评估
print('可解释方差值：{}'.format(round(metrics.explained_variance_score(all_y_test, all_y_pred), 2)))
print('平均绝对误差：{}'.format(round(metrics.mean_absolute_error(all_y_test, all_y_pred), 2)))
print('均方误差：{}'.format(round(metrics.mean_squared_error(all_y_test, all_y_pred), 2)))
print('R方值：{}'.format(round(metrics.r2_score(all_y_test, all_y_pred), 2)))

# 真实值与预测值比对图
plt.plot(range(len(all_y_test)), all_y_test, color="green", linewidth=1.5, linestyle="-")
plt.plot(range(len(all_y_pred)), all_y_pred, color="red", linewidth=1.5, linestyle="-.")
plt.legend(['真实值', '预测值'])
plt.title("真实值与预测值比对图")
plt.show()  # 显示图片

feature_importance = model.get_feature_importance(type='FeatureImportance')

# 获取特征名称
feature_names = model.feature_names_

# 可视化特征重要性
sorted_idx = np.argsort(feature_importance)
plt.figure(figsize=(10, 8))
plt.barh(range(len(sorted_idx)), feature_importance[sorted_idx], align='center')
plt.yticks(range(len(sorted_idx)), np.array(feature_names)[sorted_idx])
plt.xlabel('Feature Importance')
plt.title('CatBoost Feature Importance')
plt.show()

# 保存模型

torch.save(model, "full_model.pt")


# 加载模型
model_loaded = torch.load("full_model.pt")

# 测试是否可以用户端输入并预测
def predict_price():
    # 接收用户输入的特征参数
    # 用户输入特征值

    global latitude, longitude, move_in_date, air_conditioning, personal_outdoor_space, smoking_permitted, utilities_included, wi_fi_and_more, parking_included, agreement_type, pet_friendly, size_sqft, furnished, post_time, Type, bedroom, bathroom, appliances
    try:
        latitude = float(input("Enter Latitude: "))
        longitude = float(input("Enter Longitude: "))
        Type = input(
            "Enter the Type of home ('Apartment' or 'House' or 'Condo' or 'Duplex/Triplex' or 'Basement' or 'Townhouse'): ")
        bedroom = float(input("Enter the number of bedrooms: "))
        bathroom = float(input("Enter the number of bathrooms: "))

        # 逐个询问
        hydro = input("Is hydro included? (Yes/No): ").capitalize()
        heat = input("Is heat included? (Yes/No): ").capitalize()
        water = input("Is water included? (Yes/No): ").capitalize()
        # 将用户输入的内容转换成指定格式
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
        # 检查用户的输入情况，确定输出的字符串
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

    # 构建特征向量
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

    # 进行价格预测
    X = pd.DataFrame(input_data, index=[0])
    predicted_price = model_loaded.predict(X)

    return predicted_price


# 调用函数进行价格预测
predicted_price = predict_price()
print("Predicted price:", predicted_price)