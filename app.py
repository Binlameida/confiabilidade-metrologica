import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# ------------------- INICIALIZAÇÃO DA SESSÃO -------------------
if "mostrar_resultado" not in st.session_state:
    st.session_state.mostrar_resultado = False

# ------------------- CONFIGURAÇÃO DA PÁGINA -------------------
st.set_page_config(page_title="Confiabilidade Metrológica", layout="centered")
st.title("Calculadora Estatística")
st.write("Insira dados para calcular média, variância, desvio padrão, incertezas e visualizar gráficos.")

# ------------------- INTERFACE INICIAL -------------------
st.subheader("1. Escolha a quantidade de valores e insira os dados")
qtd = st.selectbox("Selecione a quantidade de valores (2 a 50):", options=list(range(2, 51)), key="qtd")

valores = []
for i in range(qtd):
    num = st.number_input(f"Valor {i+1}", key=f"valor_{i}")
    valores.append(num)

if st.button("Confirmar e calcular"):
    st.session_state.mostrar_resultado = True
    st.session_state.valores = valores

# ------------------- RESULTADOS -------------------
if st.session_state.mostrar_resultado:
    st.subheader("Resultados Estatísticos")

    dados = np.array(st.session_state.valores)
    n = len(dados)
    media = np.mean(dados)

    # População
    var_pop = np.var(dados)
    desvio_pop = np.std(dados)

    # Amostra
    var_amostral = np.var(dados, ddof=1)
    desvio_amostral = np.std(dados, ddof=1)

    # Incerteza padrão
    u_padrao = desvio_amostral / np.sqrt(n)

    # Incerteza expandida (k=2)
    k = 2
    u_expandida = k * u_padrao

    # Intervalo de confiança (95%) com t de Student
    gl = n - 1
    t_student = stats.t.ppf(0.975, df=gl)  # 95% bilateral
    margem_erro = t_student * u_padrao
    intervalo = (media - margem_erro, media + margem_erro)

    st.markdown(f"**Média:** {media:.4f}")

    st.markdown("### Cálculos como População:")
    st.markdown(f"Variância: {var_pop:.4f}")
    st.markdown(f"Desvio padrão: {desvio_pop:.4f}")

    st.markdown("### Cálculos como Amostra:")
    st.markdown(f"Variância: {var_amostral:.4f}")
    st.markdown(f"Desvio padrão: {desvio_amostral:.4f}")
    st.markdown(f"Incerteza padrão (u): {u_padrao:.4f}")
    st.markdown(f"Incerteza expandida (U, k=2): {u_expandida:.4f}")
    st.markdown(f"Intervalo de confiança 95%: [{intervalo[0]:.4f}, {intervalo[1]:.4f}]")

    # ------------------- GRÁFICO -------------------
    fig, ax = plt.subplots()
    ax.hist(dados, bins='auto', color='skyblue', edgecolor='black')
    ax.axvline(media, color='red', linestyle='--', label='Média')
    ax.set_title("Distribuição dos Valores")
    ax.set_xlabel("Valor")
    ax.set_ylabel("Frequência")
    ax.legend()
    st.pyplot(fig)
