# SAP Schema Extractor

Extractor de esquemas de tablas SAP basado en documentación pública.

## 🚀 Características

- Extrae información de esquemas de tablas SAP comunes
- Genera salida en formato JSON
- Containerizado con Docker
- No requiere acceso directo a SAP

## 📋 Prerequisitos

- Docker
- Docker Compose

## 🔧 Instalación y Uso

1. Clona este repositorio:
```bash
git clone <repository-url>
cd sap-schema-extractor
```

2. Construye y ejecuta con Docker Compose:
```bash
docker-compose up --build
```

Los esquemas se exportarán a `./data/sap_schemas.json`

## 📝 Ejemplo de Salida

```json
{
  "MARA": {
    "table_name": "MARA",
    "description": "Material Master Data",
    "fields": [
      {
        "name": "MATNR",
        "type": "CHAR",
        "length": 18,
        "description": "Material Number"
      }
    ]
  }
}
```

## 🤝 Contribuciones

¡Las contribuciones son bienvenidas! Puedes:
- Agregar más tablas al diccionario predefinido
- Mejorar la documentación
- Reportar bugs

## 📄 Licencia

Este proyecto está bajo la Licencia MIT