# BlackWing Process Killer

## 📌 Visão Geral

O **BlackWing Process Killer** é uma ferramenta de gerenciamento de processos com interface gráfica desenvolvida em Python, projetada para oferecer controle avançado sobre processos em execução no sistema. Com um tema escuro inspirado em corvos (BlackWing = "Asa Negra"), combina funcionalidade robusta com uma experiência visual elegante.

## ✨ Funcionalidades Principais

- 🖥️ **Listagem completa de processos** com detalhes (PID, Nome, Status, Usuário, CPU, Memória)
- 🔍 **Filtro inteligente** por nome de processo
- 💀 **Finalização de processos** (normal e forçada)
- 🛡️ **Modo administrador** para controle total do sistema
- 📊 **Atualização em tempo real** dos recursos consumidos
- 🖱️ **Menu de contexto** para ações rápidas
- 🎨 **Interface dark mode** com estilos personalizados

## 🛠️ Tecnologias Utilizadas

- Python 3.8+
- Biblioteca Tkinter (interface gráfica)
- Módulo psutil (gerenciamento de processos)
- Threading (para operações assíncronas)

## ⚙️ Requisitos do Sistema

- Python 3.8 ou superior instalado
- Pip para gerenciamento de dependências
- Privilégios de administrador (recomendado para funcionalidade completa)

## 🚀 Instalação

1. Clone o repositório ou baixe o arquivo `blackwing.py`:
   ```bash
   git clone https://github.com/seu-usuario/blackwing-process-killer.git
   cd blackwing-process-killer
   ```

2. Instale as dependências:
   ```bash
   pip install psutil
   ```

3. Execute o aplicativo:
   ```bash
   python blackwing.py
   ```

   **Para acesso completo:** execute como administrador:
   - **Windows**: Clique direito > "Executar como administrador"
   - **Linux/macOS**: `sudo python3 blackwing.py`

## 🖥️ Como Usar

1. **Listar processos**: A lista é carregada automaticamente ao iniciar
2. **Filtrar**: Digite na barra de pesquisa para encontrar processos específicos
3. **Finalizar**:
   - Selecione um processo
   - Clique em "Finalizar Processo" (terminate) ou "Finalizar Forçadamente" (kill)
   - Confirme a ação
4. **Atualizar**: Use o botão "Atualizar" para refresh na lista

## 📸 Capturas de Tela

*(Inclua imagens da interface funcionando aqui)*

## 🤝 Contribuição

Contribuições são bem-vindas! Siga estes passos:

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/incrivel`)
3. Commit suas mudanças (`git commit -m 'Adicionando feature incrível'`)
4. Push para a branch (`git push origin feature/incrivel`)
5. Abra um Pull Request

## 📜 Licença

Distribuído sob a licença MIT. Veja `LICENSE` para mais informações.


---

**Nota**: Este projeto foi desenvolvido para fins educacionais e de produtividade. Use com responsabilidade ao finalizar processos de sistema.
