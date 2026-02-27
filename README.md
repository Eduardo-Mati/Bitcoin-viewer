# 🚀 Bitcoin Viewer - Crypto Dashboard & AI Analyst

![Project Status](https://img.shields.io/badge/status-online-brightgreen)
![React](https://img.shields.io/badge/react-%2320232a.svg?style=flat&logo=react&logoColor=%2361DAFB)
![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=flat&logo=fastapi)
![Redis](https://img.shields.io/badge/redis-%23DD0031.svg?style=flat&logo=redis&logoColor=white)
![MongoDB](https://img.shields.io/badge/MongoDB-%234ea94b.svg?style=flat&logo=mongodb&logoColor=white)
![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=flat&logo=docker&logoColor=white)

> Um dashboard financeiro *Full-Stack* de alta performance que monitora criptomoedas em tempo real, gera gráficos históricos no backend e utiliza **Inteligência Artificial Generativa (Google Gemini)** para fornecer análises de mercado instantâneas.

---

## 🧠 Diferenciais Técnicos

Este não é apenas um CRUD simples. O projeto foi desenhado com uma arquitetura de microsserviços orientada a eventos para garantir performance e escalabilidade:

1.  **Arquitetura Worker/Cache:**
    * Um **Worker Python** independente coleta dados da CoinGecko API a cada 30 segundos em background.
    * Os dados são salvos em um **Cache Redis** (camada de acesso rápido) e persistidos para histórico.
    * O **Backend FastAPI** consome apenas do Redis, garantindo resposta em milissegundos (<10ms) para o usuário, sem depender da latência de APIs externas.

2.  **AI Market Analyst:**
    * Integração nativa com **Google Gemini 1.5 Flash**.
    * O sistema envia os últimos candles de preço para a IA, que atua como um "Day Trader Sênior", analisando a tendência (Alta/Baixa) e recomendando Compra ou Venda em linguagem natural.

3.  **Gráficos Server-Side:**
    * Geração de gráficos de tendência utilizando `Matplotlib` no backend, servidos como streaming de imagem otimizado.

---

## 🛠 Tech Stack

### Backend & Dados
* **Python 3.11** + **FastAPI**: API REST assíncrona.
* **Redis**: Cache distribuído e Message Broker.
* **MongoDB**: Banco NoSQL para gestão de usuários e logs.
* **Google Gemini API**: Motor de inteligência artificial.
* **Matplotlib**: Processamento de dados e plotagem.

### Frontend
* **React.js (Vite)**: SPA reativa e veloz.
* **TailwindCSS**: Estilização moderna e responsiva.
* **Recharts / Axios**: Visualização e consumo de dados.

### Infraestrutura (DevOps)
* **Docker & Docker Compose**: Orquestração completa do ambiente.
* **Nginx**: Servidor web de alta performance (Proxy reverso).
* **CI/CD Friendly**: Estrutura pronta para deploy em nuvem (AWS/Render/VPS).

---

## 📸 Funcionalidades

* ✅ **Monitoramento em Tempo Real:** Preços de Bitcoin, Ethereum e Solana atualizados via WebSocket/Polling.
* ✅ **Autenticação Segura:** Sistema de Login e Registro com hash de senha e JWT (JSON Web Tokens).
* ✅ **Análise de IA sob Demanda:** Botão "Pedir Análise" que consulta o LLM em tempo real.
* ✅ **Histórico Visual:** Gráficos de 24h gerados dinamicamente.
* ✅ **Resiliência:** O sistema continua funcionando (lendo do cache) mesmo se a API externa cair temporariamente.

---

## 🚀 Como Rodar Localmente

Siga os passos abaixo para subir a arquitetura completa na sua máquina:

### Pré-requisitos
* Docker e Docker Compose instalados.
* Uma chave de API do Google Gemini (Gratuita no Google AI Studio).

### 1. Clone o repositório
```bash
git clone [https://github.com/SEU_USUARIO/bitcoin-viewer.git](https://github.com/SEU_USUARIO/bitcoin-viewer.git)
cd bitcoin-viewer
#
