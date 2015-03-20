#encoding: utf-8-
import xlrd
import psycopg2
import sys
'''use for importing data from excle.'''
reload(sys)
sys.setdefaultencoding('utf-8')

erro_list = [] # 错误信息列表,数据为0时才可以进行别的操作
create_sql_list = [] # 建表语句
insert_sql = [] # 插入curd表语句
database_info = {} # 数据库信息
this_file_path = '' # 文件路径

def open_excel(files = this_file_path):
    '''
    打开Excel
    '''
    try:
        data = xlrd.open_workbook(files)
        return data
    except Exception:
        pass

def getTable():
    '''
    取得excle
    '''
    try:
        data = open_excel(files = this_file_path)
        table = data.sheets()[0]
        return table
    except Exception:
        pass

def excelDate():
    '''
    取得excle数据
    '''
    try:
        excle_data_list = [] # excle的列表数据
        table = getTable()
        nrows = table.nrows # 行数
        ncols = table.ncols # 列数  
        for i in range(5,nrows):
            cell_value = table.cell_value(i,1)
            for j in range(ncols):
                cell_value = table.cell_value(i,j)
                if j == 1:
                    lie_name = cell_value
                if j == 2:
                    lie_table_name = cell_value 
                if j == 3:
                    lie_table_type = cell_value
                if j == 5:
                    json_string = cell_value   
                '''if j==5:
                    unitType = cell_value '''
                if j == 6:
                    crud_type = cell_value 
                if j == 7:
                    order_num = cell_value 
                if j == 8:
                    is_view = cell_value
            hang={'lie_name':lie_name,'lie_table_name':lie_table_name,'lie_table_type':lie_table_type,'crud_type':crud_type,'order_num':order_num,'is_view':is_view,'json_string':json_string} 
            excle_data_list.append(hang)  
        return excle_data_list 
    except Exception:
        pass 
            
def checkExcelNull():
    '''
    数据检查
    '''
    try:
        table = getTable()
        if table.nrows <= 4:
            erro_list.append("Error:No fill in the data template!") 
        for i in range(5,table.nrows):
            for j in range(table.ncols):
                cell_value = str(table.cell_value(i,j))
                if j != 5:
                    if not cell_value.strip():
                        erro_list.append("line: %d , column: %d is null,Please check." % (i,j)) 
    except Exception:
        pass                     

def getDatabaseInfo():
    '''
    获取数据库基本信息
    '''
    try:
        table = getTable()
        database = table.cell_value(0,1)
        if not database.strip():
            erro_list.append("database is null,Please check.")
        url = str(table.cell_value(1,1))
        if not url.strip():
            erro_list.append("hosts is null,Please check.")
        table_name = str(table.cell_value(2,1))
        if not table_name.strip():
            erro_list.append("table_name is null,Please check.")
        table_name_des = str(table.cell_value(3,1))
        if not table_name_des.strip():
            erro_list.append("table_nameDec is null,Please check.")
        port = str(table.cell_value(1,3))
        if not port.strip():
            erro_list.append("port is null,Please check.")
        user_name = str(table.cell_value(2,3))
        if not user_name.strip():
            erro_list.append("user is null,Please check.")
        pass_Word = str(table.cell_value(3,3))
        if not pass_Word.strip():
            erro_list.append("password is null,Please check.")
        database_info = {'database':database,'url':url,'table_name':table_name,'table_name_des':table_name_des,'port':port,'user_name':user_name,'pass_Word':pass_Word}
        return database_info   
    except Exception:
        pass   
     
def checkExcelConn():
    '''
    检查数据连接及数据是否存在  
    '''
    try:
        database_info = getDatabaseInfo()
        conn = psycopg2.connect(database=database_info['database'], user=database_info['user_name'], password=database_info['pass_Word'], host=database_info['url'], port=database_info['port'])
        cur = conn.cursor()
        try:
            table_name = database_info['table_name']
            cur.execute("select * From pg_tables  where tablename = '" + table_name+"'" )
            rows = cur.fetchall()
            if len(rows) > 0:
                erro_list.append("%s Table already exists, please delete the table."% table_name)
            cur.execute("select * from crud_conf where table_name =  '" + table_name+"'" )
            rows = cur.fetchall()
            if len(rows) > 0:
                erro_list.append("crud_conf already exists data of %s ,please delete the data." % table_name)
        except Exception,e:
            erro_list.append("The database connection information is incorrect, please check! 详请：%s" % e)
        cur.close()
        conn.close()
    except Exception,e:
        pass

