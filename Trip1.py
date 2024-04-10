import pandas as pd
import numpy as np
import plotly.express as px
import skimage
import plotly.graph_objects as go

# Read Dataset
df = pd.read_csv("STP/trip1_ABM.csv")
df.head()
df["Longitude"] = df["Longitude"][::-1]

df2 = pd.read_csv("STP/trip1_LCPA.csv")
df2.head()
df2["Longitude"] = df2["Longitude"][::-1]

# Read the basemap
img = skimage.io.imread('STP/trip1_basemap.png')
skimage.io.imshow(img)

x = np.linspace(df.Longitude.min(),df.Longitude.max(), 200)
y = np.linspace(df.Latitude.min(),df.Latitude.max(), 200)
X, Y = np.meshgrid(x,y)
z = np.full(X.shape,df.Time.min())

# fig = px.scatter_3d(df, x='Latitude', y='Longitude', z='Time', color='Destination', hover_data=['Section', 'Date', 'Latitude', 'Longitude'])
# fig.show()

# Rotate the image 
#if img.shape[0] < img.shape[1]:
#    img = np.rot90(img)

img = skimage.transform.resize(img, (x.shape[0], y.shape[0]))
img = np.flipud(img)
img = np.fliplr(img)

# Add the image to the 3d line graph
surfcolor = np.fliplr(img[:, :, 1])

# Page Layout
layout = go.Layout(
    title='Comparsion of Overland Routes and waterways to Pengcheng and Back Home',
    font_family='Balto',
    width=1000,
    height=800,
    )

# Pre-process: Chate Time to datetime format
df.Time = pd.to_datetime(df.Time)
df2.Time = pd.to_datetime(df2.Time)

# Create ABM Path
ABM = go.Scatter3d(
        x = df.Longitude,
        y = df.Latitude,
        z = df.Time,
        name = "Waterway",
        mode ='markers+lines',
        hovertext=["Latitude: "+str(x) +"<br>Longitude: "+ str(y) +"<br>Time: "+str(z.strftime("%m-%d"))  for x,y,z in zip(df.Latitude,df.Longitude,df.Time)],
        hoverinfo='text',
        textposition='top center',
        marker = dict(
         size = 3,
         opacity = 0.8,
        color = "blue"
        )
    )

# Create LCPA path
LCPA = go.Scatter3d(
        x = df2.Longitude,
        y = df2.Latitude,
        z = df2.Time,
        name = "Overland Routes",
        mode ='markers+lines',
        hovertext=["Latitude: "+str(x) +"<br>Longitude: "+ str(y) +"<br>Time: "+str(z.strftime("%m-%d"))  for x,y,z in zip(df2.Latitude,df2.Longitude,df2.Time)],
        hoverinfo='text',
        marker = dict(
         size = 2,
         opacity = 0.8,
        color = "red"
        )
    )


# Combine surface layer, ABM path and LCPA path together
fig = go.Figure(data=[ABM, LCPA], layout=layout)

fig.update_layout(scene = dict(zaxis=dict(range=[df.Time.min(),df.Time.max()])))
surf = go.Surface(x=x, y=y, z=np.full(X.shape,df.Time.min()),
    surfacecolor=surfcolor,
    showscale=False,
    hoverinfo='skip')
fig.add_trace(surf)


fig.update_layout(scene = dict(
                    xaxis_title='Longitude',
                    yaxis_title='Latitude',
                    zaxis_title='Time',
                    zaxis_tickformat = '%m-%d'),
                    width=1200,
                    margin=dict(r=20, b=40, l=30, t=40),
                )

fig.show()


















