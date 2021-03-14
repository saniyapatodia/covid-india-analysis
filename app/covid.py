import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import datetime
import time
import matplotlib
import matplotlib.pyplot as plt
import requests
from PIL import Image

CODE_TO_STATE = {
    'AN': 'Andaman and Nicobar Islands',		
    'AP': 'Andhra Pradesh',	
    'AR': 'Arunachal Pradesh',
    'AS': 'Assam',
    'BR': 'Bihar',
    'CH': 'Chandigarh',
    'CT': 'Chhattisgarh',
    'DN': 'Dadra and Nagar Haveli',
    'DD': 'Daman and Diu',
    'DL': 'Delhi',
    'GA': 'Goa',
    'GJ': 'Gujarat',
    'HR': 'Haryana',
    'HP': 'Himachal Pradesh',
    'JK': 'Jammu and Kashmir',	
    'JH': 'Jharkhand',
    'KA': 'Karnataka',
    'KL': 'Kerala',
    'LA': 'Lakshadweep',
    'LD': 'Ladakh',
    'MP': 'Madhya Pradesh',
    'MH': 'Maharashtra',
    'MN': 'Manipur',
    'ML': 'Meghalaya',
    'MZ': 'Mizoram',
    'NL': 'Nagaland',
    'OR': 'Odisha',
    'PY': 'Puducherry',
    'PB': 'Punjab',
    'RJ': 'Rajasthan',
    'SK': 'Sikkim',
    'TN': 'Tamil Nadu',
    'TG': 'Telangana',
    'TR': 'Tripura',
    'TT': 'Total',
    'UP': 'Uttar Pradesh',
    'UT': 'Uttarakhand',
    'WB': 'West Bengal',
}


def display_covid_introduction():
    st.title('COVID-19 Overview')
    st.write('Coronavirus disease (COVID-19) is an infectious disease caused by a newly ' +
             'discovered coronavirus.')
    st.write('Most people infected with the COVID-19 virus will experience mild to moderate ' +
             'respiratory illness and recover without requiring special treatment.  Older ' + 
             'people, and those with underlying medical problems like cardiovascular disease, ' + 
             'diabetes, chronic respiratory disease, and cancer are more likely to develop serious illness.')
    corona_virus_image = Image.open('./images/corona-virus.png')
    st.image(corona_virus_image, width=650, caption='Visualisation of a virus')
    st.write('The best way to prevent and slow down transmission is to be well informed about the COVID-19 ' +
             'virus, the disease it causes and how it spreads. Protect yourself and others from infection by ' + 
             'washing your hands or using an alcohol based rub frequently and not touching your face.')
    st.write('The COVID-19 virus spreads primarily through droplets of saliva or discharge from the nose when ' +
             'an infected person coughs or sneezes, so it’s important that you also practice respiratory etiquette ' +
             '(for example, by coughing into a flexed elbow).')

def display_covid_symptom_data():
    st.title('Symptoms of COVID-19')
    st.write("COVID-19 affects different people in different ways. Most infected people will develop mild " +
             "to moderate illness and recover without hospitalization.")
    st.subheader("Most common symptoms")
    st.write("1. Fever.")
    st.write("2. Dry cough.")
    st.write("3. Tiredness.")
    symptoms_image = Image.open('./images/symptoms.jpeg')
    st.image(symptoms_image, width=650, caption='Symptoms of coronavirus')
    st.subheader("Less common symptoms")
    st.write("1. Aches and pains.")
    st.write("2. Sore throat.")
    st.write("3. Diarrhoea.")
    st.write("4. Conjunctivitis.")
    st.write("5. Headache.")
    st.write("6. Loss of taste or smell.")
    st.write("7. A rash on skin, or discolouration of fingers or toes.")
    body_symptoms_image = Image.open('./images/body-symptoms.png')
    st.image(body_symptoms_image, width=650, caption='Symptoms of coronavirus')
    st.subheader("Serious symptoms:")
    st.write("1. Difficulty breathing or shortness of breath.")
    st.write("2. Chest pain or pressure.")
    st.write("3. Loss of speech or movement.")
    st.write("4. Seek immediate medical attention if you have serious symptoms.")
    st.write("5. Always call before visiting your doctor or health facility.")
    st.write("People with mild symptoms who are otherwise healthy should manage their symptoms at home." + 
             "On average it takes 5–6 days from when someone is infected with the virus for symptoms to show," +
             "however it can take up to 14 days.")


