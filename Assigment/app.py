import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Function to integrate acceleration to velocity and then to position
def get_positions(imu_data, sampling_rate):
    imu_data[['Acc_x', 'Acc_y', 'Acc_z']] *= 9.81 # Convert acceleration to m/s^2 if needed (assuming input in g)
    velocities = np.cumsum(imu_data[['Acc_x', 'Acc_y', 'Acc_z']] / sampling_rate, axis=0) # Integrating acceleration to get velocity
    positions = np.cumsum(velocities / sampling_rate, axis=0) # Integrating velocity to get position
    return positions

# Streamlit UI
st.title("IMU Trajectory Visualization")

# File upload
uploaded_file = st.file_uploader("IMU dataset (csv format)", type="csv")
sampling_rate = st.number_input("Sampling Rate (Hz)", value=100)

if uploaded_file is not None:
    # Read the file
    imu_data = pd.read_csv(uploaded_file)
    
    # Get Positions
    positions = get_positions(imu_data, sampling_rate)
    
    # Convert position to NumPy array
    positions = positions.to_numpy()
    
    # Debugging: Print shape of position array
    st.write("Position array shape:", positions.shape)
    
    try:
        # Plotting
        st.subheader("Trajectory Plot")
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        
        ax.plot(positions[:, 0], positions[:, 1], positions[:, 2], label='Device Trajectory')
        ax.set_xlabel('X Position (m)')
        ax.set_ylabel('Y Position (m)')
        ax.set_zlabel('Z Position (m)')
        ax.legend()
        
        st.pyplot(fig)
    
    except IndexError as e:
        st.error(f"Indexing error occurred: {e}")

    # Display data if needed
    if st.checkbox("Show raw data"):
        st.write(imu_data)
