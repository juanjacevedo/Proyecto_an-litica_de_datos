/*Sentencias CREATE*/

DROP TABLE IF EXISTS matricula_IETDH;
CREATE TABLE matricula_IETDH (
	indice INT,
	Secretaría VARCHAR(100),
	Código_Institución INT,
	Nombre_Institución VARCHAR(100) NOT NULL,
	Estado_Institución VARCHAR(20),
	Código_Programa INT,
	Nombre_Programa VARCHAR(100),
	Estado_Programa VARCHAR(50),
	Tipo_Certificado VARCHAR(70),
	Subtipo_Certificado VARCHAR(70),
	Area_de_Desempeño VARCHAR(100),
	Auxiliar_en_el_área_de_la_Salud VARCHAR(70),
	Departamento VARCHAR(70) NOT NULL,
	Municipio VARCHAR(70),
	Localidad VARCHAR(70),
	Sede VARCHAR(70),
	Total_Matrícula_2010 INT,
	Total_Matrícula_2011 INT,
	Total_Matrícula_2012 INT,
	Total_Matrícula_2014 INT,
	Total_Matrícula_2015 INT,
	Total_Matrícula_2016 INT,
	Total_Matrícula_2017 INT,
	Total_Matrícula_2018 INT,
	Total_Matrícula_2019 INT,
	Total_Matrícula_2020 INT,
	Total_Matrícula_2021 INT
);

DROP TABLE IF EXISTS MATRICULA_ESTADISTICA;
CREATE TABLE MATRICULA_ESTADISTICA (
  indice INT,
  codigo_institucion INT,
  IES_padres INT,
  Institución_de_Educación_Superior_IES_ VARCHAR(50) NOT NULL,
  Principal_oSeccional VARCHAR(25),
  id_sector INT,
  id_caracter INT,
  codigo_del_departamento_IES INT,
  Departamento_de_domicilio_la_IES VARCHAR(70) NOT NULL,
  Código_del_Municipio_IES INT,
  municipio_domicilio_IES VARCHAR(70),
  codigo_SNIES_prog INT,
  programa_academico VARCHAR(100),
  id_nivel INT,
  id_nivel_formacion INT,
  id_metodologia INT,
  Nucleo_Básico_del_Conocimiento_NBC VARCHAR(70),
  cod_depto_prog INT,
  cod_munic_prog INT,
  depto_oferta_prog VARCHAR(100),
  munic_oferta_prog VARCHAR(100),
  id_genero INT,
  año INT,
  semestre INT,
  total_matriculados INT
);

DROP TABLE IF EXISTS INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO;
CREATE TABLE INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO(
	indice INT,
	cod_sed INT,
	secretaria VARCHAR(100),
	codigo_institucion INT,
	nombre_institucion VARCHAR(100) NOT NULL,
	licencia VARCHAR(100),
	nit VARCHAR(100),
	cod_dpto INT,
	departamento VARCHAR(100) NOT NULL,
	cod_mpio INT,
	municipio VARCHAR(100),
	localidad VARCHAR(100),
	barrio VARCHAR(100),
	direccion VARCHAR(100),
	telefono VARCHAR(100),
	correo_electronico VARCHAR(100),
	pagina_web VARCHAR(100),
	naturaleza VARCHAR(100),
	nombre_representante VARCHAR(100),
	certificado_calidad VARCHAR(100),
	numero_certificacion VARCHAR(100),
	norma VARCHAR(100),
	entidad_emisora VARCHAR(100),
	estado_certificacion VARCHAR(100),
	longitud FLOAT,
	latitud FLOAT,
	año_corte INT,
	mes_corte INT
);

