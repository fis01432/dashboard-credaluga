import streamlit as st
import plotly.express as px
import pandas as pd
import datetime
import os
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# Load variáveis de ambiente
load_dotenv(".env")

# Função para envio de email
def enviar_email(respostas_dict):
    EMAIL_USER = os.getenv("EMAIL_USER")
    EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
    EMAIL_DESTINO = os.getenv("EMAIL_DESTINO")

    corpo = "Diagnóstico do Score Collection:\n\n"
    for k, v in respostas_dict.items():
        corpo += f"{k.replace('_', ' ').capitalize()}: {v}\n"

    msg = EmailMessage()
    msg.set_content(corpo)
    msg["Subject"] = "Diagnóstico Score Collection - Formulário Streamlit"
    msg["From"] = EMAIL_USER
    msg["To"] = EMAIL_DESTINO

    try:
        with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
            smtp.login(EMAIL_USER, EMAIL_PASSWORD)
            smtp.send_message(msg)
        return True
    except Exception as e:
        st.error(f"❌ Erro ao enviar e-mail: {e}")
        return False

# Configuração da página
st.set_page_config(layout="wide", page_title="Dashboard de Inadimplência")

# Sidebar
with st.sidebar:
    st.image("logo.png", caption="", use_container_width=True)
    st.markdown("## Navegação")
    st.markdown("- Visão Geral")
    st.markdown("- Segmentações")
    st.markdown("- Diagnóstico Base")

st.title("📊 Dashboard Executivo - Análise de Inadimplência")

# Simulação de dados
df = pd.DataFrame({
    'cliente_inadimplente': ['Adimplente'] * 27800 + ['Inadimplente'] * 2243,
    'cat_empresas': ['0'] * 17765 + ['1'] * 7871 + ['2+'] * 4407,
    'cat_emails': ['0'] * 10815 + ['1'] * 11796 + ['2+'] * 7432,
    'faixa_idade': ['18-29'] * 9163 + ['30-44'] * 11656 + ['45-59'] * 6409 + ['60+'] * 2815
})

# Dimensão do dataset
st.markdown("### 📦 Dimensão do Dataset")
col1, col2 = st.columns(2)
with col1:
    st.metric("🔢 Total de Linhas", f"{df.shape[0]:,}".replace(",", "."))
with col2:
    st.metric("🧬 Total de Colunas", "28")

# Funções auxiliares
def bar_plot(df, x, y, title):
    fig = px.bar(df, x=x, y=y, text=y, labels={y: 'Percentual (%)'})
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(showlegend=False, yaxis_range=[0, 100], title=title)
    return fig

def stacked_bar(df, x, y, color, title):
    fig = px.bar(df, x=x, y=y, color=color, barmode='stack',
                 text_auto='.1f', labels={y: 'Percentual (%)'})
    fig.update_layout(yaxis_range=[0, 100], title=title)
    return fig

# Abas principais
tab1, tab2, tab3 = st.tabs(["📊 Visão Geral", "🔎 Segmentações", "🧠 Diagnóstico Base"])

with tab1:
    st.subheader("🎯 Distribuição do Target")
    df_target = pd.DataFrame({
        'cliente_inadimplente': ['Adimplente', 'Inadimplente'],
        'percentual': [92.6, 7.4]
    })
    fig = px.bar(df_target, x='cliente_inadimplente', y='percentual', text='percentual',
                 color='cliente_inadimplente',
                 color_discrete_map={'Adimplente': '#2E86AB', 'Inadimplente': '#FF6B6B'})
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(showlegend=False, yaxis_range=[0, 110])
    st.plotly_chart(fig, use_container_width=True)
    st.markdown("""
📌 **Análise de Distribuição:**  
A base é **fortemente desbalanceada**, com mais de **92% de clientes adimplentes**.  
➡️ Use métricas como **AUC-ROC, F1-score e Recall** e técnicas como **SMOTE** para reequilibrar.
""")

with tab2:
    st.subheader("🏢 Empresas Associadas")
    df_emp = pd.DataFrame({'cat_empresas': ['0', '1', '2+'], 'percentual': [59.1, 26.2, 14.8]})
    st.plotly_chart(bar_plot(df_emp, 'cat_empresas', 'percentual', ""), use_container_width=True)
    df_emp_stack = pd.DataFrame({
        'cat_empresas': ['0', '1', '2+'] * 2,
        'cliente_inadimplente': ['Adimplente']*3 + ['Inadimplente']*3,
        'percentual': [91.9, 93.6, 93.5, 8.1, 6.4, 6.5]
    })
    st.plotly_chart(stacked_bar(df_emp_stack, 'cat_empresas', 'percentual', 'cliente_inadimplente', ""), use_container_width=True)

    st.subheader("📧 Contatos por E-mail")
    df_email = pd.DataFrame({'cat_emails': ['0', '1', '2+'], 'percentual': [36.0, 39.2, 24.8]})
    st.plotly_chart(bar_plot(df_email, 'cat_emails', 'percentual', ""), use_container_width=True)
    df_email_stack = pd.DataFrame({
        'cat_emails': ['0', '1', '2+'] * 2,
        'cliente_inadimplente': ['Adimplente']*3 + ['Inadimplente']*3,
        'percentual': [90.4, 93.2, 94.9, 9.6, 6.8, 5.1]
    })
    st.plotly_chart(stacked_bar(df_email_stack, 'cat_emails', 'percentual', 'cliente_inadimplente', ""), use_container_width=True)

    st.subheader("👥 Faixa Etária")
    df_idade = pd.DataFrame({'faixa_idade': ['18-29', '30-44', '45-59', '60+'],
                             'percentual': [30.5, 38.8, 21.3, 9.4]})
    st.plotly_chart(bar_plot(df_idade, 'faixa_idade', 'percentual', ""), use_container_width=True)
    df_idade_stack = pd.DataFrame({
        'faixa_idade': ['18-29', '30-44', '45-59', '60+'] * 2,
        'cliente_inadimplente': ['Adimplente']*4 + ['Inadimplente']*4,
        'percentual': [90.8, 93.7, 93.8, 91.1, 9.2, 6.3, 6.2, 8.9]
    })
    st.plotly_chart(stacked_bar(df_idade_stack, 'faixa_idade', 'percentual', 'cliente_inadimplente', ""), use_container_width=True)

