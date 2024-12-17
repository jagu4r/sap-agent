import json
import os
import logging
from typing import Dict, List

class SAPSchemaExtractor:
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.setup_logging()
        
        # Diccionario actualizado con la información de la documentación SAP
        self.predefined_schemas = {
            'MARA': {
                'table_name': 'MARA',
                'description': 'Material Master Data',
                'fields': [
                    {'name': 'MATNR', 'type': 'CHAR', 'length': 18, 'decimals': 0, 'description': 'Material Number'},
                    {'name': 'MTART', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Material Type'},
                    {'name': 'MBRSH', 'type': 'CHAR', 'length': 1, 'decimals': 0, 'description': 'Industry Sector'},
                    {'name': 'MEINS', 'type': 'UNIT', 'length': 3, 'decimals': 0, 'description': 'Base Unit of Measure'}
                ]
            },
            'KNA1': {
                'table_name': 'KNA1',
                'description': 'Customer Master Data',
                'fields': [
                    {'name': 'KUNNR', 'type': 'CHAR', 'length': 10, 'decimals': 0, 'description': 'Customer Number'},
                    {'name': 'LAND1', 'type': 'CHAR', 'length': 3, 'decimals': 0, 'description': 'Country Key'},
                    {'name': 'NAME1', 'type': 'CHAR', 'length': 35, 'decimals': 0, 'description': 'Name 1'},
                    {'name': 'ORT01', 'type': 'CHAR', 'length': 35, 'decimals': 0, 'description': 'City'}
                ]
            },
            'LFA1': {
                'table_name': 'LFA1',
                'description': 'Vendor Master Data',
                'fields': [
                    {'name': 'LIFNR', 'type': 'CHAR', 'length': 10, 'decimals': 0, 'description': 'Vendor Number'},
                    {'name': 'NAME1', 'type': 'CHAR', 'length': 35, 'decimals': 0, 'description': 'Name 1'},
                    {'name': 'STRAS', 'type': 'CHAR', 'length': 35, 'decimals': 0, 'description': 'Street'},
                    {'name': 'LAND1', 'type': 'CHAR', 'length': 3, 'decimals': 0, 'description': 'Country Key'},
                    {'name': 'COMSIZE', 'type': 'CHAR', 'length': 2, 'decimals': 0, 'description': 'Company Size'},
                    {'name': 'DECREGPC', 'type': 'CHAR', 'length': 2, 'decimals': 0, 'description': 'Declaration Regimen for PIS/COFINS'}
                ]
            },
            'EKPO': {
                'table_name': 'EKPO',
                'description': 'Purchasing Document Item',
                'fields': [
                    {'name': 'EBELN', 'type': 'CHAR', 'length': 10, 'decimals': 0, 'description': 'Purchasing Document Number'},
                    {'name': 'EBELP', 'type': 'NUMC', 'length': 5, 'decimals': 0, 'description': 'Item Number'},
                    {'name': 'WERKS', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Plant'},
                    {'name': 'MENGE', 'type': 'QUAN', 'length': 13, 'decimals': 3, 'description': 'Purchase Order Quantity'}
                ]
            },
            'BSEG': {
                'table_name': 'BSEG',
                'description': 'Accounting Document Segment',
                'fields': [
                    {'name': 'BUKRS', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Company Code'},
                    {'name': 'BELNR', 'type': 'CHAR', 'length': 10, 'decimals': 0, 'description': 'Accounting Document Number'},
                    {'name': 'GJAHR', 'type': 'NUMC', 'length': 4, 'decimals': 0, 'description': 'Fiscal Year'},
                    {'name': 'BUZEI', 'type': 'NUMC', 'length': 3, 'decimals': 0, 'description': 'Line Item'}
                ]
            },
            'MARC': {
                'table_name': 'MARC',
                'description': 'Plant Data for Material',
                'fields': [
                    {'name': 'MANDT', 'type': 'CLNT', 'length': 3, 'decimals': 0, 'description': 'Client'},
                    {'name': 'MATNR', 'type': 'CHAR', 'length': 18, 'decimals': 0, 'description': 'Material Number'},
                    {'name': 'WERKS', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Plant'},
                    {'name': 'STEUC', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Control Code'},
                    {'name': 'DISMM', 'type': 'CHAR', 'length': 2, 'decimals': 0, 'description': 'MRP Type'},
                    {'name': 'MAABC', 'type': 'CHAR', 'length': 1, 'decimals': 0, 'description': 'ABC Indicator'},
                    {'name': 'LGPRO', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Storage Location'},
                    {'name': 'LGFSB', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Storage Location for Production Supply'},
                    {'name': 'DISGR', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'MRP Group'},
                    {'name': 'DISLS', 'type': 'CHAR', 'length': 2, 'decimals': 0, 'description': 'Lot Size'},
                    {'name': 'BWSCL', 'type': 'CHAR', 'length': 1, 'decimals': 0, 'description': 'Source of Supply'},
                    {'name': 'BWTTY', 'type': 'CHAR', 'length': 1, 'decimals': 0, 'description': 'Valuation Category'},
                    {'name': 'SERNP', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Serial Number Profile'},
                    {'name': 'CUOBJ', 'type': 'NUMC', 'length': 18, 'decimals': 0, 'description': 'Internal Object Number'},
                    {'name': 'VRVEZ', 'type': 'DEC', 'length': 5, 'decimals': 2, 'description': 'Shipping Setup Time'},
                    {'name': 'VBAMG', 'type': 'QUAN', 'length': 13, 'decimals': 3, 'description': 'Base Quantity for Capacity Planning'},
                    {'name': 'LOSGR', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Logistics Handling Group'},
                    {'name': 'STRGR', 'type': 'CHAR', 'length': 2, 'decimals': 0, 'description': 'Planning Strategy Group'},
                    {'name': 'STLAN', 'type': 'CHAR', 'length': 1, 'decimals': 0, 'description': 'BOM Usage'},
                    {'name': 'AUSME', 'type': 'CHAR', 'length': 3, 'decimals': 0, 'description': 'Base Unit of Measure for Production'}
                ]
            },
            'T000': {
                'table_name': 'T000',
                'description': 'Clients',
                'fields': [
                    {'name': 'MANDT', 'type': 'CLNT', 'length': 3, 'decimals': 0, 'description': 'Client'},
                    {'name': 'CCCATEGORY', 'type': 'CHAR', 'length': 1, 'decimals': 0, 'description': 'Client Category'},
                    {'name': 'CCNOCLIIND', 'type': 'CHAR', 'length': 1, 'decimals': 0, 'description': 'Non-Client-Specific Client'}
                ]
            },
            'T001': {
                'table_name': 'T001',
                'description': 'Company Codes',
                'fields': [
                    {'name': 'BUKRS', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Company Code'},
                    {'name': 'BUTXT', 'type': 'CHAR', 'length': 25, 'decimals': 0, 'description': 'Company Name'},
                    {'name': 'LAND1', 'type': 'CHAR', 'length': 3, 'decimals': 0, 'description': 'Country Key'}
                ]
            },
            'BKPF': {
                'table_name': 'BKPF',
                'description': 'Accounting Document Header',
                'fields': [
                    {'name': 'BUKRS', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Company Code'},
                    {'name': 'BELNR', 'type': 'CHAR', 'length': 10, 'decimals': 0, 'description': 'Document Number'},
                    {'name': 'GJAHR', 'type': 'NUMC', 'length': 4, 'decimals': 0, 'description': 'Fiscal Year'},
                    {'name': 'BLART', 'type': 'CHAR', 'length': 2, 'decimals': 0, 'description': 'Document Type'}
                ]
            },
            'MKPF': {
                'table_name': 'MKPF',
                'description': 'Material Document Header',
                'fields': [
                    {'name': 'MBLNR', 'type': 'CHAR', 'length': 10, 'decimals': 0, 'description': 'Material Document'},
                    {'name': 'MJAHR', 'type': 'NUMC', 'length': 4, 'decimals': 0, 'description': 'Material Document Year'},
                    {'name': 'BUDAT', 'type': 'DATS', 'length': 8, 'decimals': 0, 'description': 'Posting Date'}
                ]
            },
            'MSEG': {
                'table_name': 'MSEG',
                'description': 'Material Document Segment',
                'fields': [
                    {'name': 'MBLNR', 'type': 'CHAR', 'length': 10, 'decimals': 0, 'description': 'Material Document'},
                    {'name': 'MJAHR', 'type': 'NUMC', 'length': 4, 'decimals': 0, 'description': 'Material Document Year'},
                    {'name': 'ZEILE', 'type': 'NUMC', 'length': 4, 'decimals': 0, 'description': 'Item in Material Document'},
                    {'name': 'MATNR', 'type': 'CHAR', 'length': 18, 'decimals': 0, 'description': 'Material Number'},
                    {'name': 'WERKS', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Plant'},
                    {'name': 'LGORT', 'type': 'CHAR', 'length': 4, 'decimals': 0, 'description': 'Storage Location'}
                ]
            }
        }

    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )

    def get_table_schema(self, table_name: str) -> Dict:
        """Obtiene el esquema predefinido de una tabla específica"""
        if table_name in self.predefined_schemas:
            return self.predefined_schemas[table_name]
        else:
            self.logger.warning(f"Tabla {table_name} no encontrada en el diccionario predefinido")
            return None

    def export_to_json(self, table_names: List[str], output_file: str = 'sap_schemas.json') -> str:
        """Exporta los esquemas de múltiples tablas a un archivo JSON"""
        schemas = {}
        
        for table in table_names:
            schema = self.get_table_schema(table)
            if schema:
                schemas[table] = schema
                self.logger.info(f"Esquema extraído para la tabla: {table}")
            else:
                self.logger.warning(f"No se pudo extraer el esquema para la tabla: {table}")

        # Asegurarse de que el directorio data existe
        os.makedirs('data', exist_ok=True)
        output_path = os.path.join('data', output_file)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(schemas, f, indent=2, ensure_ascii=False)
            self.logger.info(f"Esquemas exportados a: {output_path}")

        return output_path

def main():
    # Lista actualizada de tablas para extraer esquemas
    tables_to_extract = [
        'MARA',  # Material Master
        'MARC',  # Plant Data for Material
        'KNA1',  # Customer Master
        'LFA1',  # Vendor Master
        'EKPO',  # Purchase Order Items
        'BSEG',  # Accounting Document Segment
        'BKPF',  # Accounting Document Header
        'MKPF',  # Material Document Header
        'MSEG',  # Material Document Segment
        'T000',  # Clients
        'T001'   # Company Codes
    ]

    # Crear instancia y extraer esquemas
    extractor = SAPSchemaExtractor()
    output_file = extractor.export_to_json(tables_to_extract)
    print(f"Esquemas exportados a: {output_file}")

if __name__ == "__main__":
    main() 