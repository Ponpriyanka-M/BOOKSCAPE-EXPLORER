import streamlit as st
import pandas as pd
import requests
import time
from sqlalchemy import create_engine

#Questions
qn_one = '1.Check Availability of eBooks vs Physical Books'
qn_two = '2.Find the Publisher with the Most Books Published'
qn_three = '3.Identify the Publisher with the Highest Average Rating'
qn_four = '4.Get the Top 5 Most Expensive Books by Retail Price'
qn_five = '5.Find Books Published After 2010 with at Least 500 Pages'
qn_six = '6.List Books with Discounts Greater than 20%'
qn_seven = '7.Find the Average Page Count for eBooks vs Physical Books'
qn_eight = '8.Find the Top 3 Authors with the Most Books'
qn_nine = '9.List Publishers with More than 10 Books'
qn_ten = '10.Find the Average Page Count for Each Category'
qn_eleven = '11.Retrieve Books with More than 3 Authors'
qn_twelve = '12.Books with Ratings Count Greater Than the Average'
qn_thirteen = '13.Books with the Same Author Published in the Same Year'
qn_fourteen = '14.Books with a Specific Keyword in the Title'
qn_fifteen = '15.Year with the Highest Average Book Price'
qn_sixteen = '16.Count Authors Who Published 3 Consecutive Years'
qn_seventeen = '17.Find the authors, year, and the count of books they published in a particular year but different publishers'
qn_eighteen = '18.Find the average amount_retailPrice of eBooks and physical books'
qn_nineteen = '19.Find the books which has outliers and display title, averageRating, and ratingsCount'
qn_twenty = '20.Find the publisher with highest average rating among its books'

#Generating the query for the selected question

def generate_query(question):
        questionMap = {
        qn_one : 'select isEbook,count(*) as total_count from books_data group by isEbook',
        qn_two : 'select publisher,count(*) as books_published from books_data where publisher != "N/A" group by publisher order by books_published desc limit 5',
        qn_three : 'select publisher,avg(averageRating) as total_avg_rating from books_data where publisher != "N/A" group by publisher order by total_avg_rating desc limit 5',
        qn_four : 'select book_id,book_title,amount_retailPrice from books_data order by amount_retailPrice Desc limit 5',
        qn_five : 'select book_id,pageCount,extract(year from year)as extracted_year from books_data where extract(year from year) > 2010 and pageCount >=500 limit 10',
        qn_six : """ select book_id,amount_listPrice,amount_retailPrice,
        ((amount_listPrice - amount_retailPrice)/amount_listPrice)*100 as discount_percent from books_data where 
        ((amount_listPrice - amount_retailPrice)/amount_listPrice)*100 > 0.2""",
        qn_seven : 'select isEbook,avg(pageCount) as avg_pageCount from books_data group by isEbook',
        qn_eight : 'select book_authors,count(book_id) as total_books from books_data where book_authors != "N/A" group by book_authors order by total_books desc limit 3',
        qn_nine : 'select publisher,count(book_id) as total_books from books_data where publisher != "N/A" group by publisher having count(*)>10',
        qn_ten : 'select categories,avg(pageCount) as avg_page_count from books_data group by categories order by avg(pageCount) desc limit 10',
        qn_eleven : 'select book_id,count(book_authors) as author_count from books_data group by book_id having count(book_authors)>3',
        qn_twelve : 'select book_id,book_title,ratingsCount,averageRating from books_data where ratingsCount > averageRating',
        qn_thirteen : """select book_authors,extract(year FROM year) as year,group_concat(book_title) AS book_titles,count(*) AS book_count
        from books_data where book_authors != 'N/A' AND extract(year FROM year) is not null group by 
        book_authors,extract(year FROM year) having count(*) > 1""",
        qn_fourteen : 'select book_id,book_title,book_authors from books_data where book_title like "%Learning" ',
        qn_fifteen : """select extract(year FROM year) as year,avg((amount_listPrice + amount_retailPrice)/2) as avg_price
        from books_data  group by year order by avg_price desc limit 3""",
        qn_sixteen : """ select count(distinct b1.book_authors) as author_count from books_data b1 where exists (
        select 1 from books b2 where b1.book_authors = b2.book_authors and extract(YEAR FROM b2.year) = extract(YEAR FROM b1.year) + 1)
        and exists (SELECT 1 FROM books b3 where b1.book_authors = b3.book_authors 
        and extract(YEAR FROM b3.year) = extract(YEAR FROM b1.year) + 2)""",
        qn_seventeen : """ select book_authors,extract(year from year) as year,count(*) AS book_count from books_data  where book_authors !='N/A' and extract(year from year) is not null
        group by book_authors,extract(year from year) having count(DISTINCT publisher) > 1""",
        qn_eighteen : 'select avg(CASE WHEN isEBook THEN amount_retailPrice END) as avg_ebook_price,avg(CASE WHEN !isEBook THEN amount_retailPrice END) as avg_physical_price from books_data',
        qn_nineteen : """ with findStdDev as (select avg(averageRating) as avg_rating,stddev(averageRating) as stddev_rating from books) 
        select book_title,averageRating,ratingsCount FROM books_data, findStdDev where
        abs(averageRating - findStdDev.avg_rating) > 2 * findStdDev.stddev_rating limit 20""",
        qn_twenty : """select publisher,avg(averageRating) as avg_rating,count(book_id) as no_of_books_published from books_data where publisher != 'N/A'
        group by publisher having count(book_id) >10 order by avg(averageRating) desc"""
        }
        return questionMap.get(question)

