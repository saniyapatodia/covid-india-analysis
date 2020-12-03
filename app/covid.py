import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import datetime
import time
import matplotlib
import matplotlib.pyplot as plt
import requests

st.title(' Analysis of COVID-19 cases in India')

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

@st.cache
def load_covid_data(nrows=-1):
    DATA_URL = ('../data/covid_19_india.csv')
    if nrows == -1:
        data = pd.read_csv(DATA_URL)
    else:
        data = pd.read_csv(DATA_URL, nrows=nrows)
    data['Date'] = pd.to_datetime(data['Date'], format='%d/%m/%y')
    data['Time'] = pd.to_datetime(data['Time'], format='%I:%M %p').dt.time
    data['ConfirmedIndianNational'] = data['ConfirmedIndianNational'].replace('-', '0')
    data['ConfirmedIndianNational'] = data['ConfirmedIndianNational'].astype(int)
    data['ConfirmedForeignNational'] = data['ConfirmedForeignNational'].replace('-', '0')
    data['ConfirmedForeignNational'] = data['ConfirmedForeignNational'].astype(int)
    data['Cured'] = data['Cured'].astype(int)
    data['Deaths'] = data['Deaths'].astype(int)
    data['Confirmed'] = data['Confirmed'].astype(int)
    return data

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
    pass

state_comparison_data = load_and_display_state_comparison_data()

def display_covid_prevention_data():
    pass

covid_prevention_data = display_covid_prevention_data()


sidebar_options = {
    'Covid-19 State-specific data': load_and_display_state_data,
    'Covid-19 State-comparison data': load_and_display_state_comparison_data,
    'Covid-19 Prevention': display_covid_prevention_data,

}

sidebar_selection = st.sidebar.selectbox(
    'What type of analysis would you like to conduct?',
    list(sidebar_options.keys())
)

sidebar_options[sidebar_selection]()

print('=' * 40)

def get_testing_data():
    response = requests.get("https://api.covid19india.org/state_test_data.json")
    content = response.json()

def get_datewise_daily_changes():
    response = requests.get("https://api.covid19india.org/v4/data-YYYY-MM-DD.json")
    content = response.json()




