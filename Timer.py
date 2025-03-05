import streamlit as st
import pygame
import time
from datetime import datetime
import os

class TrainingTimer:
    def __init__(self):
        # Inicializar pygame mixer para audio
        try:
            pygame.mixer.init()
            # Caminho corrigido para o arquivo de som
            base_dir = os.path.dirname(os.path.abspath(__file__))
            sound_path = os.path.join(base_dir, "Data", "Áudios", "beep-08b.wav")
            
            if os.path.exists(sound_path):
                self.beep_sound = pygame.mixer.Sound(sound_path)
            else:
                # Tentar caminho alternativo se o primeiro falhar
                alt_sound_path = os.path.join(base_dir, "Assets", "beep-08b.wav")
                if os.path.exists(alt_sound_path):
                    self.beep_sound = pygame.mixer.Sound(alt_sound_path)
                else:
                    self.beep_sound = None
                    st.warning("Arquivo de som não encontrado. Alertas sonoros desativados.")
        except Exception as e:
            self.beep_sound = None
            st.warning(f"Não foi possível inicializar o sistema de áudio: {e}")

    def initialize_session_state(self):
        # Configurações iniciais
        if 'total_sessions' not in st.session_state:
            st.session_state.total_sessions = 4
        if 'session_duration' not in st.session_state:
            st.session_state.session_duration = 30
        if 'team_name' not in st.session_state:
            st.session_state.team_name = "Meu Treino"
        
        # Estado do timer
        if 'current_session' not in st.session_state:
            st.session_state.current_session = 0
        if 'is_running' not in st.session_state:
            st.session_state.is_running = False
        if 'end_time' not in st.session_state:
            st.session_state.end_time = None
        if 'time_remaining' not in st.session_state:
            st.session_state.time_remaining = 0
        if 'session_completed' not in st.session_state:
            st.session_state.session_completed = False

    def create_ui(self):
        # Logo e título quando não estiver rodando
        if not st.session_state.is_running:
            col1, col2 = st.columns([1, 4])
            
            with col1:
                # Verificar se o arquivo de logo existe
                logo_path = os.path.join(os.path.dirname(__file__), "Assets", "logo.png")
                if os.path.exists(logo_path):
                    st.image(logo_path, width=80)
                else:
                    # Fallback para logo em emoji
                    st.markdown(
                        """
                        <div style="text-align: center; background-color: #0e1117; border-radius: 50%; width: 80px; height: 80px; 
                             display: flex; align-items: center; justify-content: center; margin: 10px auto;">
                            <span style="font-size: 40px;">⏱️</span>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
            
            with col2:
                st.title("Timer de Treinamento")
                st.markdown("<p style='margin-top: -15px; color: #888;'>Controle preciso para seus exercícios</p>", unsafe_allow_html=True)
        
        # Configurações (apenas visíveis quando o timer não está rodando)
        if not st.session_state.is_running:
            # Nome do Time
            st.session_state.team_name = st.text_input("Nome do Treino", value=st.session_state.team_name)
            
            # Layout em duas colunas para os controles numéricos
            col1, col2 = st.columns(2)
            
            # Número de Sessões com input numérico
            with col1:
                st.markdown("<p style='margin-bottom: 5px;'><b>Número de Sessões</b></p>", unsafe_allow_html=True)
                sessions_col1, sessions_col2, sessions_col3 = st.columns([1, 3, 1])
                
                with sessions_col1:
                    if st.button("-", key="dec_sessions"):
                        if st.session_state.total_sessions > 1:
                            st.session_state.total_sessions -= 1
                
                with sessions_col2:
                    st.session_state.total_sessions = st.number_input(
                        "", 
                        min_value=1, 
                        max_value=30, 
                        value=st.session_state.total_sessions,
                        label_visibility="collapsed"
                    )
                
                with sessions_col3:
                    if st.button("+", key="inc_sessions"):
                        if st.session_state.total_sessions < 30:
                            st.session_state.total_sessions += 1
            
            # Duração da Sessão com input numérico
            with col2:
                st.markdown("<p style='margin-bottom: 5px;'><b>Duração (segundos)</b></p>", unsafe_allow_html=True)
                duration_col1, duration_col2, duration_col3 = st.columns([1, 3, 1])
                
                with duration_col1:
                    if st.button("-", key="dec_duration"):
                        if st.session_state.session_duration > 10:
                            st.session_state.session_duration -= 5
                
                with duration_col2:
                    st.session_state.session_duration = st.number_input(
                        "", 
                        min_value=10, 
                        max_value=300, 
                        value=st.session_state.session_duration,
                        step=5,
                        label_visibility="collapsed"
                    )
                
                with duration_col3:
                    if st.button("+", key="inc_duration"):
                        if st.session_state.session_duration < 300:
                            st.session_state.session_duration += 5
        # Atualizar o timer se estiver rodando
        if st.session_state.is_running:
            self.update_timer()
        
        # Formatar tempo para exibição
        minutes, seconds = divmod(int(st.session_state.time_remaining), 60)
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        # Container principal para o timer e informações
        timer_container = st.empty()  # Usar empty container para substituir conteúdo
        
        with timer_container.container():
            if st.session_state.is_running:
                # Título do treino em andamento
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-bottom: 10px;">
                        <h1 style="color: #0e1117; font-size: 36px;">{st.session_state.team_name}</h1>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Display do timer com estilo melhorado para modo ativo
                timer_color = "#0e1117"
                bg_color = "#f0f2f6"
                border_color = "#e0e0e0"
                
                if st.session_state.time_remaining < 5:
                    timer_color = "#FF0000"  # Vermelho quando faltam menos de 5 segundos
                    bg_color = "#fff0f0"     # Fundo levemente avermelhado
                    border_color = "#ffcccc" # Borda avermelhada
                
                st.markdown(
                    f"""
                    <div style="text-align: center; background-color: {bg_color}; padding: 30px; 
                         border-radius: 15px; margin: 20px 0; border: 2px solid {border_color}; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
                        <h1 style="font-size: 120px; font-weight: bold; margin: 0; color: {timer_color};">{time_str}</h1>
                        <h3 style="color: #555; margin-top: 10px;">Sessão {st.session_state.current_session} de {st.session_state.total_sessions}</h3>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Informações adicionais em um painel mais compacto
                st.markdown(
                    f"""
                    <div style="display: flex; justify-content: space-between; background-color: #f8f9fa; 
                         padding: 15px; border-radius: 10px; margin: 15px 0; text-align: center;">
                        <div style="flex: 1;">
                            <p style="font-weight: bold; margin: 0; color: #555;">Sessão</p>
                            <p style="font-size: 24px; margin: 0;">{st.session_state.current_session}/{st.session_state.total_sessions}</p>
                        </div>
                        <div style="flex: 1; border-left: 1px solid #ddd; border-right: 1px solid #ddd; padding: 0 10px;">
                    """,
                    unsafe_allow_html=True
                )
                
                # Calcular tempo total restante
                sessoes_restantes = st.session_state.total_sessions - st.session_state.current_session
                tempo_total_restante = st.session_state.time_remaining + (sessoes_restantes * st.session_state.session_duration)
                mins, secs = divmod(int(tempo_total_restante), 60)
                
                st.markdown(
                    f"""
                        <p style="font-weight: bold; margin: 0; color: #555;">Tempo Total</p>
                        <p style="font-size: 24px; margin: 0;">{mins:02d}:{secs:02d}</p>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Calcular progresso em porcentagem
                tempo_total = st.session_state.total_sessions * st.session_state.session_duration
                tempo_decorrido = tempo_total - tempo_total_restante
                progresso = int((tempo_decorrido / tempo_total) * 100) if tempo_total > 0 else 0
                
                st.markdown(
                    f"""
                        <div style="flex: 1;">
                            <p style="font-weight: bold; margin: 0; color: #555;">Progresso</p>
                            <p style="font-size: 24px; margin: 0;">{progresso}%</p>
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Barra de progresso
                st.markdown(
                    f"""
                    <div style="background-color: #e0e0e0; border-radius: 10px; height: 10px; margin: 10px 0;">
                        <div style="background-color: #4CAF50; width: {progresso}%; height: 10px; border-radius: 10px;"></div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Botão de parar centralizado e maior
                st.markdown(
                    f"""
                    <div style="text-align: center; margin-top: 20px;">
                        <div style="background-color: #f44336; color: white; border: none; 
                                padding: 12px 30px; text-align: center; display: inline-block; 
                                font-size: 18px; margin: 4px 2px; border-radius: 8px;">
                            PARAR TREINO
                        </div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                
                # Botão real do Streamlit (invisível mas funcional)
                col1, col2, col3 = st.columns([1, 1, 1])
                with col2:
                    if st.button("Parar", key="stop_button", use_container_width=True):
                        self.stop_timer()
                
                # Estilizar o botão para ficar invisível mas clicável sobre o botão visual
                st.markdown(
                    """
                    <style>
                    div[data-testid="stButton"] > button {
                        opacity: 0;
                        position: relative;
                        top: -60px;
                        height: 50px;
                        cursor: pointer;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )
                
            else:
                # Display do timer com estilo melhorado para modo inativo
                st.markdown(
                    f"""
                    <div style="text-align: center; background-color: #f0f2f6; padding: 20px; border-radius: 10px; margin: 20px 0;">
                        <h1 style="font-size: 100px; font-weight: bold; margin: 0; color: #0e1117;">{time_str}</h1>
                    </div>
                    """, 
                    unsafe_allow_html=True
                )
                
                # Botão de iniciar
                if st.button("Iniciar Treino", use_container_width=True):
                    self.start_timer()
            
            # Mensagem de conclusão
            if st.session_state.session_completed:
                st.success("Treino concluído!")
                st.balloons() # Adiciona um efeito visual de celebração
                st.session_state.session_completed = False
        
        # Rerun para atualização em tempo real - movido para fora do container
        if st.session_state.is_running:
            time.sleep(0.1)  # Pequena pausa para não sobrecarregar
            st.rerun()

    def update_timer(self):
        # Calcular tempo restante
        if st.session_state.end_time:
            now = datetime.now()
            remaining = (st.session_state.end_time - now).total_seconds()
            
            if remaining <= 0:
                # Sessão atual terminou
                self.play_beep()
                
                # Verificar se há mais sessões
                if st.session_state.current_session < st.session_state.total_sessions:
                    # Iniciar próxima sessão
                    st.session_state.current_session += 1
                    st.session_state.end_time = datetime.now().timestamp() + st.session_state.session_duration
                    st.session_state.end_time = datetime.fromtimestamp(st.session_state.end_time)
                    st.session_state.time_remaining = st.session_state.session_duration
                else:
                    # Treino completo
                    self.stop_timer()
                    st.session_state.session_completed = True
            else:
                st.session_state.time_remaining = remaining

    def start_timer(self):
        # Validações
        if not st.session_state.team_name.strip():
            st.warning("Digite o nome do treino")
            return

        # Configurar estado inicial
        st.session_state.current_session = 1
        st.session_state.time_remaining = st.session_state.session_duration
        st.session_state.is_running = True
        st.session_state.end_time = datetime.now().timestamp() + st.session_state.session_duration
        st.session_state.end_time = datetime.fromtimestamp(st.session_state.end_time)
        st.session_state.session_completed = False
        
        # Adicionar JavaScript para rolar para o topo da página
        st.markdown(
            """
            <script>
                window.scrollTo(0, 0);
            </script>
            """,
            unsafe_allow_html=True
        )
    def stop_timer(self):
        st.session_state.is_running = False
        st.session_state.current_session = 0
        st.session_state.time_remaining = 0
        st.session_state.end_time = None

    def play_beep(self):
        if self.beep_sound:
            try:
                self.beep_sound.play()
            except:
                pass

def main():
    st.set_page_config(
        page_title="Timer de Treinamento",
        page_icon="⏱️",
        layout="centered"
    )
    
    timer = TrainingTimer()
    timer.initialize_session_state()  # Add this line to initialize session state
    timer.create_ui()

if __name__ == "__main__":
    main()