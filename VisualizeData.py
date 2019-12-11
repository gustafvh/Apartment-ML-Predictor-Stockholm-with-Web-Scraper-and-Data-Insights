import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
pd.plotting.register_matplotlib_converters()


def showBarChart(df, column):
    plt.figure(figsize=(10, 6))

    plt.title("For every apartment, the " + column)

    sns.barplot(x=df.index, y=df[column])

    plt.ylabel(column)
    plt.xlabel('Index')

    plt.show()


def showHeatMap(df):
    # plt.figure(figsize=(14, 7))

    plt.title("For every apartment")

    # Heatmap showing average arrival delay for each airline by month

    sns.heatmap(data=df, annot=True)

    # Add label for horizontal axis
    plt.xlabel("Columns")

    plt.show()


def showScatterPlotLine(df, col1, col2):
    sns.regplot(x=df[col1], y=df[col2])
    #sns.scatterplot(x=df[col1], y=df[col2], hue=df['Price'])

    plt.show()
