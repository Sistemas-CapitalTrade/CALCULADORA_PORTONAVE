from PIL import Image

def convert_to_icon(png_path, icon_path):
    try:
        # Abre a imagem PNG
        img = Image.open(png_path)

        # Verifica se a imagem tem informações de resolução DPI
        if 'dpi' in img.info:
            # Define a resolução DPI para 600 DPI
            img.info['dpi'] = (600, 600)
        else:
            # Adiciona informações de resolução DPI para 600 DPI
            img.info['dpi'] = (600, 600)

        # Salva a imagem como ícone
        img.save(icon_path, format="ICO")

        print("Imagem convertida com sucesso para ícone!")
    except Exception as e:
        print("Ocorreu um erro ao converter a imagem:", e)

# Caminho para a imagem PNG que você deseja converter
png_path = "C:/Users/rafael.souza.CAPITAL/OneDrive - CAPITAL TRADE/Área de Trabalho/Documentos/BI/CONTROLE DE DI/ÍCONES/ícone2.png"

# Caminho onde você deseja salvar o ícone
icon_path = "C:/Users/rafael.souza.CAPITAL/OneDrive - CAPITAL TRADE/Área de Trabalho/Documentos/BI/CONTROLE DE DI/ÍCONES/ícone2.ico"

# Chamada da função para converter a imagem PNG em ícone
convert_to_icon(png_path, icon_path)
