
How to run:
1. Open a terminal and navigate to this directory
2. Run 'python RS.py'
3. Enter a User ID, you can pick one from the list below (but any valid ID will work)
4. Enter other information
5. Allow up to 20 seconds for recommendations to be generated


Here are some user IDs you can use (and the names of the corresponding users):

1. bLbSNkLggFnqwNNzzq-Ijw : Stefany
2. U4INQZOPSUaj8hMjLlZ3KA : Michael
3. CxDOIDnH8gp9KXzpBHJYXw : Jennifer
4. PKEzKWv_FktMm2mGPjwd0Q : Norm
5. MMf0LhEk5tGa1LvN7zcDnA : Deni
6. DK57YibC5ShBmqQl97CKog : Karen
7. Lfv4hefW1VbvaC2gatTFWA : DJ
8. zFYs8gSUYDvXkb6O7YkRkw : Joyce
9. dIIKEfOgo0KqUfGQvGikPg : Gabi

I picked these users because they have given the greatest number of useful reviews of restaurants. 
Thus I avoid the cold-start problem.


Python modules imported:
1. json
2. surprise
3. texttable
4. pandas


Processed data files used:
1. users.json
2. businesses.json
3. covid.json
4. cities/*city*.json (10 files)
5. reviews.csv

The file 'filter.py' contains functions that I used for data preparation, 
it is not required for the system to run but I have included it to demonstrate 
my extensive work with the data. 
