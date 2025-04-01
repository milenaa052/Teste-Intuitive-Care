import os
import requests
from bs4 import BeautifulSoup
from zipfile import ZipFile


def criar_diretorios():
    os.makedirs('downloads', exist_ok=True)
    os.makedirs('output', exist_ok=True)


def baixar_arquivo(url, nome_arquivo):
    resposta = requests.get(url, stream=True)
    
    with open(f'downloads/{nome_arquivo}', 'wb') as arquivo:
        for chunk in resposta.iter_content(chunk_size=1024):
            if chunk:
                arquivo.write(chunk)
    
    print(f'Arquivo {nome_arquivo} baixado com sucesso!')


def encontrar_links_pdf(url):
    resposta = requests.get(url)
    soup = BeautifulSoup(resposta.text, 'html.parser')
    
    links = []
    
    for link in soup.find_all('a'):
        href = link.get('href', '')
        
        if href.lower().endswith('.pdf'):
            if 'anexo i' in link.text.lower() or 'anexo 1' in link.text.lower():
                links.append(('Anexo_I.pdf', href))
            if 'anexo ii' in link.text.lower() or 'anexo 2' in link.text.lower():
                links.append(('Anexo_II.pdf', href))
    
    return links


def compactar_arquivos(nome_zip):
    arquivos_pdf = [zip for zip in os.listdir('downloads') if zip.endswith('.pdf')]
    
    with ZipFile(f'output/{nome_zip}', 'w') as zipf:
        for pdf in arquivos_pdf:
            zipf.write(f'downloads/{pdf}', pdf)
    
    print(f'Arquivos compactados em output/{nome_zip}')


def main():
    url = 'https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos'
    
    criar_diretorios()
    
    print("Procurando links para os Anexos I e II...")
    links_pdf = encontrar_links_pdf(url)
    
    if not links_pdf:
        print("Não foram encontrados links para os Anexos I e II.")
        return
    
    print("Iniciando download dos arquivos...")
    for nome_arquivo, url_pdf in links_pdf:
        baixar_arquivo(url_pdf, nome_arquivo)
    
    print("Compactando arquivos...")
    compactar_arquivos('Anexos_ANS.zip')
    
    print("Processo concluído com sucesso!")


if __name__ == '__main__':
    main()