import math

DENSIDADE_USUARIOS_ATIVOS = 600  # usuarios/km2
AREA_CIDADE_KM2 = 200
DEMANDA_POR_USUARIO_ATIVO_MBPS = 50
RAIO_CELULA_5G_KM = 0.25
RAIO_CELULA_6G_KM = 0.10
CAPACIDADE_CELULA_5G_GBPS = 20
CAPACIDADE_CELULA_6G_GBPS = 55
TAMANHO_PACOTE_BYTES = 1500
BITS_POR_BYTE = 8

def calcular_erbs_cobertura(raio_km):
    area_celula = calcular_area_celula(raio_km)
    return AREA_CIDADE_KM2 / area_celula

def calcular_capex_opex(raio_celula, capex_por_celula, opex_por_celula):
    erbs = calcular_erbs_cobertura(raio_celula)
    return erbs * capex_por_celula, erbs * opex_por_celula

def calcular_area_celula(raio_km):
    return math.pi * raio_km**2

def calcular_mm1_completo(raio_celula, capacidade_celula):
    area_celula = calcular_area_celula(raio_celula)
    capacidade_gbps = capacidade_celula
    
    # Calculo demandanda por usuário (pacotes por segundo)
    taxa_bits_usuario = DEMANDA_POR_USUARIO_ATIVO_MBPS * 1e6  # bits/s
    tamanho_pacote_bits = TAMANHO_PACOTE_BYTES * BITS_POR_BYTE  # bits
    demanda_usuario_pkts = taxa_bits_usuario / tamanho_pacote_bits  # pkt/s
    
    # Calculo capacidade célula (pacotes por segundo)
    capacidade_bits = capacidade_gbps * 1e9  # bits/s
    mu = capacidade_bits / tamanho_pacote_bits  # pkt/s
    
    erbs_km2 = 1 / area_celula
    num_erbs_total = AREA_CIDADE_KM2 * erbs_km2
    usuarios_erb = DENSIDADE_USUARIOS_ATIVOS / erbs_km2
    lambd = usuarios_erb * demanda_usuario_pkts  # Total pkt/s por ERB
    rho = lambd / mu
    
    # rho >= 1 significa sistema instavel
    if rho >= 1:
        return {'ERRO': f'ρ={rho:.3f} >= 1: Rede instável!'}
    
    latencia = (1 / (mu - lambd)) * 1000  # ms
    jitter = math.sqrt(rho / (mu * (1 - rho)**2)) * 1000  # ms
    ber = math.tanh(rho)
    
    return {
        'Número total de ERBs': math.ceil(num_erbs_total),
        'ERBs/km²': erbs_km2,
        'Usuários/ERB': usuarios_erb,
        'λ (pkt/s)': lambd,
        'μ (pkt/s)': mu,
        'ρ': rho,
        'BER': ber,
        'Latência (ms)': latencia,
        'Jitter (ms)': jitter
    }

# Executar
print(
    "5G:", calcular_mm1_completo(RAIO_CELULA_5G_KM, CAPACIDADE_CELULA_5G_GBPS)
)
print(
    "6G:", calcular_mm1_completo(RAIO_CELULA_6G_KM, CAPACIDADE_CELULA_6G_GBPS)
)