import numpy as np
import streamlit as st
import pandas as pd
import altair as alt
import datetime
import time
import matplotlib
import matplotlib.pyplot as plt

st.title(' Analysis of COVID-19 cases in India')

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

'''def individual_details_pie_chart(individual_details_data):
    #Plotting a pie chart showing the number of covid cases on the basis of their travelling history
    st.subheader('Pie chart showing the number of covid cases on the basis of their travelling history')
    fig = plt.figure(figsize =(10, 10))
    plt.pie(individual_details_data['TotalCases'], labels = individual_details_data['notes'])
    plt.legend(loc = 'upper right')
    st.pyplot()'''
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
