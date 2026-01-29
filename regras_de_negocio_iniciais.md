Regras de Negócio Iniciais

Sistema de Cálculo de Lucratividade

Objetivo do Projeto



Este projeto tem como objetivo construir um Sistema de Cálculo de Lucratividade, baseado na leitura de planilhas financeiras extraídas de sistemas distintos, considerando regras de negócio específicas, com foco exclusivo em tarifas cobradas aos clientes elegíveis do GV8.



O sistema deverá:



Ler planilhas de diferentes sistemas de origem



Interpretar corretamente as operações



Identificar e marcar clientes elegíveis ao GV8 (regra crítica)



Aplicar explicitamente a elegibilidade no cálculo financeiro



Aplicar custos operacionais externos à planilha



Calcular a lucratividade em etapas controladas



Permitir evolução para novos sistemas, bancos e contratos



Decisões Técnicas (Sprint 0)



Linguagem: Python



Tipo de aplicação: Console



Nível: Iniciante



Abordagem: Desenvolvimento incremental por sprints



Fonte de dados: Planilhas (Excel) extraídas de sistemas financeiros



Sistemas de Origem



O sistema trabalha com múltiplos sistemas de origem, que podem possuir características distintas quanto à elegibilidade dos clientes.



3.1 Sistema Privilege



Banco liquidante: BMP



Formato de planilha: específico do sistema Privilege



Observação importante:

A planilha do sistema Privilege contém movimentações financeiras e tarifas de:



clientes indicados pelo GV8



clientes que não pertencem à carteira do GV8



O sistema Privilege não distingue explicitamente quais clientes pertencem ao GV8.

A elegibilidade deve ser determinada por regra externa.



3.2 Sistema Fourbank



Sistema contratado exclusivamente pelo GV8



👉 Para o sistema Fourbank, a elegibilidade dos clientes é implícita.



3.3 Sistema Aarin (futuro)



Banco liquidante: Bradesco



Sistema contratado exclusivamente pelo GV8



👉 Para o sistema Aarin, a elegibilidade dos clientes também é implícita.



Consideração Geral sobre Sistemas de Origem



Cada sistema pode possuir:



planilha própria



banco liquidante próprio



regras contratuais específicas



regras distintas de elegibilidade



O sistema deve tratar essas diferenças de forma explícita, rastreável e extensível.



Princípios Fundamentais de Cálculo

4.1 Base de Cálculo



A lucratividade é calculada exclusivamente com base em TARIFAS.



Movimentações financeiras, transações operacionais ou ajustes sistêmicos não representam receita nem custo para fins de lucratividade do GV8.



4.2 Elegibilidade de Clientes (Regra Crítica – GV8)



Somente clientes indicados/comercializados pelo GV8 podem participar de qualquer cálculo financeiro.



A aplicação da regra de elegibilidade depende do sistema de origem:



Sistemas exclusivos do GV8 (Fourbank, Aarin)

Todos os clientes são elegíveis.



Sistema compartilhado (Privilege)

A elegibilidade é verificada por base externa mantida pelo GV8.



Regras absolutas:



Clientes não elegíveis devem ser totalmente ignorados



Nenhuma tarifa desses clientes pode:



gerar receita



gerar custo



participar de rateio



👉 Esta regra se sobrepõe a qualquer outra regra do sistema.



Modelo Padrão Interno (Contrato de Dados)



Após a leitura de qualquer planilha, cada linha deve ser convertida para o seguinte modelo interno:



data → data/hora da movimentação



valor → valor financeiro da linha



descricao\_operacao → descrição original da operação



categoria\_operacao → tarifa | transacao | estorno | desconhecida



impacto\_lucro → receita | neutro



sistema\_origem → sistema que gerou o relatório



banco\_liquidante → banco responsável pela liquidação



cliente → identificador do cliente



cliente\_elegivel → booleano (True / False)



👉 Somente registros com cliente\_elegivel = True podem seguir para qualquer cálculo financeiro.



Classificação das Operações – Sistema Privilege / BMP

6.1 Princípio de Classificação (Whitelist)



Somente operações explicitamente classificadas como TARIFA participam do cálculo de lucratividade.



Qualquer operação não classificada deve ter impacto neutro.



6.2 Operações classificadas como TARIFA

Descrição da Operação	Descrição Funcional

CUSTO REGISTRO BOLETO ONLINE	Tarifa de emissão/registro de boletos

CUSTO ENVIO TED	Tarifa de envio TED

CUSTO ENVIO PIX	Tarifa de envio Pix

CUSTO RECEBIMENTO PIX	Tarifa de recebimento Pix

SPLIT PERCENTUAL	Tarifa de recebimento (Cash In)

MANUTENÇÃO DE CONTA	Tarifa mensal

7\. Aplicação da Elegibilidade no Cálculo (Sprint 3)



A partir da Sprint 3:



A elegibilidade deixa de ser informativa e passa a ser operacional



Registros não elegíveis:



não geram receita



não geram custo



não participam de nenhum cálculo



A filtragem por cliente\_elegivel ocorre antes de qualquer apuração financeira.



Ordem de Aplicação das Regras Financeiras



A ordem correta e imutável é:



Filtragem de clientes elegíveis



Identificação de tarifas



Apuração da receita bruta



Aplicação de custos operacionais



Cálculo do lucro líquido



Rateio conforme contrato



Custos Operacionais (Conceito Geral)



Custos operacionais:



Não vêm da planilha de origem



São definidos externamente



Devem ser:



explícitos



rastreáveis



aplicados apenas sobre registros elegíveis



Nenhum custo pode ser aplicado implicitamente.



Custos Operacionais – Banco Liquidante BMP



(mantido como regra futura, a ser detalhada em sprint específica)



Estornos e Operações Desconhecidas



Estornos e operações desconhecidas possuem impacto neutro



Não geram receita nem custo



Servem apenas para rastreabilidade histórica



Extensibilidade do Sistema



O sistema deve permitir:



inclusão de novos sistemas



inclusão de novos bancos



inclusão/exclusão de clientes elegíveis



inclusão de novos tipos de custo



evolução sem refatoração estrutural



Status do Projeto

Sprint 0 — Concluída



Escopo definido



Regras de negócio documentadas



Sprint 1 — Concluída



Leitura da planilha Privilege



Modelo interno inicial



Classificação via whitelist



Soma de tarifas



Código versionado



Sprint 2 — Concluída



Introdução de sistema\_origem



Introdução de cliente



Introdução de cliente\_elegivel



Elegibilidade explícita e rastreável



Sprint 3 — Concluída



Elegibilidade aplicada ao cálculo



Filtragem explícita de registros elegíveis



Separação clara entre leitura, classificação e cálculo



Sprint 4 — Concluída



Introdução do campo impacto\_lucro



Classificação explícita do impacto financeiro



Preservação integral das regras anteriores



Base preparada para custos e lucro líquido



Sprint 5 — Concluída



Introdução de encargos operacionais explícitos, externos à planilha



Aplicação de encargos de forma controlada, individual e rastreável



Definição explícita de tarifas isentas de encargo:



Mensalidade (MANUTENÇÃO DE CONTA)



Cash In (SPLIT PERCENTUAL)



Encargos aplicados somente quando:



cliente é elegível



operação é tarifa



impacto financeiro é de receita



Preservação integral das Sprints 1 a 4



Nenhum cálculo de lucro líquido



Nenhum rateio



Nenhuma refatoração de código existente



Observação Final



Cada sprint consolida uma camada lógica isolada.

Nenhuma sprint futura pode alterar o comportamento validado das anteriores.

