use books_scrape;

#1.Check Availability of eBooks vs Physical Books
SELECT isEbook,COUNT(*) AS total_books FROM Books_data GROUP BY isEbook;


#2.Find the Publisher with the Most Books Published
select publisher,
count(book_id) as number_of_books
from books_data
where publisher != '' and publisher is not null and publisher not in ('unknown')
group by publisher
order by number_of_books desc
limit 1;

#3.Identify the Publisher with the Highest Average Rating
select distinct publisher,averageRating from books_data order by averageRating desc;

#4.Get the Top 10 Most Expensive Books by Retail Price
select book_title,amount_retailPrice from books_data order by amount_retailPrice asc limit 10;

#5.Find Books Published After 2010 with at Least 500 Pages
select book_title, book_subtitle,year,pageCount  from books_data where year > 2010 and pageCount >=500;

#6.List Books with Discounts Greater than 20%
select book_title,book_subtitle from books_data where amount_listPrice>(amount_retailPrice-amount_listPrice)/amount_listPrice*0.20;

#7.books_dataFind the Average Page Count for eBooks vs Physical Books
SELECT isEbook, AVG(pageCount) AS average_page_count FROM books_data GROUP BY isEbook;

#8.Find the Top 3 Authors with the Most Books
SELECT book_authors, COUNT(*) AS book_count FROM books_data GROUP BY book_authors ORDER BY book_count DESC LIMIT 3;

#9.List Publishers with More than 10 Books
SELECT publisher, COUNT(*) AS book_count FROM books_data GROUP BY publisher HAVING book_count > 10;

#10. Find the Average Page Count for Each Category
SELECT categories, AVG(pageCount) AS average_page_count FROM books_data GROUP BY categories;

#11.Retrieve Books with More than 3 Authors
SELECT book_title, book_authors FROM books_data WHERE LENGTH(book_authors) - LENGTH(REPLACE(book_authors, ',', '')) + 1 > 3;

#12.Books with Ratings Count Greater Than the Average
SELECT book_title, ratingsCount FROM books_data WHERE ratingsCount > (SELECT AVG(ratingsCount) FROM books_data);

#13.Books with the Same Author Published in the Same Year
SELECT book_authors, year, COUNT(*) AS book_count FROM books_data GROUP BY book_authors, year HAVING book_count > 1;

#14.Books with a Specific Keyword in the Title
SELECT book_title FROM books_data WHERE book_title LIKE '%1%';

#15.Year with the Highest Average Book Price
SELECT year, AVG(amount_listPrice) AS average_price FROM books_data GROUP BY year ORDER BY average_price DESC LIMIT 5;

#16.Count Authors Who Published 3 Consecutive Years
SELECT book_authors, COUNT(DISTINCT year) AS consecutive_years
FROM books_data
GROUP BY book_authors
HAVING MAX(year) - MIN(year) >= 2;

  
#17. Authors Published in Same Year Under Different Publishers
SELECT book_authors, year, COUNT(DISTINCT publisher) AS publisher_count
FROM books_data
GROUP BY book_authors, year
HAVING publisher_count > 1;

#18.Average eBook vs Physical Book Retail Prices
SELECT 
    AVG(CASE WHEN isEbook THEN amount_listPrice END) AS ebook_price,
    AVG(CASE WHEN NOT isEbook THEN amount_listPrice END) AS physicalbook_price
FROM books_data;

#19. Books with Ratings Far from the Mean
WITH stats AS (
    SELECT AVG(averageRating) AS mean_rating, STDDEV(averageRating) AS stddev_rating
    FROM books_data
)
SELECT book_title, averageRating, ratingsCount
FROM books_data, stats
WHERE ABS(averageRating - mean_rating) > 2 * stddev_rating;

#20.Publisher with Highest Average Rating (More than 10 Books)
SELECT publisher, AVG(averageRating) AS average_rating, COUNT(*) AS book_count
FROM books_data
GROUP BY publisher
HAVING book_count > 10
ORDER BY average_rating DESC
LIMIT 1;

#test
select book_title  from books_data;