DROP TABLE IF EXISTS INSTITUCIONES_EDUCACION_SUPERIOR;
CREATE TABLE INSTITUCIONES_EDUCACION_SUPERIOR (
  Código_Institución INT,
  Nombre_Institución VARCHAR(200) NOT NULL,
  Número_Identificación_Tributaria_NIT VARCHAR(100),
  Principal_Seccional VARCHAR(50),
  Naturaleza_Jurídica VARCHAR(50),
  Sector VARCHAR(50),
  Carácter_Académico VARCHAR(100),
  Cod_Departamento VARCHAR(50),
  Departamento_Domicilio VARCHAR(50) NOT NULL,
  Cod_Municipio FLOAT,
  Municipio_Domicilio VARCHAR(100),
  Dirección_Domicilio VARCHAR(100),
  Teléfono_Domicilio VARCHAR(15),
  Norma_de_Creación VARCHAR(50),
  Fecha_Norma_de_Creación VARCHAR(100),
  Acreditada_Alta_Calidad VARCHAR(15),
  Fecha_Acreditación VARCHAR(50),
  Resolución_de_la_acreditación FLOAT,
  Vigencia_de_la_acreditación FLOAT,
  Estado VARCHAR(50),
  Página_Web VARCHAR(100)
);


/*Consultas*/

/*1. ¿Cuántos departamentos cuentan con entidades de educación superior o entidades de educación para el trabajo y el desarrollo humano en orden descendente? */

SELECT (COUNT(DISTINCT Nombre_Instituci__n) + COUNT(DISTINCT nombre_institucion)) AS Total, LPAD(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(departamento, ',',''), 'Á', 'A'),'É','E'), 'Í','I'), 'Ó', 'O'), 'Ú', 'U'),60, '-') AS departamentos FROM `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO`
FULL JOIN `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR` ON REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(departamento, ',',''), 'Á', 'A'),'É','E'), 'Í','I'), 'Ó', 'O'), 'Ú', 'U') = REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(REPLACE(UPPER(Departamento_Domicilio), ',',''), 'Á', 'A'),'É','E'), 'Í','I'), 'Ó', 'O'), 'Ú', 'U')
GROUP BY departamentos
ORDER BY Total DESC;


/*2. ¿Cuántas entidades presentan acreditación de alta calidad o certificado de calidad por departamento?*/

SELECT (COUNT(Nombre_Instituci__n) + COUNT(nombre_institucion))AS Total, departamento FROM `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO`
FULL OUTER JOIN `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR` ON departamento = UPPER(Departamento_Domicilio)
WHERE certificado_calidad LIKE '%SI%' AND __Acreditada_Alta_Calidad_ LIKE '%SI%'
GROUP BY departamento
ORDER BY Total;

/*3. ¿Qué porcentaje de entidades presentan acreditación de alta calidad por departamento? Nota: Universidades...*/

SELECT Departamento_Domicilio AS Departamento, COUNT(CASE WHEN __Acreditada_Alta_Calidad_ = "SI" THEN 1 ELSE NULL END)/COUNT(__Acreditada_Alta_Calidad_) AS promedio FROM `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR`
GROUP BY Departamento; 

/*4. ¿Qué porcentaje de entidades presentan certificado de calidad por municipio en orden ascendente? Nota: Educación para el trabajo y desarrollo humano (IETDH)*/

SELECT municipio, (COUNT(CASE WHEN certificado_calidad = 'SI' THEN 1 ELSE NULL END)/COUNT(certificado_calidad)) AS promedio FROM `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO`
GROUP BY municipio
ORDER BY promedio ASC;

/*5. ¿Cuántas entidades de educación superior y de educación para el trabajo y el desarrollo humano son de naturaleza privada?*/

SELECT naturaleza, COUNT(DISTINCT Nombre_Instituci__n) AS Edu_Sup, COUNT(DISTINCT nombre_institucion) AS IETDH FROM `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO`
FULL OUTER JOIN `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR` ON departamento = UPPER(Departamento_Domicilio)
WHERE naturaleza LIKE '%PRIVADA%' AND Sector LIKE '%Privado%'
GROUP BY naturaleza;

/*6. ¿Cuántas entidades de educación superior y de educación para el trabajo y el desarrollo humano son de naturaleza pública?*/

