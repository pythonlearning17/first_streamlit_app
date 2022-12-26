import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My Parents New Healthy Dinner') 

streamlit.header('Breakfast Favorites')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach & Rocket Smoothie')
streamlit.text('🐔Hard-Boiled Free-Range Egg')
streamlit.text('  🥑🍞 Avocado Toast')


streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')


my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit') #setting fruit name column as index
# Let's put a pick list here so they can pick the fruit they want to include 
fruits_selected=streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]


# Display the table on the page.
streamlit.dataframe(fruits_to_show)
#creating function
def get_fruityvice_data(this_fruit_choice):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + this_fruit_choice) #added the input variable
# normalize the JSON data
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
# shows the output in a table form
    return fruityvice_normalized
    

#new section to display api response
streamlit.header("Fruityvice Fruit Advice!")
try:
    fruit_choice = streamlit.text_input('What fruit would you like information about?')#'value 'kiwi' removed
    if not fruit_choice:
        streamlit.error("Please select a fruit to get information.")
    else:    
       back_from_function = get_fruityvice_data(fruit_choice)
       streamlit.dataframe(back_from_function)

except URLError as e:
      streamlit.error()
#don't run anything from here while we trouble shoot 
streamlit.stop()



my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
my_cur = my_cnx.cursor()
my_cur.execute("select * from fruit_load_list")
my_data_rows = my_cur.fetchall() #fetching all rows
streamlit.header("The fruit load list contains:")
streamlit.dataframe(my_data_rows)

# Adding code for challange lab 
#adding text field to allow end user to add fruit 
add_my_fruit = streamlit.text_input('What fruit would you like to add?','jackfruit')
#adding the confirmation message 
streamlit.write('Thanks for adding', add_my_fruit)

#Trying to add fruit name from streamlit to snowflakes table
my_cur.execute("insert into fruit_load_list values ('from streamlit')")
