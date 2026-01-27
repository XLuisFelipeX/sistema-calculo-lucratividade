\# Regras de Negócio Iniciais



\## Sistema de Cálculo de Lucratividade



---



\## 1. Objetivo do Projeto



Este projeto tem como objetivo construir um \*\*Sistema de Cálculo de Lucratividade\*\*, baseado na leitura de planilhas financeiras extraídas de sistemas distintos, considerando regras de negócio específicas, com foco exclusivo em \*\*tarifas cobradas aos clientes elegíveis do GV8\*\*.



O sistema deverá:



\* Ler planilhas de diferentes sistemas de origem

\* Interpretar corretamente as operações

\* Identificar e marcar clientes elegíveis ao GV8 (regra crítica)

\* \*\*Aplicar explicitamente a elegibilidade no cálculo financeiro\*\*

\* Aplicar custos operacionais externos à planilha (futuro)

\* Calcular a lucratividade semanal

\* Permitir evolução para novos sistemas, bancos e contratos



---



\## 2. Decisões Técnicas (Sprint 0)



\* Linguagem: Python

\* Tipo de aplicação: Console

\* Nível: Iniciante

\* Abordagem: Desenvolvimento incremental por sprints

\* Fonte de dados: Planilhas (Excel) extraídas de sistemas financeiros



---



\## 3. Sistemas de Origem



O sistema trabalha com múltiplos sistemas de origem, que podem possuir características distintas quanto à elegibilidade dos clientes.



\### 3.1 Sistema Privilege



\* Banco liquidante: BMP

\* Formato de planilha: específico do sistema Privilege



\*\*Observação importante:\*\*

A planilha do sistema Privilege contém movimentações financeiras e tarifas de:



\* clientes indicados pelo GV8

\* clientes que não pertencem à carteira do GV8



O sistema Privilege \*\*não distingue explicitamente\*\*, em seu relatório, quais clientes são do GV8.

Por esse motivo, a elegibilidade de clientes deve ser verificada por \*\*regra externa\*\*.



---



\### 3.2 Sistema Fourbank



\* Sistema contratado exclusivamente pelo GV8

\* Todos os clientes presentes no relatório pertencem ao GV8



👉 Para o sistema Fourbank, a elegibilidade de clientes é \*\*implícita\*\*.



---



\### 3.3 Sistema Aarin (futuro)



\* Banco liquidante: Bradesco

\* Formato de planilha: diferente do sistema Privilege

\* Sistema contratado exclusivamente pelo GV8



👉 Para o sistema Aarin, a elegibilidade de clientes também é \*\*implícita\*\*.



---



\### Consideração Geral sobre Sistemas de Origem



Cada sistema pode possuir:



\* planilha própria

\* banco liquidante próprio

\* regras contratuais específicas

\* regras distintas de elegibilidade



O sistema deve estar preparado para lidar com essas diferenças de forma \*\*explícita, rastreável e extensível\*\*.



---



\## 4. Princípios Fundamentais de Cálculo



\### 4.1 Base de Cálculo



A lucratividade é calculada \*\*exclusivamente com base em TARIFAS\*\*.



Movimentações financeiras, transações operacionais ou ajustes sistêmicos \*\*não representam receita nem custo\*\* para fins de lucratividade do GV8.



---



\### 4.2 Elegibilidade de Clientes (Regra Crítica – GV8)



Somente clientes \*\*indicados/comercializados pelo GV8\*\* devem ser considerados no cálculo de lucratividade.



A aplicação da regra de elegibilidade depende do sistema de origem:



\* \*\*Sistemas exclusivos do GV8 (Fourbank, Aarin):\*\*

&nbsp; Todos os clientes são considerados elegíveis.



\* \*\*Sistema compartilhado (Privilege):\*\*

&nbsp; A elegibilidade do cliente deve ser verificada por meio de uma base externa de referência, mantida pelo GV8.



Portanto:



\* Clientes não indicados pelo GV8 devem ser \*\*totalmente ignorados\*\*

\* Nenhuma tarifa desses clientes deve:



&nbsp; \* gerar receita

&nbsp; \* gerar custo

&nbsp; \* participar de rateio



O fato de o cliente constar na mesma planilha \*\*não o torna elegível\*\*.



👉 Esta regra \*\*se sobrepõe a qualquer outra regra do sistema\*\*.



---



\## 5. Modelo Padrão Interno (Contrato de Dados)



Após a leitura de qualquer planilha, cada linha será convertida para o seguinte modelo interno:



