from PyQt5.QtWidgets import (QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QLabel, QLineEdit, QPushButton, QTreeView, QMessageBox, 
                            QMenu, QStatusBar, QHeaderView)
from PyQt5.QtCore import Qt, QAbstractTableModel, QModelIndex, pyqtSignal
from PyQt5.QtGui import QColor, QBrush
from typing import List, Tuple, Optional
from script import ProcessManager

class ProcessTableModel(QAbstractTableModel):
    def __init__(self, data: List[Tuple], headers: List[str], parent=None):
        super().__init__(parent)
        self._data = data
        self._headers = headers
    
    def rowCount(self, parent: QModelIndex = None) -> int:
        return len(self._data)
    
    def columnCount(self, parent: QModelIndex = None) -> int:
        return len(self._headers)
    
    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid():
            return None
        
        if role == Qt.DisplayRole:
            return self._data[index.row()][index.column()]
        
        if role == Qt.TextAlignmentRole:
            return Qt.AlignLeft | Qt.AlignVCenter
        
        return None
    
    def headerData(self, section: int, orientation: Qt.Orientation, role: int = Qt.DisplayRole):
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return self._headers[section]
        return None
    
    def update_data(self, new_data: List[Tuple]):
        self.beginResetModel()
        self._data = new_data
        self.endResetModel()

