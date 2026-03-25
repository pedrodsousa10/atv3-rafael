import os
import time
import re
from multiprocessing import Process, Queue

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


def produtor(pasta, fila, num_processos):
    for arq in os.listdir(pasta):
        caminho = os.path.join(pasta, arq)
        if os.path.isfile(caminho):
            fila.put(caminho)

    for _ in range(num_processos):
        fila.put(None)


def consumidor(fila, fila_resultados):
    while True:
        arquivo = fila.get()
        if arquivo is None:
            break

        resultado = processar_arquivo(arquivo)
        fila_resultados.put(resultado)


def executar(pasta, num_processos):
    inicio = time.time()

    fila = Queue(maxsize=10)
    fila_resultados = Queue()

    p = Process(target=produtor, args=(pasta, fila, num_processos))
    p.start()

    consumidores = []
    for _ in range(num_processos):
        c = Process(target=consumidor, args=(fila, fila_resultados))
        c.start()
        consumidores.append(c)

    p.join()

    for c in consumidores:
        c.join()

    total_linhas = total_palavras = total_caracteres = 0
    total_contagem = {k: 0 for k in KEYWORDS}

    while not fila_resultados.empty():
        l, p, c, cont = fila_resultados.get()
        total_linhas += l
        total_palavras += p
        total_caracteres += c

        for k in KEYWORDS:
            total_contagem[k] += cont[k]

    fim = time.time()

    print(f"\n=== PARALELO ({num_processos} processos) ===")
    print(f"Tempo: {fim - inicio:.4f} segundos")

    return fim - inicio


if __name__ == "__main__":
    pasta = "logs/log1"  # primeiro testa com log1

    for n in [2, 4, 8, 12]:
        executar(pasta, n)