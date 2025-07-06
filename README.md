# 📚 BookScape Explorer

### 👋 Welcome to BookScape Explorer!

**BookScape Explorer** is a user-friendly web application that allows you to **search, fetch, and analyze book data** from the internet using the **Google Books API**. It helps users explore book details and perform meaningful data analysis through a simple interface powered by **Streamlit**.

---

### 🔍 What is this project about?

BookScape Explorer connects to the Google Books API to gather information about books (title, authors, language, rating, availability, etc.) and stores the data in a **MySQL** database. The app then allows users to explore and analyze this data visually and interactively.

---

### 📊 What can you do with this project?

- **📈 Data Analysis**:  
  Explore book data to answer questions like:
  - How many books are eBooks vs printed?
  - What are the most popular categories?
  - What is the average rating per language?

- **🔍 Data Extraction**:  
  Enter a search term and retrieve structured data (title, authors, rating, publisher, etc.) for books matching that keyword.

---

### 📚 How does it work?

1. **📥 Data Fetching**  
   The app fetches data from the **Google Books API** and stores it in a **MySQL** database.

2. **📊 Data Analysis**  
   Select from predefined questions to view SQL-generated results and insights.

3. **🔍 Data Extraction**  
   Enter any search topic and the app retrieves and displays relevant book info.

---

### 🛠️ Technologies Used

- **Streamlit** – Web app framework for Python  
- **Google Books API** – For fetching book data  
- **MySQL** – Backend database for storage  
- **SQLAlchemy** – Python SQL toolkit  
- **Pandas** – Data processing and manipulation

---

### 🚀 How to Use

1. Launch the app using `streamlit run application.py`
2. Use the sidebar to switch between:
   - 📊 **Data Analysis**
   - 🔍 **Data Extraction**
   - 📘 **About Project**
3. Enter search terms or select predefined queries to get insights.

---

### 🙌 Contributions

Feel free to fork, explore, and enhance this project! Pull requests are welcome.