# Function to get books data using Google Books API
def get_books_data(query):
    #Google API Key(Replace with your key)
    api_key = "AIzaSyBjehTwSPqe6wCYi_mL4TgmwoAyst5oADI"

    #URL for Google Books API
    url = "https://www.googleapis.com/books/v1/volumes"

    max_results = 40
    all_books_data = []
    start_index = 0 
    while len(all_books_data) < max_results:
        
        # Make the API request
        response = requests.get(url,params={"key":api_key,"q":query,"maxResults":40,"startIndex":start_index})
        if response.status_code != 200:
            print(f"Error fetching data: {response.status_code}")
            break
        
        # Parse the response data to JSON
        books = response.json()
       
        # Check if the 'items' key is in the response
        if 'items' not in books:
            print("No more books found!")
            break
        
        # Extract information for each book
        for book in books['items']:
            volume_info = book.get('volumeInfo', {})
            sale_info = book.get('saleInfo',{})
            book_info = {
                'book_id': book.get('id'),
                'search_key': query,
                'book_title': volume_info.get('title', 'N/A'),
                'book_subtitle': volume_info.get('subtitle', 'N/A'),
                'book_authors': ",".join(volume_info.get('authors', ['N/A'])),
                'book_description': volume_info.get('description', 'N/A'),
                'industryIdentifiers': volume_info.get('industryIdentifiers',[{}])[0].get('type'),
                'text_readingModes': volume_info.get('readingModes', {}).get('text',False),
                'image_readingModes': volume_info.get('readingModes', {}).get('image',False),
                'pageCount': volume_info.get('pageCount',0),
                'categories': ",".join(volume_info.get('categories','N/A')),
                'language': volume_info.get('language','N/A'),
                'imageLinks': volume_info.get('imageLinks',{}).get('thumbnail','N/A'),
                'ratingsCount': volume_info.get('ratingsCount',0),
                'averageRating': volume_info.get('averageRating',0),
                'country': sale_info.get('country','N/A'),
                'saleability': sale_info.get('saleability','N/A'),
                'isEbook': sale_info.get('isEbook',False),
                'amount_listPrice': sale_info.get('listPrice',{}).get('amount',0),
                'currencyCode_listPrice': sale_info.get('listPrice',{}).get('currencyCode','N/A'),
                'amount_retailPrice': sale_info.get('retailPrice',{}).get('amount',0),
                'currencyCode_retailPrice': sale_info.get('retailPrice',{}).get('currencyCode','N/A'),
                'buyLink': sale_info.get('buyLink','N/A'),
                'year': volume_info.get('publishedDate','N/A'),
                'publisher': book.get('volumeInfo', {}).get('publisher', 'N/A'),
            }
            
            # Add the book info to the list
            all_books_data.append(book_info)
            
            # Stop if we have reached the required number of results
            if len(all_books_data) >= max_results:
                break
    df = pd.DataFrame(all_books_data)
    # Save the DataFrame to the database
    connection_string = "mysql+pymysql://root:pritri@localhost:3306/books_scrape"
    engine = create_engine(connection_string)
    df.to_sql(
        name="books_data",        # Name of the table in the database
        con=engine,            # SQLAlchemy engine connection
        index=False,           # Do not include DataFrame index as a column
        if_exists="append",   # Replace the table if it already exists
        chunksize=40           # Number of rows to insert in each chunk (for performance)
    )
    #st.success("Data saved to the database successfully!")
    return df  # Optionally return the DataFrame for further use
    


def validate_books_data(query):
     with st.spinner("Fetching Data..."):
          time.sleep(2)

     book_datas = get_books_data(query)
     if book_datas is None:
          st.error("No books found")
     else:
        st.success("Data fetched successfully..!")

        st.write(book_datas)
    