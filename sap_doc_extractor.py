import requests
from bs4 import BeautifulSoup
import json
import os
from typing import Dict, List
import logging

class SAPDocExtractor:
    def __init__(self):
        self.base_url = "https://help.sap.com/docs"
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def get_table_schema(self, table_name: str) -> Dict:
        """
        Extrae información de la tabla desde la documentación de SAP
        """
        try:
            # Diccionario de tablas comunes y sus campos (ya que no podemos acceder directamente a SAP)
            common_tables = {
                "MARA": {
                    "description": "Material Master Data",
                    "fields": [
                        {"name": "MATNR", "type": "CHAR", "length": 18, "description": "Material Number"},
                        {"name": "MTART", "type": "CHAR", "length": 4, "description": "Material Type"},
                        {"name": "MBRSH", "type": "CHAR", "length": 1, "description": "Industry Sector"},
                        {"name": "MEINS", "type": "UNIT", "length": 3, "description": "Base Unit of Measure"}
                    ]
                },
                "KNA1": {
                    "description": "Customer Master Data",
                    "fields": [
                        {"name": "KUNNR", "type": "CHAR", "length": 10, "description": "Customer Number"},
                        {"name": "LAND1", "type": "CHAR", "length": 3, "description": "Country Key"},
                        {"name": "NAME1", "type": "CHAR", "length": 35, "description": "Name 1"},
                        {"name": "ORT01", "type": "CHAR", "length": 35, "description": "City"}
                    ]
                }
            }
            
            if table_name in common_tables:
                return {
                    "table_name": table_name,
                    **common_tables[table_name]
                }
            else:
                self.logger.warning(f"Tabla {table_name} no encontrada en el diccionario predefinido")
                return None
                
        except Exception as e:
            self.logger.error(f"Error al procesar la tabla {table_name}: {str(e)}")
            return None

    def export_to_json(self, table_names: List[str], output_file: str = '/app/data/sap_schemas.json') -> str:
        """Exporta los esquemas a un archivo JSON"""
        schemas = {}
        
        for table in table_names:
            schema = self.get_table_schema(table)
            if schema:
                schemas[table] = schema

        os.makedirs(os.path.dirname(output_file), exist_ok=True)
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(schemas, f, indent=2, ensure_ascii=False)

        return output_file

def main():
    tables_to_extract = [
        'MARA',
        'KNA1'
    ]

    extractor = SAPDocExtractor()
    output_file = extractor.export_to_json(tables_to_extract)
    print(f"Schemas exported to: {output_file}")

if __name__ == "__main__":
    main() 