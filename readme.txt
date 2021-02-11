
How to run:
1. Open a terminal and navigate to this directory
2. Run 'python RS.py'
3. Enter a User ID, you can pick one from the list below (but any valid ID will work)
4. Enter other information
5. Allow up to 20 seconds for recommendations to be generated


Here are some user IDs you can use (and the names of the corresponding users):

1. CxDOIDnH8gp9KXzpBHJYXw : Jennifer
2. ELcQDlf69kb-ihJfxZyL0A : Brad
3. bLbSNkLggFnqwNNzzq-Ijw : Stefany
4. d_TBs6J3twMy9GChqUEXkg : Jennifer
5. U4INQZOPSUaj8hMjLlZ3KA : Michael
6. DK57YibC5ShBmqQl97CKog : Karen
7. PKEzKWv_FktMm2mGPjwd0Q : Norm
8. cMEtAiW60I5wE_vLfTxoJQ : Jennifer
9. V-BbqKqO8anwplGRx9Q5aQ : Pepper

I picked these users because they have given the greatest number of reviews of restaurants. 
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
