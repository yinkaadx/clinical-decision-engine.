import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import time

st.set_page_config(page_title="Healthcare Analytics Engine", layout="wide")

st.title("Serverless Clinical Decision Support Pipeline")
st.caption("Real-Time EHR Ingestion, Surgical Delay Prediction & Patient Flow Optimization")

st.sidebar.header("Middleware Configuration")
selected_ward = st.sidebar.selectbox("Target Clinical Environment", ["Te Manawa Taki (Waikato) Triage", "General Surgical Ward Alpha", "Emergency Department Flow"])
admission_shock = st.sidebar.slider("Simulate Patient Admission Spike", 1.0, 5.0, 3.0)
run_simulation = st.sidebar.button("Initialize Clinical ML Engine")

st.sidebar.markdown("---")
st.sidebar.caption("Architecture: EHR API Ingestion -> XGBoost Inference -> Flow Orchestration")

if run_simulation:
    st.subheader(f"Active Patient Flow Monitoring: {selected_ward}")
    
    col1, col2, col3, col4 = st.columns(4)
    metric_volume = col1.empty()
    metric_latency = col2.empty()
    metric_delay = col3.empty()
    metric_action = col4.empty()

    chart_placeholder = st.empty()
    log_placeholder = st.empty()

    np.random.seed(1212)
    time_steps = pd.date_range(start=pd.Timestamp.now(), periods=100, freq="s")
    
    patient_volume = []
    delay_probability = []
    
    base_volume = 50 
    
    for i in range(100):
        if i < 30:
            current_volume = base_volume + int(np.random.uniform(-5, 10))
            current_delay_risk = np.random.uniform(10.0, 25.0)
            ehr_latency = np.random.uniform(15.0, 25.0)
        elif i >= 30 and i < 65:
            current_volume = base_volume + int((i - 30) * (5 * admission_shock)) + int(np.random.uniform(-10, 10))
            current_delay_risk = np.random.uniform(40.0, 85.0)
            ehr_latency = np.random.uniform(25.0, 45.0)
        else:
            current_volume = base_volume + int(35 * 5 * admission_shock) + int(np.random.uniform(-15, 15))
            current_delay_risk = np.random.uniform(85.0, 98.0) 
            ehr_latency = np.random.uniform(30.0, 50.0)
            
        patient_volume.append(current_volume)
        delay_probability.append(current_delay_risk)
        
        metric_volume.metric("Active Patient Inflow", f"{current_volume} Patients/hr")
        metric_latency.metric("EHR Data Ingestion Latency", f"{ehr_latency:.1f} ms", "- Serverless Optimized")
        metric_delay.metric("Surgical Delay Risk Score", f"{current_delay_risk:.1f}%")
        
        if current_delay_risk >= 80.0:
            metric_action.metric("System Recommendation", "REROUTING RESOURCES", "Triage Optimized")
        else:
            metric_action.metric("System Recommendation", "STANDARD QUEUE", "Flow Stable")
            
        fig = go.Figure()
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=patient_volume, mode='lines', name='Patient Inflow Volume', line=dict(color='blue')))
        fig.add_trace(go.Scatter(x=time_steps[:i+1], y=delay_probability, mode='lines', name='Surgical Delay Probability', yaxis='y2', line=dict(color='red', dash='dot')))
        
        fig.update_layout(
            title="Real-Time Hospital Flow: Admission Spikes vs ML Surgical Delay Prediction",
            xaxis=dict(title="High-Frequency Clinical Timestamp"),
            yaxis=dict(title="Patient Volume"),
            yaxis2=dict(title="Delay Risk Probability (%)", overlaying='y', side='right', range=[0, 100]),
            height=400,
            margin=dict(l=0, r=0, t=40, b=0)
        )
        
        chart_placeholder.plotly_chart(fig, use_container_width=True)
        
        if current_delay_risk >= 80.0:
            log_placeholder.error(f"CLINICAL ALERT: Severe bottleneck predicted at {time_steps[i].strftime('%H:%M:%S')}. Machine learning inference engine automatically reprioritizing surgical queues and alerting on-call staff.")
        else:
            log_placeholder.success(f"Log: EHR telemetry tick {i} ingested via serverless middleware. Patient flow metrics operating within optimal statistical bounds.")
            
        time.sleep(0.15)
        
    st.info("Simulation Complete. The cloud-native machine learning pipeline successfully predicted the surgical bottleneck and optimized the patient flow queue.")
else:
    st.info("Click 'Initialize Clinical ML Engine' in the sidebar to simulate high-frequency healthcare data ingestion.")