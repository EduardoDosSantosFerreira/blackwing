# BlackWing Process Killer

**BlackWing Process Killer** é uma ferramenta gráfica desenvolvida com PyQt5 que permite visualizar, filtrar e finalizar processos em execução no sistema operacional. Ideal para administradores de sistema e usuários que desejam uma interface simples e eficiente para gerenciar processos.

---

## ✨ Funcionalidades

* 🔍 Pesquisa dinâmica por nome de processo.
* 📋 Visualização de processos em uma tabela interativa.
* 🔄 Atualização da lista de processos.
* ✅ Finalização segura de processos.
* 💀 Finalização forçada de processos.
* ⚠️ Aviso quando executado sem privilégios administrativos.
* 📦 Verificação automática e instalação opcional da dependência `psutil`.

---

## 🖼️ Interface

A interface contém:

* Um **campo de pesquisa** para filtrar os processos.
* Uma **tabela de processos** com colunas: `PID`, `Nome`, `Status`, `Usuário`, `CPU %`, `Memória %`.
* Botões de **Finalizar Processo** e **Finalizar Forçadamente**.
* Um **menu de contexto** com opções rápidas ao clicar com o botão direito.
* Uma **barra de status** com mensagens de sistema e feedback ao usuário.

---

## 🚀 Requisitos

* Python 3.6+
* PyQt5
* psutil

### Instalação das dependências:

```bash
pip install pyqt5 psutil
```

Ou, ao executar o programa, caso `psutil` não esteja instalado, você será solicitado a instalá-lo automaticamente.

---

## 📁 Estrutura

```
.
├── main.py             # Código principal com a interface (este arquivo)
├── script.py           # Script auxiliar com a lógica de manipulação de processos (requerido)
└── README.md           # Este arquivo
```

---

## ⚙️ Executando o Programa

Certifique-se de que `script.py` esteja no mesmo diretório que `main.py`, e então execute:

```bash
python main.py
```

> 💡 Para acesso completo (como finalizar processos protegidos), execute como **administrador/root**.

---

## 🔐 Permissões

O programa detecta automaticamente se está sendo executado com privilégios de administrador. Caso não esteja, um aviso será exibido, e algumas funções podem estar limitadas.

---

## 🛠️ Desenvolvedor

**Modelo de Tabela Personalizada:**
A classe `ProcessTableModel` implementa um modelo baseado em `QAbstractTableModel`, que permite exibir e atualizar os dados dos processos dinamicamente.

**Gerenciamento de Processos:**
A lógica de listagem, filtragem e finalização dos processos está encapsulada em `script.py`, através da classe `ProcessManager`.

---

## 📌 Observações

* Compatível com Windows, Linux e macOS (funcionalidade de finalização pode variar por SO).
* O menu de contexto permite operações rápidas diretamente da tabela de processos.

---