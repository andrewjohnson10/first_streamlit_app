
import streamlit
import pandas as pd

# create title for application
streamlit.title('My parents healthy diner')

# add breakfast menu to application
streamlit.header('Breakfast Menu')

# breakfast menu items
streamlit.text('🥣 Omega 3 Oatmeal')
streamlit.text('🥗 Kale and rocket smoothie')
streamlit.text('🐔 Hard-boiled egg')
streamlit.text('🥑🍞 Avocardo toast')

# Add smoothie menu
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

# get smoothie recepie from s3 bucket
smoothie_recepies = 'https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt'
my_fruit_list = pd.read_csv(smoothie_recepies)
my_fruit_list = my_fruit_list.set_index('Fruit')

# add fruit selection dropdown box - set default avocardo and strawberries
choices = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocardo', Strawberries'])

# display the table with the chosen fruits on the page
streamlit.dataframe(my_fruit_list)
