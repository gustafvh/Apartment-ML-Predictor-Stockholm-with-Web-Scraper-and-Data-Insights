import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
pd.plotting.register_matplotlib_converters()


def showBarChart(df, column):
    plt.figure(figsize=(10, 6))

    plt.title("For every apartment, the " + column)

    sns.barplot(x=df.index, y=df[column])

    plt.ylabel(column)
    plt.xlabel('Index')

    plt.show()


def showHeatMap(df):

    df.set_index('Size')

    print(df.info())

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


def plotPredictionsTowardsActual(dfA, dfB):

    plt.title('Graph from plotScatterGraphMultiple()')
    plt.axis([100000, 14700000, 100000, 14700000])
    plt.scatter(dfA, dfB)

    z = np.polyfit(dfA, dfB, 1)
    p = np.poly1d(z)
    plt.plot(dfA, p(dfA), "r--")

    plt.show()


def plot3DWireframe(df):

    x = df['Longitude']
    y = df['Latitude']
    Z = df['PricePerKvm']

    def z_function(x, y):
        return np.sin(np.sqrt(x ** 2 + y ** 2))

    #x = np.linspace(-6, 6, 30)
    #y = np.linspace(-6, 6, 30)

    X, Y = np.meshgrid(x, y)
    Z = z_function(X, Y)

    fig = plt.figure()
    ax = plt.axes(projection="3d")
    ax.plot_wireframe(X, Y, Z, color='green')
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    ax = plt.axes(projection='3d')
    ax.plot_surface(X, Y, Z, rstride=1, cstride=1,
                    cmap='winter', edgecolor='none')
    ax.set_title('surface')

    plt.show()


def plotThreeDimensionsGraph(df):

    df.columns = ["Latitude", "Longitude", "PricePerKvm"]

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.plot_trisurf(df['Longitude'], df['Latitude'], df['PricePerKvm'],
                    cmap=plt.cm.viridis, linewidth=0)
    plt.show()

    surf = ax.plot_trisurf(df['Longitude'], df['Latitude'], df['PricePerKvm'],
                           cmap=plt.cm.viridis, linewidth=0)
    fig.colorbar(surf, shrink=0.5, aspect=5)
    plt.show()

    # Rotate view
    ax.view_init(30, 45)

    ax.plot_trisurf(df['Longitude'], df['Latitude'], df['PricePerKvm'],
                    cmap=plt.cm.jet, alpha=0.2, linewidth=0, antialiased=True)
    plt.show()
