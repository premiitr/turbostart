import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to get position by integrating velocity and velocity by integrating acceleration
# Intuition:
#    acceleration(a), velocity(v), time(t) or 1/Hz
#    v = ∫adt = Σa.t = Σ(a/sampling_rate)
#    s = ∫vdt = Σv.t = Σ(v/sampling_rate)

def get_positions(df, sr):
    velocities = np.cumsum(df[['Acc_x', 'Acc_y', 'Acc_z']] / sr, axis=0) # Integrating acceleration to get velocity
    positions = np.cumsum(velocities / sr, axis=0) # Integrating velocity to get position
    return positions.to_numpy() # Converting to numpy array

# Streamlit UI
st.title("IMU Trajectory Visualization")

file_path = 'IMU_Data_1.csv'
sampling_rate = 100

# Read the file
df = pd.read_csv(file_path)
    
# Get Positions
positions = get_positions(df, sampling_rate)
positions = positions/1000.0
try:
    # Plotting
    st.subheader("Trajectory Plot")
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
        
    ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], label='Device Trajectory')

    ax.set_xlabel('X (units)', fontsize=10)
    ax.set_ylabel('Y (units)', fontsize=10)
    ax.set_zlabel('Z (units)', fontsize=10)
    ax.legend()

    st.pyplot(fig)
    
except Exception as e:
    st.error(f"Error occurred: {e}")
