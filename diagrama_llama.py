import os
import re
from openai import OpenAI
import sys

# Configuração da API
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") or "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"

def extract_plantuml(response_text: str) -> str:
    """Extrai o bloco PlantUML da resposta do modelo"""
    pattern = r'@startuml(.*?)@enduml'
    match = re.search(pattern, response_text, re.DOTALL)
    if match:
        return f"@startuml{match.group(1)}@enduml"
    return ""

def generate_class_diagram(code_path: str = "relogio.py") -> str:
    """Gera diagrama de classes em formato PlantUML"""
    try:
        # Ler código fonte
        with open(code_path, "r") as f:
            code = f.read()
        
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=OPENROUTER_API_KEY,
        )

        # Prompt otimizado
        prompt = f"""
        Gere um diagrama de classes PlantUML completo e preciso para o seguinte código Python.
        Inclua todas as classes, atributos, métodos e relações (herança, composição, etc).
        Use formatação padrão PlantUML e evite explicações textuais extras.

        Código:
        ```python
        {code}
        ```

        Formato esperado:
        @startuml
        ...código PlantUML...
        @enduml
        """
        
        # Gerar resposta
        completion = client.chat.completions.create(
            extra_headers={
                "HTTP-Referer": "https://github.com/gerador-diagramas",
                "X-Title": "CI/CD Diagram Generator",
            },
            model="meta-llama/llama-3.3-8b-instruct:free",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        
        response_text = completion.choices[0].message.content
        #print(response_text)
        return extract_plantuml(response_text) # type: ignore
    
    except Exception as e:
        print(f"Erro na geração do diagrama: {str(e)}")
        return ""

def save_and_convert_diagram(plantuml_code: str):
    """Salva e converte o diagrama para PNG"""
    try:
        # Salvar arquivo PlantUML
        with open("diagrama_classes_LLAMA.puml", "w") as f:
            f.write(plantuml_code)
        
        # Converter para PNG
        os.system("plantuml diagrama_classes_LLAMA.puml")
        print("Diagrama gerado com sucesso!")
        
    except Exception as e:
        print(f"Erro ao salvar diagrama: {str(e)}")

if __name__ == "__main__":
    # Gerar diagrama a partir do código
    plantuml_code = generate_class_diagram()
    
    if plantuml_code:
        save_and_convert_diagram(plantuml_code)
    else:
        print("Falha na geração do diagrama")
        sys.exit(1)