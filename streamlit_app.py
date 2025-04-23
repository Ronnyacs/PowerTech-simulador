import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from math import pi

st.set_page_config(page_title="Simulador PowerTech", layout="centered")
st.title("🚗 Simulador PowerTech - Velocidad por Marcha")

# Entrada de parámetros técnicos
st.subheader("📋 Datos de entrada")
col1, col2 = st.columns(2)

with col1:
    torque = st.number_input("Par máximo (Nm)", value=373)
    rpm_torque = st.number_input("RPM de par máximo", value=3200)
    potencia = st.number_input("Potencia máxima (HP)", value=212)
    rpm_potencia = st.number_input("RPM de potencia máxima", value=4600)

with col2:
    marchas = st.slider("Número de marchas", min_value=1, max_value=6, value=6)
    relacion_diferencial = st.number_input("Relación de diferencial", value=4.1)
    diametro_neumatico = st.number_input("Diámetro del neumático (m)", value=0.6676)
    peso = st.number_input("Peso del vehículo (kg)", value=2600)

st.markdown("---")

# Relaciones de caja
st.subheader("⚙️ Relaciones de caja")
relaciones = []
cols = st.columns(marchas)
default_vals = [4.529, 2.517, 1.519, 1.0, 0.741, 0.620]

for i in range(marchas):
    valor_default = float(default_vals[i]) if i < len(default_vals) else 1.0
    relaciones.append(cols[i].number_input(f"{i+1}ª marcha", value=valor_default, key=f"rel_{i}"))

# Cálculo de velocidades por RPM
st.markdown("---")
st.subheader("📊 Tabla de velocidades por RPM")
rpm_range = np.arange(1000, 5500, 100)
data = {"RPM": rpm_range}

for i, rel in enumerate(relaciones):
    data[f"{i+1}ª"] = [(rpm * pi * diametro_neumatico * 60) / (rel * relacion_diferencial * 1000) for rpm in rpm_range]

df_vel = pd.DataFrame(data)
st.dataframe(df_vel, use_container_width=True)

# Gráfica
st.markdown("---")
st.subheader("📈 Gráfica Velocidad vs RPM")
fig, ax = plt.subplots()
colores = ['blue', 'red', 'green', 'purple', 'deepskyblue', 'orange']

for i in range(marchas):
    ax.plot(df_vel["RPM"], df_vel[f"{i+1}ª"], label=f"{i+1}ª", color=colores[i])

ax.set_xlabel("RPM")
ax.set_ylabel("Velocidad (km/h)")
ax.legend()
ax.grid(True)
st.pyplot(fig)