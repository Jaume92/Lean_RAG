import streamlit as st
import requests
import os
from typing import Dict

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page config
st.set_page_config(
    page_title="Lean AI Assistant",
    layout="wide"
)

# ----------- LIGHT / DARK THEME SUPPORT -----------

theme = st.toggle("Modo oscuro", value=True)

if theme:
    st.markdown("""
    <style>
    html, body, .stApp {
        background: radial-gradient(circle at 50% -20%, #1e293b, #020617);
        color: #e5e7eb;
    }

    /* HERO WOW */
    .hero {
        text-align: center;
        padding: 4rem 0 2.5rem 0;
    }

    .title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(90deg, #60a5fa, #818cf8, #22d3ee);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle {
        color: #94a3b8;
        margin-top: 0.7rem;
        font-size: 1.15rem;
    }

    /* CHAT GLASS CARD */
    .chat-card {
        background: rgba(15, 23, 42, 0.65);
        border: 1px solid rgba(148, 163, 184, 0.18);
        backdrop-filter: blur(18px);
        border-radius: 22px;
        padding: 1.8rem;
        box-shadow: 0 25px 80px rgba(0,0,0,0.55);
        transition: all 0.3s ease;
    }

    .chat-card:hover {
        box-shadow: 0 30px 100px rgba(0,0,0,0.7);
        transform: translateY(-2px);
    }

    /* MESSAGES */
    .msg-user {
        background: linear-gradient(135deg, #2563eb, #4f46e5);
        color: white;
        padding: 0.85rem 1.1rem;
        border-radius: 16px;
        margin: 0.45rem 0;
        text-align: right;
        font-weight: 500;
        box-shadow: 0 8px 25px rgba(37,99,235,0.35);
    }

    .msg-assistant {
        background: rgba(30, 41, 59, 0.9);
        border: 1px solid rgba(148, 163, 184, 0.18);
        padding: 0.85rem 1.1rem;
        border-radius: 16px;
        margin: 0.45rem 0;
    }

    .footer {
        text-align: center;
        color: #64748b;
        margin-top: 3rem;
        font-size: 0.85rem;
    }
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    html, body, .stApp { background:#f8fafc; color:#0f172a; }

    .hero { text-align:center; padding:4rem 0 2.5rem 0; }

    .title {
        font-size: 3rem;
        font-weight: 800;
        letter-spacing: -0.03em;
        background: linear-gradient(90deg, #2563eb, #7c3aed);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .subtitle { color:#475569; margin-top:0.7rem; font-size:1.15rem; }

    .chat-card {
        background:white;
        border:1px solid #e2e8f0;
        border-radius:22px;
        padding:1.8rem;
        box-shadow:0 20px 60px rgba(0,0,0,0.08);
        transition:all .25s ease;
    }

    .chat-card:hover { transform:translateY(-2px); box-shadow:0 25px 70px rgba(0,0,0,0.12); }

    .msg-user {
        background:#2563eb;
        color:white;
        padding:0.85rem 1.1rem;
        border-radius:16px;
        margin:0.45rem 0;
        text-align:right;
        font-weight:500;
    }

    .msg-assistant {
        background:#f1f5f9;
        border:1px solid #e2e8f0;
        padding:0.85rem 1.1rem;
        border-radius:16px;
        margin:0.45rem 0;
    }

    .footer { text-align:center; color:#64748b; margin-top:3rem; font-size:0.85rem; }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------------- API ----------------

def send_chat_message(message: str) -> Dict:
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/chat",
            json={"message": message}
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error backend: {str(e)}")
        return None


def calculate_oee(availability: float, performance: float, quality: float) -> Dict:
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/calculate/oee",
            json={
                "availability": availability,
                "performance": performance,
                "quality": quality
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


def calculate_takt_time(available_time: float, demand: int) -> Dict:
    try:
        response = requests.post(
            f"{BACKEND_URL}/api/calculate/takt-time",
            json={
                "available_time_minutes": available_time,
                "customer_demand_units": demand
            }
        )
        response.raise_for_status()
        return response.json()
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return None


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.markdown("### Lean AI")
    page = st.radio("", ["Chat", "Calculadoras", "Acerca de"])


# ---------------- CHAT PAGE ----------------
if page == "Chat":

    st.markdown('<div class="hero">', unsafe_allow_html=True)
    st.markdown('<div class="title">Lean AI </div>', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="chat-card">', unsafe_allow_html=True)

    if not st.session_state.messages:
        st.markdown("<div style='text-align:center;color:#64748b;padding:2.5rem;font-size:1.05rem'>Haz tu primera pregunta sobre eficiencia, producción u OEE…</div>", unsafe_allow_html=True)

    for message in st.session_state.messages:
        role = message["role"]
        content = message["content"]

        if role == "assistant":
            st.markdown(f'<div class="msg-assistant">{content}</div>', unsafe_allow_html=True)
        else:
            st.markdown(f'<div class="msg-user">{content}</div>', unsafe_allow_html=True)

    st.markdown('</div>', unsafe_allow_html=True)

    if prompt := st.chat_input("Pregunta sobre Lean, eficiencia, pérdidas u OEE…"):
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Pensando…"):
            response = send_chat_message(prompt)

        if response:
            answer = response.get("answer", "No pude generar respuesta.")
            st.session_state.messages.append({"role": "assistant", "content": answer})

        st.rerun()


# ---------------- CALCULATORS ----------------
elif page == "Calculadoras":

    st.markdown('<div class="hero"><div class="title">Calculadoras Lean</div></div>', unsafe_allow_html=True)

    calc_type = st.selectbox("", ["OEE", "Takt Time"])

    if calc_type == "OEE":
        col1, col2, col3 = st.columns(3)

        with col1:
            availability = st.slider("Disponibilidad (%)", 0.0, 100.0, 90.0, 0.1)
        with col2:
            performance = st.slider("Performance (%)", 0.0, 100.0, 95.0, 0.1)
        with col3:
            quality = st.slider("Calidad (%)", 0.0, 100.0, 99.0, 0.1)

        if st.button("Calcular OEE"):
            result = calculate_oee(availability, performance, quality)
            if result:
                st.metric("OEE", f"{result['oee']}%")

    elif calc_type == "Takt Time":
        col1, col2 = st.columns(2)

        with col1:
            available_time = st.number_input("Tiempo disponible (min)", 1.0, value=480.0)
        with col2:
            demand = st.number_input("Demanda (unidades)", 1, value=240)

        if st.button("Calcular Takt Time"):
            result = calculate_takt_time(available_time, demand)
            if result:
                st.metric("Takt Time (min)", f"{result['takt_time_minutes']:.2f}")


# ---------------- ABOUT ----------------
elif page == "Acerca de":

    st.markdown('<div class="hero"><div class="title">Lean AI Assistant</div></div>', unsafe_allow_html=True)

    st.markdown("""
**Lean AI Assistant** es un copiloto de inteligencia artificial diseñado para
mejorar la eficiencia operativa en entornos industriales reales.

Combina conocimiento experto en **Lean Manufacturing**, análisis de procesos y
modelos de IA modernos para ayudar a:

- Detectar pérdidas de producción y oportunidades de mejora
- Analizar indicadores clave como **OEE** y **Takt Time**
- Resolver dudas operativas en tiempo real
- Impulsar la mejora continua basada en datos

Este proyecto forma parte de una línea de desarrollo centrada en la
**aplicación práctica de la inteligencia artificial en industria, operaciones y
optimización de procesos**.

---

### Sobre el desarrollador

Desarrollado por **Jaume RRM** con ayuda de claude, enfocado en la creación de soluciones de
**IA aplicada a operaciones industriales, automatización y mejora continua**.

Puedes ver más proyectos, avances y recursos en su web personal:

👉 https://www.jaumerrm.dev

---

Lean AI Assistant se encuentra en evolución constante hacia un
**copiloto industrial completo**, integrando analítica operativa,
memoria contextual y recomendaciones inteligentes para planta.
""")


# ---------------- FOOTER ----------------
st.markdown('<div class="footer">Lean AI · Industrial Copilot</div>', unsafe_allow_html=True)