def createTableSql():
    '''
    创建create语句
    '''
    try: 
        database_info = getDatabaseInfo()
        this_Excle_Date = excelDate()
        createSqlPart1 = 'CREATE TABLE ' + database_info['table_name'] + '('
        createSqlPart2 = ''
        j = 0
        for i in this_Excle_Date:
            j = j+1
            createSqlPart2=createSqlPart2+i['lie_table_name'] + ' ' + i['lie_table_type'] 
            if j == len(this_Excle_Date):
                createSqlPart2=createSqlPart2+ '--' + i['lie_name'] + '\n'+')' 
            else:
                createSqlPart2=createSqlPart2+ ',--' + i['lie_name'] + '\n' 
        createSqlPart3 = 'INHERITS (base) WITH (OIDS=FALSE);'
        createSql = createSqlPart1+createSqlPart2+createSqlPart3
        alertOwnerSql = 'ALTER TABLE ' + database_info['table_name'] + ' OWNER TO '+database_info['database'] + ';'
        alertTabNameDec = 'COMMENT ON TABLE '+ database_info['table_name'] +' IS \''+database_info['table_name_des'] + '\';'
        create_sql_list.append(createSql)
        create_sql_list.append(alertOwnerSql)
        create_sql_list.append(alertTabNameDec)
        for i in this_Excle_Date:
            alertTabCl = 'COMMENT ON COLUMN '+database_info['table_name'] + '.' + i['lie_table_name'] + ' IS \'' + i['lie_name'] + '\'; ' 
            create_sql_list.append(alertTabCl)
        alertPkey = 'ALTER TABLE '+database_info['table_name'] + ' ADD CONSTRAINT ' + database_info['table_name'] + '_pkey PRIMARY KEY(id);'
        create_sql_list.append(alertPkey)
    except Exception:
        pass

def insertTableSql(): 
    '''
    插入crud表语句
    '''
    try:
        database_info = getDatabaseInfo()
        this_Excle_Date = excelDate()
        insert_sql_part_1 = 'INSERT INTO crud_conf(name, description, table_name, grid_show, c_type, seq, options,sql_parm)'
        for i in this_Excle_Date:
            insert_sql_part_2 = ''
            if str(i['json_string']):
                insert_sql_part_2 = insert_sql_part_1 + ' VALUES(\'' + str(i['lie_table_name']) + '\',\'' + str(i['lie_name']) + '\',\''+str(database_info['table_name']) + '\',\'' + str(i['is_view'])[:-2] + '\'::int' +',\'' + str(i['crud_type']) + '\',\'' + str(i['order_num'])[:-2] + '\',\'' + str(i['json_string']) + '\',' + '\'\');'  
            else:
                insert_sql_part_2 = insert_sql_part_1 + ' VALUES(\'' + str(i['lie_table_name']) + '\',\'' + str(i['lie_name']) + '\',\''+str(database_info['table_name']) + '\',\'' + str(i['is_view'])[:-2] + '\'::int' +',\'' + str(i['crud_type']) + '\',\'' + str(i['order_num'])[:-2] + '\',null,' + '\'\');'  
            insert_sql.append(insert_sql_part_2)
    except Exception:
        pass
            
def excuteSql(sqlString = ''):
    '''
    执行语句
    '''
    database_info = getDatabaseInfo()
    conn = psycopg2.connect(database=database_info['database'], user=database_info['user_name'], password=database_info['pass_Word'], host=database_info['url'], port=database_info['port'])
    cur = conn.cursor()
    cur.execute(sqlString)
    conn.commit()
    cur.close()
    conn.close()

def main():
    if not file:
        print erro_list[0]
    else:
        checkExcelNull()
        checkExcelConn()
        createTableSql()
        insertTableSql()
        if len(erro_list) > 0:
            for i in erro_list:
                print i
            return
        else:
            print 'The database connection and data check is successful.' 
            if len(create_sql_list) == 3:
                print 'Create table statement to create error.'
                return
            else:
                for i in create_sql_list:
                    try:
                        print '------------------------------------------------------------'
                        excuteSql(i)
                        print i
                    except Exception,e:
                        print 'Execute the create statement is incorrect, details : %s' % e
                        return
                print '------------------------------------------------------------'        
                print '*************Table created!****************'
            if len(insert_sql) <= 0:
                print 'Insert table create statement is wrong.'
                return
            else:
                for i in insert_sql:
                    try:
                        print '------------------------------------------------------------'
                        excuteSql(i)
                        print i
                    except Exception,e:
                        print 'Execute the insert statement is incorrect, details : %s' % e
                        return
            print '------------------------------------------------------------'          
            print '*************Insert the crud_conf table complete !****************'
            
def checkFile():
        try:
            xlrd.open_workbook(this_file_path)
        except Exception,e:
            print "Error:no read file! Error details: %s" % str(e)
            return 1         

if __name__ == "__main__":
    sys.setrecursionlimit(10000)
    if len(sys.argv) == 2:
        this_file_path = sys.argv[1]
        if checkFile() == 1:
            pass
        else:
            main()  
    else:
        '''update this path'''
        this_file_path = 'e://d.xlsx'
        if checkFile() == 1:
            pass
        else:
            main()    