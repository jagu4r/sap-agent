import json
import os

class SAPSchemaExtractor:
    def __init__(self):
        # Diccionario predefinido de esquemas comunes de SAP
        self.predefined_schemas = {
            'MARA': {
                'table_name': 'MARA',
                'description': 'Tabla Maestra de Materiales',
                'fields': [
                    {'name': 'MATNR', 'type': 'CHAR', 'length': 18, 'decimals': 0, 'description': 'Número de Material'},
                    {'name': 'MTART', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Tipo de Material'},
                    {'name': 'MBRSH', 'type': 'CHAR', 'length': 1, 'decimals': 0, 'description': 'Rama Industrial'}
                ]
            },
            'KNA1': {
                'table_name': 'KNA1',
                'description': 'Maestro de Clientes',
                'fields': [
                    {'name': 'KUNNR', 'type': 'CHAR', 'length': 10, 'decimals': 0, 'description': 'Número de Cliente'},
                    {'name': 'NAME1', 'type': 'CHAR', 'length': 35, 'decimals': 0, 'description': 'Nombre'},
                    {'name': 'LAND1', 'type': 'CHAR', 'length': 3, 'decimals': 0, 'description': 'País'}
                ]
            },
            'LFA1': {
                'table_name': 'LFA1',
                'description': 'Maestro de Proveedores',
                'fields': [
                    {'name': 'LIFNR', 'type': 'CHAR', 'length': 10, 'decimals': 0, 'description': 'Número de Proveedor'},
                    {'name': 'NAME1', 'type': 'CHAR', 'length': 35, 'decimals': 0, 'description': 'Nombre'},
                    {'name': 'STRAS', 'type': 'CHAR', 'length': 35, 'decimals': 0, 'description': 'Dirección'}
                ]
            }
        }

    def get_table_schema(self, table_name):
        """Obtiene el esquema predefinido de una tabla específica"""
        return self.predefined_schemas.get(table_name)

    def export_to_json(self, table_names, output_file='sap_schemas.json'):
        """Exporta los esquemas de múltiples tablas a un archivo JSON"""
        schemas = {}
        
        for table in table_names:
            schema = self.get_table_schema(table)
            if schema:
                schemas[table] = schema

        # Asegurarse de que el directorio data existe
        os.makedirs('data', exist_ok=True)
        output_path = os.path.join('data', output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(schemas, f, indent=2, ensure_ascii=False)

        return output_path

def main():
    # Lista de tablas para extraer esquemas
    tables_to_extract = [
        'MARA',  # Tabla de materiales
        'KNA1',  # Tabla de clientes
        'LFA1'   # Tabla de proveedores
    ]

    # Crear instancia y extraer esquemas
    extractor = SAPSchemaExtractor()
    output_file = extractor.export_to_json(tables_to_extract)
    print(f"Esquemas exportados a: {output_file}")

if __name__ == "__main__":
    main() 