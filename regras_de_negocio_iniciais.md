Regras de Negócio Iniciais

Sistema de Cálculo de Lucratividade

1\. Objetivo do Projeto



Este projeto tem como objetivo construir um Sistema de Cálculo de Lucratividade, baseado na leitura de planilhas financeiras extraídas de sistemas distintos, considerando regras de negócio específicas, com foco exclusivo em tarifas cobradas aos clientes elegíveis do GV8.



O sistema deverá:



Ler planilhas de diferentes sistemas de origem



Interpretar corretamente as operações



Filtrar clientes elegíveis ao GV8



Aplicar custos operacionais externos à planilha



Calcular a lucratividade semanal



Permitir evolução para novos sistemas, bancos e contratos



2\. Decisões Técnicas (Sprint 0A)



Linguagem: Python



Tipo de aplicação: Console



Nível: Iniciante



Abordagem: Desenvolvimento incremental por sprints



Fonte de dados: Planilhas (Excel) extraídas de sistemas financeiros



3\. Sistemas de Origem

3.1 Sistema Privilege



Banco liquidante: BMP



Formato de planilha: específico do sistema Privilege



Observação:

A planilha contém movimentações financeiras e tarifas de clientes do GV8 e de terceiros.



3.2 Sistema Aarin (futuro)



Banco liquidante: Bradesco



Formato de planilha: diferente do sistema Privilege



O sistema deve estar preparado para novos sistemas no futuro, cada um com:



planilha própria



banco liquidante próprio



regras contratuais específicas



4\. Princípios Fundamentais de Cálculo

4.1 Base de Cálculo



A lucratividade é calculada exclusivamente com base em TARIFAS.



Movimentações financeiras, transações operacionais ou ajustes sistêmicos não representam receita nem custo para fins de lucratividade do GV8.



4.2 Elegibilidade de Clientes (Regra Crítica)



Somente clientes indicados/comercializados pelo GV8 devem ser considerados no cálculo de lucratividade.



Embora a planilha do sistema Privilege contenha uma base mais ampla de clientes, nem todos pertencem à carteira do GV8.



Portanto:



Clientes não indicados pelo GV8 devem ser totalmente ignorados



Nenhuma tarifa desses clientes deve:



gerar receita



gerar custo



participar de rateio



O fato de o cliente constar na mesma base ou planilha não o torna elegível



Essa regra se sobrepõe a qualquer outra.



5\. Modelo Padrão Interno (Contrato de Dados)



Após a leitura de qualquer planilha, cada linha será convertida para o seguinte modelo interno:



data                → data/hora da movimentação

valor               → valor financeiro da linha

descricao\_operacao  → descrição original da coluna "Operação"

categoria\_operacao  → classificação configurável (tarifa, transacao, estorno, desconhecida)

impacto\_lucro       → receita | custo | reversao | neutro

sistema\_origem      → sistema que gerou o relatório

banco\_liquidante    → banco responsável pela liquidação

cliente\_elegivel    → booleano (True/False)





Somente registros com cliente\_elegivel = True podem seguir para cálculo.



6\. Classificação das Operações – Sistema Privilege / BMP

6.1 Princípio de Classificação (Whitelist)



Somente operações explicitamente classificadas como TARIFA entram no cálculo de lucratividade.



Qualquer operação que:



não seja tarifa



não possua regra explícita



seja desconhecida



deve ter impacto neutro.



6.2 Operações classificadas como TARIFA



As descrições abaixo representam tarifas cobradas do cliente:



Descrição da Operação	Descrição Funcional

CUSTO REGISTRO BOLETO ONLINE	Tarifa de emissão/registro de boletos

CUSTO ENVIO TED	Tarifa de envio TED

CUSTO ENVIO PIX	Tarifa de envio Pix

CUSTO RECEBIMENTO PIX	Tarifa de recebimento Pix

SPLIT PERCENTUAL	Tarifa de recebimento (Cash In)

MANUTENÇÃO DE CONTA	Tarifa mensal

7\. Rateio de Lucratividade por Cliente / Contrato



O rateio da receita proveniente de tarifas não é fixo e depende do contrato vigente do cliente.



Exemplos:



Cliente X



GV8: 30%



Privilege IP: 30%



Representante Comercial GV8: 40%



Cliente Y



GV8: 45%



Privilege IP: 45%



Representante Comercial GV8: 10%



Princípios:



A soma dos percentuais deve ser 100%



O contrato é definido por regra externa



O representante comercial não vem da planilha



Clientes não elegíveis não entram no rateio



8\. Custos Operacionais (Externos à Planilha)



Os custos operacionais:



não constam na planilha



são definidos por contrato



variam conforme banco liquidante e sistema



Custos são considerados fixos por operação dentro do contrato vigente, podendo ser alterados futuramente.



9\. Custos Operacionais – Banco Liquidante BMP



O banco liquidante BMP aplica custos operacionais fixos por tarifa.



9.1 Custos aplicáveis

Tipo de Tarifa	Custo Unitário

REGISTRO BOLETO	R$ 1,50

TED	R$ 1,50

RECEBIMENTO PIX	R$ 0,30

PIX RECEBIMENTO VIA BOLETO	R$ 0,50

ENVIO PIX	R$ 0,50

9.2 Tarifas sem custo BMP



MANUTENÇÃO DE CONTA



SPLIT PERCENTUAL



10\. Estornos e Operações Desconhecidas



Estornos de tarifas → reversão



Estornos de transações → impacto neutro



Operações sem regra → impacto neutro por padrão



11\. Ordem de Aplicação das Regras Financeiras



A ordem correta é:



Filtragem de clientes elegíveis (GV8)



Identificação da tarifa



Apuração da receita bruta



Aplicação dos custos operacionais



Cálculo do lucro líquido



Rateio conforme contrato



12\. Extensibilidade do Sistema



O sistema deve permitir:



inclusão de novos sistemas



inclusão de novos bancos



inclusão/exclusão de clientes elegíveis



alteração de custos e contratos



evolução sem refatoração estrutural



13\. Status do Projeto



Sprint 0: Concluído (escopo e regras fechados)



Sprint 1: Implementação do primeiro cálculo funcional

