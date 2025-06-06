import ast
import os

def parse_python_for_class_diagram(code_path: str) -> str:
    """
    Analisa um arquivo Python para extrair informações de classes, atributos e métodos,
    gerando uma string PlantUML correspondente.
    """
    try:
        with open(code_path, "r") as f:
            code = f.read()
    except FileNotFoundError:
        return f"Erro: Arquivo não encontrado em {code_path}"

    tree = ast.parse(code)
    plantuml_elements = []
    plantuml_relationships = []

    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            class_attributes = []
            class_methods = []
            inherited_classes = []

            # Extrair classes herdadas
            for base in node.bases:
                if isinstance(base, ast.Name):
                    inherited_classes.append(base.id)
                elif isinstance(base, ast.Attribute):
                    # Lida com herança de classes de outros módulos (ex: 'module.ClassName')
                    inherited_classes.append(f"{base.value.id}.{base.attr}")

            # Analisar o corpo da classe para atributos e métodos
            for item in node.body:
                if isinstance(item, ast.FunctionDef):
                    method_name = item.name
                    # Inferência básica de visibilidade:
                    # __ prefixo (não dunder) -> private (-)
                    # _ prefixo -> protected (#)
                    # Outros -> public (+)
                    if method_name.startswith('__') and not method_name.endswith('__'):
                        visibility = '-'
                    elif method_name.startswith('_'):
                        visibility = '#'
                    else:
                        visibility = '+'
                    class_methods.append(f"{visibility}{method_name}()")
                elif isinstance(item, ast.Assign):
                    # Tenta pegar atributos de classe e atributos de instância no __init__
                    # Percorre os alvos da atribuição (pode ser "a = b = 1")
                    for target in item.targets:
                        if isinstance(target, ast.Name):
                            # Atributo de classe
                            attr_name = target.id
                            if f"+{attr_name}" not in class_attributes: # Evita duplicatas se já adicionado
                                class_attributes.append(f"+{attr_name}")
                        elif isinstance(target, ast.Attribute) and \
                             isinstance(target.value, ast.Name) and \
                             target.value.id == 'self':
                            # Atributo de instância dentro de um método (ex: self.name)
                            attr_name = target.attr
                            if f"+{attr_name}" not in class_attributes: # Evita duplicatas
                                class_attributes.append(f"+{attr_name}")


            # Formata a classe para PlantUML
            class_body_lines = []
            if class_attributes:
                class_body_lines.extend(sorted(class_attributes))
                class_body_lines.append("--") # Separador visual para PlantUML
            if class_methods:
                class_body_lines.extend(sorted(class_methods))

            plantuml_elements.append(f"class {class_name} {{\\n{';\\n'.join(class_body_lines)}\\n}}")

            # Adiciona relações de herança
            for inherited_class in inherited_classes:
                plantuml_relationships.append(f"{inherited_class} <|-- {class_name}")

    if not plantuml_elements:
        return "Nenhuma classe encontrada no código fornecido."

    full_plantuml = "@startuml\\n"
    full_plantuml += "\\n\\n".join(plantuml_elements)
    if plantuml_relationships:
        full_plantuml += "\\n\\n" + "\\n".join(plantuml_relationships)
    full_plantuml += "\\n@enduml"

    return full_plantuml

def save_and_convert_diagram(plantuml_code: str, output_puml_file: str = "diagrama_classes_relogio.puml"):
    """
    Salva o código PlantUML em um arquivo e tenta convertê-lo em imagem.
    Requer o PlantUML instalado e acessível via PATH.
    """
    if not plantuml_code:
        print("Nenhum código PlantUML para salvar ou converter.")
        return

    try:
        with open(output_puml_file, "w") as f:
            f.write(plantuml_code)
        print(f"Código PlantUML salvo em {output_puml_file}")

        print("Tentando gerar o diagrama de imagem com PlantUML...")
        # Certifique-se de que 'plantuml' está no seu PATH ou forneça o caminho completo para o .jar
        os.system(f"plantuml {output_puml_file}")
        print("Comando de geração de diagrama executado. Verifique o diretório para o arquivo de imagem (ex: .png).")
    except Exception as e:
        print(f"Erro ao salvar ou converter o diagrama: {str(e)}")

if __name__ == "__main__":
    # --- O arquivo Python a ser analisado ---
    target_file_name = "relogio.py"

    # --- Gerar e Salvar o Diagrama ---
    plantuml_output = parse_python_for_class_diagram(target_file_name)
    if plantuml_output and "Erro: Arquivo não encontrado" not in plantuml_output:
        print("\n--- Código PlantUML Gerado ---")
        print(plantuml_output)
        save_and_convert_diagram(plantuml_output)
    else:
        print(plantuml_output) # Imprime a mensagem de erro se o arquivo não for encontrado
        print("Falha ao gerar o diagrama PlantUML.")