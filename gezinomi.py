""""
Kural Tabanlı Sınıflandırma ile Potansiyel Müşteri Getirisi Hesaplama Gezinomi yaptığı satışların bazı özelliklerini kullanarak seviye tabanlı
(level based) yeni satış tanımları oluşturmak ve bu yeni satış tanımlarına göre segmentler oluşturup bu segmentlere göre yeni
gelebilecek müşterilerin şirkete ortalama ne kadar kazandırabileceğini tahmin etmek istemektedir.
Örneğin:
Antalya’dan Herşey Dahil bir otele yoğun bir dönemde gitmek isteyen
bir müşterinin ortalama ne kadar kazandırabileceği belirlenmek
isteniyor.

gezinomi_miuul.xlsx veri seti Gezinomi şirketinin yaptığı satışların fiyatlarını ve bu
satışlara ait bilgiler içermektedir. Veri seti her satış işleminde oluşan kayıtlardan
meydana gelmektedir. Bunun anlamı tablo tekilleştirilmemiştir. Diğer bir ifade ile
müşteri birden fazla alışverişyapmış olabilir.
"""

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)
pd.set_option('display.expand_frame_repr', False)
pd.set_option('display.float_format', lambda x: '%.2f' % x)

data = pd.read_excel("C:/Users/Neziha/Documents/YAZILIM/MIUUL/1_KuralTabanlSnflandrma221012102820-230129-185115/gezinomi_tantm-230304-111358/gezinomi/miuul_gezinomi.xlsx")
data.head()
df = data.copy()


# Soru1 : miuul_gezinomi.xlsx dosyasını okutunuz ve veri seti ile ilgili genel bilgileri gösteriniz..
def check_df(dataframe, head=5):
    print(20 * "*" + "Shape".center(20) + 20 * "*")
    print(dataframe.shape)
    print(20 * "*" + "Types".center(20) + 20 * "*")
    print(dataframe.dtypes)
    print(20 * "*" + "Head".center(20) + 20 * "*")
    print(dataframe.head(head))
    print(20 * "*" + "Tail".center(20) + 20 * "*")
    print(dataframe.tail(head))
    print(20 * "*" + "NA".center(20) + 20 * "*")
    print(dataframe.isnull().sum())
    print(20 * "*" + "Quantiles".center(20) + 20 * "*")
    print(dataframe.describe([0,0.25, 0.50, 0.75, 1]).T)

check_df(df)

# Soru 2:Kaçunique şehirvardır? Frekanslarınedir?
df["SaleCityName"].value_counts()

# Soru 3:Kaç unique Concept vardır?
df["ConceptName"].value_counts()

# Soru4: Hangi Concept’den kaçar tane satış gerçekleşmiş?
# Soru5: Şehirlere göre satışlardan toplam ne kadar kazanılmış?
df.groupby("SaleCityName").agg({"Price": "sum"})

# Soru6:Concept türlerine göre göre ne kadar kazanılmış?
df.groupby("ConceptName").agg({"Price": "sum"})

# Soru7: Şehirlere göre PRICE ortalamaları nedir?
df.groupby("SaleCityName").agg({"Price": "mean"})

# Soru 8:Conceptlere göre PRICE ortalamaları nedir?
df.groupby("ConceptName").agg({"Price": "mean"})

# Soru 9: Şehir-Concept kırılımındaPRICE ortalamalarınedir?
df.groupby(["SaleCityName","ConceptName"]).agg({"Price": "mean"})
#
# Görev 2: SaleCheckInDayDiff değişkenini kategorik bir değişkene çeviriniz.
# • SaleCheckInDayDiff değişkeni müşterinin CheckIn tarihinden ne kadar önce satin alımını tamamladığını gösterir.
# • Aralıkları ikna edici şekilde oluşturunuz.
# Örneğin: ‘0_7’, ‘7_30', ‘30_90', ‘90_max’ aralıklarını kullanabilirsiniz.
# • Bu aralıklar için "Last Minuters", "Potential Planners", "Planners", "Early Bookers“ isimlerini kullanabilirsiniz.
df["EB_Score"] = pd.cut(df["SaleCheckInDayDiff"],bins=[-1,7,30,90,df["SaleCheckInDayDiff"].max()], labels=["Last Minuters", "Potential Planners", "Planners", "Early Bookers"])
df.tail()

# Şehir-Concept-EB Score, Şehir-Concept- Sezon, Şehir-Concept-CInDay kırılımında ortalama ödenen ücret ve yapılan işlem sayısı cinsinden
# inceleyiniz ?
df.groupby(["SaleCityName","ConceptName","EB_Score"]).agg({"Price": ["mean","count"]})
df.head()

# Görev 4: City-Concept-Season kırılımının çıktısını PRICE'a göre sıralayınız.
df2 = df.groupby(["SaleCityName","ConceptName","Seasons"]).agg({"Price": "mean"}).sort_values("Price",ascending=False)
df2.head()
df2.reset_index(inplace=True)

# Görev 6: Yeni seviye tabanlı müşterileri (persona) tanımlayınız.
df2["sales_level_based"] = pd.DataFrame([["SaleCityName"]].+"_"+df2["ConceptName"]+"_"+df2["Seasons"])
df2["sales_level_based"] = df2["sales_level_based"].apply(lambda x: x.upper())
df2.drop("sales_level_based2", axis= 1, inplace=True)

# Görev 7: Yeni müşterileri (personaları) segmentlere ayırınız.
df2["segment"] = pd.qcut(df2["Price"],4,labels=("D","C","B","A"))
df2.groupby("segment").agg({"Price": ["mean", "max", "sum"]}).sort_values('segment',ascending=False)


# Görev 8: Yeni gelen müşterileri sınıflandırıp, ne kadar gelir getirebileceklerini tahmin ediniz.
new_user = "GIRNE_HERŞEY DAHIL_HIGH"
df2[df2["sales_level_based"] == new_user]["Price"].mean()
df2.loc[df2["sales_level_based"] == new_user,["Price","segment"]]