SELECT naturaleza, COUNT(DISTINCT Nombre_Instituci__n) AS Edu_Sup, COUNT(DISTINCT nombre_institucion) AS ETDH FROM `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO`
FULL OUTER JOIN `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR` ON departamento = UPPER(Departamento_Domicilio)
WHERE naturaleza LIKE '%OFICIAL%' AND Sector LIKE '%Oficial%'
GROUP BY naturaleza;

/*7. ¿Cuales son las instituciones para el trabajo que no cuentan con página web?*/
SELECT nombre_institucion, COALESCE(pagina_web, 'No tiene') AS pagina FROM `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO`
WHERE  COALESCE(pagina_web, 'No tiene') = 'No tiene';

/*8.¿A qué departamento pertenece cada IES con su página web?*/
SELECT 	UPPER(Departamento_Domicilio) As Departamento, CONCAT(Nombre_Instituci__n, ' - ', UPPER(P__gina_Web)) AS Institucion_Pagina FROM `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR`;

/*9. ¿Cuál es el departamento con más entidades de educación superior?*/
SELECT Departamento_Domicilio AS Departamento, COUNT(Nombre_Instituci__n) AS Entidad FROM `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR`
GROUP BY Departamento
ORDER BY Entidad DESC
LIMIT 1;


/*10. ¿Cuál es el departamento con más entidades de educación para el trabajo y el desarrollo humano?*/
SELECT departamento, COUNT(nombre_institucion) AS Entidad FROM `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO`
GROUP BY Departamento
ORDER BY Entidad DESC
LIMIT 1;

/*11. ¿Cuáles son los 10 departamentos con menos entidades de educación superior?*/
SELECT Departamento_Domicilio AS Departamento, COUNT(Nombre_Instituci__n) AS Entidad FROM `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR`
GROUP BY Departamento
ORDER BY Entidad ASC
LIMIT 10;

/*12.¿Cuáles son los 10 departamentos con menos entidades de educación para el trabajo y el desarrollo humano?*/

SELECT departamento, COUNT(nombre_institucion) AS Entidad FROM `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO`
GROUP BY Departamento
ORDER BY Entidad ASC
LIMIT 10;

/*13.¿Cuál es el total de matriculados en las instituciones ETDH y de educación superior entre 2015 y 2020 por departamento?*/

WITH table1 AS (
  SELECT cod_dpto, Nombre_Instituci__n, C__digo_Instituci__n, (SUM(_Total_Matr__cula_2015_)+ SUM(_Total_Matr__cula_2016_) + SUM(_Total_Matr__cula_2017_) + SUM(_Total_Matr__cula_2018_) + SUM(_Total_Matr__cula_2019_) + SUM(_Total_Matr__cula_2020_)) AS Total FROM `Primera_entrega.matricula_IETDH`
INNER JOIN `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO` ON C__digo_Instituci__n = codigo_institucion
GROUP BY Nombre_Instituci__n, C__digo_Instituci__n, cod_dpto
),

table2 AS (
  SELECT C__digo_del_departamento_IES_ AS Cod, Departamento_Domicilio, Instituci__n_de_Educaci__n_Superior__IES_, C__digo_de_la_Instituci__n, SUM(Total_Matriculados) AS Total FROM `Primera_entrega.MATRICULA_ESTADISTICA`
INNER JOIN `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR` ON C__digo_Instituci__n = C__digo_de_la_Instituci__n
GROUP BY Instituci__n_de_Educaci__n_Superior__IES_, C__digo_de_la_Instituci__n, C__digo_del_departamento_IES_, Departamento_Domicilio
)

SELECT table2.Departamento_Domicilio, (SUM(table2.Total) + SUM(table1.Total)) AS Total FROM table2
INNER JOIN table1 ON Cod = cod_dpto
GROUP BY table2.Departamento_Domicilio
ORDER BY Total DESC;

/*14.¿Total de matriculados en una institución de educación superior y ETDH con acreditación de calidad entre 2015 y 2020 por departamento? */

