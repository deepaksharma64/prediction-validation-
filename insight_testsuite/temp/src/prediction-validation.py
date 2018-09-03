import pandas as pd
import numpy as np
import sys

def main():
    script = sys.argv[0]
    Sactual = sys.argv[1]
    Spredicted = sys.argv[2]
    Swindow = sys.argv[3]
    
    actual = pd.read_csv(Sactual, sep="|", header=None,names = ['time','stock','price'])
    predicted = pd.read_csv(Spredicted, sep="|", header=None, names = ['time','stock','price'])
    window = pd.read_csv(Swindow, sep=" ", header=None)
    
    #merge actual and predicted dataset
    merge_df = pd.merge(actual,predicted, on = ['time','stock'], how='left')
    
    #remove NAs
    pred_df = merge_df.dropna() 
    
    #delete rows with duplicate data in 'time' and 'stock' columns 
    pred_df = pred_df.drop_duplicates(['time','stock'], keep=False)
    
    #remove rows with faulty/non-numeric values 
    pred_df = pred_df[pred_df.applymap(np.isreal)]
    pred_df = pred_df.drop(['stock'], axis=1)
    pred_df = pred_df.dropna()
    
    #compute err
    pred_df['err'] = (pred_df['price_y'] - pred_df['price_x']).abs()
    
    #make index values continuous
    pred_df.index = range(len(pred_df))
    
    #compute mean in each of the hour frames 
    comparison_df = pred_df.groupby('time').err.mean() 
    comparison_df = comparison_df.to_frame(name=None)
    freq = pred_df.groupby('time').count()
    
    #compute freq of each of the hour
    comparison_df['freq'] = freq.iloc[:,1] 
    
    #reading value of the given window
    value = window.iloc[0,0]  
    n = len(comparison_df)
    
    #range of valid time frames for mean calculations:
    time = comparison_df.index
    time=time[:-(value-1)]
    
    #create a df with window of time (based on given value) in each rows
    mat_df = pd.DataFrame(np.zeros(((n-value+1), 2)))
    mat_df.iloc[:,0] = time
    mat_df.iloc[:,1]= mat_df.iloc[:,0]+value-1
    
    #computing total error in every hour time frame
    comparison_df['total_err'] = comparison_df['err']*comparison_df['freq']
    
    #compute the mean err values in the given window
    r_list = pd.DataFrame(np.zeros((len(mat_df),1)))
    for i in range(len(mat_df)):
        r_list.iloc[i,:] = sum(comparison_df.total_err[i:i+value])/sum(comparison_df.freq[i:i+value])

    #round to two decimal point and store in the output file by the name comparison  
    comparison = pd.concat([mat_df, r_list], axis=1)
    comparison = comparison.round(2)
    
    comparison1  = sys.argv[4]
    comparison.to_csv(comparison1,sep="|",header=False,index=False)
  
if __name__ == '__main__':
    main()