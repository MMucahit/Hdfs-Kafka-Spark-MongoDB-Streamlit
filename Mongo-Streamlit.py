
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pymongo

st.title('Welcome To Our BigData Project')

## Connect to MongoDB
def connection(db, collection):
    myclient = pymongo.MongoClient('mongodb://127.0.0.1:27017/')
    mydb = myclient[db]
    mycol = mydb[collection]
    return mycol

raw = connection('company','raw')
raw = pd.DataFrame(raw.find())

cat_columns = st.selectbox('Categorical Columns',[x for x in raw.columns if raw[x].dtype == 'object' and x != '_id'])
num_columns = st.selectbox('Numerical Columns',[x for x in raw.columns if raw[x].dtype != 'object' and x != 'id'])

is_sort = st.radio('What do you want ?', ('Not Sort','Sort'))

if is_sort == 'Sort':
    is_Asc = st.radio('What do you want ?', ('Ascending','Descending'))
    if is_Asc == 'Ascending':
        st.dataframe(raw.groupby(cat_columns)[num_columns].mean().sort_values(ascending=True).head())
    else:    
        st.dataframe(raw.groupby(cat_columns)[num_columns].mean().sort_values(ascending=False).head())
else:
    st.dataframe(raw.groupby(cat_columns)[num_columns].mean().head())

columns = st.selectbox('Choose columns',['salary','car_model_year'])
st.write(f'{columns} was selected!')

fig = plt.figure(figsize=(15,5))
sns.boxplot(data=raw, x=columns)
plt.title(columns)
st.pyplot(fig)

country_gender_salary = connection('company','country_gender_salary')

status = st.radio('What do you want to see ?', ('Female','Male'))

if status == 'Male':
    df = pd.DataFrame(country_gender_salary.find()).sort_values('Male',ascending=False).iloc[:10,:]

    fig = plt.figure(figsize=(15,5))
    sns.barplot(data=df, x='country',y='Male', palette='Blues_d')
    plt.title('Country-Male-Salary')
    plt.xlabel('Country')
    plt.ylabel('Salary')
    st.pyplot(fig)

else:
    df = pd.DataFrame(country_gender_salary.find()).sort_values('Female',ascending=False).iloc[:10,:]

    fig = plt.figure(figsize=(15,5))
    sns.barplot(data=df, x='country',y='Female', palette='Blues_d')
    plt.title('Country-Female-Salary')
    plt.xlabel('Country')
    plt.ylabel('Salary')
    st.pyplot(fig)

car_make_count = connection('company','car_make_count')

df = pd.DataFrame(car_make_count.find()).iloc[:10,:]

fig = plt.figure(figsize=(10,5))
sns.barplot(data=df, x='car_make',y='count(id)', palette='Blues_d')
plt.title('Brand-count')
plt.xlabel('brand')
plt.ylabel('count')
st.pyplot(fig)

country_gender = connection('company','country_gender')    

status = st.radio('What do you want to see ?', ('Female-Population','Male-Populaiton'))

if status == 'Female-Population':

    df = pd.DataFrame(country_gender.find())[['country','Female','Male']].sort_values('Female',ascending=False).iloc[:10,:]

    fig = plt.figure(figsize=(10,5))
    sns.barplot(data=df, x='country',y='Female', palette='Purples')
    plt.title('Female-Population')
    st.pyplot(fig)

else:

    df = pd.DataFrame(country_gender.find())[['country','Female','Male']].sort_values('Male',ascending=False).iloc[:10,:]

    fig = plt.figure(figsize=(10,5))
    sns.barplot(data=df, x='country',y='Male', palette='Blues_d')
    plt.title('Male-Population')
    st.pyplot(fig)