class BlackWingUI(QMainWindow):
    process_selected = pyqtSignal(int)
    
    def __init__(self):
        super().__init__()
        self.process_manager = ProcessManager()
        self.selected_pid: Optional[int] = None
        self.init_ui()
        self.check_admin_status()
        self.load_processes()
    
    def init_ui(self):
        """Inicializa a interface do usuário"""
        self.setWindowTitle("BlackWing Process Killer")
        self.setGeometry(100, 100, 1000, 700)
        self.setMinimumSize(800, 600)
        
        # Widget central
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        
        # Layout principal
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # Cabeçalho
        self.create_header(main_layout)
        
        # Barra de pesquisa
        self.create_search_bar(main_layout)
        
        # Lista de processos
        self.create_process_table(main_layout)
        
        # Controles
        self.create_controls(main_layout)
        
        # Barra de status
        self.create_status_bar()
        
        # Conexões de sinal
        self.process_selected.connect(self.on_process_selected)
    
    def create_header(self, layout: QVBoxLayout):
        """Cria o cabeçalho da aplicação"""
        header_layout = QHBoxLayout()
        
        title_label = QLabel("BlackWing Process Killer")
        title_label.setStyleSheet("font-size: 14pt; font-weight: bold; color: #4a6baf;")
        header_layout.addWidget(title_label)
        
        self.admin_label = QLabel()
        self.admin_label.setStyleSheet("color: #ff5555;")
        header_layout.addWidget(self.admin_label, alignment=Qt.AlignRight)
        
        layout.addLayout(header_layout)
    
    def create_search_bar(self, layout: QVBoxLayout):
        """Cria a barra de pesquisa"""
        search_layout = QHBoxLayout()
        
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Pesquisar processos...")
        self.search_input.textChanged.connect(self.filter_processes)
        search_layout.addWidget(self.search_input)
        
        self.refresh_btn = QPushButton("Atualizar")
        self.refresh_btn.clicked.connect(self.load_processes)
        search_layout.addWidget(self.refresh_btn)
        
        layout.addLayout(search_layout)
    
    def create_process_table(self, layout: QVBoxLayout):
        """Cria a tabela de processos"""
        self.table_view = QTreeView()
        self.table_view.setSelectionBehavior(QTreeView.SelectRows)
        self.table_view.setSelectionMode(QTreeView.SingleSelection)
        self.table_view.setContextMenuPolicy(Qt.CustomContextMenu)
        self.table_view.customContextMenuRequested.connect(self.show_context_menu)
        self.table_view.clicked.connect(self.on_table_click)
        
        # Modelo de dados
        self.model = ProcessTableModel([], ["PID", "Nome", "Status", "Usuário", "CPU %", "Memória %"])
        self.table_view.setModel(self.model)
        
        # Ajustar largura das colunas
        for i in range(self.model.columnCount()):
            self.table_view.header().setSectionResizeMode(i, QHeaderView.ResizeToContents)
        
        layout.addWidget(self.table_view)
    
    def create_controls(self, layout: QVBoxLayout):
        """Cria os controles principais"""
        controls_layout = QHBoxLayout()
        
        self.kill_btn = QPushButton("Finalizar Processo")
        self.kill_btn.setStyleSheet("background-color: #4a6baf; color: white;")
        self.kill_btn.clicked.connect(lambda: self.kill_selected(False))
        self.kill_btn.setEnabled(False)
        controls_layout.addWidget(self.kill_btn)
        
        self.force_kill_btn = QPushButton("Finalizar Forçadamente")
        self.force_kill_btn.setStyleSheet("background-color: #af4a4a; color: white;")
        self.force_kill_btn.clicked.connect(lambda: self.kill_selected(True))
        self.force_kill_btn.setEnabled(False)
        controls_layout.addWidget(self.force_kill_btn)
        
        layout.addLayout(controls_layout)
    
    def create_status_bar(self):
        """Cria a barra de status"""
        self.status_bar = QStatusBar()
        self.status_bar.showMessage("Pronto")
        self.setStatusBar(self.status_bar)
    
    def check_admin_status(self):
        """Verifica e exibe o status de administrador"""
        if not self.process_manager.admin_mode:
            self.admin_label.setText("(Modo limitado - Execute como administrador para acesso completo)")
    
    def load_processes(self):
        """Carrega a lista de processos"""
        self.status_bar.showMessage("Obtendo lista de processos...")
        QApplication.processEvents()
        
        try:
            processes = self.process_manager.get_processes()
            self.model.update_data(processes)
            self.status_bar.showMessage(f"Pronto - {len(processes)} processos listados")
        except Exception as e:
            self.status_bar.showMessage(f"Erro ao carregar processos: {str(e)}")
            QMessageBox.critical(self, "Erro", f"Erro ao carregar processos: {str(e)}")
    
    def filter_processes(self):
        """Filtra os processos com base no texto de pesquisa"""
        search_term = self.search_input.text()
        filtered = self.process_manager.filter_processes(search_term)
        self.model.update_data(filtered)
        self.status_bar.showMessage(f"Pronto - {len(filtered)} processos listados")
    
    def on_table_click(self, index: QModelIndex):
        """Lida com a seleção de um processo na tabela"""
        row = index.row()
        pid = self.model._data[row][0]
        self.process_selected.emit(pid)
    
    def on_process_selected(self, pid: int):
        """Atualiza a interface quando um processo é selecionado"""
        self.selected_pid = pid
        self.kill_btn.setEnabled(True)
        self.force_kill_btn.setEnabled(True)
    
    def kill_selected(self, force: bool = False):
        """Finaliza o processo selecionado"""
        if not self.selected_pid:
            return
        
        process_name = next(
            (p[1] for p in self.model._data if p[0] == self.selected_pid),
            str(self.selected_pid)
        )
        
        action = "finalizar forçadamente" if force else "finalizar"
        reply = QMessageBox.question(
            self, "Confirmar",
            f"Tem certeza que deseja {action} o processo {process_name} (PID: {self.selected_pid})?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.No
        )
        
        if reply == QMessageBox.No:
            return
        
        try:
            success = self.process_manager.kill_process(self.selected_pid, force)
            if success:
                QMessageBox.information(
                    self, "Sucesso",
                    f"Processo {process_name} (PID: {self.selected_pid}) {action.replace('finalizar', 'finalizado')} com sucesso."
                )
                self.load_processes()
            else:
                QMessageBox.warning(
                    self, "Aviso",
                    f"O processo {process_name} (PID: {self.selected_pid}) não existe mais."
                )
                self.load_processes()
        except PermissionError as e:
            QMessageBox.critical(
                self, "Erro de Permissão",
                f"Permissão negada para {action} o processo {process_name} (PID: {self.selected_pid})."
            )
        except Exception as e:
            QMessageBox.critical(
                self, "Erro",
                f"Ocorreu um erro ao {action} o processo: {str(e)}"
            )
    
    def show_context_menu(self, position):
        """Mostra o menu de contexto"""
        index = self.table_view.indexAt(position)
        if index.isValid():
            pid = self.model._data[index.row()][0]
            self.process_selected.emit(pid)
            
            menu = QMenu()
            
            kill_action = menu.addAction("Finalizar Processo")
            kill_action.triggered.connect(lambda: self.kill_selected(False))
            
            force_kill_action = menu.addAction("Finalizar Forçadamente")
            force_kill_action.triggered.connect(lambda: self.kill_selected(True))
            
            menu.exec_(self.table_view.viewport().mapToGlobal(position))
    
    def show_admin_warning(self):
        """Mostra aviso sobre falta de privilégios"""
        QMessageBox.warning(
            self, "Aviso de Permissão",
            "Você está executando sem privilégios de administrador.\n"
            "Alguns processos podem não ser listados ou finalizados.\n\n"
            "Para acesso completo, execute o programa como administrador."
        )
    
    def show_dependency_error(self):
        """Mostra erro de dependência"""
        reply = QMessageBox.question(
            self, "Biblioteca necessária",
            "O módulo 'psutil' não está instalado. Deseja instalar agora?",
            QMessageBox.Yes | QMessageBox.No, QMessageBox.Yes
        )
        
        if reply == QMessageBox.Yes:
            try:
                success = self.process_manager.install_dependencies()
                if success:
                    QMessageBox.information(
                        self, "Sucesso",
                        "Biblioteca instalada com sucesso. Por favor, execute o programa novamente."
                    )
                else:
                    QMessageBox.critical(
                        self, "Erro",
                        "Não foi possível instalar a biblioteca automaticamente.\n"
                        "Por favor, instale manualmente com: pip install psutil"
                    )
            except:
                QMessageBox.critical(
                    self, "Erro",
                    "Ocorreu um erro durante a instalação."
                )
        self.close()