from matplotlib import pyplot as plt
import pandas as pd



if __name__ == '__main__':
    data_dict = {}
    data_dict['category'] = ['Survey 1', 'Survey 2']
    data_dict['lower'] = [0.55, 0.67]
    data_dict['middle'] = [0.67, 0.78]
    data_dict['upper'] = [0.79, 0.89]
    dataset = pd.DataFrame(data_dict)
    for lower, middle, upper, y in zip(dataset['lower'], dataset['middle'], dataset['upper'], range(len(dataset))):
        plt.plot((lower,middle, upper), (y, y, y), 'ro-', color='orange')
        plt.annotate(lower,(lower,y),ha='left')
        plt.annotate(middle,(middle,y),ha='left')
        plt.annotate(upper,(upper,y),ha='left')

    plt.yticks(range(len(dataset)), list(dataset['category']))
    plt.suptitle("Comparison of 95% Confidence Intervals of Both Survey")
    plt.show()