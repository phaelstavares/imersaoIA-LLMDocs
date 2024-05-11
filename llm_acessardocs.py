# -*- coding: utf-8 -*-
"""LLM-acessarDocs.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1Y21pYgTfkrs9S8x2ASTRkrAdOqhm3pGW
"""

!pip install -q -U google-generativeai

#Configurações iniciais
import numpy as np
import pandas as pd
import google.generativeai as genai

GOOGLE_API_KEY="PEGAR A API KEY NO: https://aistudio.google.com/app/apikey E COLOCAR AQUI! (A API KEY NÃO DEVE SER COMPARTILHADA)"
genai.configure(api_key=GOOGLE_API_KEY)

for m in genai.list_models():
  if "embedContent" in m.supported_generation_methods:
    print(m.name)

#Exemplo de embedding
title = "Programação"
sample_text = ("Olá, mundo!")

embeddings = genai.embed_content(model="models/embedding-001",
                                 content=sample_text,
                                 title=title,
                                 task_type="RETRIEVAL_DOCUMENT")
print(embeddings)

DOCUMENT1 = {
    "title": "Operando o sistema de controle climático",
    "content": "Seu Googlecar possui um sistema de controle de temperatura que permite ajustar a temperatura e o fluxo de ar no carro. Para operar o sistema de controle climático, use os botões e botões localizados no console central. Temperatura: O botão de temperatura controla a temperatura dentro do carro. Gire o botão no sentido horário para aumentar a temperatura ou no sentido anti-horário para diminuir a temperatura. Fluxo de ar: O botão de fluxo de ar controla a quantidade de fluxo de ar dentro do carro. Gire o botão no sentido horário para aumentar o fluxo de ar ou no sentido anti-horário para diminuí-lo. Velocidade do ventilador: O botão de velocidade do ventilador controla a velocidade do ventilador. Gire o botão no sentido horário para aumentar a velocidade do ventilador ou no sentido anti-horário para diminuir a velocidade do ventilador. Modo: O botão de modo permite selecionar o modo desejado. Os modos disponíveis são: Auto: O carro ajustará automaticamente a temperatura e o fluxo de ar para manter um nível confortável. Legal: O carro soprará ar frio para dentro do carro. Calor: O carro soprará ar quente para dentro do carro. Degelo: O carro soprará ar quente no para-brisa para descongelá-lo."}
DOCUMENT2 = {
    "title": "Tela sensível ao toque",
    "content": "Seu Googlecar possui uma grande tela sensível ao toque que fornece acesso a uma variedade de recursos, incluindo navegação, entretenimento e controle de temperatura. Para utilizar o display touchscreen, basta tocar no ícone desejado. Por exemplo, você pode tocar no ícone \"Navegação\" para obter rotas até seu destino ou tocar no ícone \"Música\" para reproduzir suas músicas favoritas."}
DOCUMENT3 = {
    "title": "Mudança de marcha",
    "content": "Seu Googlecar possui transmissão automática. Para mudar de marcha, basta mover a alavanca de câmbio para a posição desejada. Estacionar: Esta posição é usada quando você está estacionado. As rodas estão travadas e o carro não pode se mover. Reverso: Esta posição é usada para fazer backup. Neutro: Esta posição é usada quando você está parado em um semáforo ou no trânsito. O carro não está engatado e não se moverá a menos que você pressione o pedal do acelerador. Drive: Esta posição é usada para avançar. Baixo: Esta posição é usada para dirigir na neve ou em outras condições escorregadias."}

documents = [DOCUMENT1, DOCUMENT2, DOCUMENT3]

df = pd.DataFrame(documents)
df.columns = ["Titulo", "Conteudo"]
df

model = "models/embedding-001"

def embed_fn(title, text):
  return genai.embed_content(model=model,
                             content=text,
                             title=title,
                             task_type="RETRIEVAL_DOCUMENT")["embedding"]

df["Embeddings"] = df.apply(lambda row: embed_fn(row["Titulo"], row["Conteudo"]), axis=1)
df

def gerar_e_buscar_consulta(consulta, base, model):
  embed_da_consulta = genai.embed_content(model=model,
                             content=consulta,
                             task_type="RETRIEVAL_QUERY")["embedding"]

  produtos_escalares = np.dot(np.stack(df["Embeddings"]), embed_da_consulta)

  indice = np.argmax(produtos_escalares)
  return df.iloc[indice]["Conteudo"]

consulta = "Como faço para trocar a marcha em um carro do Google?"

trecho = gerar_e_buscar_consulta(consulta, df, model)
print(trecho)

config = {
    "candidate_count": 1,
    "temperature": 0,
}

prompt = f"Reescreva esse texto de uma forma mais descontraída, sem adicionar informações que não façam parte do texto: {trecho}"

model_2 = genai.GenerativeModel("gemini-1.0-pro",
                                generation_config=config)
response = model_2.generate_content(prompt)
print(response.text)