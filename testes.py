import tkinter as tk
import time

class Tema:
    def __init__(self, nome, fundo, texto, botao_fundo, botao_texto):
        self.nome = nome
        self.fundo = fundo
        self.texto = texto
        self.botao_fundo = botao_fundo
        self.botao_texto = botao_texto

class RelogioDigital(tk.Frame):
    def __init__(self, master, tema):
        super().__init__(master, bg=tema.fundo)
        self.tema = tema
        self.master = master
        
        # Widgets do relógio
        self.label_relogio = tk.Label(
            self,
            font=('Arial', 48, 'bold'),
            bg=tema.fundo,
            fg=tema.texto
        )
        self.label_relogio.pack(pady=20)
        
        self.label_data = tk.Label(
            self,
            font=('Arial', 14),
            bg=tema.fundo,
            fg=tema.texto
        )
        self.label_data.pack()
        
        self.atualizar_horario()

    def atualizar_horario(self):
        horario_atual = time.strftime('%H:%M:%S')
        data_atual = time.strftime('%d/%m/%Y')
        
        self.label_relogio.config(text=horario_atual)
        self.label_data.config(text=data_atual)
        self.after(1000, self.atualizar_horario)
    
    def aplicar_tema(self, novo_tema):
        self.tema = novo_tema
        self.config(bg=novo_tema.fundo)
        self.label_relogio.config(
            bg=novo_tema.fundo, 
            fg=novo_tema.texto
        )
        self.label_data.config(
            bg=novo_tema.fundo, 
            fg=novo_tema.texto
        )

class GerenciadorTemas:
    def __init__(self):
        self.temas = {
            "claro": Tema(
                "claro", 
                "white", "black", 
                "#f0f0f0", "black"
            ),
            "escuro": Tema(
                "escuro", 
                "#121212", "#ffffff", 
                "#333333", "white"
            )
        }
        self.tema_atual = "claro"
    
    def obter_tema(self, nome=None):
        if nome is None:
            return self.temas[self.tema_atual]
        return self.temas[nome]
    
    def alternar_tema(self):
        self.tema_atual = "escuro" if self.tema_atual == "claro" else "claro"
        return self.obter_tema()

class BotaoTema(tk.Button):
    def __init__(self, master, gerenciador, callback):
        self.gerenciador = gerenciador
        tema = gerenciador.obter_tema()
        
        super().__init__(
            master,
            text="Alternar Tema",
            command=callback,
            bg=tema.botao_fundo,
            fg=tema.botao_texto,
            font=('Arial', 12)
        )
    
    def atualizar_aparencia(self, tema):
        self.config(
            bg=tema.botao_fundo,
            fg=tema.botao_texto
        )

class RelogioApp:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Relógio Digital v2.0")
        self.janela.geometry("400x250")
        self.janela.resizable(False, False)
        
        # Gerenciador de temas
        self.gerenciador_temas = GerenciadorTemas()
        
        # Container principal
        self.container = tk.Frame(janela)
        self.container.pack(expand=True, fill='both')
        
        # Cria relógio com tema inicial
        self.criar_widgets()
    
    def criar_widgets(self):
        # Remove widgets existentes
        for widget in self.container.winfo_children():
            widget.destroy()
        
        # Cria relógio com tema atual
        tema_atual = self.gerenciador_temas.obter_tema()
        self.relogio = RelogioDigital(self.container, tema_atual)
        self.relogio.pack(expand=True, fill='both', padx=20, pady=10)
        
        # Cria botão de alternância
        self.botao_tema = BotaoTema(
            self.container,
            self.gerenciador_temas,
            self.alternar_tema
        )
        self.botao_tema.pack(pady=10)
    
    def alternar_tema(self):
        # Alterna tema e aplica a todos os componentes
        novo_tema = self.gerenciador_temas.alternar_tema()
        self.relogio.aplicar_tema(novo_tema)
        self.botao_tema.atualizar_aparencia(novo_tema)
        
        # Atualiza fundo do container
        self.container.config(bg=novo_tema.fundo)

if __name__ == "__main__":
    root = tk.Tk()
    app = RelogioApp(root)
    root.mainloop()