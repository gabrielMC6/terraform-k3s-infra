 AWS K3s Lab: Infraestrutura, Persistência e CI/CD
Este projeto demonstra o provisionamento de uma infraestrutura em nuvem na AWS utilizando Terraform e a orquestração de uma aplicação Python/Flask em um cluster K3s. O foco está na automação do deploy e na garantia de persistência dos dados.

<img width="803" height="236" alt="modelo diagrama" src="https://github.com/user-attachments/assets/e42b4de3-c49a-4278-90b2-b3f85299948f" />

 O que foi implementado:
1. Infraestrutura como Código (IaC)
Provisionamento automatizado de VPC, Security Groups e instância EC2 via Terraform. O cluster K3s é configurado via User Data script, garantindo um ambiente pronto para uso logo após o boot da máquina.

<img width="806" height="147" alt="VPCCC" src="https://github.com/user-attachments/assets/1f2be9ba-1149-407a-aec1-d9b1d8bab7a3" />


2. Persistência de Dados
O banco de dados PostgreSQL utiliza Persistent Volume Claims (PVC) para armazenamento.

Por que importa: Isso garante que as informações salvas no banco não sejam perdidas caso o container ou a instância precisem ser reiniciados.

3. Segurança no Pipeline (DevSecOps)
Integração do Trivy no GitHub Actions para realizar o scan da imagem Docker.

O que faz: O pipeline interrompe o deploy caso sejam detectadas vulnerabilidades críticas na imagem, garantindo que apenas código minimamente seguro chegue ao cluster.


<img width="941" height="326" alt="ciecd" src="https://github.com/user-attachments/assets/92e75595-b267-4ed9-b46e-9c32b494cbec" />



4. Monitoramento e Métricas
Uso de Prometheus & Grafana para observabilidade do sistema.

Métricas: Acompanhamento de visitas por hora.
<img width="945" height="425" alt="grafana acessos" src="https://github.com/user-attachments/assets/ee880238-210c-4538-80c1-798e5a9ad7e0" />


## 📂 Estrutura do Projeto
/terraform: Scripts de automação AWS.

/k8s: Manifestos de Deployment, Service e PVC.

/app: Código Flask, Dockerfile e Testes unitários.

 Endpoints da Infraestrutura
A aplicação e os serviços de monitoramento podem ser acessados através dos endereços abaixo:

Aplicação Web: http://98.84.117.231:30005/

Teste de Persistência (DB): http://98.84.117.231:30005/db

Métricas da App (Prometheus): http://98.84.117.231:30005/metrics

Dashboard Grafana: http://98.84.117.231:30007

