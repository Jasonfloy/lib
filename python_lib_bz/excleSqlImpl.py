#encoding: utf-8-
import xlrd
import psycopg2
import sys
'''use for importing data from excle.'''
reload(sys)
sys.setdefaultencoding('utf-8')

erroList=[]#错误信息列表,数据为0时才可以进行别的操作
createSqlList=[]#建表语句
insertSql=[]#插入curd表语句
databaseInfo={}#数据库信息
thisFilePath=''#文件路径

#打开Excel
def open_excel(files=thisFilePath):
    try:
        data = xlrd.open_workbook(files)
        return data
    except Exception:
        pass

#取得excle
def getTable():
    try:
        data = open_excel(files=thisFilePath)
        table = data.sheets()[0]
        return table
    except Exception:
        pass

#取得excle数据
def excelDate():
    try:
        excleDataList=[]#excle的列表数据
        table = getTable()
        nrows = table.nrows #行数
        ncols = table.ncols #列数
        for i in range(5,nrows):
            cell_value = table.cell_value(i,1)
            for j in range(ncols):
                cell_value = table.cell_value(i,j)
                if j==1:
                    lieName = cell_value
                if j==2:
                    lieTableName = cell_value
                if j==3:
                    lieTableType = cell_value
                if j==5:
                    jsonString = cell_value
                '''if j==5:
                    unitType = cell_value '''
                if j==6:
                    crudType = cell_value
                if j==7:
                    orderNum = cell_value
                if j==8:
                    isView = cell_value
            hang={'lieName':lieName,'lieTableName':lieTableName,'lieTableType':lieTableType,'crudType':crudType,'orderNum':orderNum,'isView':isView,'jsonString':jsonString}
            excleDataList.append(hang)
        return excleDataList
    except Exception:
        pass

#数据检查
def checkExcelNull():
    try:
        table = getTable()
        if table.nrows <=4:
            erroList.append("Error:No fill in the data template!")
        for i in range(5,table.nrows):
            for j in range(table.ncols):
                cell_value = str(table.cell_value(i,j))
                if j!=5:
                    if not cell_value.strip():
                        erroList.append("line: %d , column: %d is null,Please check." % (i,j))
    except Exception:
        pass

#获取数据库基本信息
def getDataBaseInfo():
    try:
        table = getTable()
        database = table.cell_value(0,1)
        if not database.strip():
            erroList.append("database is null,Please check.")
        url = str(table.cell_value(1,1))
        if not url.strip():
            erroList.append("hosts is null,Please check.")
        tableName = str(table.cell_value(2,1))
        if not tableName.strip():
            erroList.append("tableName is null,Please check.")
        tableNameDes = str(table.cell_value(3,1))
        if not tableNameDes.strip():
            erroList.append("tableNameDec is null,Please check.")
        port = str(table.cell_value(1,3))
        if not port.strip():
            erroList.append("port is null,Please check.")
        userName = str(table.cell_value(2,3))
        if not userName.strip():
            erroList.append("user is null,Please check.")
        passWord = str(table.cell_value(3,3))
        if not passWord.strip():
            erroList.append("password is null,Please check.")
        databaseInfo = {'database':database,'url':url,'tableName':tableName,'tableNameDes':tableNameDes,'port':port,'userName':userName,'passWord':passWord}
        return databaseInfo
    except Exception:
        pass

#检查数据连接及数据是否存在
def check_excel_conn():
    try:
        databaseInfo=getDataBaseInfo()
        conn = psycopg2.connect(database=databaseInfo['database'], user=databaseInfo['userName'], password=databaseInfo['passWord'], host=databaseInfo['url'], port=databaseInfo['port'])
        cur = conn.cursor()
        try:
            tableName=databaseInfo['tableName']
            cur.execute("select * From pg_tables  where tablename = '"+tableName+"'" )
            rows = cur.fetchall()
            if len(rows)>0:
                erroList.append("%s Table already exists, please delete the table."% tableName)
            cur.execute("select * from crud_conf where table_name =  '"+tableName+"'" )
            rows = cur.fetchall()
            if len(rows)>0:
                erroList.append("crud_conf already exists data of %s ,please delete the data."% tableName)
        except Exception,e:
            erroList.append("The database connection information is incorrect, please check! 详请：%s" % e)
        cur.close()
        conn.close()
    except Exception,e:
        pass

