import tkinter as tk
from tkinter import messagebox
import requests
import io # Ajuda o Python a ler dados brutos da internet
from PIL import Image, ImageTk # NOVA BIBLIOTECA: Lida com as imagens

# ==========================================
# 1. FUNÇÃO PARA BUSCAR O CLIMA NA INTERNET
# ==========================================
def buscar_clima():
    cidade = entrada_cidade.get()
    
    # IMPORTANTE: Cole sua API Key do OpenWeatherMap aqui
    chave_api = "91b58077aff4cddfc29d0533969abc79" 
    
    url = f"http://api.openweathermap.org/data/2.5/weather?q={cidade}&appid={chave_api}&units=metric&lang=pt_br"

    try:
        resposta = requests.get(url)
        dados = resposta.json()
        print(dados)

        if dados["cod"] == 200:
            nome_cidade = dados["name"]
            temperatura = dados["main"]["temp"]
            descricao = dados["weather"][0]["description"]
            
            # NOVO: Pega o código do ícone (ex: '01d', '04n')
            codigo_icone = dados["weather"][0]["icon"] 

            # Atualiza o texto na tela
            texto_resultado.set(f"{nome_cidade}\n{temperatura}°C\n{descricao.capitalize()}")

            # ==========================================
            # NOVO: BAIXANDO E EXIBINDO O ÍCONE
            # ==========================================
            # O OpenWeatherMap guarda as imagens neste endereço padrão:
            url_icone = f"http://openweathermap.org/img/wn/{codigo_icone}@2x.png"
            
            # Fazemos um novo "pedido" para baixar a imagem
            resposta_icone = requests.get(url_icone)
            
            # Transformamos os dados brutos da internet em uma imagem visível
            imagem_bytes = io.BytesIO(resposta_icone.content)
            imagem = Image.open(imagem_bytes)
            foto = ImageTk.PhotoImage(imagem)
            
            # Colocamos a foto no nosso Label
            label_icone.config(image=foto)
            
            # ATENÇÃO: Essa linha é obrigatória no Tkinter! 
            # Se não salvarmos a foto dentro do label, o Python apaga ela da memória.
            label_icone.image = foto 
            
        else:
            messagebox.showerror("Erro", "Cidade não encontrada.")
            texto_resultado.set("")
            label_icone.config(image="") # Limpa a foto se der erro
            
    except Exception:
        messagebox.showerror("Erro", "Erro ao conectar com a internet.")


# ==========================================
# 2. CONFIGURAÇÃO DA JANELA (INTERFACE)
# ==========================================
janela = tk.Tk()
janela.title("Previsão do Tempo")
janela.geometry("350x450") # Aumentamos um pouco a altura para caber o ícone
janela.configure(bg="#87CEEB") 

texto_resultado = tk.StringVar()

# Título do app
titulo = tk.Label(janela, text="Como está o clima?", font=("Arial", 18, "bold"), bg="#87CEEB")
titulo.pack(pady=20)

# Campo para digitar a cidade
entrada_cidade = tk.Entry(janela, font=("Arial", 14), justify="center")
entrada_cidade.pack(pady=10)

# Botão de busca
botao_buscar = tk.Button(janela, text="Buscar Clima", font=("Arial", 12, "bold"), command=buscar_clima)
botao_buscar.pack(pady=10)

# ==========================================
# NOVO: ESPAÇO PARA O ÍCONE
# ==========================================
# Criamos um Label vazio. A foto vai aparecer dentro dele depois da busca.
label_icone = tk.Label(janela, bg="#87CEEB")
label_icone.pack(pady=5)

# Local onde o resultado vai aparecer
label_resultado = tk.Label(janela, textvariable=texto_resultado, font=("Arial", 16), bg="#87CEEB", fg="#333333")
label_resultado.pack(pady=10)

janela.mainloop()