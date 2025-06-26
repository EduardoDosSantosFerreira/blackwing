import psutil
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys
import ctypes
import subprocess
from threading import Thread

class BlackWing:
    def __init__(self, root):
        self.root = root
        self.setup_basics()
        self.check_dependencies()
        self.initialize_variables()
        self.setup_styles()
        self.build_ui()
        self.setup_bindings()
        self.update_process_list()

    def setup_basics(self):
        """Configurações básicas da janela principal"""
        self.root.title("BlackWing Process Killer")
        self.root.geometry("1000x700")
        self.root.minsize(800, 600)
        
        # Verificação de privilégios
        self.admin_mode = self.is_admin()
        if not self.admin_mode:
            self.show_admin_warning()

    def check_dependencies(self):
        """Verifica se todas as dependências estão instaladas"""
        try:
            import psutil
        except ImportError:
            self.show_dependency_error()
            sys.exit(1)

    def initialize_variables(self):
        """Inicializa variáveis importantes"""
        self.process_list = []
        self.filtered_processes = []
        self.selected_pid = None
        self.status_text = tk.StringVar()
        self.status_text.set("Pronto")
        self.search_text = tk.StringVar()

    def setup_styles(self):
        """Configura todos os estilos visuais"""
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Cores base
        self.bg_color = '#1a1a1a'
        self.fg_color = '#e6e6e6'
        self.accent_color = '#4a6baf'
        self.danger_color = '#af4a4a'
        
        # Configuração de estilos
        self.configure_styles()

    def configure_styles(self):
        """Configura os estilos individuais"""
        # Frame principal
        self.style.configure('Main.TFrame', background=self.bg_color)
        
        # Labels
        self.style.configure(
            'Title.TLabel',
            background=self.bg_color,
            foreground=self.accent_color,
            font=('Helvetica', 14, 'bold')
        )
        
        self.style.configure(
            'Status.TLabel',
            background='#2d2d2d',
            foreground=self.fg_color,
            relief=tk.SUNKEN,
            padding=5
        )
        
        # Botões
        self.style.configure(
            'Dark.TButton',
            background='#2d2d2d',
            foreground=self.fg_color
        )
        
        self.style.configure(
            'Kill.TButton',
            background=self.accent_color,
            foreground=self.fg_color
        )
        
        self.style.configure(
            'ForceKill.TButton',
            background=self.danger_color,
            foreground=self.fg_color
        )
        
        # Treeview
        self.style.configure(
            'Process.Treeview',
            background='#2d2d2d',
            foreground=self.fg_color,
            fieldbackground='#2d2d2d',
            rowheight=25
        )
        
        self.style.configure(
            'Process.Treeview.Heading',
            background='#3a3a3a',
            foreground=self.fg_color,
            relief=tk.FLAT
        )
        
        self.style.map(
            'Process.Treeview',
            background=[('selected', self.accent_color)]
        )

    def build_ui(self):
        """Constrói toda a interface do usuário"""
        # Frame principal
        self.main_frame = ttk.Frame(self.root, style='Main.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # Cabeçalho
        self.build_header()
        
        # Barra de pesquisa
        self.build_search_bar()
        
        # Lista de processos
        self.build_process_list()
        
        # Controles
        self.build_controls()
        
        # Barra de status
        self.build_status_bar()

    def build_header(self):
        """Constrói o cabeçalho da aplicação"""
        header_frame = ttk.Frame(self.main_frame)
        header_frame.pack(fill=tk.X, pady=(0, 10))
        
        title_label = ttk.Label(
            header_frame,
            text="BlackWing Process Killer",
            style='Title.TLabel'
        )
        title_label.pack(side=tk.LEFT)
        
        if not self.admin_mode:
            admin_warning = ttk.Label(
                header_frame,
                text="(Modo limitado - Execute como administrador para acesso completo)",
                style='Title.TLabel',
                foreground='#ff5555'
            )
            admin_warning.pack(side=tk.RIGHT)

    def build_search_bar(self):
        """Constrói a barra de pesquisa"""
        search_frame = ttk.Frame(self.main_frame)
        search_frame.pack(fill=tk.X, pady=(0, 10))
        
        self.search_entry = ttk.Entry(
            search_frame,
            textvariable=self.search_text,
            style='Dark.TEntry'
        )
        self.search_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 10))
        
        refresh_btn = ttk.Button(
            search_frame,
            text="Atualizar",
            command=self.update_process_list,
            style='Dark.TButton'
        )
        refresh_btn.pack(side=tk.LEFT)

    def build_process_list(self):
        """Constrói a lista de processos"""
        tree_frame = ttk.Frame(self.main_frame)
        tree_frame.pack(fill=tk.BOTH, expand=True)
        
        # Treeview
        self.tree = ttk.Treeview(
            tree_frame,
            columns=("pid", "name", "status", "user", "cpu", "memory"),
            show="headings",
            style='Process.Treeview',
            selectmode='browse'
        )
        
        # Configuração das colunas
        columns = [
            ("pid", "PID", 80),
            ("name", "Nome", 250),
            ("status", "Status", 100),
            ("user", "Usuário", 150),
            ("cpu", "CPU %", 80),
            ("memory", "Memória %", 90)
        ]
        
        for col_id, col_text, col_width in columns:
            self.tree.heading(col_id, text=col_text)
            self.tree.column(col_id, width=col_width, anchor=tk.W)
        
        # Barra de rolagem
        scrollbar = ttk.Scrollbar(tree_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tree.pack(fill=tk.BOTH, expand=True)

    def build_controls(self):
        """Constrói os controles principais"""
        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(fill=tk.X, pady=(10, 0))
        
        self.kill_btn = ttk.Button(
            control_frame,
            text="Finalizar Processo",
            command=self.kill_selected,
            style='Kill.TButton',
            state=tk.DISABLED
        )
        self.kill_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        self.force_kill_btn = ttk.Button(
            control_frame,
            text="Finalizar Forçadamente",
            command=lambda: self.kill_selected(force=True),
            style='ForceKill.TButton',
            state=tk.DISABLED
        )
        self.force_kill_btn.pack(side=tk.LEFT)

    def build_status_bar(self):
        """Constrói a barra de status"""
        status_frame = ttk.Frame(self.main_frame)
        status_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_label = ttk.Label(
            status_frame,
            textvariable=self.status_text,
            style='Status.TLabel'
        )
        status_label.pack(fill=tk.X)

    def setup_bindings(self):
        """Configura os eventos da interface"""
        self.search_entry.bind('<KeyRelease>', self.filter_processes)
        self.tree.bind('<<TreeviewSelect>>', self.on_select_process)
        self.tree.bind('<Button-3>', self.show_context_menu)

    def update_process_list(self):
        """Atualiza a lista de processos"""
        self.status_text.set("Obtendo lista de processos...")
        self.root.update()
        
        try:
            # Executa em uma thread separada para não travar a interface
            Thread(target=self._load_processes, daemon=True).start()
        except Exception as e:
            self.status_text.set(f"Erro: {str(e)}")

    def _load_processes(self):
        """Carrega os processos em uma thread separada"""
        try:
            processes = []
            for proc in psutil.process_iter(['pid', 'name', 'status', 'username', 'cpu_percent', 'memory_percent']):
                try:
                    processes.append((
                        proc.info['pid'],
                        proc.info['name'],
                        proc.info['status'],
                        proc.info['username'] or 'N/A',
                        f"{proc.info['cpu_percent']:.1f}",
                        f"{proc.info['memory_percent']:.1f}"
                    ))
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
            
            self.process_list = processes
            self.filtered_processes = processes
            
            # Atualiza a interface na thread principal
            self.root.after(0, self._update_process_display)
        except Exception as e:
            self.root.after(0, lambda: self.status_text.set(f"Erro ao carregar processos: {str(e)}"))

    def _update_process_display(self):
        """Atualiza a exibição dos processos na interface"""
        self.tree.delete(*self.tree.get_children())
        
        for proc in self.filtered_processes:
            self.tree.insert('', tk.END, values=proc, iid=proc[0])
        
        self.status_text.set(f"Pronto - {len(self.filtered_processes)} processos listados")

    def filter_processes(self, event=None):
        """Filtra os processos com base no texto de pesquisa"""
        search_term = self.search_text.get().lower()
        
        if not search_term:
            self.filtered_processes = self.process_list
        else:
            self.filtered_processes = [
                p for p in self.process_list 
                if search_term in p[1].lower()
            ]
        
        self._update_process_display()

    def on_select_process(self, event):
        """Lida com a seleção de um processo"""
        selected = self.tree.selection()
        if selected:
            self.selected_pid = int(selected[0])
            self.kill_btn.config(state=tk.NORMAL)
            self.force_kill_btn.config(state=tk.NORMAL)
        else:
            self.selected_pid = None
            self.kill_btn.config(state=tk.DISABLED)
            self.force_kill_btn.config(state=tk.DISABLED)

    def kill_selected(self, force=False):
        """Finaliza o processo selecionado"""
        if not self.selected_pid:
            return
        
        process_name = next(
            (p[1] for p in self.process_list if p[0] == self.selected_pid),
            str(self.selected_pid)
        )

        action = "finalizar forçadamente" if force else "finalizar"
        
        if not messagebox.askyesno(
            "Confirmar",
            f"Tem certeza que deseja {action} o processo {process_name} (PID: {self.selected_pid})?"
        ):
            return
        
        try:
            proc = psutil.Process(self.selected_pid)
            if force:
                proc.kill()
            else:
                proc.terminate()
            
            messagebox.showinfo(
                "Sucesso",
                f"Processo {process_name} (PID: {self.selected_pid}) {action.replace('finalizar', 'finalizado')} com sucesso."
            )
            self.update_process_list()
        except psutil.NoSuchProcess:
            messagebox.showerror(
                "Erro",
                f"O processo {process_name} (PID: {self.selected_pid}) não existe mais."
            )
            self.update_process_list()
        except psutil.AccessDenied:
            messagebox.showerror(
                "Erro de Permissão",
                f"Permissão negada para {action} o processo {process_name} (PID: {self.selected_pid})."
            )
        except Exception as e:
            messagebox.showerror(
                "Erro",
                f"Ocorreu um erro ao {action} o processo: {str(e)}"
            )

    def show_context_menu(self, event):
        """Mostra o menu de contexto"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            self.selected_pid = int(item)
            
            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(
                label="Finalizar Processo",
                command=self.kill_selected
            )
            menu.add_command(
                label="Finalizar Forçadamente",
                command=lambda: self.kill_selected(force=True)
            )
            
            try:
                menu.tk_popup(event.x_root, event.y_root)
            finally:
                menu.grab_release()

    def is_admin(self):
        """Verifica se o programa está sendo executado como administrador"""
        try:
            return os.getuid() == 0
        except AttributeError:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0

    def show_admin_warning(self):
        """Mostra aviso sobre falta de privilégios"""
        messagebox.showwarning(
            "Aviso de Permissão",
            "Você está executando sem privilégios de administrador.\n"
            "Alguns processos podem não ser listados ou finalizados.\n\n"
            "Para acesso completo, execute o programa como administrador."
        )

    def show_dependency_error(self):
        """Mostra erro de dependência"""
        root = tk.Tk()
        root.withdraw()
        
        if messagebox.askyesno(
            "Biblioteca necessária",
            "O módulo 'psutil' não está instalado. Deseja instalar agora?"
        ):
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
                messagebox.showinfo(
                    "Sucesso",
                    "Biblioteca instalada com sucesso. Por favor, execute o programa novamente."
                )
            except:
                messagebox.showerror(
                    "Erro",
                    "Não foi possível instalar a biblioteca automaticamente.\n"
                    "Por favor, instale manualmente com: pip install psutil"
                )
        
        root.destroy()

def main():
    """Função principal de inicialização"""
    root = tk.Tk()
    app = BlackWing(root)
    
    # No Windows, tenta pedir elevação após 1 segundo
    if not app.admin_mode and sys.platform == 'win32':
        root.after(1000, lambda: ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, " ".join(sys.argv), None, 1
        ))
    
    root.mainloop()

if __name__ == "__main__":
    main()