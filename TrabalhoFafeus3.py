import networkx as nx
import folium
from geopy.distance import geodesic
from datetime import datetime, timedelta

# Coordenadas das cidades
coordenadas = {
    'Curitiba/PR': (-25.4296, -49.2719),
    'Londrina/PR': (-23.3045, -51.1696),
    'Foz do Iguaçu/PR': (-25.5163, -54.5854),
    'União da Vitória/PR': (-26.2286, -51.0870),
    'Joinville/SC': (-26.3031, -48.8417),
    'Chapecó/SC': (-27.1006, -52.6152),
    'Porto Alegre/RS': (-30.0330, -51.2200),
    'Uruguaiana/RS': (-29.7621, -57.0881),
    'Pelotas/RS': (-31.7719, -52.3456)
}

# Criar um grafo direcionado
grafo = nx.DiGraph()

# Adicionar vértices (cidades) ao grafo
grafo.add_nodes_from(coordenadas.keys())

# Função para calcular a distância entre duas cidades
def calcular_distancia(cidade_origem, cidade_destino):
    coord_origem = coordenadas[cidade_origem]
    coord_destino = coordenadas[cidade_destino]
    return geodesic(coord_origem, coord_destino).kilometers

# Limite diário de quilômetros
limite_diario_km = 500

# Escolher cidades de origem e destino
print("Escolha a cidade de origem:")
for i, cidade in enumerate(coordenadas.keys()):
    print(f"{i + 1}. {cidade}")

try:
    cidade_origem = list(coordenadas.keys())[int(input("Escolha a cidade de origem (número):")) - 1]
except (ValueError, IndexError):
    print("Escolha inválida.")

print("\nEscolha a cidade de destino:")
for i, cidade in enumerate(coordenadas.keys()):
    print(f"{i + 1}. {cidade}")

try:
    cidade_destino = list(coordenadas.keys())[int(input("Escolha a cidade de destino (número):")) - 1]
except (ValueError, IndexError):
    print("Escolha inválida.")

# Adicionar exceções para cidades de origem
if cidade_origem == 'Joinville/SC':
    cidade_intermediaria_origem = 'Chapecó/SC'
elif cidade_origem == 'Chapecó/SC':
    cidade_intermediaria_origem = 'Joinville/SC'
elif cidade_origem == 'Foz do Iguaçu/PR':
    cidade_intermediaria_origem = 'União da Vitória/PR'
elif cidade_origem == 'União da Vitória/PR':
    cidade_intermediaria_origem = 'Foz do Iguaçu/PR'
else:
    cidade_intermediaria_origem = None

# Adicionar exceções para cidades de destino
if cidade_destino == 'Joinville/SC':
    cidade_intermediaria_destino = 'Chapecó/SC'
elif cidade_destino == 'Chapecó/SC':
    cidade_intermediaria_destino = 'Joinville/SC'
elif cidade_destino == 'Foz do Iguaçu/PR':
    cidade_intermediaria_destino = 'União da Vitória/PR'
elif cidade_destino == 'União da Vitória/PR':
    cidade_intermediaria_destino = 'Foz do Iguaçu/PR'
else:
    cidade_intermediaria_destino = None

# Adicionar vértice intermediário e criar arestas
if cidade_intermediaria_origem and cidade_intermediaria_destino:
    # Caso ambas as cidades tenham intermediárias, ajustar a ordem das cidades intermediárias
    distancia1 = calcular_distancia(cidade_origem, cidade_intermediaria_origem)
    distancia2 = calcular_distancia(cidade_intermediaria_origem, cidade_intermediaria_destino)
    distancia3 = calcular_distancia(cidade_intermediaria_destino, cidade_destino)

    grafo.add_edge(cidade_origem, cidade_intermediaria_origem, distancia=distancia1)
    grafo.add_edge(cidade_intermediaria_origem, cidade_intermediaria_destino, distancia=distancia2)
    grafo.add_edge(cidade_intermediaria_destino, cidade_destino, distancia=distancia3)

    print(f"\nDistância de {cidade_origem} para {cidade_intermediaria_origem}: {distancia1:.1f} km")
    print(f"Distância de {cidade_intermediaria_origem} para {cidade_intermediaria_destino}: {distancia2:.1f} km")
    print(f"Distância de {cidade_intermediaria_destino} para {cidade_destino}: {distancia3:.1f} km")

