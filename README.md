1.  **Infraestrutura (Terraform)**: Provisiona uma instância EC2 na AWS, instala o K3s (um cluster Kubernetes leve) e configura os Security Groups necessários.
2.  **Aplicação (Python/Flask)**: Uma aplicação web simples que expõe uma rota `/` e uma rota `/metrics` para monitoramento com Prometheus.
3.  **Banco de Dados (PostgreSQL)**: Banco de dados relacional rodando dentro do cluster, com persistência em disco (PVC).
4.  **Contêiner (Docker)**: A aplicação é empacotada em uma imagem Docker.
5.  **Orquestração (Kubernetes)**: Deployments e Services gerenciam a aplicação e o banco no cluster K3s.
6.  **CI/CD (GitHub Actions)**: Um pipeline automatizado que:
    *   **Testa** a aplicação com `pytest`.
    *   **Verifica Segurança** da imagem Docker com **Trivy** (DevSecOps).
    *   **Constrói** a imagem Docker e a **publica** no GitHub Container Registry (GHCR).
    *   **Implanta** a nova versão da aplicação no cluster K3s.

- **Infraestrutura como Código**: Toda a infraestrutura é gerenciável e versionável.
- **Deploy Automatizado**: Zero intervenção manual para novos deploys após o setup inicial.
- **Testes Integrados**: O pipeline só prossegue se os testes unitários passarem.
- **Segurança (DevSecOps)**: Bloqueia o deploy se vulnerabilidades críticas forem encontradas na imagem.
- **Acesso Remoto Seguro**: Geração automática de chave SSH e configuração para acesso ao cluster.

## 📂 Estrutura do Projeto
│   ├── test_app.py
│   └── Dockerfile
├── k8s/                  # Manifestos do Kubernetes
│   ├── k8s-deployment.yaml
│   ├── postgres.yaml
│   └── postgres-secret.yaml
├── terrafrom/            # Código Terraform para a infraestrutura
│   ├── main.tf
│   ├── variables.tf

- **URL da Aplicação**: `http://<IP_PUBLICO_DA_INSTANCIA>:30005`
- **URL das Métricas**: `http://<IP_PUBLICO_DA_INSTANCIA>:30005/metrics`
- **Teste de Conexão DB**: `http://<IP_PUBLICO_DA_INSTANCIA>:30005/db`
- **Grafana**: `http://<IP_PUBLICO_DA_INSTANCIA>:30007` (Login: admin / admin)

O IP público pode ser obtido novamente com o comando `terraform output ec2_public_ip` na pasta `terrafrom`.
