import streamlit as st
import re
import pandas as pd
import plotly.graph_objects as go

def extract_data_from_log(file_content):
    pattern = r"Iter:\s+(\d+)\s+\|\s+Avg Reward:\s+([-\d.]+)\s+\|\s+Avg Return:\s+([-\d.]+)\s+\|\s+Avg Value:\s+([-\d.]+)\s+\|\s+Avg Episode Length:\s+([-\d.]+)"
    data = {'Iteration': [], 'Avg Reward': [], 'Avg Return': [], 'Avg Value': [], 'Avg Episode Length': []}

    for line in file_content:
        match = re.search(pattern, line)
        if match:
            data['Iteration'].append(int(match.group(1)))
            data['Avg Reward'].append(float(match.group(2)))
            data['Avg Return'].append(float(match.group(3)))
            data['Avg Value'].append(float(match.group(4)))
            data['Avg Episode Length'].append(float(match.group(5)))

    return pd.DataFrame(data)

def moving_average(data, window_size):
    return data.rolling(window=window_size).mean()

def plot_metric(df, metric, window_size):
    ma_df = moving_average(df, window_size)
    fig = go.Figure()

    # Add traces for raw data and moving average
    fig.add_trace(go.Scatter(x=df['Iteration'], y=df[metric], mode='lines', name=metric))
    fig.add_trace(go.Scatter(x=df['Iteration'], y=ma_df[metric], mode='lines', name=f'{metric} (MA)'))

    # Update layout
    fig.update_layout(title=f'{metric} and Moving Average',
                      xaxis_title='Iteration',
                      yaxis_title=metric)
    return fig

# Streamlit app
st.title("UE5 Learning to Drive Data Visualizer")

uploaded_file = st.file_uploader("Upload your log file", type=["log"])
window_size = st.slider("Select window size for moving average", min_value=1, max_value=100, value=10)

if uploaded_file is not None:
    file_content = uploaded_file.readlines()
    file_content = [line.decode("utf-8") for line in file_content]
    
    df = extract_data_from_log(file_content)

    st.header("Average Reward")
    st.plotly_chart(plot_metric(df, 'Avg Reward', window_size), use_container_width=True)

    st.header("Average Return")
    st.plotly_chart(plot_metric(df, 'Avg Return', window_size), use_container_width=True)

    st.header("Average Value")
    st.plotly_chart(plot_metric(df, 'Avg Value', window_size), use_container_width=True)

    st.header("Average Episode Length")
    st.plotly_chart(plot_metric(df, 'Avg Episode Length', window_size), use_container_width=True)
