"""
Utility functions shared across controller generators.
"""


def build_escaped_inner_json(params):
    """Build C++ code to construct escaped inner JSON for embedding in con field.
    
    Args:
        params: List of parameter dictionaries with 'name', 'type', and 'default'
        
    Returns:
        Tuple of (declarations_string, inner_json_building_lines)
    """
    decls = []
    lines = []
    for i, p in enumerate(params):
        name = p['name']
        dtype = p['type']
        default = p.get('default', '0')
        if dtype == 'int':
            decls.append(f"int {name} = {default};")
            lines.append(f'  inner += "\\\"m2m:{name}\\\":";')
            lines.append(f'  inner += String({name});')
        elif dtype == 'float':
            decls.append(f"float {name} = {default};")
            lines.append(f'  inner += "\\\"m2m:{name}\\\":";')
            lines.append(f'  inner += String({name}, 2);')
        elif dtype == 'string':
            decls.append(f'String {name} = "{default}";')
            lines.append(f'  inner += "\\\"m2m:{name}\\\":\\\"";')
            lines.append(f'  inner += {name};')
            lines.append(f'  inner += "\\\"";')
        elif dtype == 'boolean':
            decls.append(f"bool {name} = {default.lower()};")
            lines.append(f'  inner += "\\\"m2m:{name}\\\":";')
            lines.append(f'  inner += {name} ? "true" : "false";')

        if i < len(params) - 1:
            lines.append('  inner += ",";')

    return '\n'.join(decls), '\n'.join(lines)
