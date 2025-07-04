 
import streamlit as st
import mysql.connector
from matplotlib.pyplot import ecdf
import pandas as pd 
import book_scrape as bs
from streamlit_option_menu import option_menu


# Function to create a connection to MySQL
def create_connection():
      return mysql.connector.connect(
             host="127.0.0.1",
             user="root",
             password="pritri06",
             database="books_scrape"
        )

# Connect to MySQL
conn = create_connection()

# Create a cursor object
mycursor = conn.cursor()

#Change main page styles
st.markdown(
    """ 
    <style>
    body{
    font-family : 'Times New Roman';
    font-style :bold;
    }
   
    [data-testid="stAppViewContainer"]{  

    background-image:url("https://img.freepik.com/premium-photo/book-leaves-wallpaper-copy-space-literary-events-literary-backdrop-design-open-book-with_980716-58481.jpg");
    background-size:cover;
    background-position:left;
    background-repeat:no-repeat;
    background-attachment:fixed;
    }
    
    header[data-testid="stHeader"]{
    background-color:#4f6f6c ;
    }

    [data-testid="stHeadingWithActionElements"]{
    color:white;
    }
   </style>

    """, unsafe_allow_html=True)



def fetch_data(query):
    try:
        mycursor = conn.cursor()
        mycursor.execute(query)
        rows = mycursor.fetchall()
        columns = [desc[0] for desc in mycursor.description]
        return pd.DataFrame(rows, columns=columns)
    finally:
        mycursor.close()  # Close the cursor
        conn.close()  # Close the connection

#Sidebar Navigation menu
with st.sidebar:
 selected = option_menu(
    menu_title = "",
    options = ["About Project",
               "Data Analysis",
               "Data Extraction"],
    icons = ["info-square-fill","book-fill","binoculars-fill"],
    default_index=0,
    orientation="vertical")

if selected == "About Project":
    st.snow()
    st.title("BOOKSCAPE EXPLORER")
    st.markdown(""" 
    #### Objective:
    **The BookScape Explorer project aims to facilitate users in discovering and analyzing book data through a web application. 
    The application will extract data from online book APIs, store this information in a SQL database, and enable data analysis using SQL queries**
    #### Skills take away from this project : 
    **Python scripting, Data Collection, Streamlit, API integration, Data Management using SQL**   
    """)

elif selected == "Data Analysis":
    st.write("#### Data Analysis")
    # SelectBox to select the question
    optionInput = st.selectbox('Select the Question',[bs.qn_one,bs.qn_two,bs.qn_three,
    bs.qn_four,bs.qn_five,bs.qn_six,bs.qn_seven,bs.qn_eight,bs.qn_nine,bs.qn_ten,
    bs.qn_eleven,bs.qn_twelve,bs.qn_thirteen,bs.qn_fourteen,bs.qn_fifteen,bs.qn_sixteen,bs.qn_seventeen,
    bs.qn_eighteen,bs.qn_nineteen,bs.qn_twenty])
    query = bs.generate_query(optionInput)
    result = fetch_data(query)
    # Expander to view the query
    with st.expander("Click to view the query"):
        st.write(query)
    st.dataframe(result)

elif selected == "Data Extraction":
    st.write("#### Data Extraction")
    search_key = st.text_input("Enter the Search Key",placeholder="Type your search key here",autocomplete="off")
    if st.button("Fetch Data") and search_key == "":
        @st.dialog(" ")
        def isSearchKeyPresent():
            st.write("Please enter the search key")
            if st.button("ok"):
                st.rerun()
        if "isSearchKeyPresent" not in st.session_state:
            isSearchKeyPresent()
    elif search_key !="":
        bs.validate_books_data(search_key)

    
    
