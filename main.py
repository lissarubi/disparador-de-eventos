from helper.functions import scrapper_sympla

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