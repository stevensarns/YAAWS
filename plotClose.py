
import matplotlib.pyplot as plt

def plot():
        try:
                plt.rcParams['figure.figsize'] = [8,2]
                plt.close("all")
        except:
                print("plot.close() fail")
        
