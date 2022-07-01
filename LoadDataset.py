import pandas as pd

def loadDataset(file_location, format):
    if(format == 'csv'):
        return pd.read_csv(file_location)
    elif(format == 'tsv'):
        return pd.read_csv(file_location, sep='\t')
    elif(format == 'excel'):
        return pd.read_excel(file_location)
    else:
        return 'invalid file type'
