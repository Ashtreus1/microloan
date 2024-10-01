import pandas as pd


dummydata = {
	'Budget' : [10000, 20000, 30000, 40000, 50000],
	'Expected Revenue': [20000, 40000, 60000, 80000, 100000],
	'Repayment History': ['Good', 'Excellent', 'Average', 'Good', 'Excellent'],
	'Profit Margins': [10, 12, 8, 15, 13],
	'Savings': [2000, 2500, 3000, 3500, 4000]
}


df = pd.DataFrame(dummydata)


csvfilepath = 'msme_data.csv'
df.to_csv(csvfilepath, index=False)

print("Dummy data successfully seeded!")
