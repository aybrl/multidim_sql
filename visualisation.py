from cProfile import label
import matplotlib.pyplot as plt
import numpy as np


def get_query_4_visualisation(result_query_4):
    droite = result_query_4[1]
    gauche = result_query_4[0]

    droite_data = [i[0] for i in droite]
    gauche_data = [i[0] for i in gauche]
    years = [i[1] for i in gauche]

    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))
    
    # Set position of bar on X axis
    br1 = np.arange(len(droite_data))
    br2 = [x + barWidth for x in br1]
    
    # Make the plot
    plt.bar(br1, droite_data, color ='#f09f0a', width = barWidth,edgecolor ='grey', label ='Droite')
    plt.bar(br2, gauche_data, color ='#5416f2', width = barWidth,edgecolor ='grey', label ='Gauche')
    
    # Adding Xticks
    plt.xlabel('Année', fontweight ='bold', fontsize = 15)
    plt.ylabel('Votes', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(droite_data))], years)
    
    plt.legend()
    plt.show()

def get_query_5_visualisation(result_query_5):

    # sort in-place from highest to lowest
    result_query_5.sort(key=lambda x: x[1], reverse=True) 

    # save the names and their respective scores separately
    # reverse the tuples to go from most frequent to least frequent 
    departement = list(zip(*result_query_5))[0]
    seuils = list(zip(*result_query_5))[1]
    x_pos = np.arange(len(departement)) 

    # calculate slope and intercept for the linear trend line
    slope, intercept = np.polyfit(x_pos, seuils, 1)
    trendline = intercept + (slope * x_pos)

    plt.plot(x_pos, trendline, color='red', linestyle='--')    
    plt.bar(x_pos, seuils,align='center')
    plt.xticks(x_pos, departement, rotation = 90) 
    plt.ylabel('Seuil')
    plt.show()


def get_query_6_visualisation(result_query_6):
    plt.scatter(*zip(*result_query_6))
    plt.xticks(rotation=90)
    plt.show()