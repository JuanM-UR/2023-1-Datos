import psycopg2

tablas: list = ['CIIU','CIIU_empresa','clase','ciudad','contacto','estado_empresa','sector_economico',
          'tamanio_empresa','tipo_domicilio','tipo_juridico','Matricula','Empresa']

if __name__ == '__main__':
    try:
        connection=psycopg2.connect(
            host="localhost",
            user="postgres",
            password="123456789",
            database="Proyecto"
        )   
        print("Conexión exitosa\n")
        cursor=connection.cursor()
        for tabla in tablas:
            print(f'Tabla: {tabla}')
            cursor.execute(f'select * from {tabla};')
            rows=cursor.fetchmany()
            for row in rows:
                print(row)
            print('\n')
    except Exception as ex:
        print(ex)
    finally:
        connection.close()
        print("Conexión Finalizada") 