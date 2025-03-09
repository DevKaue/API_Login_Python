import uuid
import hashlib


def generate_api_key(base_string):
    """
    Gera uma chave de API única baseada em um UUID e um hash SHA-256.

    :param base_string: String base para compor a chave
    :return: Chave de API gerada
    """
    # Gera um UUID único
    unique_id = uuid.uuid4()

    # Cria um hash baseado na string base e no UUID
    hash_object = hashlib.sha256(f"{base_string}{unique_id}".encode())
    hashed_value = hash_object.hexdigest()[:8]  # Pegamos os primeiros 8 caracteres do hash

    # Combina os valores para formar a API key
    api_key = f"{base_string}-{hashed_value.upper()}-{str(unique_id).upper()}"

    return api_key


# Exemplo de uso
base_string = "key"
api_key = generate_api_key(base_string)
print(f"API Key Gerada: {api_key}")