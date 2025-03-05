import tkinter as tk
from tkinter import messagebox
import pygame
import threading
import time

class TrainingTimer:
    def __init__(self, master):
        self.master = master
        master.title("Timer de Treinamento")
        master.geometry("400x500")
        master.configure(bg='#f0f4f8')

        # Configurações iniciais
        self.total_sessions = tk.IntVar(value=4)
        self.session_duration = tk.IntVar(value=30)
        self.team_name = tk.StringVar(value="Meu Treino")
        
        # Estado do timer
        self.current_session = 0
        self.time_remaining = 0
        self.is_running = False
        self.timer_thread = None

        # Inicializar pygame mixer para audio
        pygame.mixer.init()
        try:
            self.beep_sound = pygame.mixer.Sound("C:/Users/dacio/OneDrive - 8250gg/Python Pro/Projetos/Timer Exercícios/Data/Áudios/beep-08b.wav")
        except:
            # Fallback caso não consiga carregar o som
            self.beep_sound = None

        # Criar interface
        self.create_widgets()

    def create_widgets(self):
        # Container principal
        main_frame = tk.Frame(self.master, bg='#f0f4f8')
        main_frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        # Nome do Time
        tk.Label(main_frame, text="Nome do Treino", bg='#f0f4f8').pack(fill=tk.X)
        team_entry = tk.Entry(main_frame, textvariable=self.team_name, 
                               font=('Arial', 12), justify='center')
        team_entry.pack(fill=tk.X, pady=(0,10))

        # Número de Sessões
        tk.Label(main_frame, text="Número de Sessões", bg='#f0f4f8').pack(fill=tk.X)
        sessions_scale = tk.Scale(main_frame, from_=1, to=10, 
                                  variable=self.total_sessions, 
                                  orient=tk.HORIZONTAL)
        sessions_scale.pack(fill=tk.X, pady=(0,10))

        # Duração da Sessão
        tk.Label(main_frame, text="Duração da Sessão (segundos)", bg='#f0f4f8').pack(fill=tk.X)
        duration_scale = tk.Scale(main_frame, from_=10, to=300, 
                                  variable=self.session_duration, 
                                  orient=tk.HORIZONTAL)
        duration_scale.pack(fill=tk.X, pady=(0,10))

        # Display do Timer
        self.timer_label = tk.Label(main_frame, text="00:00", 
                                    font=('Arial', 48), 
                                    bg='#f0f4f8')
        self.timer_label.pack(pady=20)

        # Label de Sessão
        self.session_label = tk.Label(main_frame, text="", 
                                      font=('Arial', 16), 
                                      bg='#f0f4f8')
        self.session_label.pack()

        # Botões de Controle
        button_frame = tk.Frame(main_frame, bg='#f0f4f8')
        button_frame.pack(fill=tk.X, pady=10)

        self.start_button = tk.Button(button_frame, text="Iniciar Treino", 
                                      command=self.start_timer, 
                                      bg='#4CAF50', fg='white')
        self.start_button.pack(side=tk.LEFT, expand=True, padx=5)

        self.stop_button = tk.Button(button_frame, text="Parar", 
                                     command=self.stop_timer, 
                                     bg='#f44336', fg='white', 
                                     state=tk.DISABLED)
        self.stop_button.pack(side=tk.RIGHT, expand=True, padx=5)

    def start_timer(self):
        # Validações
        if not self.team_name.get().strip():
            messagebox.showwarning("Aviso", "Digite o nome do time")
            return

        # Configurar estado inicial
        self.current_session = 1
        self.time_remaining = self.session_duration.get()
        self.is_running = True

        # Habilitar/desabilitar botões
        self.start_button.config(state=tk.DISABLED)
        self.stop_button.config(state=tk.NORMAL)

        # Iniciar thread do timer
        self.timer_thread = threading.Thread(target=self.run_timer)
        self.timer_thread.start()

    def run_timer(self):
        while self.is_running and self.current_session <= self.total_sessions.get():
            # Atualizar display
            self.update_display()

            # Contagem regressiva
            while self.time_remaining > 0 and self.is_running:
                time.sleep(1)
                self.time_remaining -= 1
                self.update_display()

            # Fim da sessão
            if self.is_running:
                self.play_beep()
                
                # Próxima sessão
                if self.current_session < self.total_sessions.get():
                    self.current_session += 1
                    self.time_remaining = self.session_duration.get()
                else:
                    # Treino completo
                    self.is_running = False

        # Finalizar timer
        self.master.after(0, self.reset_timer)

    def update_display(self):
        # Atualizar no thread principal
        self.master.after(0, self._update_display_ui)

    def _update_display_ui(self):
        # Formatar tempo
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60
        time_str = f"{minutes:02d}:{seconds:02d}"
        
        # Atualizar labels
        self.timer_label.config(text=time_str)
        self.session_label.config(
            text=f"{self.team_name.get()} - Sessão {self.current_session} de {self.total_sessions.get()}"
        )

    def stop_timer(self):
        self.is_running = False
        self.reset_timer()

    def reset_timer(self):
        # Reset na interface
        self.timer_label.config(text="00:00")
        self.session_label.config(text="")
        
        # Habilitar/desabilitar botões
        self.start_button.config(state=tk.NORMAL)
        self.stop_button.config(state=tk.DISABLED)

    def play_beep(self):
        if self.beep_sound:
            try:
                self.beep_sound.play()
            except:
                pass

def main():
    root = tk.Tk()
    app = TrainingTimer(root)
    root.mainloop()

if __name__ == "__main__":
    main()