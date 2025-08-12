import requests
from bs4 import BeautifulSoup
import time

# Faz um scrapping na página do evento para retornar a descrição completa
def obter_descricao_evento(link):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    try:
        response = requests.get(link, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, "html.parser")
            descricao_elemento = soup.find("div", class_="sc-537fdfcb-0 bdUbUp")
            if descricao_elemento:
                descricao_texto = " ".join([p.get_text(strip=True) for p in descricao_elemento.find_all("p")])
                return descricao_texto
            else:
                return "Descrição não encontrada"
        else:
            return f"Erro ao acessar o link: Status {response.status_code}"
    except Exception as e:
        return f"Erro: {str(e)}"

# Função principal do web scrapping, indo página por página para encontrar todos os eventos, buscar a descrição de cada um
# junta em único objeto e retorna todos os eventos encontrados em uma lista.
def scrapper_sympla(paginas=1):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/102.0.0.0 Safari/537.36"
    }
    base_url = "https://www.sympla.com.br/eventos"
    eventos = []

    # For para buscar página por página, caso não seja informado irá buscar apenas a primeira página
    for pagina in range(1, paginas + 1):
        url = f"{base_url}?page={pagina}"

        print(f"\nAcessando página {pagina}: {url}")

        try:
            response = requests.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Erro na página {pagina}: Status {response.status_code}")
                break

            soup = BeautifulSoup(response.content, "html.parser")
            eventos_html = soup.find_all("a", class_="sympla-card")

            if not eventos_html:
                print(f"Nenhum evento encontrado na página {pagina}")
                break

            for i, evento_html in enumerate(eventos_html, 1):
                try:
                    titulo_elemento = evento_html.find("h3", class_="pn67h1a")
                    localizacao_elemento = evento_html.find("p", class_="pn67h1c")
                    data_elemento = evento_html.find("div", class_="qtfy415 qtfy413 qtfy416")
                    
                    nome = titulo_elemento.text.strip() if titulo_elemento else "Título não encontrado"
                    localizacao = localizacao_elemento.text.strip() if localizacao_elemento else "Localização não encontrada"
                    data = data_elemento.text.strip() if data_elemento else "Data não encontrada"
                    link = evento_html.get("href", "Link não encontrado")
                    
                    print(f"  Processando evento {i}/{len(eventos_html)}: {nome[:30]}...")
                    descricao = obter_descricao_evento(link)
                    
                    eventos.append({
                        "nome": nome,
                        "local": localizacao,
                        "data": data,
                        "link": link,
                        "descricao": descricao
                    })
                    
                except Exception as e:
                    print(f"Erro ao processar evento: {str(e)}")
            
        except Exception as e:
            print(f"Erro ao acessar a página {pagina}: {str(e)}")
            break

    return eventos

## Função main que busca os eventos usando a função de scrapping e mostra de forma legível em tela
if __name__ == "__main__":
    NUMERO_PAGINAS = 1
    
    print("Iniciando raspagem de eventos do Sympla...")
    print(f"Serão raspadas {NUMERO_PAGINAS} páginas")
    
    todos_eventos = scrapper_sympla(paginas=NUMERO_PAGINAS)
    
    print("\n" + "="*50)
    print(f"Raspagem concluída! Total de eventos coletados: {len(todos_eventos)}")
    print("="*50)
    
    for i, evento in enumerate(todos_eventos, 1):
        print(f"\nEvento #{i}:")
        print(f"Nome: {evento['nome']}")
        print(f"Local: {evento['local']}")
        print(f"Data: {evento['data']}")
        print(f"Link: {evento['link']}")
        print(f"Descrição: {evento['descricao']}")