\* `data` → data/hora da movimentação

\* `valor` → valor financeiro da linha

\* `descricao\_operacao` → descrição original da coluna "Operação"

\* `categoria\_operacao` → tarifa | transacao | estorno | desconhecida

\* `impacto\_lucro` → receita | custo | reversao | neutro

\* `sistema\_origem` → sistema que gerou o relatório

\* `banco\_liquidante` → banco responsável pela liquidação

\* `cliente` → identificador do cliente

\* `cliente\_elegivel` → booleano (True / False), derivado por regra de negócio



👉 \*\*Somente registros com `cliente\_elegivel = True` podem seguir para qualquer cálculo financeiro.\*\*



---



\## 6. Classificação das Operações – Sistema Privilege / BMP



\### 6.1 Princípio de Classificação (Whitelist)



Somente operações explicitamente classificadas como \*\*TARIFA\*\* entram no cálculo de lucratividade.



Qualquer operação que:



\* não seja tarifa

\* não possua regra explícita

\* seja desconhecida



Deve ter impacto \*\*neutro\*\*.



---



\### 6.2 Operações classificadas como TARIFA



| Descrição da Operação        | Descrição Funcional                   |

| ---------------------------- | ------------------------------------- |

| CUSTO REGISTRO BOLETO ONLINE | Tarifa de emissão/registro de boletos |

| CUSTO ENVIO TED              | Tarifa de envio TED                   |

| CUSTO ENVIO PIX              | Tarifa de envio Pix                   |

| CUSTO RECEBIMENTO PIX        | Tarifa de recebimento Pix             |

| SPLIT PERCENTUAL             | Tarifa de recebimento (Cash In)       |

| MANUTENÇÃO DE CONTA          | Tarifa mensal                         |



---



\## 7. Aplicação da Elegibilidade no Cálculo (Sprint 3)



A partir da Sprint 3, a elegibilidade deixa de ser apenas \*\*informativa\*\* e passa a ser \*\*operacional\*\*.



Regras:



\* Registros não elegíveis \*\*não participam do cálculo\*\*, mesmo que:



&nbsp; \* sejam tarifas válidas

&nbsp; \* estejam corretamente classificados



\* O sistema deve manter \*\*separação explícita\*\* entre:



&nbsp; \* registros lidos

&nbsp; \* registros classificados

&nbsp; \* registros elegíveis

&nbsp; \* registros efetivamente utilizados no cálculo



\* A filtragem por `cliente\_elegivel` ocorre \*\*antes de qualquer soma ou apuração financeira\*\*.



---



\## 8. Ordem de Aplicação das Regras Financeiras



A ordem correta é:



1\. Filtragem de clientes elegíveis (GV8)

2\. Identificação da tarifa

3\. Apuração da receita bruta

4\. Aplicação dos custos operacionais

5\. Cálculo do lucro líquido

6\. Rateio conforme contrato



---



\## 9. Rateio de Lucratividade por Cliente / Contrato



\*(inalterado – permanece como regra futura)\*



---



\## 10. Custos Operacionais (Externos à Planilha)



\*(inalterado – permanece como regra futura)\*



---



\## 11. Custos Operacionais – Banco Liquidante BMP



\*(inalterado – permanece como regra futura)\*



---



\## 12. Estornos e Operações Desconhecidas



\*(inalterado)\*



---



\## 13. Extensibilidade do Sistema



O sistema deve permitir:



\* inclusão de novos sistemas

\* inclusão de novos bancos

\* inclusão/exclusão de clientes elegíveis

\* alteração de custos e contratos

\* evolução sem refatoração estrutural



---



\## 14. Status do Projeto (Atualizado)



\### Sprint 0 — Concluída



\* Escopo definido

\* Regras de negócio documentadas



\### Sprint 1 — Concluída



\* Leitura da planilha Privilege

\* Modelo interno inicial de registros

\* Classificação de operações via whitelist

\* Soma de tarifas

\* Código revisado e versionado



\### Sprint 2 — Concluída



\* Introdução de `sistema\_origem`

\* Introdução de `cliente`

\* Introdução de `cliente\_elegivel`

\* Diferenciação entre sistemas exclusivos e compartilhados

\* Elegibilidade explícita, rastreável e extensível



\### Sprint 3 — Em andamento



\* Aplicação prática da elegibilidade no cálculo

\* Filtragem explícita de registros elegíveis

\* Garantia de que registros não elegíveis não geram receita nem custo

\* Preparação da base para custos operacionais e lucro líquido

