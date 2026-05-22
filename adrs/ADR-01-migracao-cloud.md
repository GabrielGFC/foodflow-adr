# ADR-01 — Estratégia de Migração Cloud da FoodFlow

**Projeto:** FoodFlow (sistema de pedidos de delivery)
**Autor:** Gabriel Carvalho — 23201412
**Disciplina:** Arquitetura de Software
**Data:** 22/05/2026
**Status:** Proposto

---

## 1. Decisão

Adotar a **Opção A — PaaS Gerenciado**: migrar a aplicação Django para **Railway** e o banco PostgreSQL para **Supabase**.

---

## 2. Contexto

A FoodFlow opera hoje como monolito Python/Django em um único VPS IaaS, com PostgreSQL no mesmo servidor e deploy manual via SSH. O sistema atingiu o limite operacional:

- **Saturação:** servidor a 80% de CPU nos picos de fim de semana, com pedidos atrasando.
- **Downtime:** 30 min/semana de deploy manual — incompatível com SLA informal de >99% (orçamento de 7h12min/mês de indisponibilidade; um único deploy já consome ~7%).
- **Budget rígido:** R$ 2.000/mês de infra.
- **Time enxuto:** 4 devs, 1 DBA, 1 ops part-time — sem especialista em Kubernetes nem em IaC avançada.
- **Janela curta:** decisão precisa entregar valor em semanas, não meses.

Três restrições pesaram mais na decisão:

1. **Orçamento (R$ 2k/mês)** — elimina diretamente a Opção C (R$ 3.500, +75% acima do teto).
2. **Expertise disponível** — o time não tem ops dedicado nem experiência operando K8s/EKS em produção; assumir essa complexidade introduziria risco de incidentes maior que o problema atual.
3. **SLA + janela de entrega** — precisamos reduzir o downtime de deploy *agora*, não em 2 meses.

---

## 3. Justificativa com Trade-off

### O que ganhamos

- **Custo abaixo do teto:** ~R$ 800/mês deixa R$ 1.200 de folga mensal para observabilidade (Sentry, Datadog) e tráfego futuro.
- **Time-to-value rápido:** 1 semana de setup contra 3 semanas (B) ou 2 meses (C).
- **Auto-scaling automático** até 10 instâncias — resolve o gargalo dos fins de semana sem script manual.
- **Deploy zero-downtime** nativo do Railway, eliminando os 30 min semanais e viabilizando o SLA >99%.
- **PostgreSQL gerenciado (Supabase):** backup, replicação e patching saem da mesa do DBA, liberando-o para modelagem e performance.
- **Carga operacional baixa:** o ops part-time consegue sustentar a operação sem virar gargalo.

### O que abrimos mão

- **Controle de infraestrutura:** sem acesso a tuning de SO, networking customizado ou kernel.
- **Portabilidade / lock-in:** acoplamento operacional a Railway + Supabase; sair custa esforço de migração.
- **Granularidade de escala:** auto-scaling é por aplicação inteira, não por módulo (como seria em K8s).
- **Custo unitário em escala alta:** PaaS fica mais caro por requisição quando o volume cresce muito acima do plano atual.

### Por que o trade-off vale a pena **neste contexto**

O trade-off central é **controle × velocidade de entrega e carga operacional**. A FoodFlow hoje não tem problema de controle fino — tem problema de **saturação, downtime e time pequeno**. Pagar com "menos controle" para resolver os três problemas reais em uma semana, dentro do orçamento, é uma troca racional. O lock-in só se torna doloroso em escala muito maior que a atual; até lá a empresa terá receita e time para reavaliar.

K8s (Opção C) é tecnicamente superior em controle e granularidade, mas **fora do budget e acima da capacidade operacional do time**. "Mais moderno" não é justificativa — é custo sem retorno proporcional neste estágio.

Docker puro (Opção B) fica no meio do caminho: paga 87% mais que PaaS, ainda exige scripts de auto-scaling manuais e mantém o ops como gargalo. Não resolve o problema de carga operacional.

---

## 4. Consequências

### Próximos 30 dias

1. **Semana 1** — Provisionar Railway + Supabase; configurar variáveis de ambiente e secrets; validar deploy de staging.
2. **Semana 2** — Migrar dados do PostgreSQL on-premise para Supabase (dump + restore + validação de integridade); ensaiar rollback.
3. **Semana 3** — Cutover em janela de baixo tráfego (madrugada de terça); manter VPS antigo em standby por 7 dias.
4. **Semana 4** — Desligar VPS antigo; instrumentar métricas básicas (latência, erro, throughput) e configurar alertas no Sentry.

### Decisões que essa escolha vai forçar no futuro

- **Observabilidade:** PaaS oculta a infra, então precisaremos escolher uma stack de APM (Sentry/Datadog/New Relic) — não dá mais para `tail -f` no servidor.
- **Estratégia de saída do monolito:** quando o auto-scaling do Railway começar a ficar caro (estimativa: >3× o tráfego atual), seremos forçados a decidir entre (i) extrair módulos críticos para Serverless/Functions ou (ii) migrar para a Opção C (K8s) com o time já maior.
- **Compliance e dados sensíveis:** se a FoodFlow passar a processar pagamentos diretamente (PCI-DSS) ou crescer para outros países (LGPD/GDPR cross-border), será necessário reavaliar se Supabase atende aos requisitos regulatórios.
- **Disaster Recovery:** será preciso documentar como restaurar de um backup do Supabase em outro provedor — mitigação parcial do lock-in.

---

## 5. Referências

- Aulas de Arquitetura — modelos de serviço (IaaS, PaaS, SaaS, FaaS) e trade-offs cloud.
- Hooker — princípios de decisão arquitetural (contexto sobre tecnologia).
- Caso FoodFlow — Ciclo 1 e enunciado do Ciclo 3.
