import os
import re
import sys
import requests # Importação adicionada
import json     # Importação adicionada

# --- Configuração da API ---
# Tenta obter a chave da API da variável de ambiente.
# É crucial que OPENROUTER_API_KEY esteja definida no ambiente
# (ex: no GitHub Actions como um secret).
# O valor hardcoded abaixo é APENAS para testes LOCAIS e deve ser removido em produção.
OPENROUTER_API_KEY = "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"

# Exemplo de uso para depuração local (descomente se precisar testar sem definir a env)
# if not OPENROUTER_API_KEY:
#     print("ATENÇÃO: OPENROUTER_API_KEY não definida. Usando chave hardcoded (apenas para DEV/TESTE).")
#     OPENROUTER_API_KEY = "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" # Chave descartável de exemplo

if not OPENROUTER_API_KEY:
    print("ERRO: OPENROUTER_API_KEY não está configurada como variável de ambiente.")
    print("Por favor, defina-a (ex: export OPENROUTER_API_KEY='') ou use segredos no GitHub Actions.")
    sys.exit(1) # Sai se a chave não estiver disponível

# --- Funções para Geração de Diagramas ---

def extract_plantuml(response_text: str) -> str:
    """Extrai o bloco PlantUML da resposta do modelo."""
    pattern = r'@startuml(.*?)@enduml'
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return f"@startuml{match.group(1)}@enduml"
    return ""

def generate_class_diagram(code_path: str = "relogio.py") -> str:
    """
    Gera um diagrama de classes em formato PlantUML a partir do código Python.
    Por padrão, lê o arquivo 'zologico_galactico.py'.
    """
    try:
        # Ler código fonte
        with open(code_path, "r") as f:
            code = f.read()

        # Prompt otimizado para o modelo de linguagem
        prompt = f"""
        Gere um diagrama de classes PlantUML completo e preciso para o seguinte código Python.
        Inclua todas as classes, atributos, métodos e relações (herança, composição, agregação, uso de Enum).
        Use formatação padrão PlantUML e evite explicações textuais extras fora do bloco PlantUML.
        Mostre os modificadores de visibilidade (+ público, - privado, # protegido) quando aplicável.

        Código:
        ```python
        {code}
        ```

        Formato esperado:
        @startuml
        ...código PlantUML...
        @enduml
        """

        # Payload da requisição (corpo JSON para a API do OpenRouter)
        payload = {
            "model": "meta-llama/llama-3.3-8b-instruct:free", # Modelo Llama 3.3 8B
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "stream": False, # Não queremos streaming para este caso
            "temperature": 0.1 # Para respostas mais consistentes
        }

        # Cabeçalhos da requisição HTTP
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json",
            "HTTP-Referer": "https://github.com/gerador-diagramas", # Referer do seu projeto
            "X-Title": "CI/CD Diagram Generator", # Título para OpenRouter
        }

        # Realiza a requisição POST para a API do OpenRouter
        print(f"Gerando diagrama para '{code_path}' usando OpenRouter com Llama...")
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            data=json.dumps(payload),
            timeout=120 # Aumenta o timeout para requisições mais longas
        )

        # Lança uma exceção se a requisição HTTP não for bem-sucedida (status 4xx ou 5xx)
        response.raise_for_status()

        # Extrai a resposta JSON e o conteúdo da mensagem do modelo
        response_data = response.json()
        response_text = response_data['choices'][0]['message']['content']

        # Opcional: Imprimir a resposta bruta para depuração
        # print("Resposta Bruta do LLM:")
        # print(response_text)
        # print("-" * 50)

        # Extrai e retorna o bloco PlantUML
        plantuml_code = extract_plantuml(response_text)
        if not plantuml_code:
            print("Aviso: Nenhum bloco '@startuml...@enduml' encontrado na resposta do LLM.")
        return plantuml_code

    except FileNotFoundError:
        print(f"Erro: O arquivo de código '{code_path}' não foi encontrado.")
        return ""
    except requests.exceptions.RequestException as req_err:
        print(f"Erro na requisição HTTP para OpenRouter: {req_err}")
        if req_err.response is not None:
            print(f"Status Code: {req_err.response.status_code}")
            print(f"Corpo da Resposta do Servidor: {req_err.response.text}")
        return ""
    except json.JSONDecodeError as json_err:
        print(f"Erro ao decodificar a resposta JSON da API: {json_err}")
        return ""
    except KeyError as key_err:
        print(f"Erro na estrutura de resposta da API (chave ausente): {key_err}")
        print(f"Resposta completa: {response_data}")
        return ""
    except Exception as e:
        print(f"Erro inesperado na geração do diagrama: {str(e)}")
        return ""

def save_and_convert_diagram(plantuml_code: str, output_puml: str = "diagrama_classes_LLAMA.puml", output_png: str = "diagrama_classes_LLAMA.png") -> bool:
    """Salva o código PlantUML em um arquivo e o converte para PNG."""
    try:
        # Salvar arquivo PlantUML
        with open(output_puml, "w") as f:
            f.write(plantuml_code)
        print(f"Código PlantUML salvo como '{output_puml}'")

        # Converter para PNG usando PlantUML (requer PlantUML e Java instalados)
        # Usando subprocess.run para melhor controle e tratamento de erros
        import subprocess
        print(f"Convertendo '{output_puml}' para '{output_png}'...")
        
        result = subprocess.run(["plantuml", output_puml, "-o", output_png], capture_output=True, text=True, check=False)

        if result.returncode == 0:
            print("Diagrama PNG gerado com sucesso!")
            # print("Saída do PlantUML (stdout):\n", result.stdout) # Descomente para ver a saída do PlantUML
            return True
        else:
            print(f"Erro ao converter diagrama com PlantUML. Código de saída: {result.returncode}")
            print("Saída do PlantUML (stderr):\n", result.stderr)
            return False
            
    except FileNotFoundError:
        print("Erro: O comando 'plantuml' não foi encontrado. Certifique-se de que PlantUML e Java estão instalados e acessíveis no PATH.")
        return False
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar PlantUML: {e}")
        print(f"Stderr: {e.stderr}")
        return False
    except Exception as e:
        print(f"Erro geral ao salvar ou converter diagrama: {str(e)}")
        return False

# --- Ponto de Entrada Principal ---
if __name__ == "__main__":
    # Define o caminho do arquivo de código para o "Zoológico Galáctico"
    # Certifique-se de que este arquivo existe no mesmo diretório ou forneça o caminho completo.
    code_file = "relogio.py" 
    
    # Você pode criar um arquivo chamado 'zologico_galactico.py' e colar o código lá.
    # Ou, se for usar o relogio.py, mude a linha acima:
    # code_file = "relogio.py"

    plantuml_code = generate_class_diagram(code_path=code_file)
    
    if plantuml_code:
        # Define os nomes dos arquivos de saída específicos para este gerador
        output_puml_name = "diagrama_llama.puml"
        output_png_name = "diagrama_llama.png"

        if save_and_convert_diagram(plantuml_code, output_puml=output_puml_name, output_png=output_png_name):
            print(f"Processo de geração e conversão concluído para '{code_file}'.")
        else:
            print(f"Falha na conversão do diagrama para '{code_file}'.")
            sys.exit(1)
    else:
        print(f"Falha na geração do código PlantUML para '{code_file}'.")
        sys.exit(1)