'''
def plot_statewise_bar_chart(statewise_bar_data):
    #Plotting a graph showing the statewise cases of the people in a state
    st.subheader('COVID-19 bar plot showing the statewise cases of the people in a state: ')
    chart = alt.Chart(statewise_bar_data).mark_bar().encode(
    x='state', y='confirmed').interactive()
    st.altair_chart(chart)

bar_plot = plot_statewise_bar_chart(statewise_bar_data)




def plot_covid_data(covid_data):
    #Plotting a graph showing the number of covid cases datewise
    st.subheader('COVID-19 plot of confirmed cases: ')
    chart = alt.Chart(covid_data).mark_line().encode(
    x='Date', y='Confirmed', color='State/UnionTerritory'
    ).interactive()
    st.altair_chart(chart)

def plot_covid_state_data(covid_data):
    st.subheader('COVID-19 statewise analysis of cases: ')
    states = np.sort(pd.unique(covid_data['State/UnionTerritory']))
    option = st.selectbox('Please select a state!', list(states))
    st.write('You selected:', option)

    #Plotting a graph showing the number of covid cases datewise and statewise
    state_data  = covid_data[covid_data['State/UnionTerritory'] == option]
    state_data_melted = state_data.reset_index().melt('Date')
    state_data_melted
    state_data_melted = state_data_melted[
        (state_data_melted['variable'] == 'Confirmed') |
        (state_data_melted['variable'] == 'Deaths') |
        (state_data_melted['variable'] == 'Cured')
    ]
    chart = alt.Chart(state_data_melted).mark_line().encode(
        x='Date', y='value', color='variable'
    )
    st.altair_chart(chart)

def load_and_display_covid_data():
    data_load_state = st.text('Loading covid data...')
    covid_data = load_covid_data()
    data_load_state.text('Loading covid data... done!')
    st.subheader('Covid-19 Data Table: ')
    covid_data
    plot_covid_data(covid_data)
    plot_covid_state_data(covid_data)
                                                

#url 2
@st.cache
def load_age_group_covid_data():
    DATA_URL = '../data/AgeGroupDetails.csv'
    data = pd.read_csv(DATA_URL)
    data['AgeGroup'] = data['AgeGroup'].astype(str)
    return data


def plot_age_group_bar_chart(age_group_data):
    #Plotting a graph showing the number of covid cases on the basis of the age group of the people
    st.subheader('COVID-19 bar plot of cases on the basis of the age group of the people: ')
    chart = alt.Chart(age_group_data).mark_bar().encode(
    x='AgeGroup', y='TotalCases').interactive()
    st.altair_chart(chart)

def plot_age_group_pie_chart(age_group_data):
    #Plotting a pie chart showing the number of covid cases on the basis of the age group of the people
    st.subheader('Pie chart showing the number of covid cases on the basis of the age group of the people')
    fig = plt.figure(figsize =(10, 10))
    plt.pie(age_group_data['TotalCases'], labels = age_group_data['AgeGroup'])
    plt.legend(loc = 'upper right')
    st.pyplot()

def load_and_display_age_group_covid_data():
    age_group_data = load_age_group_covid_data()
    st.write(age_group_data)
    plot_age_group_bar_chart(age_group_data)
    plot_age_group_pie_chart(age_group_data)

#url 3
@st.cache
def load_individual_details():
    DATA_URL = '../data/IndividualDetails.csv'
    data = pd.read_csv(DATA_URL)
    return data

def individual_details_pie_chart(individual_details_data):
    #Plotting a pie chart showing the number of covid cases on the basis of their travelling history
    st.subheader('Pie chart showing the number of covid cases on the basis of their travelling history')
    fig = plt.figure(figsize =(10, 10))
    plt.pie(individual_details_data['TotalCases'], labels = individual_details_data['notes'])
    plt.legend(loc = 'upper right')
    st.pyplot()
def load_and_display_individual_details():
    Individual_Details_data = load_individual_details()
    st.write(Individual_Details_data)

#url 4
@st.cache
def load_testing_details():
    DATA_URL = '../data/StatewiseTestingDetails.csv'
    data = pd.read_csv(DATA_URL)
    data['Negative'] = data['TotalSamples'] - data['Positive']
    data['Date'] = pd.to_datetime(data['Date'], format='%Y-%m-%d')
    return data

def plot_testing_details(testing_details_data):
    st.subheader('Analysis of Testing Details: ')

    states = np.sort(pd.unique(testing_details_data['State']))
    option = st.selectbox('Please select a state!', list(states))
    st.write('You selected:', option)
    state_data = testing_details_data[testing_details_data['State'] == option]

    #Plotting a graph showing the number of covid cases datewise and statewise
    st.subheader('COVID-19 bar plot showing the testing details of a group of people: ')
    state_data = state_data.reset_index().melt('Date')
    state_data = state_data[
        (state_data['variable'] == 'Positive') |
        (state_data['variable'] == 'Negative')
    ]
    st.write(state_data)
    chart = alt.Chart(state_data).mark_line().encode(
        x='Date',
        y='value',
        color='variable',
    ).interactive()
    st.altair_chart(chart)


def plot_testing_details_bar_chart(testing_details_data):
    #Plotting a graph showing the testing details of a group of people
    st.subheader('COVID-19 bar plot showing the details of a group of people tested positive: ')
    chart = alt.Chart(testing_details_data).mark_bar().encode(
    x='State', y='Positive').interactive()
    st.altair_chart(chart)

def plot_testing_details2_bar_chart(testing_details_data):
    #Plotting a graph showing the testing details of a group of people
    st.subheader('COVID-19 bar plot showing the details of a group of people tested negative: ')
    chart = alt.Chart(testing_details_data).mark_bar().encode(
    x='State', y='Negative').interactive()
    st.altair_chart(chart)


def load_and_display_testing_details():
    testing_details_data = load_testing_details()
    st.write(testing_details_data)
    plot_testing_details_bar_chart(testing_details_data)
    plot_testing_details2_bar_chart(testing_details_data)
    plot_testing_details(testing_details_data)


sidebar_options = {
    'Covid-19 Overview': load_and_display_covid_data,
    'Covid-19 Age-wise analysis': load_and_display_age_group_covid_data,
    'Individual Details': load_and_display_individual_details,
    'Testing Details': load_and_display_testing_details
}

sidebar_selection = st.sidebar.selectbox(
    'What type of analysis would you like to conduct?',
    list(sidebar_options.keys())
)

sidebar_options[sidebar_selection]()
'''