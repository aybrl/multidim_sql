from cProfile import label
import matplotlib.pyplot as plt
import numpy as np

def get_query_1_visualisation(result_query_1):
    participation = [i[0] for i in result_query_1]
    years = [i[1] for i in result_query_1]

    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))
    
    # Set position of bar on X axis
    br1 = np.arange(len(participation))
    
    # Make the plot
    plt.bar(br1, participation, color ='#f09f0a', width = barWidth,edgecolor ='grey', label ='Droite')
    
    # Adding Xticks
    plt.xlabel('Année', fontweight ='bold', fontsize = 15)
    plt.ylabel('Taux (Votants / inscrits)', fontweight ='bold', fontsize = 15)
    plt.xticks([r + barWidth for r in range(len(participation))], years)

    plt.legend()
    plt.show()

def get_query_2_visualisation(result_query_2):
    participation = [i[0] for i in result_query_2]
    years = [i[1] for i in result_query_2]
    regions = [i[2] for i in result_query_2] 

    # setup the figure and axes
    fig = plt.figure(figsize=(8, 3))
    ax1 = fig.add_subplot(121, projection='3d')
    fig.set_size_inches(18.5, 10.5)

    plt.xlabel('Année', fontweight ='bold', fontsize = 15)
    plt.ylabel('Région', fontweight ='bold', fontsize = 4)
    plt.xlabel('Votes', fontweight ='bold', fontsize = 15)
    ax1.set_title('Participation par année et région')
    ax1.bar(years, regions, zs=participation, zdir='y', color='#232323', alpha=0.8)  

    fig.savefig('./charts/participation_year_region.png', dpi=100)
    plt.show()

def get_query_3_visualisation(result_query_3):
    droite = result_query_3[1]
    gauche = result_query_3[0]

    droite_data = [i[0] for i in droite]
    gauche_data = [i[0] for i in gauche]
    years = [i[1] for i in gauche]

    barWidth = 0.25
    fig = plt.subplots(figsize =(12, 8))
    

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

def get_query_4_visualisation(result_query_4):
    droite = result_query_4[1]
    gauche = result_query_4[0]

    droite_data = [i[0] for i in droite]
    gauche_data = [i[0] for i in gauche]

    regions = [i[2] for i in gauche] 
    years = [i[1] for i in gauche]

    # setup the figure and axes
    fig = plt.figure(figsize=(8, 3))
    ax1 = fig.add_subplot(121, projection='3d')
    ax2 = fig.add_subplot(122, projection='3d')
    fig.set_size_inches(18.5, 10.5)


    plt.xlabel('Année', fontweight ='bold', fontsize = 15)
    plt.ylabel('Région', fontweight ='bold', fontsize = 4)
    plt.xlabel('Votes', fontweight ='bold', fontsize = 15)
    
    ax1.set_title('Évolution par année et région | TENDANCE DROITE')
    ax1.bar(years, regions, zs=droite_data, zdir='y', color='#232323', alpha=0.8)  

    ax2.set_title('Évolution par année et région | TENDANCE GAUCHE')
    ax2.bar(years, regions, zs=gauche_data, zdir='y', color='#221323', alpha=0.8)  

    fig.savefig('./charts/year_region_evolution.png', dpi=100)
    plt.show()


def get_query_5_visualisation(result_query_5):

    result_query_5.sort(key=lambda x: x[1], reverse=True) 
    
    
    departement = list(zip(*result_query_5))[0]
    seuils = list(zip(*result_query_5))[1]
    x_pos = np.arange(len(departement)) 
   
    plt.plot(seuils, linestyle='--', marker='o', color='#eb4034', label='seuil')
    plt.xticks(x_pos, departement, rotation = 90) 
    plt.ylabel('Seuil')
    plt.show()


def get_query_6_visualisation(result_query_6):
    plt.scatter(*zip(*result_query_6))
    plt.xticks(rotation=90)
    plt.show()