def display_covid_prevention_data():
    st.title("Prevention of COVID-19")
    st.subheader('Protect yourself and others from Covid-19')
    st.write('If COVID-19 is spreading in your community, stay safe by taking some simple precautions, such as physical distancing, wearing a mask, keeping rooms well ventilated, avoiding crowds, cleaning your hands, and coughing into a bent elbow or tissue. Check local advice where you live and work. Do it all!')
    mask_image = Image.open('./images/wear-a-mask.png')
    if mask_image.mode != 'RGB':
        mask_image = mask_image.convert('RGB')
    st.image(mask_image, width=350)
    
    st.subheader('A Few Precautions that must be taken:')
    st.write('''1.Maintain at least a 1-metre distance between yourself and others to reduce your risk of infection when they cough, sneeze or speak. Maintain an even greater distance between yourself and others when indoors. The further away, the better.\n
2.Make wearing a mask a normal part of being around other people. The appropriate use, storage and cleaning or disposal are essential to make masks as effective as possible.\n
3.Avoid the 3Cs: spaces that are closed, crowded or involve close contact.\n
4.Avoid meeting people. However, if necessary, choose outdoor settings and avoid crowded or indoor settings.''')
    
    hygiene_image = Image.open('./images/hygiene-icons.png')
    st.image(hygiene_image, width=700)

@st.cache()
def get_overall_data():
    # response = requests.get("https://api.covid19india.org/csv/latest/case_time_series.csv")
    #content = response.content
    # st.write(type(content))
    df = pd.read_csv("https://api.covid19india.org/csv/latest/case_time_series.csv")
    df['Date_YMD'] = pd.to_datetime(df['Date_YMD'])
    return df

def load_and_display_overall_data():
    st.title('COVID-19 cases in India')
    time_series_data = get_overall_data()
    st.subheader('Daily Data')
    st.write(time_series_data)

    st.subheader('Confirmed Cases')
    plt.xticks(time_series_data['Date_YMD'][::30])

    fig = plt.figure()
    plt.plot(
        time_series_data['Date_YMD'], 
        time_series_data['Daily Confirmed'],
    )
    plt.title('Plot of daily cases in India')
    plt.xlabel('Date')
    plt.ylabel('Cases')
    st.write(fig)

    fig = plt.figure()
    plt.plot(
        time_series_data['Date_YMD'], 
        time_series_data['Total Confirmed'],
    )
    plt.title('Plot of total cases in India')
    plt.xlabel('Date')
    plt.ylabel('Cases')
    st.write(fig)

    st.subheader('Recoveries')

    fig = plt.figure()
    plt.plot(
        time_series_data['Date_YMD'], 
        time_series_data['Daily Recovered']
    )
    plt.xlabel('Date')
    plt.ylabel('Recoveries')
    plt.title('Plot of daily recoveries in India')
    st.write(fig)

    fig = plt.figure()
    plt.plot(
        time_series_data['Date_YMD'], 
        time_series_data['Total Recovered']
    )
    plt.xlabel('Date')
    plt.ylabel('Recoveries')
    plt.title('Plot of total recoveries in India')
    st.write(fig)

  
    
@st.cache(allow_output_mutation=True)
def get_statewise_data():
    response = requests.get("https://api.covid19india.org/v4/data.json")
    content = response.json()
    # Dictionary with keys: statename, confirmed, deceased, recovered, tested
    cases = {
        'state': [],
        'state_code': [],
        'confirmed': [],
        'deceased': [],
        'recovered': [],
        'tested': [],
    }    
    for state_code, state_data in content.items():
        totals = state_data['total']
        cases['state'].append(CODE_TO_STATE[state_code])
        cases['state_code'].append(state_code)
        cases['confirmed'].append(totals['confirmed'])
        cases['deceased'].append(totals['deceased'])
        cases['recovered'].append(totals['recovered'])
        cases['tested'].append(totals['tested'])  
    return pd.DataFrame.from_dict(cases)


@st.cache(allow_output_mutation=True)
def get_statewise_daily_changes():
    response = requests.get("https://api.covid19india.org/states_daily.json")
    content = response.json()
    values = content['states_daily']

    confirmed, recovered, deceased = [], [], []  

    for element in values:
        if element['status'] == 'Confirmed':
            confirmed.append(element)
            
        elif element['status'] == 'Recovered':
            recovered.append(element)

        elif element['status'] == 'Deceased':
            deceased.append(element)

    confirmed = pd.DataFrame(confirmed)
    recovered = pd.DataFrame(recovered)
    deceased = pd.DataFrame(deceased)

    return confirmed, recovered, deceased


