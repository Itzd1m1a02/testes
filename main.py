# diagrama_generator.py
import os
import google.generativeai as genai
import re

# Configuração da API
GEMINI_API_KEY = "AIzaSyDTN2wVwLueQnJkF_8WnUsNDNagw0m8keM"

if not GEMINI_API_KEY:
    raise ValueError("Erro: Chave da API Gemini não configurada")

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash")  # Modelo mais avançado

def extract_plantuml_from_response(response_text: str) -> str:
    """Extrai o bloco PlantUML da resposta do Gemini"""
    pattern = r'@startuml(.*?)@enduml'
    match = re.search(pattern, response_text, re.DOTALL)
    return f"@startuml{match.group(1)}@enduml" if match else ""

def generate_class_diagram(code_path: str = "testes.py") -> str:
    """Gera diagrama de classes em formato PlantUML"""
    try:
        # Ler código fonte
        with open(code_path, "r") as f:
            code = f.read()
        
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
        response = model.generate_content(prompt)
        
        # Processar resposta
        if response.text:
            return extract_plantuml_from_response(response.text)
        else:
            raise ValueError("Resposta vazia do modelo")
    
    except Exception as e:
        print(f"Erro na geração do diagrama: {str(e)}")
        return ""

def save_and_convert_diagram(plantuml_code: str):
    """Salva e converte o diagrama para PNG"""
    try:
        # Salvar arquivo PlantUML
        with open("diagrama_classes.puml", "w") as f:
            f.write(plantuml_code)
        
        # Converter para PNG
        os.system("plantuml diagrama_classes.puml")
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