import pandas as pd
import os
import sys

# Full path to folder containing folders of results
path=sys.argv[1]

# If the sample is missing any gene in this list, substitute the gene for the gene found by running
# script "nearest_neighbor.py
if len(sys.argv) > 2:
    gene_list = sys.argv[2]
else:
    gene_list = ['FBgn0003963', 'FBgn0003896','FBgn0264959', 'FBgn0035089','FBgn0035160',
 'FBgn0002945','FBgn0004053','FBgn0011655','FBgn0004650','FBgn0015558']

def read_in_reff():
	for folder in os.listdir(path):
		for filename in os.listdir(f'{path}/{folder}'):
			if filename.endswith('_liftoff'):
				with open(os.path.join(f'{path}/{folder}', filename)) as f:
					df = pd.read_csv(f,sep='\t', header=None)
					print(f"{filename}: started")
					process_file(filename, df)

def process_file(filename, df):
	df.columns=['seqname','source','feature','start','end','Xscore','strand','Xframe','attributes']
# expand the columns and make sure the number is correct 
	try:
		df[['gene id','name','coverage','seqID','copy number','5','6','7','8']]= df.attributes.str.split(";",expand=True,)
	except:
		df[['gene id','name','coverage','seqID','copy number','5','6','7','8','9']]= df.attributes.str.split(";",expand=True,)
		df= df.drop(['9'], axis=1)
		print('expansion error, expanded to 9')
# grab only genes
	df.drop(df[df['feature'] != 'gene'].index, inplace=True)
	df.loc[df['seqname'].str.contains('Ch'), 'seqname'] = df['seqname'].str.replace('Chr-','')
	df = df.drop(df[~df['seqname'].isin(['X', '3L','3R', '2L','2R','4'])].index)

	df= df.drop(['source','attributes','feature','strand','name','coverage','seqID','copy number','Xscore','Xframe','5','6','7','8'], axis=1)
# tidy the values
	df['gene id'] = df['gene id'].str.replace('gene_id ','')
	df['gene id'] = df['gene id'].str.replace('"','')
# get the min and max for list of specific genes
	df = df.drop(df[~df['gene id'].isin(gene_list)].index)

# check for missing genes
	df = (df.sort_values('seqname', ascending=[True]))
	seqnames = df['seqname'].values.tolist()
	seqnames
	if seqnames != ['2L', '2L', '2R', '2R', '3L', '3L', '3R', '3R', 'X', 'X']:
		error = "ERROR"
	else:
		error = None

# print
	df.to_csv(f'boundaries_{filename}.csv', index=False)
	if error != None:
		print(f'ERROR: {seqnames}')

def run():
	read_in_reff()

run()
