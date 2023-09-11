import pandas as pd  
import plotly.express as px

from nicegui import ui

df = pd.read_csv('.\data.csv')
fig1 = px.bar(df, x='name', y='value')  
fig2 = px.pie(df, names='name', values='value')  

def print_hello(in_label):
    in_label.set_text('Hello!')

ui.markdown('## My first nicegui app')

ui.markdown('### Bar chart')
ui.plotly(fig1)

ui.markdown('### Pie chart')
ui.plotly(fig2)

ui.markdown('### Button')
change_label = ui.label('Click the button to say hello')
ui.button('Click me', on_click=lambda: print_hello(change_label))

# run
ui.run(reload=True)