def load_and_display_state_data():
    st.title(' Analysis of COVID-19 cases in India')
    statewise_data = get_statewise_data()
    st.subheader('Statewise covid-19 data:')
    st.write(statewise_data)
    states = statewise_data['state']
    state = st.selectbox(
        'Which state would you like to further analyse the graph of?',
        states,
    )
    state_data = statewise_data.loc[statewise_data['state'] == state]
    st.write(state_data)
    state_code = state_data['state_code'].iloc[0]
    state_code = state_code.lower()
    state_data = pd.DataFrame({
        'Covid-19 Case Status': ['confirmed', 'deceased', 'recovered', 'tested'],
        'Number (corresponding to each category)': [
            state_data['confirmed'].iloc[0], state_data['deceased'].iloc[0],
            state_data['recovered'].iloc[0], state_data['tested'].iloc[0],
        ]
    })

    chart = alt.Chart(state_data).mark_bar().encode(
        x='Covid-19 Case Status',
        y='Number (corresponding to each category)',
    ).properties(
        width=400,
        height=400,
    )
    st.altair_chart(chart)

    confirmed, recovered, deceased = get_statewise_daily_changes()

    # st.subheader('A table of daily confirmed cases per state:')
    # st.write(confirmed)
    # st.subheader('A table of daily recovered cases per state:')
    # st.write(recovered)
    # st.subheader('A table of daily deceased cases per state:')
    # st.write(deceased)
    confirmed[state_code] = pd.to_numeric(confirmed[state_code])
    recovered[state_code] = pd.to_numeric(recovered[state_code])
    deceased[state_code] = pd.to_numeric(deceased[state_code])
  
    dates = confirmed['dateymd'].tolist()
    dates = dates[::7]
    st.subheader('COVID-19 plot of confirmed cases of the selected state: ')
    chart = alt.Chart(confirmed).mark_line().encode(
    x = alt.X('dateymd', axis=alt.Axis(values=dates, title='Date')),
    y = alt.Y(state_code, axis=alt.Axis( title=' No. of Confirmed Cases'))
    ).properties(
        width=800,
        height=500,
    ).interactive()
    st.altair_chart(chart)

    st.subheader('COVID-19 plot of recovered cases of the selected state: ')
    chart = alt.Chart(recovered).mark_line().encode(
    x = alt.X('dateymd', axis=alt.Axis(values=dates, title='Date')),
    y = alt.Y(state_code, axis=alt.Axis( title=' No. of Recovered Cases'))
    ).properties(
        width=800,
        height=500,
    ).interactive()
    st.altair_chart(chart)

    st.subheader('COVID-19 plot of deceased cases of the selected state: ')
    chart = alt.Chart(deceased).mark_line().encode(
    x = alt.X('dateymd', axis=alt.Axis(values=dates, title='Date')),
    y = alt.Y(state_code, axis=alt.Axis( title=' No. of Deceased Cases'))
    ).properties(
        width=800,
        height=500,
    ).interactive()
    st.altair_chart(chart)

def load_and_display_state_comparison_data():
    st.title('Covid-19 Inter-State Comparison')
    statewise_data = get_statewise_data()
    states = statewise_data['state'].tolist()
    state_one = st.selectbox(
        'Pick the first state to analyse:',
        states)
    state_two = st.selectbox(
        'Pick the second state to analyse:',
        list(reversed(states)))
    state_one_data = statewise_data.loc[statewise_data['state'] == state_one]
    state_two_data = statewise_data.loc[statewise_data['state'] == state_two]
    state_data = pd.concat([state_one_data, state_two_data])
    st.write(state_data)
    state_code = state_one_data['state_code'].iloc[0]
    state_code = state_two_data['state_code'].iloc[0]
    state_code = state_code.lower()
    state_one_data = pd.DataFrame({
        'Covid-19 Case Status': ['confirmed', 'deceased', 'recovered', 'tested'],
        'Number (corresponding to each category)': [
            state_one_data['confirmed'].iloc[0], state_one_data['deceased'].iloc[0],
            state_one_data['recovered'].iloc[0], state_one_data['tested'].iloc[0]]})
    state_two_data = pd.DataFrame({
        'Covid-19 Case Status': ['confirmed', 'deceased', 'recovered', 'tested'],
        'Number (corresponding to each category)': [
            state_two_data['confirmed'].iloc[0], state_two_data['deceased'].iloc[0],
            state_two_data['recovered'].iloc[0], state_two_data['tested'].iloc[0]]})
    
    st.subheader('Plot comparing the no. of confirmed cases of the selected states:')
    chart = alt.Chart(state_data).mark_bar().encode(
        x = 'state',
        color = 'state',
        y = 'confirmed',
    ).properties(
        width=500,
        height=450)
    st.altair_chart(chart)

    st.subheader('Plot comparing the no. of recovered cases of the selected states:')
    chart = alt.Chart(state_data).mark_bar().encode(
        x = 'state',
        color='state',
        y='recovered',
    ).properties(
        width=500,
        height=450)
    st.altair_chart(chart)

    st.subheader('Plot comparing the no. of deceased cases of the selected states:')
    chart = alt.Chart(state_data).mark_bar().encode(
        x = 'state',
        color='state',
        y='deceased',
    ).properties(
        width=500,
        height=450)
    st.altair_chart(chart)


sidebar_options = {
    'Overview': display_covid_introduction,
    'Symptoms': display_covid_symptom_data,
    'Prevention': display_covid_prevention_data,
    'Cases in India': load_and_display_overall_data,
    'State-wise Analysis': load_and_display_state_data,
    'State-comparison Analysis': load_and_display_state_comparison_data,
}

sidebar_selection = st.sidebar.selectbox(
    'COVID-19 Application',
    list(sidebar_options.keys())
)

sidebar_options[sidebar_selection]()
