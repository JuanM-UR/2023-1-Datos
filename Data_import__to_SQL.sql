COPY PUBLIC.tipo_juridico(codigo, nombre)
from 
'C:\Tablas\TipoJuridico.csv' delimiter ';' csv header;
--------------------------------------------------
COPY PUBLIC.clase(codigo, nombre)
from 
'C:\Tablas\Clase.csv' delimiter ';' csv header;
--------------------------------------------------
COPY PUBLIC.tipo_domicilio(codigo, nombre)
from 
'C:\Tablas\Domicilio.csv' delimiter ';' csv header; 
--------------------------------------------------
COPY PUBLIC.estado_empresa(codigo, nombre)
from 
'C:\Tablas\Estado.csv' delimiter ';' csv header; 
--------------------------------------------------
COPY PUBLIC.ciudad(codigo, nombre)
from 
'C:\Tablas\Ciudad.csv' delimiter ';' csv header; 
-------------------------------------------------
COPY PUBLIC.CIIU(codigo, descripcion)
from 
'C:\Tablas\CIIU.csv' delimiter ';' csv header;
--------------------------------------------------
COPY PUBLIC.tamanio_empresa(codigo, nombre)
from 
'C:\Tablas\TamanioEmpresa.csv' delimiter ';' csv header;
--------------------------------------------------
COPY PUBLIC.sector_economico(codigo, nombre)
from 
'C:\Tablas\SectorEconomico.csv' delimiter ';' csv header;
--------------------------------------------------
COPY PUBLIC.empresa(nit,tipo_identificacion,razon_social,num_empleados,
					valor_activos,cod_tamanio_empresa,cod_tipo_juridico,
					cod_clase,cod_tipo_domicilio,cod_estado_empresa,cod_ciudad,
				   cod_sector_economico)
from 
'C:\Tablas\Empresa.csv' delimiter ';' csv header;
--------------------------------------------------
COPY PUBLIC.contacto(nit_empresa,telefono,correo)
from 
'C:\Tablas\Contacto.csv' delimiter ';' csv header;
--------------------------------------------------
COPY PUBLIC.matricula(nit_empresa,codigo_matricula,fecha_matricula,fecha_revovacion)
from 
'C:\Tablas\Matricula.csv' delimiter ';' csv header;
--------------------------------------------------
COPY PUBLIC.CIIU_empresa(nit_empresa,num_act_economica,cod_CIIU)
from 
'C:\Tablas\CIIU_Empresa.csv' delimiter ';' csv header;
