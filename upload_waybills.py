import psycopg2
import os
import xml.etree.ElementTree as ET
from ftp_dowload import dowload_new_waybills


def update_fact_waybills():
    read_conn = psycopg2.connect(dbname='taxi', user='etl_tech_user', 
                            password='etl_tech_user_password', host='de-edu-db.chronosavant.ru')
    read_cursor = read_conn.cursor()


    write_conn = psycopg2.connect(dbname='dwh', user='dwh_krasnoyarsk', 
                            password='dwh_krasnoyarsk_uBPaXNSx', host='de-edu-db.chronosavant.ru')
    write_cursor = write_conn.cursor()

    #Загрузка новых файлов
    dowload_new_waybills()

    directory = 'waybills/'
    files = os.listdir(directory)
        
        
    error_files = []
    write_cursor.execute("SELECT MAX(waybill_num) FROM fact_waybills")
    res = write_cursor.fetchall()
    if res != [(None,)]:
        waybill_num = res[-1][0] + 1
    else:
        waybill_num = 0
    
    # print(files)
    for file in files:
        try:
            #выборка данных
            tree = ET.parse('waybills/'+file)

            plate_num = tree.findall('waybill/car')[0].text #car num
            license = tree.findall('waybill/driver/license')[0].text
            work_start_dt = tree.findall('waybill/period/start')[0].text
            work_end_dt = tree.findall('waybill/period/stop')[0].text
            issue_dt = tree.findall('./')[0].attrib['issuedt']
            
            write_cursor.execute(f"SELECT personnel_num FROM dim_drivers WHERE driver_license_num = '{license}'")
            driver_pers_num = write_cursor.fetchall()[-1][0]
            # print(waybill_num, driver_pers_num, plate_num, work_start_dt, work_end_dt, issue_dt)
            
            #запись данных
            write_cursor.execute('INSERT INTO fact_waybills VALUES(%s, %s, %s, %s, %s, %s);',
                (waybill_num, driver_pers_num, plate_num, work_start_dt, work_end_dt, issue_dt))
            write_conn.commit()
            waybill_num += 1
            os.remove('waybills/'+file)
        except Exception as e:
            # print(e)
            # print(file)
            # os.remove('waybills/'+file)
            error_files.append(file)

    #возможно стоити перенести в другое место и добавить проверку на ошибки
    if files != []:
        with open('last_waybill.txt', 'w') as f:
            f.write(files[-1])
            
    if error_files != []:
        print('Problems with files:' + ' '.join(error_files))


    write_cursor.close()
    write_conn.close()
    read_cursor.close()
    read_conn.close()
    
    return error_files
    
    
if __name__ == '__main__':
    update_fact_waybills()