# Import python packages
import streamlit as st
#from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col
import requests

# Write directly to the app
st.title(":cup_with_straw: Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose your fruits!!!.
    """
)

name_on_order = st.text_input('Name of Smoothie:')
st.write('The name on your smoothie will be:', name_on_order)

# Get the current credentials
#session = get_active_session()
cnx = st.connection("snowflake")
session = cnx.session()

my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
#st.dataframe(my_dataframe, use_container_width=True)
ingredients_list = st.multiselect(
    "Choose up to five ingredientes:",
    my_dataframe,
    max_selections = 5
)
if ingredients_list:
    #st.write(ingredients_list)
    #st.text(ingredients_list)
    ingredients_string = ''
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '

    st.write(ingredients_string)
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, NAME_ON_ORDER)
            values ('""" + ingredients_string + """','""" + name_on_order + """')"""
    time_to_insert = st.button('Submit Order')
    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, ' + name_on_order + '', icon="✅")

fruityvice_response = requests.get("https://fruityvice.com/api/fruit/watermelon")
fruityvice_json = False #fruityvice_response.json()
if fruityvice_json:
    fv_df = st.dataframe(data=fruityvice_response.json(), use_container_width=True)
else:
    st.write('The was an error trying to retrieve data from Fruityvice.')
    st.write(fruityvice_response)
