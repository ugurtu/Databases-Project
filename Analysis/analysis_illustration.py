import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from Connector import Connector
from adjustText import adjust_text
import probabilities


def month_bar():
    # a = probabilities.month()
    # a.groupby("Month").count().reset_index("Amount")
    """
    # sns.barplot(a)
    sns.set_theme()
    cases_and_accidents = pd.DataFrame()
    df = pd.read_csv("Hotspot.csv")
    cases_and_accidents["Speed Violations"] = df["Amount of violations in street"]
    cases_and_accidents["Accidents"] = df["Accidents in total"]
    N = len(cases_and_accidents["Speed Violations"])
    color = (np.random.rand(N))
    text = df["Accidents in total"].tolist()
    y_text =[cases_and_accidents["Accidents"]]
    print(text)
    area = 2 * cases_and_accidents["Accidents"] ** 1.25
    #plt.scatter(cases_and_accidents["cases"], cases_and_accidents["Accidents], s=area, c=color, alpha=0.5)
    x = np.array(cases_and_accidents["Speed Violations"])
    y = cases_and_accidents["Accidents"]
    m, b = np.polyfit(x, y, deg=1)
    print(m,b)
    plt.axline(xy1=(0, b), slope=m, color="blue", alpha=0.5) #label=f"y={m:.2f}x{b:+.2f}")
    sns.scatterplot(data=cases_and_accidents,x="Speed Violations",y="Accidents",s=75,alpha=0.7,color="red")
    texts = []
    for i, txt in enumerate(text):
        texts.append(plt.annotate(txt, (cases_and_accidents["Speed Violations"][i], cases_and_accidents["Accidents"][i])))
    adjust_text(texts)

    plt.legend()
    plt.title("Scatter plot for hotspots")
    plt.grid(True)
    plt.savefig("ScatterPlot.png")
    plt.show()
    """
    sns.set_theme()
    df = pd.read_csv("CSVs/Exceeding30%.csv")
    df2 = pd.read_csv("CSVs/Exceeding50%.csv")

    merged = pd.merge(df,df2,on="Wohnviertel",how="left").fillna(0)
    merged.to_csv("merged.csv")



    width = 0.5
    X_axis = np.arange(len(merged["Wohnviertel"].tolist()))
    fig = plt.figure()
    ax = fig.add_subplot(111)

    team = ['Team 1', 'Team 2', 'Team 3']
    list_30 = merged["Amount"].tolist()
    list_50 = merged["Amount50"].tolist()
    print(merged["Amount50"])
    x_axis = np.arange(len(merged["Wohnviertel"]))


    ax = plt.subplots()
    # plotting columns
    ax = sns.barplot(x=merged["Wohnviertel"], y=merged["Amount"],color="blue",alpha=0.7,label="30 Zone")
    ax = sns.barplot(x=merged["Wohnviertel"], y=merged["Amount50"],color="skyblue",alpha=0.7,label="50 Zone")

    # renaming the axes
    ax.set(ylabel="Amount of Exceeding")
    plt.xticks(rotation=90)
    plt.title("Exceeding in districts")
    plt.tight_layout()
    ax.legend()
    # visualizing illustration
    plt.show()
    plt.savefig("DistrictsAndZones.png")

    plt.title("Accidents in district sorted after total")
    plt.figure(figsize=(16, 16))
    acc = pd.read_csv("CSVs/Accidents_District.csv")
    acc = acc.sort_values("Total")
    wv = acc["Wohnviertel"].tolist()
    total = acc["Total"].tolist()

    # creating the bar plot
    plt.barh(wv, total, color='maroon',alpha=0.6)
    plt.grid(True)
    plt.xlabel("Accidents")
    plt.savefig("AccidentsInDistrict.png")
    plt.show()

    a = Connector()
    query = """ select q.Wohnviertel, a.category ,count(*) as anzahl
                from Integrated.Accidents as a,
                     Integrated.Events as e,
                     Integrated.Locations as l,
                     Integrated.Quartier as q
                where a.event_id = e.event_id
                and e.location_id = l.location_id
                and l.Street = q.Strassenname
                group by q.Wohnviertel, a.category;"""
    df = pd.DataFrame(a.execute(query),columns=["wohn","acc","amount"])
    print(df)
    print(df.head())
    print(df.columns)

    # plotting columns
    #ax = sns.barplot(df, color="blue", alpha=0.7, label="30 Zone")
    df.plot()
    plt.show()


if __name__ == "__main__":
    month_bar()
