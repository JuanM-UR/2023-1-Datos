create table tipo_juridico(
	codigo char(2) primary key,
	nombre varchar(45) not null
);

create table clase(
	codigo char(1) primary key,
	nombre varchar(10) not null
);

create table tipo_domicilio(
	codigo char(1) primary key,
	nombre varchar(20) not null
);

create table estado_empresa(
	codigo char(2) primary key,
	nombre varchar(35) not null
);

create table ciudad(
	codigo varchar(5) primary key,
	nombre varchar(30)
);

create table CIIU(
	codigo varchar(4) primary key,
	descripcion varchar(210) not NULL
);

create table tamanio_empresa(
	codigo char(1) primary key,
	nombre varchar(15)
);

create table sector_economico(
	codigo char(2) primary key,
	nombre character varying not null
);

create table empresa(
	nit varchar(30) primary key,
	tipo_identificacion varchar(4) not null,
	razon_social varchar(160) not null,
	num_empleados int not null,
	valor_activos decimal(15,2) not null,
	cod_tamanio_empresa char(1),
	cod_tipo_juridico char(2),
	cod_clase char(1) not null,
	cod_tipo_domicilio char(1),
	cod_estado_empresa char(2),
	cod_ciudad varchar(5),
	cod_sector_economico char(2),
	foreign key (cod_tamanio_empresa) REFERENCES tamanio_empresa(codigo),
	foreign key (cod_tipo_juridico) REFERENCES tipo_juridico(codigo),
	foreign key (cod_clase) REFERENCES clase(codigo),
	foreign key (cod_tipo_domicilio) REFERENCES tipo_domicilio(codigo),
	foreign key (cod_estado_empresa) REFERENCES estado_empresa(codigo),
	foreign key (cod_ciudad) REFERENCES ciudad(codigo),
	foreign key (cod_sector_economico) REFERENCES sector_economico(codigo)
);

create table contacto(
	nit_empresa varchar(30),
	telefono varchar(12),
	correo character varying,
	foreign key (nit_empresa) REFERENCES empresa(nit)
);

create table matricula(
	nit_empresa varchar(30),
	codigo_matricula varchar(10),
	fecha_matricula date not null,
	fecha_revovacion date,
	foreign key (nit_empresa) REFERENCES empresa(nit),
	primary key (nit_empresa,codigo_matricula)
);

create table CIIU_empresa(
	nit_empresa varchar(30),
	num_act_economica int,
	cod_CIIU varchar(4),
	foreign key (nit_empresa) REFERENCES empresa(nit),
	foreign key (cod_CIIU) REFERENCES CIIU(codigo),
	primary key(nit_empresa,cod_CIIU)
);
