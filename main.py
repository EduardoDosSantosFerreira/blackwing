import sys
import ctypes
from PyQt5.QtWidgets import QApplication
from ui import BlackWingUI
from script import ProcessManager

def run_as_admin():
    """Tenta executar o programa como administrador no Windows"""
    if sys.platform == 'win32':
        ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, " ".join(sys.argv), None, 1)

def main():
    """Função principal de inicialização"""
    app = QApplication(sys.argv)
    
    # Verificar dependências antes de iniciar
    process_manager = ProcessManager()
    if not process_manager.check_dependencies():
        # Criar uma QApplication temporária para mostrar a mensagem
        temp_app = QApplication(sys.argv)
        window = BlackWingUI()
        window.show_dependency_error()
        sys.exit(1)
    
    # Criar e mostrar a janela principal
    window = BlackWingUI()
    window.show()
    
    # No Windows, tentar pedir elevação após a janela ser mostrada
    if not process_manager.admin_mode and sys.platform == 'win32':
        window.show_admin_warning()
        # Aguardar um pouco antes de pedir elevação
        from PyQt5.QtCore import QTimer
        QTimer.singleShot(1000, run_as_admin)
    
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()