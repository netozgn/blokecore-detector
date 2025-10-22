from simple_image_download import simple_image_download as simp
import os

# Times e termos de busca
TIMES = {
    "gremio": [
        "camisa do gremio jogador em campo",
        "camisa do gremio torcida",
        "camisa do gremio 2024",
        "camisa do gremio branca",
        "camisa do gremio celeste"
        "camisa do gremio preta"
    ],
    "santos": [
        "camisa do santos jogador em campo",
        "camisa do santos torcida",
        "camisa do santos reserva",
        "camisa do santos azul",
        "camisa do santos 2024"
    ],
    
    # Times europeus
    "real_madrid": [
        "camisa do real madrid jogador em campo",
        "camisa do real madrid torcida",
        "camisa do real madrid reserva",
        "camisa do real madrid 2024"
    ],
    "barcelona": [
        "camisa do barcelona jogador em campo",
        "camisa do barcelona torcida",
        "camisa do barcelona 2024",
        "camisa do barcelona reserva"
    ],
    "psg": [
        "camisa do psg jogador em campo",
        "camisa do psg torcida",
        "camisa do psg reserva",
        "camisa do psg 2024"
    ],
    "sporting": [
        "camisa do sporting jogador em campo",
        "camisa do sporting torcida",
        "camisa do sporting reserva",
        "camisa do sporting 2024"
    ],
    "benfica": [
        "camisa do benfica jogador em campo",
        "camisa do benfica torcida",
        "camisa do benfica preta",
        "camisa do benfica 2024"
    ],
    "porto": [
        "camisa do porto jogador em campo",
        "camisa do porto torcida",
        "camisa do porto azul branca",
        "camisa do porto 2024"
    ],
}

# Criar diretórios e baixar imagens
response = simp.simple_image_download()

for time, termos in TIMES.items():
    pasta = os.path.join("dataset", time)
    os.makedirs(pasta, exist_ok=True)
    
    print(f"\n🟦 Baixando imagens de: {time.upper()}")
    for termo in termos:
        print(f"   🔹 {termo}")
        response.download(termo, 20, extensions={'.jpg', '.png'}, custom_path=pasta)

print("\n✅ Coleta concluída! Imagens salvas em /dataset")