else:
    # Caso contrário, seguir a lógica anterior
    if cidade_intermediaria_origem:
        distancia1 = calcular_distancia(cidade_origem, cidade_intermediaria_origem)
        distancia2 = calcular_distancia(cidade_intermediaria_origem, cidade_destino)

        grafo.add_edge(cidade_origem, cidade_intermediaria_origem, distancia=distancia1)
        grafo.add_edge(cidade_intermediaria_origem, cidade_destino, distancia=distancia2)

        print(f"\nDistância de {cidade_origem} para {cidade_intermediaria_origem}: {distancia1:.1f} km")
        print(f"Distância de {cidade_intermediaria_origem} para {cidade_destino}: {distancia2:.1f} km")

    elif cidade_intermediaria_destino:
        distancia1 = calcular_distancia(cidade_origem, cidade_intermediaria_destino)
        distancia2 = calcular_distancia(cidade_intermediaria_destino, cidade_destino)

        grafo.add_edge(cidade_origem, cidade_intermediaria_destino, distancia=distancia1)
        grafo.add_edge(cidade_intermediaria_destino, cidade_destino, distancia=distancia2)

        print(f"\nDistância de {cidade_origem} para {cidade_intermediaria_destino}: {distancia1:.1f} km")
        print(f"Distância de {cidade_intermediaria_destino} para {cidade_destino}: {distancia2:.1f} km")

    else:
        # Calcular a distância entre as cidades
        distancia = calcular_distancia(cidade_origem, cidade_destino)

        # Adicionar aresta ao grafo
        grafo.add_edge(cidade_origem, cidade_destino, distancia=distancia)
        print(f"\nDistância de {cidade_origem} para {cidade_destino}: {distancia:.1f} km")

# Calcular o somatório total da viagem
somatorio_total = sum(aresta[2]['distancia'] for aresta in grafo.edges(data=True))
print(f"\nSomatório total da viagem: {somatorio_total:.1f} km")

# Calcular o custo da viagem
custo_por_km = 20.0  # Custo por quilômetro rodado em reais
custo_total = somatorio_total * custo_por_km
print(f"Custo total da viagem: R${custo_total:.2f}")

# Calcular a data e hora de partida
data_hora_partida = datetime.now()
print(f"\nData e hora de partida: {data_hora_partida.strftime('%d/%m/%Y %H:%M:%S')}")

# Inicializar variáveis de tempo
tempo_total_horas = 0
tempo_na_estrada_horas = 0
tempo_na_estrada_dias = 0

# Loop para calcular a viagem
for aresta in grafo.edges(data=True):
    distancia_aresta = aresta[2]['distancia']

    while distancia_aresta > 0:
        # Calcular a distância a ser percorrida no dia
        distancia_diaria = min(distancia_aresta, limite_diario_km)

        # Calcular o tempo na estrada
        tempo_diario_horas = distancia_diaria / 100  # Assumindo uma velocidade média de 100 km/h
        tempo_na_estrada_horas += tempo_diario_horas

        # Atualizar a distância total restante
        distancia_aresta -= distancia_diaria

        # Atualizar a data e hora de partida
        data_hora_partida += timedelta(hours=tempo_diario_horas)

        # Verificar se ultrapassou a meia-noite, avançando para o próximo dia
        if data_hora_partida.hour >= 24:
            data_hora_partida = data_hora_partida.replace(hour=0, minute=0, second=0, microsecond=0)
            tempo_na_estrada_dias += 1

# Exibir informações do trecho percorrido no dia
print(f"Data e hora de chegada: {data_hora_partida.strftime('%d/%m/%Y %H:%M:%S')}")
print(f"Estimativa de tempo na estrada até agora: {tempo_na_estrada_dias} dias, {int(tempo_na_estrada_horas)} horas e {int((tempo_na_estrada_horas - int(tempo_na_estrada_horas)) * 60)} minutos\n")

# Calcular a data e hora de chegada
tempo_total_horas = tempo_na_estrada_horas
tempo_total_dias = tempo_na_estrada_dias
tempo_total_horas_restantes = int(tempo_total_horas % 24)
tempo_total_minutos = int((tempo_total_horas - int(tempo_total_horas)) * 60)

data_hora_chegada = data_hora_partida + timedelta(days=tempo_total_dias, hours=tempo_total_horas_restantes, minutes=tempo_total_minutos)

# Visualizar o grafo no mapa usando Folium
mapa = folium.Map(location=[-25.4296, -49.2719], zoom_start=6)

for cidade, coord in coordenadas.items():
    folium.Marker(location=coord, popup=cidade).add_to(mapa)

# Adicionar arestas ao mapa
for aresta in grafo.edges(data=True):
    cidade_origem, cidade_destino, dados = aresta
    coord_origem = coordenadas[cidade_origem]
    coord_destino = coordenadas[cidade_destino]
    folium.PolyLine([coord_origem, coord_destino], color="blue", weight=2.5, opacity=1).add_to(mapa)

folium.LayerControl().add_to(mapa)

mapa.save("grafo_cidades.html")
print("\nMapa salvo como 'grafo_cidades.html'.")












































