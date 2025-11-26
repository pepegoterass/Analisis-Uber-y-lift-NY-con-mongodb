# Reglas de código obligatorias para Claude

1. Código siempre modular → funciones reutilizables.
2. Explicar cada bloque en forma de comentarios profesionales.
3. No usar rutas absolutas. Usar rutas relativas: ./data/ ./scripts/
4. No usar print en exceso → usar logging.
5. Siempre validar errores (try/except).
6. Nombres claros: snake_case.
7. Tareas grandes → dividir en archivos:
    - ingest.py
    - clean.py
    - load_mongo.py
    - queries.py
    - visualize.py
8. Claude debe ofrecer mejoras de eficiencia.
9. Consultas Mongo → siempre en aggregation pipeline.
10. Cuando haya decisiones de análisis → justificar con reasoning experto.
