import streamlit as st
import random
import time
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="SCADA Мыло", layout="wide")

# Нормы
TEMP_MIN, TEMP_MAX = 70, 90
PRES_MIN, PRES_MAX = 1.0, 2.5
FLOW_MIN, FLOW_MAX = 5, 10

# Заголовок
st.title("🧪 SCADA-система — Производство хозяйственного мыла")

# Кнопка запуска
start = st.button("▶ Запустить процесс")

# Данные
if "data" not in st.session_state:
    st.session_state.data = {
        "temp": [],
        "pres": [],
        "flow": []
    }

def status(value, min_v, max_v):
    if value < min_v:
        return "🔵 НИЗКО", "blue"
    elif value > max_v:
        return "🔴 ВЫСОКО", "red"
    else:
        return "🟢 НОРМА", "green"

if start:
    for i in range(20):

        temp = random.uniform(69, 91)
        pres = random.uniform(0.9, 2.6)
        flow = random.uniform(4, 11)

        st.session_state.data["temp"].append(temp)
        st.session_state.data["pres"].append(pres)
        st.session_state.data["flow"].append(flow)

        t_status, _ = status(temp, TEMP_MIN, TEMP_MAX)
        p_status, _ = status(pres, PRES_MIN, PRES_MAX)
        f_status, _ = status(flow, FLOW_MIN, FLOW_MAX)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.metric("Температура (°C)", f"{temp:.1f}", t_status)

        with col2:
            st.metric("Давление (МПа)", f"{pres:.2f}", p_status)

        with col3:
            st.metric("Расход (м³/ч)", f"{flow:.1f}", f_status)

        st.divider()

        time.sleep(0.3)

# ГРАФИКИ
if st.session_state.data["temp"]:

    st.subheader("📊 График параметров")

    fig, ax = plt.subplots()

    ax.plot(st.session_state.data["temp"], label="Температура")
    ax.plot(st.session_state.data["pres"], label="Давление")
    ax.plot(st.session_state.data["flow"], label="Расход")

    ax.legend()
    ax.set_xlabel("Время")
    ax.set_ylabel("Значения")

    st.pyplot(fig)

# ПАНЕЛЬ СТАТУСА
st.subheader("🚨 Состояние системы")

last_temp = st.session_state.data["temp"][-1] if st.session_state.data["temp"] else 0
last_pres = st.session_state.data["pres"][-1] if st.session_state.data["pres"] else 0
last_flow = st.session_state.data["flow"][-1] if st.session_state.data["flow"] else 0

if (TEMP_MIN <= last_temp <= TEMP_MAX and
    PRES_MIN <= last_pres <= PRES_MAX and
    FLOW_MIN <= last_flow <= FLOW_MAX):

    st.success("🟢 Система работает в нормальном режиме")
else:
    st.error("🔴 АВАРИЯ! Выход параметров за допустимые пределы")