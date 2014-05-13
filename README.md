Image Crawler
=============

The software traverses through the web in a breadth first fashion, and avoids viewing duplicate pages. In the process, it stores the data of links to be traversed and the ones already traversed in the database. 

Since the hyperlinks being traversed can be very large in number, there is a constraint of 100 imposed on the number of unique hyperlinks being traversed. 

While traversing the web, whenever an image is found, it is downloaded to the folder specified and its details such as height, width, alternate text etc are stored in a table in the database.

Input:
a hyperlink to begin the search

Tech Used:

Python 2.7+

(urllib, urllib2, Image, MySQLdb, re)

MySQL