WITH calidad_ETDH AS (
  SELECT cod_dpto, Nombre_Instituci__n, C__digo_Instituci__n, (SUM(_Total_Matr__cula_2015_)+ SUM(_Total_Matr__cula_2016_) + SUM(_Total_Matr__cula_2017_) + SUM(_Total_Matr__cula_2018_) + SUM(_Total_Matr__cula_2019_) + SUM(_Total_Matr__cula_2020_)) AS Total, certificado_calidad FROM `Primera_entrega.matricula_IETDH`
INNER JOIN `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO` ON C__digo_Instituci__n = codigo_institucion
WHERE certificado_calidad = 'SI'
GROUP BY Nombre_Instituci__n, C__digo_Instituci__n, cod_dpto, certificado_calidad
),

calidad_SUP AS (
  SELECT C__digo_del_departamento_IES_ AS Cod, Departamento_Domicilio, Instituci__n_de_Educaci__n_Superior__IES_, C__digo_de_la_Instituci__n, SUM(Total_Matriculados) AS Total, __Acreditada_Alta_Calidad_ FROM `Primera_entrega.MATRICULA_ESTADISTICA`
INNER JOIN `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR` ON C__digo_Instituci__n = C__digo_de_la_Instituci__n
WHERE __Acreditada_Alta_Calidad_ = "SI"
GROUP BY Instituci__n_de_Educaci__n_Superior__IES_, C__digo_de_la_Instituci__n, C__digo_del_departamento_IES_, Departamento_Domicilio, __Acreditada_Alta_Calidad_
)

SELECT calidad_SUP.Departamento_Domicilio, (SUM(calidad_SUP.Total) + SUM(calidad_ETDH.Total)) AS Total FROM calidad_SUP
INNER JOIN calidad_ETDH ON Cod = cod_dpto
GROUP BY calidad_SUP.Departamento_Domicilio
ORDER BY Total DESC;

/*15.¿Total de matriculados en una institución de educación superior y ETDH de naturaleza pública y mixta entre 2015 y 2020 por departamento? */

WITH natu_SUP AS (
  SELECT C__digo_del_departamento_IES_ AS Cod, Departamento_Domicilio, Instituci__n_de_Educaci__n_Superior__IES_, C__digo_de_la_Instituci__n, SUM(Total_Matriculados) AS Total, Sector FROM `Primera_entrega.MATRICULA_ESTADISTICA`
INNER JOIN `Primera_entrega.INSTITUCIONES_EDUCACION_SUPERIOR` ON C__digo_Instituci__n = C__digo_de_la_Instituci__n
WHERE Sector = 'Oficial'
GROUP BY Instituci__n_de_Educaci__n_Superior__IES_, C__digo_de_la_Instituci__n, C__digo_del_departamento_IES_, Departamento_Domicilio, Sector
),

natu_IETDH AS (
  SELECT cod_dpto, Nombre_Instituci__n, C__digo_Instituci__n, (SUM(_Total_Matr__cula_2015_)+ SUM(_Total_Matr__cula_2016_) + SUM(_Total_Matr__cula_2017_) + SUM(_Total_Matr__cula_2018_) + SUM(_Total_Matr__cula_2019_) + SUM(_Total_Matr__cula_2020_)) AS Total, naturaleza FROM `Primera_entrega.matricula_IETDH`
INNER JOIN `Primera_entrega.INSTITUCIONES_EDUCACION_PARA_EL_TRABAJO` ON C__digo_Instituci__n = codigo_institucion
WHERE naturaleza = 'OFICIAL' OR naturaleza = 'MIXTA'
GROUP BY Nombre_Instituci__n, C__digo_Instituci__n, cod_dpto, naturaleza
)

SELECT natu_SUP.Departamento_Domicilio, (SUM(natu_SUP.Total) + SUM(natu_IETDH.Total)) AS Total FROM natu_SUP
INNER JOIN natu_IETDH ON Cod = cod_dpto
GROUP BY natu_SUP.Departamento_Domicilio
ORDER BY Total DESC;