#创建create语句
def create_table_sql():
    try:
        dataBaseInfo=getDataBaseInfo()
        thisExcleDate=excelDate()
        createSqlPart1='CREATE TABLE '+dataBaseInfo['tableName']+'('
        createSqlPart2=''
        j=0
        for i in thisExcleDate:
            j=j+1
            createSqlPart2=createSqlPart2+i['lieTableName']+' '+i['lieTableType']
            if j==len(thisExcleDate):
                createSqlPart2=createSqlPart2+ '--'+i['lieName']+'\n'+')'
            else:
                createSqlPart2=createSqlPart2+ ',--'+i['lieName']+'\n'
        createSqlPart3='INHERITS (base) WITH (OIDS=FALSE);'
        createSql=createSqlPart1+createSqlPart2+createSqlPart3
        alertOwnerSql='ALTER TABLE '+dataBaseInfo['tableName']+' OWNER TO '+dataBaseInfo['database']+';'
        alertTabNameDec='COMMENT ON TABLE '+ dataBaseInfo['tableName']+' IS \''+dataBaseInfo['tableNameDes']+'\';'
        createSqlList.append(createSql)
        createSqlList.append(alertOwnerSql)
        createSqlList.append(alertTabNameDec)
        for i in thisExcleDate:
            alertTabCl='COMMENT ON COLUMN '+dataBaseInfo['tableName']+'.'+i['lieTableName']+ ' IS \''+i['lieName']+'\'; '
            createSqlList.append(alertTabCl)
        alertPkey='ALTER TABLE '+dataBaseInfo['tableName']+' ADD CONSTRAINT '+dataBaseInfo['tableName']+'_pkey PRIMARY KEY(id);'
        createSqlList.append(alertPkey)
    except Exception:
        pass

#插入crud表语句
def insert_table_sql():
    try:
        dataBaseInfo=getDataBaseInfo()
        thisExcleDate=excelDate()
        insertSqlPart1='INSERT INTO crud_conf(name, description, table_name, grid_show, c_type, seq, options,sql_parm)'
        for i in thisExcleDate:
            insertSqlPart2=''
            if str(i['jsonString']):
                insertSqlPart2=insertSqlPart1+' VALUES(\''+str(i['lieTableName'])+'\',\''+str(i['lieName'])+'\',\''+str(dataBaseInfo['tableName'])+'\',\''+str(i['isView'])[:-2]+'\'::int' +',\''+str(i['crudType'])+'\',\''+str(i['orderNum'])[:-2]+'\',\''+str(i['jsonString'])+'\','+'\'\');'
            else:
                insertSqlPart2=insertSqlPart1+' VALUES(\''+str(i['lieTableName'])+'\',\''+str(i['lieName'])+'\',\''+str(dataBaseInfo['tableName'])+'\',\''+str(i['isView'])[:-2]+'\'::int' +',\''+str(i['crudType'])+'\',\''+str(i['orderNum'])[:-2]+'\',null,'+'\'\');'
            insertSql.append(insertSqlPart2)
    except Exception:
        pass

#执行语句
def excuteSql(sqlString=''):
        databaseInfo=getDataBaseInfo()
        conn = psycopg2.connect(database=databaseInfo['database'], user=databaseInfo['userName'], password=databaseInfo['passWord'], host=databaseInfo['url'], port=databaseInfo['port'])
        cur = conn.cursor()
        cur.execute(sqlString)
        conn.commit()
        cur.close()
        conn.close()

def main():
    if not file:
        print erroList[0]
    else:
        checkExcelNull()
        check_excel_conn()
        create_table_sql()
        insert_table_sql()
        if len(erroList)>0:
            for i in erroList:
                print i
            return
        else:
            print 'The database connection and data check is successful.'
            if len(createSqlList)==3:
                print 'Create table statement to create error.'
                return
            else:
                for i in createSqlList:
                    try:
                        print '------------------------------------------------------------'
                        excuteSql(i)
                        print i
                    except Exception,e:
                        print 'Execute the create statement is incorrect, details : %s'%e
                        return
                print '------------------------------------------------------------'
                print '*************Table created!****************'
            if len(insertSql)<=0:
                print 'Insert table create statement is wrong.'
                return
            else:
                for i in insertSql:
                    try:
                        print '------------------------------------------------------------'
                        excuteSql(i)
                        print i
                    except Exception,e:
                        print 'Execute the insert statement is incorrect, details : %s'%e
                        return
            print '------------------------------------------------------------'
            print '*************Insert the crud_conf table complete !****************'

def checkFile():
        try:
            xlrd.open_workbook(thisFilePath)
        except Exception,e:
            print "Error:no read file! Error details: %s" % str(e)
            return 1

if __name__=="__main__":
    sys.setrecursionlimit(10000)
    if len(sys.argv) == 2:
        thisFilePath=sys.argv[1]
        if checkFile()==1:
            pass
        else:
            main()
    else:
        #update this path
        thisFilePath='e://d.xlsx'
        if checkFile()==1:
            pass
        else:
            main()
