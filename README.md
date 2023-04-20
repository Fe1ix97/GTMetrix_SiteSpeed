# GTmetrix
It is actually a website(https://gtmetrix.com/) where we analyze the Website Performance.After analyzing it will display parameters like 
PageSpeed Score,Page Size,Issues regarding page speed etc.
So,I made a project using GTmetrix API for analyzing the websites.For this project I conducted API test over 6 websites and collected some important result regarding each website and then I have put those data into a Excel File.
Data which I extracted from the API call - 1.PageSpeed Score,2.Yslow Score,3.Fully Loaded Time,4.Toatal Page Size,5.Requests,
6.PageSpeed Issues,7.Yslow Issues
#Sources:Details regarding API - https://gtmetrix.com/api/
         Help regarding how to handle API call with Python - https://github.com/aisayko/python-gtmetrix
         How to write data into Excel file using python - https://www.geeksforgeeks.org/writing-excel-sheet-using-python/
         
#Modules Required for running this program:
1.Install Requests Module(pip install requests)
2.Install xlwt Module(pip install xlwt)
3.Install Six Module(pip install six)
How to Run:-
I have already defined the input - a list of six websites.If you want to add new websites just insert into the list.
Run The Main.py and output will be a Final_Output.xls file which you can save later as per your choice. 
