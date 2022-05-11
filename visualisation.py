import matplotlib.pyplot as plt


def get_query_6_visualisation(result_query_6):
    plt.scatter(*zip(*result_query_6))
    plt.xticks(rotation=90)
    plt.show()
