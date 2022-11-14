import streamlit as st
from requests_html import HTMLSession
import matplotlib.pyplot as plt
import pandas as pd

sess = HTMLSession()
        
def get_data(in_name, in_country = None):
    if in_country and in_country != '':
        gender_url = f"https://api.genderize.io?name={in_name}&country_id={in_country}"
        age_url = f"https://api.agify.io?name={in_name}&country_id={in_country}"
    else:
        gender_url = f"https://api.genderize.io?name={in_name}"
        age_url = f"https://api.agify.io?name={in_name}"
    gender_json = sess.get(gender_url).json()
    age_json = sess.get(age_url).json()
    return gender_json, age_json

def return_pie_values(in_gender_data):
    if in_gender_data['gender'] == 'male':
        return [in_gender_data['probability'], 1 - in_gender_data['probability']]
    else:
        return [1 - in_gender_data['probability'], in_gender_data['probability']]
        
st.title('Name Analyzer')
st.markdown("## Search")
name = st.text_input("Name", "Andrea")
country = st.text_input("Country")
if st.button("Run"):
    gender, age = get_data(name, country)
    st.markdown("## Results Age")
    st.metric("Predicted Age", value = age['age'])
    st.metric("Count", value = age['count'])
    st.markdown("---")
    st.markdown("## Results Gender")
    df = pd.DataFrame({"category":["M","F"], "value":return_pie_values(gender)})
    fig, ax = plt.subplots()
    # change background color to transparent
    fig.patch.set_facecolor('none')
    ax.pie(df['value'], labels = df['category'], autopct='%1.1f%%', colors = ['blue', 'fuchsia'], textprops={'color':"w"})
    st.pyplot(fig)
    st.metric("Count", gender['count'])
    st.markdown("---")