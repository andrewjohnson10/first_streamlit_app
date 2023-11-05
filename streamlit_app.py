
import streamlit
import pandas as pd
import requests
import snowflake.connector
from urllib.error import URLError

# fruityvice data
def get_fruityvice_data(this_fruit_choice):
    responce = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice)
    responce_normalised = pd.json_normalize(responce.json())
    return responce_normalised     

# snowflake querry
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()


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
try:
  # get the fruit information for the users fruit choice
  fruit_choice = streamlit.text_input('Enter name of fruit to query', 'Kiwi')
  if not fruit_choice:
    streamlit.error("Please choose a fruit")
  else:
    #get infromation about fruit choice from fruityvice website
    back_from_function = get_fruityvice_data(fruit_choice)
    #render responce in the webpage as a dataframe
    streamlit.dataframe(back_from_function)

except URLError as e:
  streamlit.error()  


# add button to load the fruit
if streamlit.button('Get the fruit load list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)



# stop after here
streamlit.stop()

# connect to snowflake and create cursor object
my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("SELECT * from fruit_load_list")
my_data_rows = my_cur.fetchall()
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)


# add option for user to add a fruit and to store it in snowflake
add_my_fruit = streamlit.text_input('Enter name of fruit to add to snowflake table', 'Kiwi')
streamlit.write('Enter name of fruit to add to snowflake table', add_my_fruit)
my_cur.execute("insert into PC_RIVERY_DB.PUBLIC.FRUIT_LOAD_LIST values ('from streamlit')")









