-- Crear esquemas principales para la arquitectura de datos
CREATE SCHEMA IF NOT EXISTS raw;
CREATE SCHEMA IF NOT EXISTS staging;
CREATE SCHEMA IF NOT EXISTS analytics;

-- Asignar permisos al usuario del laboratorio
GRANT ALL ON SCHEMA raw TO datalab;
GRANT ALL ON SCHEMA staging TO datalab;
GRANT ALL ON SCHEMA analytics TO datalab;

COMMENT ON SCHEMA raw IS 'Capa de ingesta directa de datos crudos';
COMMENT ON SCHEMA staging IS 'Capa de limpieza y transformación intermedia';
COMMENT ON SCHEMA analytics IS 'Capa de consumo final para reporting y ML';
