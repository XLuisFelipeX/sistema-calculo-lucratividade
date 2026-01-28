from openpyxl import load_workbook

CLIENTES_ELEGIVEIS_GV8 = {
    "EMPRESA XYZ LTDA",
}

TARIFAS_VALIDAS = [
    "CUSTO REGISTRO BOLETO ONLINE",
    "CUSTO ENVIO TED",
    "CUSTO ENVIO PIX",
    "CUSTO RECEBIMENTO PIX",
    "SPLIT PERCENTUAL",
    "MANUTENÇÃO DE CONTA"
]

def eh_tarifa_valida(descricao):
    """
    Retorna True se a descrição da operação
    for uma tarifa válida segundo a whitelist.
    """
    return descricao in TARIFAS_VALIDAS

def ler_planilha_privilege(caminho_arquivo, sistema_origem):
    workbook = load_workbook(caminho_arquivo)
    sheet = workbook.active

    linhas = list(sheet.iter_rows(values_only=True))

    cabecalho = linhas[0]
    dados = linhas[1:]  # ignora o cabeçalho

    registros = []

    for linha in dados:
        registro = {
            "data": linha[6],        # Coluna G - DataMovto
            "descricao": linha[7],   # Coluna H - Operação
            "valor": linha[8],       # Coluna I - Valor
            "sistema_origem": sistema_origem,
            "cliente": "EMPRESA XYZ LTDA",
            "cliente_elegivel": True
        }
        registros.append(registro)

    return registros

def aplicar_elegibilidade_por_sistema(registro):
    sistema = registro["sistema_origem"]

    if sistema in ["FOURBANK", "AARIN"]:
        registro["cliente_elegivel"] = True
    elif sistema == "PRIVILEGE":
        cliente = registro["cliente"]
        registro["cliente_elegivel"] = cliente in CLIENTES_ELEGIVEIS_GV8
    else:
        registro["cliente_elegivel"] = False

def filtrar_tarifas(registros):
    """
    Recebe uma lista de registros e retorna
    apenas aqueles que são tarifas válidas.
    """
    tarifas = []

    for registro in registros:
        descricao = registro["descricao"]

        if eh_tarifa_valida(descricao):
            tarifas.append(registro)

    return tarifas

def classificar_operacoes(registros):
    """
    Classifica cada registro como 'tarifa' ou 'neutra'
    com base na regra de whitelist.
    """
    for registro in registros:
        descricao = registro["descricao"]

        if eh_tarifa_valida(descricao):
            registro["categoria_operacao"] = "tarifa"
        else:
            registro["categoria_operacao"] = "neutra"

    return registros

def classificar_impacto_lucro(registro):
    """
    Atribui o impacto financeiro do registro.
    Não altera elegibilidade, categoria ou valor.
    """
    if registro.get("categoria_operacao") != "tarifa":
        registro["impacto_lucro"] = "neutro"
    else:
        registro["impacto_lucro"] = "receita"

def filtrar_registros_elegiveis(registros):
    """
    Retorna apenas registros com cliente_elegivel = True.
    Não altera os registros originais.
    """
    registros_elegiveis = []

    for registro in registros:
        if registro.get("cliente_elegivel") is True:
            registros_elegiveis.append(registro)

    return registros_elegiveis

def somar_valor_tarifas(registros):
    """
    Soma o valor de todos os registros classificados como tarifa.
    """
    total = 0

    for registro in registros:
        if registro["categoria_operacao"] == "tarifa":
            total += registro["valor"]

    return total


def main():
    caminho_arquivo = r"C:\Users\Luis.Nunes\Desktop\Projeto Sistema de Cálculo de Lucratividade\Relatório Privilege - 01.12-31.12\Relatório Movimentos - 01.12-31.12.xlsx"

    registros = ler_planilha_privilege(caminho_arquivo, sistema_origem="PRIVILEGE")

    for registro in registros:
        aplicar_elegibilidade_por_sistema(registro)

    registros_classificados = classificar_operacoes(registros)

    for registro in registros_classificados:
        classificar_impacto_lucro(registro)

    # ==================================================
    # TESTE MANUAL – SPRINT 4.3
    # Validação do impacto financeiro por registro
    # ==================================================

    # for r in registros_classificados[:5]:
    #     print(
    #         r["descricao"],
    #         r["categoria_operacao"],
    #         r["impacto_lucro"],
    #         r["cliente_elegivel"]
    #     )

    # ==================================================
    # FIM DO TESTE MANUAL – SPRINT 4.3
    # ==================================================

    registros_elegiveis = filtrar_registros_elegiveis(registros_classificados)

    total_tarifas = somar_valor_tarifas(registros_elegiveis)
    print(f"Total de tarifas elegíveis: R$ {total_tarifas:.2f}")

    # ==================================================
    # TESTES MANUAIS HISTÓRICOS (SPRINTS ANTERIORES)
    # Mantidos apenas para consulta
    # ==================================================

    # print(registros[0])

    # for r in registros[:5]:
    #     print(r["cliente"], r["sistema_origem"], r["cliente_elegivel"])

    # ==================================================
    # FIM DOS TESTES MANUAIS HISTÓRICOS
    # ==================================================

    # ==================================================
    # TESTE MANUAL – VALIDAÇÃO DA CLASSIFICAÇÃO
    # ==================================================

    # print("\nTeste de classificação (3 primeiros registros):")
    # for r in registros_classificados[:3]:
    #    print(r)

    # ==================================================
    # FIM DO TESTE DE CLASSIFICAÇÃO
    # ==================================================

    # ==================================================
    # TESTE MANUAL – VALIDAÇÃO DA SOMA DE TARIFAS
    # ==================================================
   
    # total_tarifas = somar_valor_tarifas(registros_classificados)

    # print(f"\nTotal de tarifas no período: R$ {total_tarifas:.2f}")

    # ==================================================
    # FIM DO TESTE DE SOMA DE TARIFAS
    # ==================================================

    # ==================================================
    # TESTE MANUAL – VALIDAÇÃO DE VOLUME DE DADOS
    # Usado para confirmar leitura completa da planilha
    # e aplicação correta da regra de tarifas.
    # ==================================================

    # print(f"Total de registros lidos: {len(registros)}")
    # print(f"Total de tarifas válidas: {len(tarifas)}")
    # OBS: 'tarifas' era usado antes da classificação.
    # Hoje a fonte de verdade é 'categoria_operacao'.

    # ==================================================
    # FIM DO TESTE DE VOLUME
    # ==================================================


    # ==================================================
    # TESTE MANUAL – VALIDAÇÃO DA REGRA DE TARIFA
    # Usado apenas para aprendizado e verificação pontual.
    # Pode ser reativado se necessário.
    # ==================================================

    # tarifas = filtrar_tarifas(registros)

    # print("\nTeste da regra de tarifa:")

    # primeiro_registro = registros[0]
    # descricao = primeiro_registro["descricao"]

    # print("Descrição:", descricao)
    # print("É tarifa válida?", eh_tarifa_valida(descricao))

    # ==================================================
    # FIM DO TESTE MANUAL
    # ==================================================


    # ==================================================
    # TESTE MANUAL – VERIFICAÇÃO DA LEITURA DA PLANILHA
    # ==================================================

    # print("Primeiros 5 registros lidos:")
    # for r in registros[:5]:
    #     print(r)

    # ==================================================
    # FIM DO TESTE DE LEITURA
    # ==================================================

if __name__ == "__main__":
    main()
