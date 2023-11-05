
import streamlit
import pandas as pd
import requests
import snowflake.connector

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
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index), ['Avocado', 'Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]

# display the table with the chosen fruits on the page
streamlit.dataframe(fruits_to_show)

# add section to use get fruit info from fruityvice via the fruityvice API
streamlit.header('Fruit advice from the Fruityvice website') 
fruit_choice = streamlit.text_input('Enter name of fruit to query', 'Kiwi')
streamlit.write('the user entered :', fruit_choice)

# get the fruit information for the users fruit choice
responce = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)

#render it in the webpage as a dataframe
responce_normalised = pd.json_normalize(responce.json())
streamlit.dataframe(responce_normalised)

my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT CURRENT_USER(), CURRENT_ACCOUNT(), CURRENT_REGION()")
my_data_row = my_cur.fetchone()
streamlit.text("Hello from Snowflake:")
streamlit.text(my_data_row)
