import os
import time
import requests # Para baixar as imagens
import shutil   # Para salvar os arquivos
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager # Mágica!

"""
Função auxiliar para baixar e salvar uma imagem
"""
def download_image(url, folder_path, file_name):
    try:
        # Garante que a pasta de destino existe
        os.makedirs(folder_path, exist_ok=True)
        
        # Faz o download da imagem
        response = requests.get(url, stream=True, timeout=10)
        
        # Se o download foi bem-sucedido (código 200)
        if response.status_code == 200:
            path = os.path.join(folder_path, file_name)
            # Salva a imagem no arquivo
            with open(path, 'wb') as f:
                response.raw.decode_content = True
                shutil.copyfileobj(response.raw, f)
            return True
    except Exception as e:
        # Mostra um erro se o download falhar
        print(f"      - Erro ao baixar {url}: {e}")
    return False

# Times e termos de busca (O SEU DICIONÁRIO ORIGINAL)
TIMES = {
    "gremio": [
        "camisa do gremio jogador em campo",
        "camisa do gremio torcida",
        "camisa do gremio 2024",
        "camisa do gremio branca",
        "camisa do gremio dourada"
    ],
    "santos": [
        "camisa do santos jogador em campo",
        "camisa do santos torcida",
        "camisa do santos preta",
        "camisa do santos azul",
        "camisa do santos 2024"
    ],
    "flamengo": [
        "camisa do flamengo jogador em campo",
        "camisa do flamengo torcida",
        "camisa do flamengo preta",
        "camisa do flamengo branca",
        "camisa do flamengo 2024"
    ],
    "real_madrid": [
        "camisa do real madrid jogador em campo",
        "camisa do real madrid torcida",
        "camisa do real madrid branca",
        "camisa do real madrid 2024"
    ],
    "barcelona": [
        "camisa do barcelona jogador em campo",
        "camisa do barcelona torcida",
        "camisa do barcelona 2024",
        "camisa do barcelona azul grená"
    ],
    "psg": [
        "camisa do psg jogador em campo",
        "camisa do psg torcida",
        "camisa do psg azul",
        "camisa do psg 2024"
    ],
    "sporting": [
        "camisa do sporting jogador em campo",
        "camisa do sporting torcida",
        "camisa do sporting verde branca",
        "camisa do sporting 2024"
    ],
    "benfica": [
        "camisa do benfica jogador em campo",
        "camisa do benfica torcida",
        "camisa do benfica vermelha",
        "camisa do benfica 2024"
    ],
    "porto": [
        "camisa do porto jogador em campo",
        "camisa do porto torcida",
        "camisa do porto azul branca",
        "camisa do porto 2024"
    ],
}

# --- Configuração do Selenium (Inicia o Navegador) ---
print("Iniciando o navegador Selenium (isso pode levar um momento)...")
# Configurações para rodar "headless" (sem abrir uma janela)
options = webdriver.ChromeOptions()
options.add_argument("--headless")
options.add_argument("--log-level=3") # Remove poluição do terminal
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36") # Finge ser um browser normal

try:
    # Instala o driver do Chrome automaticamente e inicia o navegador
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    print("Navegador iniciado com sucesso em modo 'headless'.")
except Exception as e:
    print(f"Erro ao iniciar o Selenium. Verifique sua conexão ou instalação do Chrome. {e}")
    exit() # Sair do script se o Selenium não iniciar

# --- Loop Principal de Coleta ---
total_images_downloaded = 0
# Itera sobre cada TIME e sua lista de TERMOS
for time_key, termos in TIMES.items():
    # Define a pasta de destino (ex: dataset/gremio)
    pasta_destino_time = os.path.join("dataset", time_key)
    os.makedirs(pasta_destino_time, exist_ok=True)
    print(f"\n🟦 Baixando imagens de: {time_key.upper()}")

    for termo in termos:
        print(f"   🔹 Buscando por: {termo}")
        
        # Contador de imagens baixadas *para este termo*
        termo_image_count = 0
        
        try:
            # 1. Abre o Google Images
            driver.get("https://www.google.com/imghp?hl=pt-BR")
            time.sleep(1) # Espera a página carregar

            # 2. Encontra a barra de busca, digita o termo e pressiona Enter
            search_box = driver.find_element(By.NAME, "q")
            search_box.clear() # Limpa a busca anterior
            search_box.send_keys(termo)
            search_box.send_keys(Keys.ENTER)
            time.sleep(2) # Espera os resultados aparecerem

            # 3. Encontra os elementos das imagens (thumbnails)
            # Tenta pegar os primeiros 40, pois alguns vão falhar
            thumbnails = driver.find_elements(By.CSS_SELECTOR, "img.rg_i")[0:40]
            
            if not thumbnails:
                print("      - Nenhum thumbnail encontrado. O Google pode ter mudado o layout ou bloqueado.")
                continue # Pula para o próximo termo

            # 4. Itera sobre os thumbnails
            for i, thumb in enumerate(thumbnails):
                # Se já baixamos 20 imagens para ESTE TERMO, paramos
                if termo_image_count >= 20:
                    break
                
                try:
                    # 5. Pega a URL da imagem (do atributo 'src')
                    img_url = thumb.get_attribute("src")
                    
                    # 6. Valida a URL:
                    #    Ignora imagens 'data:image...' (são imagens embutidas)
                    #    Só queremos links 'http'
                    if img_url and img_url.startswith('http'):
                        
                        # 7. Baixa a imagem usando nossa função auxiliar
                        filename = f"{time_key}_{termo.replace(' ', '_')}_{i}.jpg"
                        if download_image(img_url, pasta_destino_time, filename):
                            termo_image_count += 1
                            total_images_downloaded += 1
                            
                except Exception as e_inner:
                    # Ignora erros em thumbnails individuais (ex: elemento ficou "velho")
                    pass

            print(f"      -> Baixadas {termo_image_count} imagens para este termo.")

        except Exception as e_outer:
            print(f"   ⚠️ Erro ao processar o termo '{termo}': {e_outer}")

# --- Finalização ---
print(f"\n✅ Coleta concluída! Total de {total_images_downloaded} imagens baixadas.")
print("Fechando o navegador.")
# Fecha o navegador e encerra o processo do Selenium
driver.quit()