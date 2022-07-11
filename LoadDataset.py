import pandas as pd

# Load dataset using pandas
def loadDataset(file_location, format):
    if(format == 'csv'):
        # if file is in csv format.
        return pd.read_csv(file_location)
    elif(format == 'tsv'):
        #if file is in tsv fromat
        return pd.read_csv(file_location, sep='\t')
    elif(format == 'excel'):
        #if is in excel format
        return pd.read_excel(file_location)
    else:
        return 'invalid file type'
