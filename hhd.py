import pandas as pd

df=pd.read_excel("data/my_new.xlsx")
df2=pd.read_excel("data/my_analysis.xlsx")


year=[2014,2015,2016,2017,2018,2019,2020,2021,2022,2023]
new_raw=[]
emirates=["Sharjah","Abu Dhabi","Ajman","Ras Al Khaimah","Dubai","Umm al-Quwain","Al Fujairah"]
for y in year:
    for e in emirates:
        new_raw.append(e)
        new_raw.append(y)
        gender=["Male","Female"]
        type=['Mentality','Auditory', 'Autism', 'Physical','Multiple' ,'Visual','Psychological', 'Communication','Audio-visual','Lack of attention and excessive activity']
        df_year=df[(df["year"]==y)&
            (df["Emirate2"]==e)]
        print(y,e)
        for gen in gender:
            new_raw.append(len(df_year[(df_year["Gender"] == gen)]))
        for i in type:
            new_raw.append(len(df_year[(df_year["DisabilityCategory2"]==i)]))
        new_raw.append(len(df_year))

        df2.loc[len(df2)]=new_raw
        df2.to_excel("data/my_analysis.xlsx",index=False)
        new_raw.clear()







