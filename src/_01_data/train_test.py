import pandas as pd
import os

# Segregar tabela raiz tournaments em treino e teste

# 1. Importar conjunto de dados tournaments 
tournaments = pd.read_csv('../../data/_01_raw/tournaments.csv')

# 1.2 Filtrar conjunto de subamostra (1998 a 2022 // masculina)
tournaments['year'] = pd.to_numeric(tournaments['tournament_id'].str[3:])

tournaments_sample = tournaments[(tournaments['year'] >= 1998) & (tournaments['tournament_name'].str.contains('Men'))].reset_index(drop=True)

# 1.3 Segregar em conjunto de treino e de teste
tournaments_train = tournaments_sample[tournaments_sample['year'] <= 2014] 
tournaments_test = tournaments_sample[tournaments_sample['year'] > 2014] 

tournaments_train_id = tournaments_train['tournament_id']
tournaments_test_id = tournaments_test['tournament_id']


# Replicar divisao treino e teste da tabela raiz nas demais tabelas 
# Neste momento, desconsidera-se as tabelas 'players' e 'teams' por nao possuirem tournament_id

caminho_pasta_input = '../../data/_01_raw/'
caminho_pasta_output = '../../data/_02_processed/'

for arquivo in os.listdir(caminho_pasta_input):

    path_arquivo = os.path.join(caminho_pasta_input, arquivo)
    df_arquivo = pd.read_csv(path_arquivo)

    if 'tournament_id' in df_arquivo.columns:
        df_train_name = arquivo[:-4] + '_train.csv'
        df_test_name = arquivo[:-4] + '_test.csv'

        path_arquivo_df_train = os.path.join(caminho_pasta_output, df_train_name)
        path_arquivo_df_test = os.path.join(caminho_pasta_output, df_test_name)

        df_train_aux = pd.read_csv(path_arquivo)
        df_train = df_train_aux[df_train_aux['tournament_id'].isin(tournaments_train_id)]
        df_train.to_csv(path_arquivo_df_train, index=False)

        df_test_aux = pd.read_csv(path_arquivo)
        df_test = df_test_aux[df_test_aux['tournament_id'].isin(tournaments_test_id)]
        df_test.to_csv(path_arquivo_df_test, index=False)
    else:
        continue


