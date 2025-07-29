import psutil
import os
import sys
import ctypes
import subprocess
from typing import List, Tuple, Optional

class ProcessManager:
    def __init__(self):
        self.process_list: List[Tuple] = []
        self.admin_mode: bool = self.is_admin()
    
    def is_admin(self) -> bool:
        """Verifica se o programa está sendo executado como administrador"""
        try:
            return os.getuid() == 0
        except AttributeError:
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
    
    def get_processes(self) -> List[Tuple]:
        """Obtém a lista de processos"""
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
        return processes
    
    def filter_processes(self, search_term: str) -> List[Tuple]:
        """Filtra os processos com base no termo de pesquisa"""
        if not search_term:
            return self.process_list
        return [p for p in self.process_list if search_term.lower() in p[1].lower()]
    
    def kill_process(self, pid: int, force: bool = False) -> bool:
        """Finaliza um processo"""
        try:
            proc = psutil.Process(pid)
            if force:
                proc.kill()
            else:
                proc.terminate()
            return True
        except psutil.NoSuchProcess:
            return False
        except psutil.AccessDenied:
            raise PermissionError("Permissão negada para finalizar o processo")
        except Exception as e:
            raise Exception(f"Erro ao finalizar processo: {str(e)}")
    
    def check_dependencies(self) -> bool:
        """Verifica se todas as dependências estão instaladas"""
        try:
            import psutil
            return True
        except ImportError:
            return False
    
    def install_dependencies(self) -> bool:
        """Tenta instalar as dependências necessárias"""
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "psutil"])
            return True
        except:
            return False