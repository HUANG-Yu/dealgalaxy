# dealgalaxy
This is the project I did during the seven-week <a href="http://insightdataengineering.com/">Insight Data Engineering Fellows Program </a>
which helps recent grads and experienced software engineers learn the latest open source technologies 
by building a data platform to handle large datasets. <br/>
DealGalaxy is batch platform that helps optimizing online shopping experience. The platform gives
you daily cheapest price. A website can be found at <a href="http://www.dealgalaxy.site:5000"> www.dealgalgaxy.site</a>

## Introduction
This is an application developed using Amazon Web Service. 
It calculates the website discount everyday by adding cash back percentage from ebates website, gift card discount from ebay website
and the coupon discount.
Then it applies the website discount to the item selling on those shopping websites and calculates the cheapest price for an item.

## Data Pipeline
![alt tag](https://github.com/HUANG-Yu/dealgalaxy/blob/master/pipeline.png)

Python script (using multithreading) runs at midnight and then pushes data into S3, using the AWS Python SDK. Then AWS Data Pipeline runs to pull data from S3 to RedShift, where there is another Python script running to update the website total discount and item discount price using the current day’s information. Then Flask is used as web server to visualize information.

<b> RedShift </b> is used for Batch Processing because RedShift combines the power of both relational database and columnar database in a distributed manner. The scraping scrape about 7GB data every day, and the past data is saved for analysis and predictions.

## Website Snapshot
<b>1) Finding the cheapest price for an item</b>
![alt tag](https://github.com/HUANG-Yu/dealgalaxy/blob/master/snapshot01.png)
<b>2) Visualize the past cash back information</b>
![alt tag](https://github.com/HUANG-Yu/dealgalaxy/blob/master/snapshot02.png)

<p>The website is also able to answer the following questions:</p>
<p> <b>3) Current day's trending website, which offers the biggest discount </b> </p>
<p> <b>4) Ebay Gift Card Buy-It-Now percentage and total number </b> </p>

