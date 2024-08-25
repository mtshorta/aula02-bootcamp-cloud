## IMPORT
import os
from typing import List
import boto3
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configurações da AWS a partir do .env
AWS_ACCESS_KEY_ID: str = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY: str = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION: str = os.getenv('AWS_REGION')
BUCKET_NAME: str = os.getenv('BUCKET_NAME')

#Configura o cliente S3
s3_client = boto3.client(
    's3',
    aws_access_key_id       = AWS_ACCESS_KEY_ID,
    aws_secret_access_key   = AWS_SECRET_ACCESS_KEY,
    region_name             = AWS_REGION
)
## LE OS ARQUIVOS DA PASTA E ADICIONA NA LISTA
def listar_arquivos(pasta:str) -> List[str]:
    """Lista todos os arquivos em uma pasta local"""
    arquivos: List[str] = []
    for nome_arquivo in os.listdir(pasta):
        caminho_completo = os.path.join(pasta, nome_arquivo)
        if os.path.isfile(caminho_completo):
            arquivos.append(caminho_completo)
    return arquivos

## JOGA OS ARQUIVOS PRO S3
def upload_arquivos_para_s3(arquivos:List[str]) -> None:
    """Faz upload dos arquivos listados para o s3"""
    for arquivo in arquivos:
        nome_arquivo:str = os.path.basename(arquivo)
        s3_client.upload_file(arquivo, BUCKET_NAME, nome_arquivo)
        print(f'{nome_arquivo} doi enviado para o seu S3')


# ## DELETA OS ARQUIVOS NA PASTA LOCAL
# def deletar_arquivos_locais(arquivos: List[str]) -> None:
#     """Deleta os arquivos locais após o upload."""
#     for arquivo in arquivos:
#         os.remove(arquivo)
#         print(f'{arquivo} foi deletado do local.')

## PIPELINE QUE EXECUTA TUDO
def executar_backup(pasta:str) -> None:
    """Executa o processo completo de backup, todas as funções em sequencia"""
    arquivos: List[str] = listar_arquivos(pasta)
    if arquivos:
        upload_arquivos_para_s3(arquivos)
    else:
        print('Nenhum arquivo encontrado na pasta informada')


if __name__ == "__main__":
    PASTA_LOCAL: str = '/Users/mateushorta/Desktop/TESTE_BACKUP_AWS'
    executar_backup(PASTA_LOCAL)