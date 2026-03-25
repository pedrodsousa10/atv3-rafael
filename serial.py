import os
import time
import re

KEYWORDS = ["erro", "warning", "info"]


def processar_arquivo(caminho):
    linhas = 0
    palavras = 0
    caracteres = 0
    contagem = {k: 0 for k in KEYWORDS}

    with open(caminho, "r", encoding="utf-8") as f:
        for linha in f:
            linhas += 1
            palavras_lista = linha.split()
            palavras += len(palavras_lista)
            caracteres += len(linha)

            for palavra in palavras_lista:
                palavra = re.sub(r'\W+', '', palavra.lower())
                if palavra in contagem:
                    contagem[palavra] += 1

    return linhas, palavras, caracteres, contagem


def main(pasta):
    inicio = time.time()

    total_linhas = 0
    total_palavras = 0
    total_caracteres = 0
    total_contagem = {k: 0 for k in KEYWORDS}

    arquivos = os.listdir(pasta)

    for arq in arquivos:
        caminho = os.path.join(pasta, arq)

        # garantir que só lê arquivos
        if not os.path.isfile(caminho):
            continue

        l, p, c, cont = processar_arquivo(caminho)

        total_linhas += l
        total_palavras += p
        total_caracteres += c

        for k in KEYWORDS:
            total_contagem[k] += cont[k]

    fim = time.time()

    print("\n=== EXECUÇÃO SERIAL ===")
    print(f"Arquivos processados: {len(arquivos)}")
    print(f"Tempo total: {fim - inicio:.4f} segundos\n")

    print("=== RESULTADO CONSOLIDADO ===")
    print(f"Total de linhas: {total_linhas}")
    print(f"Total de palavras: {total_palavras}")
    print(f"Total de caracteres: {total_caracteres}")
    print("\nContagem de palavras-chave:")
    for k in KEYWORDS:
        print(f"{k}: {total_contagem[k]}")


if __name__ == "__main__":
    main("logs/log1")  # usar log1 para testar