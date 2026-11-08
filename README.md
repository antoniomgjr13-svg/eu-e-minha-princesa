# 💕 Eu e Minha Princesa

Um aplicativo desktop feito com amor para você e sua namorada registrarem momentos especiais e acompanharem como vocês estão se sentindo! ❤️

## ✨ Funcionalidades

- 📝 **Registrar Momentos**: Anote como você está se sentindo com emojis, notas de 1-10 e mensagens
- 📷 **Adicionar Fotos**: Cada momento pode ter uma foto especial
- 📖 **Histórico Completo**: Veja todos os momentos salvos em uma timeline linda
- 📊 **Dashboard**: Estatísticas e resumo dos momentos de cada um
- 💑 **Dois Perfis**: Um para você e outro para sua princesa
- 🎨 **Interface Bonita**: Design moderno com cores personalizadas para cada pessoa
- 💾 **Tudo Local**: Seus dados ficam salvos apenas no seu computador

## 🚀 Como Usar

### 1. Instalar Dependências

Abra o terminal/prompt de comando na pasta do app e execute:

```bash
pip install -r requirements.txt
```

### 2. Rodar o Aplicativo

```bash
python app.py
```

### 3. Usar o App

1. **Primeira vez**: O app já vem configurado com dois perfis padrão ("Você" e "Minha Princesa")
2. **Registrar momento**: 
   - Clique no botão com o nome de quem está registrando
   - Escolha o sentimento (emoji)
   - Dê uma nota de 1 a 10
   - Escreva uma mensagem (opcional)
   - Adicione uma foto (opcional)
   - Clique em "Salvar Momento"
3. **Ver histórico**: Clique em "📖 Histórico" para ver todos os momentos
4. **Ver estatísticas**: Clique em "📊 Dashboard" para ver resumos
5. **Configurar**: Clique em "⚙️ Config" para mudar nomes

## 📁 Estrutura de Arquivos

```
eu_e_minha_princesa/
├── app.py              # Aplicativo principal
├── database.py         # Gerenciador do banco de dados
├── requirements.txt    # Dependências
├── README.md          # Este arquivo
├── data/
│   ├── app.db         # Banco de dados (criado automaticamente)
│   └── fotos/         # Fotos dos momentos
└── assets/            # Recursos visuais
```

## 🎨 Personalização

Você pode personalizar os nomes nas configurações do app ou diretamente editando o código em `database.py` na função `criar_pessoas_padrao()`.

## 💝 Sentimentos Disponíveis

- 😊 Muito Feliz
- 🙂 Feliz
- 😐 Normal
- 😔 Triste
- 😢 Muito Triste
- 😍 Apaixonado(a)
- 🥰 Amando Muito
- 😤 Irritado(a)

## 📝 Próximas Versões (Ideias)

- [ ] Gerar arquivo .exe para não precisar rodar via Python
- [ ] Gráficos de evolução de humor ao longo do tempo
- [ ] Exportar dados em PDF
- [ ] Modo escuro/claro
- [ ] Notificações para registrar momentos diários
- [ ] Backup automático

## ❤️ Feito com Amor

Criado especialmente para casais que querem guardar momentos especiais juntos!

---

**Versão**: 1.0  
**Data**: Novembro 2024
