import sys
import pandas as pd
import time
from markov import Markov, identify_speaker
import seaborn as sns
import matplotlib.pyplot as plt

if __name__ == "__main__":
    
    #Command line input:

    #If first argument is p, performance mode
    if sys.argv[1] == 'p':

        speech1 = open(sys.argv[2], 'r').read()
        speech2 = open(sys.argv[3], 'r').read()
        speech3 = open(sys.argv[4], 'r').read()
        order = int(sys.argv[5])
        num_runs = int(sys.argv[6])

        #Num of rows in dataframe
        num_rows = order*2

        #Row index of dataframe
        row_idx = 0

        #Create empty dataframe with columns
        column_names = ['state', 'k', 'avg_time']
        df = pd.DataFrame(columns=column_names, index=range(num_rows))

        #List of implementation
        implement_lst = ['Hashtable', 'dict']

        #Iterate thru each state
        for l in implement_lst:
            #Iterate thru 1 to k value
            for i in range(1, order + 1):
              
                #List to hold elapsed times of runs
                elapsed_times = []

                #Iterate thru num of runs
                for j in range(1, num_runs + 1):
                  
                    #Find elapsed time
                    start = time.perf_counter()
                    tup = identify_speaker(speech1, speech2, speech3, i, l)
                    end = time.perf_counter()
                    elapsed_time = float(f'{end - start:0.4f}')

                    #Append to list
                    elapsed_times.append(elapsed_time)

                avg_time = sum(elapsed_times)/len(elapsed_times)


                #Append row to dataframe
                new_row = {'state': l, 'k': i, 'avg_time': avg_time}
                df.iloc[row_idx] = new_row

                #Increment row index
                row_idx += 1
                   
        #Create seaborn point plot
        axes = sns.pointplot(x=df['k'], y=df['avg_time'], hue=df['state'], linestyle='-', marker='o')
        axes.set_title('Hashtable vs Python dict')
        axes.set_ylabel('Average Time (Runs=' + str(num_runs)+ ')')
        axes.set_xlabel('K')
        axes.legend(title='Lines')

        #To remedy parts of the plot being cut out
        plt.tight_layout()

        #Save plot into png file
        plt.savefig("execution_graph.png")

    #Else, normal mode
    else:
        speech1 = open(sys.argv[1], 'r').read()
        speech2 = open(sys.argv[2], 'r').read()
        speech3 = open(sys.argv[3], 'r').read()
        order = int(sys.argv[4])
        state = int(sys.argv[5])

        #Call identify_speaker to get tuple of probabilities
        prob_tup = identify_speaker(speech1, speech2, speech3, order, state)

        print('Speaker A:', prob_tup[0])
        print('Speaker B:', prob_tup[1])
        print('\n')
        print('Conclusion: Speaker ' + prob_tup[2] + ' is most likely')