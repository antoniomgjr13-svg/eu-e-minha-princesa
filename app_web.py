import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime, timedelta
import plotly.graph_objects as go
import plotly.express as px
from PIL import Image
import io
import base64
import os

# Configuração da página
st.set_page_config(
    page_title="💕 Eu e Minha Princesa",
    page_icon="💕",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS customizado para deixar LINDO
st.markdown("""
<style>
    /* Importar fonte Google */
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

    /* Estilo global */
    * {
        font-family: 'Poppins', sans-serif;
    }

    /* Remover padding padrão */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
    }

    /* Estilo do título principal */
    .main-title {
        text-align: center;
        font-size: 3.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
        animation: fadeIn 1s ease-in;
    }

    .subtitle {
        text-align: center;
        font-size: 1.2rem;
        color: #888;
        margin-bottom: 2rem;
    }

    /* Cards estilizados */
    .custom-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 20px;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease;
    }

    .custom-card:hover {
        transform: translateY(-5px);
    }

    .card-blue {
        background: linear-gradient(135deg, #667eea 0%, #4a90e2 100%);
    }

    .card-pink {
        background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
    }

    .card-purple {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
    }

    /* Botões personalizados */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        height: 3.5rem;
        font-weight: 600;
        font-size: 1.1rem;
        border: none;
        transition: all 0.3s ease;
    }

    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }

    /* Métricas estilizadas */
    .metric-card {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 20px rgba(0,0,0,0.08);
        text-align: center;
        margin: 1rem 0;
    }

    .metric-value {
        font-size: 2.5rem;
        font-weight: 700;
        color: #667eea;
    }

    .metric-label {
        font-size: 1rem;
        color: #888;
        margin-top: 0.5rem;
    }

    /* Animações */
    @keyframes fadeIn {
        from { opacity: 0; transform: translateY(-20px); }
        to { opacity: 1; transform: translateY(0); }
    }

    @keyframes slideIn {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }

    /* Sidebar estilizada */
    .css-1d391kg {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }

    /* Emoji grande */
    .big-emoji {
        font-size: 4rem;
        text-align: center;
        margin: 1rem 0;
    }

    /* Timeline item */
    .timeline-item {
        background: white;
        padding: 1.5rem;
        border-radius: 15px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.08);
        margin-bottom: 1.5rem;
        border-left: 5px solid;
        animation: slideIn 0.5s ease;
    }

    .timeline-blue {
        border-left-color: #4a90e2;
    }

    .timeline-pink {
        border-left-color: #f5576c;
    }

    /* Upload de foto */
    .uploadedFile {
        border-radius: 15px;
        overflow: hidden;
    }

    /* Slider customizado */
    .stSlider {
        padding: 1rem 0;
    }

    /* Text area */
    .stTextArea textarea {
        border-radius: 12px;
        border: 2px solid #e0e0e0;
        font-size: 1rem;
    }

    /* Radio buttons */
    .stRadio > div {
        gap: 1rem;
    }

    /* Sucesso/erro messages */
    .stSuccess, .stError, .stInfo {
        border-radius: 12px;
        padding: 1rem;
        font-weight: 500;
    }
</style>
""", unsafe_allow_html=True)

# Inicializar banco de dados
def init_db():
    os.makedirs("data", exist_ok=True)
    conn = sqlite3.connect('data/app.db')
    c = conn.cursor()

    # Tabela de pessoas
    c.execute('''CREATE TABLE IF NOT EXISTS pessoas
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  nome TEXT NOT NULL,
                  cor TEXT DEFAULT '#4A90E2',
                  emoji TEXT DEFAULT '😊')''')

    # Tabela de momentos
    c.execute('''CREATE TABLE IF NOT EXISTS momentos
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  pessoa_id INTEGER NOT NULL,
                  sentimento TEXT NOT NULL,
                  nota INTEGER NOT NULL,
                  mensagem TEXT,
                  foto BLOB,
                  data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (pessoa_id) REFERENCES pessoas (id))''')

    # Inserir pessoas padrão se não existirem
    c.execute("SELECT COUNT(*) FROM pessoas")
    if c.fetchone()[0] == 0:
        c.execute("INSERT INTO pessoas (nome, cor, emoji) VALUES (?, ?, ?)",
                  ("Você", "#4A90E2", "👨"))
        c.execute("INSERT INTO pessoas (nome, cor, emoji) VALUES (?, ?, ?)",
                  ("Minha Princesa", "#f5576c", "👸"))

    conn.commit()
    conn.close()

# Funções do banco de dados
def get_pessoas():
    conn = sqlite3.connect('data/app.db')
    df = pd.read_sql_query("SELECT * FROM pessoas", conn)
    conn.close()
    return df

def salvar_momento(pessoa_id, sentimento, nota, mensagem, foto):
    conn = sqlite3.connect('data/app.db')
    c = conn.cursor()

    foto_blob = None
    if foto is not None:
        foto_blob = foto.getvalue()

    c.execute('''INSERT INTO momentos (pessoa_id, sentimento, nota, mensagem, foto, data_hora)
                 VALUES (?, ?, ?, ?, ?, ?)''',
              (pessoa_id, sentimento, nota, mensagem, foto_blob, datetime.now()))

    conn.commit()
    conn.close()

def get_momentos(pessoa_id=None, limit=None):
    conn = sqlite3.connect('data/app.db')

    if pessoa_id:
        query = '''SELECT m.*, p.nome, p.cor, p.emoji
                   FROM momentos m
                   JOIN pessoas p ON m.pessoa_id = p.id
                   WHERE m.pessoa_id = ?
                   ORDER BY m.data_hora DESC'''
        df = pd.read_sql_query(query, conn, params=(pessoa_id,))
    else:
        query = '''SELECT m.*, p.nome, p.cor, p.emoji
                   FROM momentos m
                   JOIN pessoas p ON m.pessoa_id = p.id
                   ORDER BY m.data_hora DESC'''
        df = pd.read_sql_query(query, conn)

    if limit:
        df = df.head(limit)

    conn.close()
    return df

def get_estatisticas():
    conn = sqlite3.connect('data/app.db')
    df = pd.read_sql_query('''
        SELECT
            p.nome,
            p.cor,
            p.emoji,
            COUNT(m.id) as total_momentos,
            AVG(m.nota) as media_nota,
            MAX(m.nota) as max_nota,
            MIN(m.nota) as min_nota
        FROM pessoas p
        LEFT JOIN momentos m ON p.id = m.pessoa_id
        GROUP BY p.id
    ''', conn)
    conn.close()
    return df

def atualizar_pessoa(pessoa_id, nome):
    conn = sqlite3.connect('data/app.db')
    c = conn.cursor()
    c.execute("UPDATE pessoas SET nome = ? WHERE id = ?", (nome, pessoa_id))
    conn.commit()
    conn.close()

# Inicializar DB e session state
init_db()

if 'pagina' not in st.session_state:
    st.session_state.pagina = 'home'

# Sidebar
with st.sidebar:
    st.markdown("### 💕 Menu")

    if st.button("🏠 Início", use_container_width=True):
        st.session_state.pagina = 'home'

    if st.button("➕ Novo Momento", use_container_width=True):
        st.session_state.pagina = 'novo'

    if st.button("📖 Histórico", use_container_width=True):
        st.session_state.pagina = 'historico'

    if st.button("📊 Dashboard", use_container_width=True):
        st.session_state.pagina = 'dashboard'

    if st.button("📷 Galeria", use_container_width=True):
        st.session_state.pagina = 'galeria'

    if st.button("⚙️ Configurações", use_container_width=True):
        st.session_state.pagina = 'config'

    st.markdown("---")

# Página HOME
if st.session_state.pagina == 'home':
    st.markdown('<h1 class="main-title">💕 Eu e Minha Princesa 💕</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">Registre seus momentos especiais juntos</p>', unsafe_allow_html=True)

    # Estatísticas rápidas
    stats = get_estatisticas()

    col1, col2, col3 = st.columns(3)

    with col1:
        total_geral = stats['total_momentos'].sum()
        st.markdown(f"""
        <div class="metric-card">
            <div class="big-emoji">💖</div>
            <div class="metric-value">{int(total_geral)}</div>
            <div class="metric-label">Momentos Registrados</div>
        </div>
        """, unsafe_allow_html=True)

    with col2:
        if total_geral > 0:
            media_geral = stats['media_nota'].mean()
            st.markdown(f"""
            <div class="metric-card">
                <div class="big-emoji">⭐</div>
                <div class="metric-value">{media_geral:.1f}</div>
                <div class="metric-label">Média Geral</div>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="metric-card">
                <div class="big-emoji">⭐</div>
                <div class="metric-value">-</div>
                <div class="metric-label">Média Geral</div>
            </div>
            """, unsafe_allow_html=True)

    with col3:
        dias_juntos = (datetime.now() - datetime(2026, 5, 9)).days  # 09/05/2026 - Dia que começaram a conversar
        st.markdown(f"""
        <div class="metric-card">
            <div class="big-emoji">📅</div>
            <div class="metric-value">{dias_juntos}</div>
            <div class="metric-label">Dias de Amor</div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("---")

    # Últimos momentos
    st.markdown("### 🌟 Últimos Momentos")

    momentos_recentes = get_momentos(limit=5)

    if len(momentos_recentes) > 0:
        for _, momento in momentos_recentes.iterrows():
            cor_class = "timeline-blue" if momento['cor'] == "#4A90E2" else "timeline-pink"

            col_emoji, col_info = st.columns([1, 5])

            with col_emoji:
                st.markdown(f'<div class="big-emoji">{momento["sentimento"]}</div>', unsafe_allow_html=True)

            with col_info:
                st.markdown(f"""
                <div class="timeline-item {cor_class}">
                    <h4>{momento['emoji']} {momento['nome']} - Nota: {momento['nota']}/10 ⭐</h4>
                    <p style="color: #666; margin: 0.5rem 0;">{momento['mensagem'] if momento['mensagem'] else 'Sem mensagem'}</p>
                    <small style="color: #999;">{pd.to_datetime(momento['data_hora']).strftime('%d/%m/%Y às %H:%M')}</small>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.info("Nenhum momento registrado ainda. Comece agora! 💕")

    # Botão de ação
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("➕ Registrar Novo Momento", use_container_width=True, type="primary"):
        st.session_state.pagina = 'novo'
        st.rerun()

# Página NOVO MOMENTO
elif st.session_state.pagina == 'novo':
    st.markdown('<h1 class="main-title">➕ Novo Momento</h1>', unsafe_allow_html=True)

    pessoas = get_pessoas()

    # Seleção de pessoa com cards bonitos
    st.markdown("### Quem está registrando?")

    col1, col2 = st.columns(2)

    pessoa_selecionada = None

    with col1:
        if st.button(f"{pessoas.iloc[0]['emoji']} {pessoas.iloc[0]['nome']}",
                     use_container_width=True,
                     key="pessoa1",
                     type="primary"):
            pessoa_selecionada = pessoas.iloc[0]

    with col2:
        if st.button(f"{pessoas.iloc[1]['emoji']} {pessoas.iloc[1]['nome']}",
                     use_container_width=True,
                     key="pessoa2",
                     type="secondary"):
            pessoa_selecionada = pessoas.iloc[1]

    # Se pessoa selecionada via session_state
    if 'pessoa_form' not in st.session_state:
        st.session_state.pessoa_form = None

    if pessoa_selecionada is not None:
        st.session_state.pessoa_form = pessoa_selecionada

    if st.session_state.pessoa_form is not None:
        pessoa = st.session_state.pessoa_form

        st.markdown("---")
        st.markdown(f"### Registrando momento de: {pessoa['emoji']} {pessoa['nome']}")

        # Formulário
        with st.form("form_momento"):
            # Sentimento
            st.markdown("#### Como você está se sentindo?")

            sentimentos = {
                "😊 Muito Feliz": "😊",
                "🙂 Feliz": "🙂",
                "😐 Normal": "😐",
                "😔 Triste": "😔",
                "😢 Muito Triste": "😢",
                "😍 Apaixonado(a)": "😍",
                "🥰 Amando Muito": "🥰",
                "🤗 Carinhoso(a)": "🤗",
                "😤 Irritado(a)": "😤",
                "🤔 Pensativo(a)": "🤔",
                "😴 Cansado(a)": "😴",
                "🤩 Empolgado(a)": "🤩"
            }

            cols = st.columns(4)
            sentimento_keys = list(sentimentos.keys())

            sentimento_escolhido = None
            for i, sent in enumerate(sentimento_keys):
                with cols[i % 4]:
                    if st.form_submit_button(sent, use_container_width=True):
                        sentimento_escolhido = sentimentos[sent]

            # Se não escolheu via botão, usar radio como fallback
            if sentimento_escolhido is None:
                sentimento_radio = st.radio("Ou escolha aqui:", list(sentimentos.keys()), horizontal=True)
                sentimento_escolhido = sentimentos[sentimento_radio]

            st.markdown("<br>", unsafe_allow_html=True)

            # Nota
            st.markdown("#### Qual sua nota de 1 a 10?")
            nota = st.slider("", 1, 10, 7, key="nota_slider")

            # Mostrar a nota de forma bonita
            nota_emoji = "🌟" * nota
            st.markdown(f"<h2 style='text-align: center; color: {pessoa['cor']};'>{nota}/10 {nota_emoji}</h2>",
                       unsafe_allow_html=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Mensagem
            st.markdown("#### Mensagem (opcional)")
            mensagem = st.text_area("Escreva algo especial...", height=100, placeholder="Ex: Hoje foi um dia incrível! 💕")

            st.markdown("<br>", unsafe_allow_html=True)

            # Foto
            st.markdown("#### Adicionar Foto (opcional)")
            foto = st.file_uploader("Escolha uma foto", type=['png', 'jpg', 'jpeg'], label_visibility="collapsed")

            if foto:
                st.image(foto, caption="Preview da foto", use_column_width=True)

            st.markdown("<br>", unsafe_allow_html=True)

            # Botão salvar
            submitted = st.form_submit_button("💾 Salvar Momento", use_container_width=True, type="primary")

            if submitted:
                salvar_momento(pessoa['id'], sentimento_escolhido, nota, mensagem, foto)
                st.success("✅ Momento salvo com sucesso! 💕")
                st.balloons()
                st.session_state.pessoa_form = None

                # Botão para voltar
                if st.button("← Voltar ao início"):
                    st.session_state.pagina = 'home'
                    st.rerun()

# Página HISTÓRICO
elif st.session_state.pagina == 'historico':
    st.markdown('<h1 class="main-title">📖 Histórico</h1>', unsafe_allow_html=True)

    pessoas = get_pessoas()

    # Filtros
    col1, col2, col3 = st.columns([2, 2, 1])

    with col1:
        filtro_pessoa = st.selectbox(
            "Filtrar por pessoa",
            ["Todos"] + pessoas['nome'].tolist()
        )

    with col2:
        ordem = st.selectbox("Ordenar por", ["Mais recente", "Mais antigo", "Maior nota", "Menor nota"])

    # Buscar momentos
    if filtro_pessoa == "Todos":
        momentos = get_momentos()
    else:
        pessoa_id = pessoas[pessoas['nome'] == filtro_pessoa]['id'].values[0]
        momentos = get_momentos(pessoa_id)

    # Ordenar
    if ordem == "Mais antigo":
        momentos = momentos.sort_values('data_hora', ascending=True)
    elif ordem == "Maior nota":
        momentos = momentos.sort_values('nota', ascending=False)
    elif ordem == "Menor nota":
        momentos = momentos.sort_values('nota', ascending=True)

    st.markdown(f"**{len(momentos)} momentos encontrados**")
    st.markdown("---")

    # Exibir momentos
    if len(momentos) > 0:
        for _, momento in momentos.iterrows():
            with st.container():
                col_main, col_side = st.columns([4, 1])

                with col_main:
                    cor_border = momento['cor']

                    st.markdown(f"""
                    <div style="border-left: 5px solid {cor_border}; padding-left: 1.5rem; margin-bottom: 2rem;">
                        <h3>{momento['sentimento']} {momento['emoji']} {momento['nome']}</h3>
                        <p style="font-size: 1.2rem; color: #666;">
                            <strong>Nota:</strong> {momento['nota']}/10 {'⭐' * int(momento['nota'])}
                        </p>
                    """, unsafe_allow_html=True)

                    if momento['mensagem']:
                        st.markdown(f"> {momento['mensagem']}")

                    if momento['foto']:
                        try:
                            foto_img = Image.open(io.BytesIO(momento['foto']))
                            st.image(foto_img, width=400)
                        except:
                            pass

                    data_formatada = pd.to_datetime(momento['data_hora']).strftime('%d/%m/%Y às %H:%M')
                    st.markdown(f"<small style='color: #999;'>📅 {data_formatada}</small></div>", unsafe_allow_html=True)

                st.markdown("---")
    else:
        st.info("Nenhum momento encontrado com esses filtros.")

# Página DASHBOARD
elif st.session_state.pagina == 'dashboard':
    st.markdown('<h1 class="main-title">📊 Dashboard</h1>', unsafe_allow_html=True)

    stats = get_estatisticas()
    pessoas = get_pessoas()

    # Estatísticas por pessoa
    st.markdown("### 👥 Estatísticas Individuais")

    col1, col2 = st.columns(2)

    for idx, (_, pessoa_stat) in enumerate(stats.iterrows()):
        with [col1, col2][idx]:
            st.markdown(f"""
            <div style="background: linear-gradient(135deg, {pessoa_stat['cor']}40, {pessoa_stat['cor']}20);
                        padding: 2rem; border-radius: 15px; margin-bottom: 1rem;">
                <h2 style="margin: 0;">{pessoa_stat['emoji']} {pessoa_stat['nome']}</h2>
                <hr style="border-color: {pessoa_stat['cor']};">
                <p style="font-size: 1.5rem; margin: 0.5rem 0;">
                    <strong>{int(pessoa_stat['total_momentos'])}</strong> momentos
                </p>
                <p style="font-size: 1.5rem; margin: 0.5rem 0;">
                    Média: <strong>{f'{pessoa_stat["media_nota"]:.1f}' if pessoa_stat['media_nota'] else '0'}</strong>/10
                </p>
                <p style="font-size: 1rem; color: #666;">
                    Maior nota: {int(pessoa_stat['max_nota']) if pessoa_stat['max_nota'] else '-'} |
                    Menor nota: {int(pessoa_stat['min_nota']) if pessoa_stat['min_nota'] else '-'}
                </p>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("---")

    # Gráficos
    momentos = get_momentos()

    if len(momentos) > 0:
        st.markdown("### 📈 Evolução do Humor")

        # Preparar dados
        momentos['data_hora'] = pd.to_datetime(momentos['data_hora'])
        momentos['data'] = momentos['data_hora'].dt.date

        # Gráfico de linha por pessoa
        fig = go.Figure()

        for _, pessoa in pessoas.iterrows():
            dados_pessoa = momentos[momentos['pessoa_id'] == pessoa['id']].sort_values('data_hora')

            fig.add_trace(go.Scatter(
                x=dados_pessoa['data_hora'],
                y=dados_pessoa['nota'],
                mode='lines+markers',
                name=f"{pessoa['emoji']} {pessoa['nome']}",
                line=dict(color=pessoa['cor'], width=3),
                marker=dict(size=10)
            ))

        fig.update_layout(
            title="Notas ao longo do tempo",
            xaxis_title="Data",
            yaxis_title="Nota",
            height=400,
            hovermode='x unified',
            yaxis=dict(range=[0, 11])
        )

        st.plotly_chart(fig, use_container_width=True)

        st.markdown("---")

        # Distribuição de sentimentos
        st.markdown("### 😊 Distribuição de Sentimentos")

        col1, col2 = st.columns(2)

        for idx, (_, pessoa) in enumerate(pessoas.iterrows()):
            dados_pessoa = momentos[momentos['pessoa_id'] == pessoa['id']]

            if len(dados_pessoa) > 0:
                contagem = dados_pessoa['sentimento'].value_counts()

                fig_pie = go.Figure(data=[go.Pie(
                    labels=contagem.index,
                    values=contagem.values,
                    hole=0.4,
                    marker=dict(colors=[pessoa['cor']])
                )])

                fig_pie.update_layout(
                    title=f"{pessoa['emoji']} {pessoa['nome']}",
                    height=300
                )

                with [col1, col2][idx]:
                    st.plotly_chart(fig_pie, use_container_width=True)
    else:
        st.info("Registre alguns momentos para ver os gráficos! 📊")

# Página GALERIA
elif st.session_state.pagina == 'galeria':
    st.markdown('<h1 class="main-title">📷 Galeria de Fotos</h1>', unsafe_allow_html=True)

    momentos = get_momentos()
    momentos_com_foto = momentos[momentos['foto'].notna()]

    if len(momentos_com_foto) > 0:
        st.markdown(f"**{len(momentos_com_foto)} fotos encontradas**")

        # Grid de fotos
        cols = st.columns(3)

        for idx, (_, momento) in enumerate(momentos_com_foto.iterrows()):
            with cols[idx % 3]:
                try:
                    foto_img = Image.open(io.BytesIO(momento['foto']))
                    st.image(foto_img, use_column_width=True)

                    st.markdown(f"""
                    <div style="text-align: center; margin-top: -1rem; margin-bottom: 2rem;">
                        <p style="margin: 0;">{momento['sentimento']} {momento['emoji']} {momento['nome']}</p>
                        <small style="color: #999;">{pd.to_datetime(momento['data_hora']).strftime('%d/%m/%Y')}</small>
                    </div>
                    """, unsafe_allow_html=True)
                except:
                    st.error("Erro ao carregar foto")
    else:
        st.info("Nenhuma foto ainda. Adicione fotos aos seus momentos! 📷")

# Página CONFIGURAÇÕES
elif st.session_state.pagina == 'config':
    st.markdown('<h1 class="main-title">⚙️ Configurações</h1>', unsafe_allow_html=True)

    pessoas = get_pessoas()

    st.markdown("### 👥 Perfis")

    for _, pessoa in pessoas.iterrows():
        with st.expander(f"{pessoa['emoji']} {pessoa['nome']}"):
            novo_nome = st.text_input(f"Nome", value=pessoa['nome'], key=f"nome_{pessoa['id']}")

            if st.button(f"Salvar alterações", key=f"salvar_{pessoa['id']}"):
                atualizar_pessoa(pessoa['id'], novo_nome)
                st.success("✅ Alterações salvas!")
                st.rerun()

    st.markdown("---")

    st.markdown("### 📊 Estatísticas Gerais")

    total_momentos = len(get_momentos())

    st.info(f"""
    - Total de momentos registrados: **{total_momentos}**
    - Data de início: **{datetime(2026, 5, 9).strftime('%d/%m/%Y')}** 💕
    - Dias juntos: **{(datetime.now() - datetime(2026, 5, 9)).days}** dias
    """)

    st.markdown("---")

    st.markdown("### 💝 Sobre")
    st.markdown("""
    **Eu e Minha Princesa** v2.0 Web

    - Acesse de qualquer dispositivo
    - Fotos ilimitadas
    - Dados salvos localmente
    """)
