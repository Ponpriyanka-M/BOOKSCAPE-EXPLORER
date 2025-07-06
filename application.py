 
import streamlit as st
import mysql.connector
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
    default_index=0)
 

if selected == "About Project":
    st.markdown("<h1 style='text-align: center; font-style: italic; font-weight: bold;'>📚 BOOKSCAPE EXPLORER</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: center; font-style: italic;'>Explore the World of Books</h2>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("### 👋 Welcome to BookScape Explorer!")
    st.markdown("### 🔍 What is this project about?")
    st.write(
        "BookScape Explorer is a web application that helps you search, fetch, and analyze books "
        "from the internet using the Google Books API. It lets you explore book details and answer useful questions using data stored in a database."
    )
    st.markdown("### 📊 What can you do with this project?" )
    st.write(
        "- **Data Analysis**: Analyze book data to answer questions like the availability of eBooks vs physical books, the most popular book categories, and more.\n"
        "- **Data Extraction**: Extract book data based on your search key and view the results in a structured format.\n"
    )
    st.markdown("### 📚 How does it work?") 
    st.write(   
        "1. **Data Fetching**: The application fetches book data from the Google Books API and stores it in a MySQL database.\n"
        "2. **Data Analysis**: You can select predefined questions to analyze the data, and the application will generate SQL queries to fetch the relevant information.\n"
        "3. **Data Extraction**: You can enter a search key to extract specific book data from the database.\n"
    )
    st.markdown("### 📈 Technologies Used")
    st.write(
        "- **Streamlit**: For building the web application interface.\n"    
        "- **MySQL**: For storing and managing book data.\n"
        "- **Google Books API**: For fetching book details from the internet.\n"
        "- **Pandas**: For data manipulation and analysis.\n"
        "- **SQLAlchemy**: For database interactions.\n"    
    )
    st.markdown("### 📖 How to Use")
    st.write(
        "1. Navigate to the **Data Analysis** section to explore predefined questions and view the results.\n"
        "2. Go to the **Data Extraction** section to enter a search key and fetch specific book data.\n"
        "3. Use the sidebar to switch between sections.\n"      
    )
    
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

    
    