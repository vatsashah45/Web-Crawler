# Web-Crawler
This program crawls a website and analyzes the text of the pages it visits using k-means clustering and sentiment analysis. The program is designed to run on Python 3.7 or later.

## Installation
1. Clone the repository to your local machine.

2. Install the required packages by running the following command in your terminal:
```
pip install -r requirements.txt
```
3. To run the program, navigate to the root directory of the repository and run the following command:
```
python main.py
```

## Usage
The program will crawl the website specified in the crawler.py file and download the text content of each page it visits. It will then analyze the text using k-means clustering and sentiment analysis and output the results to the console.

## Configuration
You can configure the program by modifying the crawler.py file. Specifically, you can change the following variables:

* Url: the URL of the website to crawl
* numberOfPages: the number of pages to crawl
* blacklist: a list of HTML tags to exclude from the extracted text

You can also configure the k-means clustering by modifying the following variables in the main.py file:

* n_clusters: the number of clusters to use in the clustering algorithm

## Output
The program will output two tables to the console, one for each clustering run. Each table will contain the following columns:

* cluster: the ID of the cluster to which the page was assigned
* pages: the text content of the page
* scores: the sentiment score of the page
* sentiments: the sentiment label of the page (positive, negative, or neutral)

The program will also output a table showing the average sentiment score for each cluster.
