# Usar una imagen base de Python
FROM python:3.9-slim

# Establecer el directorio de trabajo
WORKDIR /app

# Copiar el código directamente
COPY . .

# Crear directorio para los datos
RUN mkdir -p /app/data

# Comando por defecto
CMD ["python", "sap_doc_extractor.py"] 