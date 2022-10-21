import pandas as pd
import streamlit as st
import streamlit.components.v1 as components
import requests
from streamlit_lottie import st_lottie as stlot
import matplotlib.pyplot as plt
# from st_aggrid import AgGrid
# import base64

# Drop unwanted data
df = pd.read_csv("Egypt_Houses_Price.csv")
df.drop(df[df['Price'] == "Unknown"].index, inplace=True)
df.drop(df[df["City"] == "(View phone number)"].index, inplace=True)
df.drop(df[df["Area"] == " "].index, inplace=True)
df.drop(['Compound', 'Payment_Option', 'Delivery_Date', 'Delivery_Term'], axis=1, inplace=True)

# Turn price into int
df['Price'] = pd.to_numeric(df['Price'])
df['Price'] = df['Price'].fillna(0).astype(int)
df.drop(df[df['Price'] == 0].index, inplace=True)

# Turn area into int
df['Area'] = pd.to_numeric(df['Area'])
df['Area'] = df['Area'].fillna(0).astype(int)
df.drop(df[df['Area'] == 0].index, inplace=True)

# Page config
st.set_page_config(layout='wide', page_title="House prices in Egypt", page_icon='🏘️', )
st.title("🏘️Egyptian House Prices sorted by location")
st.subheader("An AI342 assignment by Ahmed Ashraf")
st.markdown("""---""")

# Background image (too distracting)
# @st.experimental_memo
# def get_img_as_base64(file):
#     with open(file, "rb") as f:
#         data = f.read()
#     return base64.b64encode(data).decode()
#
# img = get_img_as_base64("photo.jpeg")
#
# page_bg_img = f"""
# <style>
# [data-testid="stAppViewContainer"] > .main {{
# background-image: url("data:image/png;base64,{img}");
# background-size: 60%;
# background-position: top left;
# background-repeat: repeat;
# background-attachment: fixed;
# </style>"""
#
# st.markdown(page_bg_img, unsafe_allow_html=True)

# Select city

City = st.sidebar.selectbox('Pick your City', sorted(df.City.unique()))

# Select sample size
if len(df[df["City"] == City]) <= 50:
    maxsize = len(df[df["City"] == City])
else:
    maxsize = 50
SampleSize = st.sidebar.slider('Pick a sample size', 0, maxsize)

# Select Price range
SelectedCity = df.groupby("City")
SelectedCity = SelectedCity.get_group(City)
PriceRange = st.sidebar.slider('Pick a Price', 0, max(SelectedCity["Price"]), step=250_000)
SelectedRange = SelectedCity[SelectedCity['Price'] <= PriceRange]

# Math Stuff
HouseAveragePrice = round(SelectedCity["Price"].mean())
STD = round(SelectedCity["Price"].std())
MedianPrice = round(SelectedCity["Price"].median())
MeterPrice = round(sum(SelectedCity.Price) / sum(SelectedCity.Area))


# load Lottie URL
@st.cache
def load_lottieurl(url: str):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


# Load animation
# money animation: https://assets8.lottiefiles.com/packages/lf20_ystsffqy.json
# house animation: https://assets2.lottiefiles.com/private_files/lf30_p5tali1o.json
anim = load_lottieurl('https://assets2.lottiefiles.com/private_files/lf30_p5tali1o.json')

text, animation = st.columns((3, 3))

with animation:
    stlot(anim, key="anim", width=500, height=200,loop=False)

with text:
    # Formatting Text
    st.markdown("")
    PriceRangeFormat = st.markdown("Selected Price: " + "{:,} EGP".format(PriceRange) + " and below")
    HouseAveragePrice = st.markdown("Average house price in {}: ".format(City) + "{:,} EGP".format(HouseAveragePrice))
    MeterPriceFormat = st.markdown("Average price per meter squared in {}: ".format(City) + "{:,} EGP".format(MeterPrice))
    MedianPrice = st.markdown("Median house price: " + "{:,} EGP".format(MedianPrice))
    STD = st.markdown("Standard Deviation: " + "{:,} EGP".format(STD))

# Display Table
try:
    tables = SelectedRange.sample(SampleSize, ignore_index=True)
    st.table(tables)
except:
    st.exception(ValueError("Not enough examples\nTry Selecting a higher price range"))

# Plot
price = SelectedCity['Price']
area = SelectedCity["Area"]

xaxislim=st.sidebar.slider("Limit for X axis (in Millions)", 1.0, float(max(SelectedCity["Price"]) / 1_000_000),step=1.0)

fig, ax = plt.subplots()
ax.scatter(price/1_000_000, area)
plt.title("Area vs Prices in {}".format(City))
plt.xlabel("Price", fontsize=14)
plt.ylabel("Area", fontsize=14)
plt.xlim([0, xaxislim])
st.pyplot(fig)

# link to project on GitHub
st.markdown("""---""")
giturl = 'https://github.com/AhmedAsh4/HousePrices'
st.write("[Project on GitHub]({})".format(giturl))

# Add linkedin
embedComponent = {'linkedin': """<script src="https://platform.linkedin.com/badges/js/profile.js" async defer type="text/javascript"></script>
        <div class="badge-base LI-profile-badge" data-locale="en_US" data-size="medium" data-theme="dark" data-type="VERTICAL" data-vanity="ahmed-ashraf-3a68ab246" data-version="v1"><a class="badge-base__link LI-simple-link" href="https://eg.linkedin.com/in/ahmed-ashraf-3a68ab246?trk=profile-badge></a></div>""",
                  'medium': """<div style="overflow-y: scroll; height:500px;"> <div id="retainable-rss-embed" """}

with st.sidebar:
    components.html(embedComponent['linkedin'], height=320)