with tab3:
    st.subheader("📥 Diagnóstico da Base para Score Collection")

    st.markdown("""
📌 **O que é Score Collection?**  
O *Score Collection* é um modelo preditivo que estima a **probabilidade de um cliente inadimplente pagar uma dívida após a negativação**.  
Ele é fundamental para **priorizar estratégias de cobrança, reduzir custos operacionais** e **aumentar a recuperação de valores**.

Para um score eficaz, são necessários dados que reflitam:
- A **janela de tempo da dívida**
- O **comportamento do devedor**
- A **capacidade de contato e negociação**

---

### 🧐 **Diagnóstico da Base Atual**
Abaixo estão variáveis essenciais ausentes ou incompletas na base atual:

| Tipo de Informação                | Situação Atual  | Exemplo Ideal                                    |
|----------------------------------|------------------|--------------------------------------------------|
| 📅 Data de negativação           | ❌ Ausente       | `data_negativacao` → 2024-01-10                  |
| 📆 Dias em aberto                | ❌ Ausente       | `dias_em_aberto` → 183 dias                      |
| 📞 Tentativas de cobrança        | ❌ Ausente       | `tentativas_cobranca` → 3                        |
| 💬 Retorno de contato            | ❌ Ausente       | `contato_estabelecido` → Sim / Não              |
| 📢 Canal de contato efetivo      | ❌ Ausente       | `canal_mais_efetivo` → WhatsApp / Voz / E-mail  |
| ⌛ Tempo até primeira resposta    | ❌ Ausente       | `tempo_resposta_primeira_interacao` → 4 dias     |
| 🧾 Motivo da inadimplência       | ❌ Ausente       | `motivo_inadimplencia` → desemprego / doença     |
| 📉 Tentativas de parcelamento    | ❌ Ausente       | `qtd_parcelamentos_anteriores` → 2               |
| 🤝 Acordos anteriores firmados   | ❌ Ausente       | `ja_firmou_acordo` → Sim / Não                   |
| ✅ Dívida quitada posteriormente | ❌ Ausente       | `divida_quitada` → Sim / Não                     |

---

### 📝 **Formulário de Levantamento de Dados**
""")

    with st.form("form_score_collection"):
        st.markdown("### 📋 Informe abaixo a presença de variáveis essenciais:")

        col1, col2 = st.columns(2)
        with col1:
            data_negativacao = st.radio("Contém data da negativação?", ["Sim", "Não"])
            tentativas = st.radio("Contém tentativas de cobrança?", ["Sim", "Não"])
            canal_contato = st.radio("Contém canal de contato efetivo?", ["Sim", "Não"])
            quitado = st.radio("Contém indicador de quitação?", ["Sim", "Não"])
        with col2:
            resposta = st.radio("Contém tempo de resposta do cliente?", ["Sim", "Não"])
            motivo = st.radio("Contém motivo da inadimplência?", ["Sim", "Não"])
            acordo = st.radio("Contém acordo anterior?", ["Sim", "Não"])
            parcelamento = st.radio("Contém tentativas de parcelamento?", ["Sim", "Não"])

        enviado = st.form_submit_button("📨 Enviar Diagnóstico")

        if enviado:
            resposta_dict = {
                "data_envio": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "data_negativacao": data_negativacao,
                "tentativas_cobranca": tentativas,
                "canal_efetivo": canal_contato,
                "divida_quitada": quitado,
                "tempo_resposta_cliente": resposta,
                "motivo_inadimplencia": motivo,
                "acordo_anterior": acordo,
                "tentativas_parcelamento": parcelamento
            }

            file_path = "diagnostico_score_collection.csv"
            file_exists = os.path.isfile(file_path)
            df_resposta = pd.DataFrame([resposta_dict])
            if file_exists:
                df_resposta.to_csv(file_path, mode='a', header=False, index=False)
            else:
                df_resposta.to_csv(file_path, index=False)

            st.success("✅ Diagnóstico salvo com sucesso!")

            if enviar_email(resposta_dict):
                st.success("📧 Diagnóstico enviado por e-mail com sucesso!")
