from kcweb.utill.db import mysql
class bank_sub:
    "分表操作数据库"
    __config=None #数据库配置信息
    __table=None #主表名
    __sub_table=None #分表名
    def connects(self,config=None):
        if config:
            self.__config=config
        return self
    def table(self,table,sub_id):
        """
        * 指定数据表
        * @param unknown $table  主表名
        * @param unknown $sub_id  分表标识
        * @return \app\api2\model\db\bank_ny
        """
        self.__table=table
        self.__sub_table=table+str(sub_id)
        if self.__table==self.__sub_table:
            print("sub_id不能为空")
            exit()
        return self
    def select(self,id=None):
        """select查询 

        返回 list(列表)
        """
        dbs=mysql.mysql()
        if self.__where:
            dbs=dbs.where(self.__where,self.__wheres)
        if self.__field:
            dbs=dbs.field(self.__field)
        if self.__limit:
            dbs=dbs.limit(self.__limit[0],self.__limit[1])
        try :
            return dbs.connect(self.__config).table(self.__sub_table).select()
        except Exception as e:
            if not dbs.connect(self.__config).query('show tables like "'+self.__sub_table+'"'):
                try:
                    dbs.connect(self.con__configfig).query("create table "+self.__sub_table+" LIKE "+self.__table+";")
                    return []
                except Exception as e:
                    raise Exception(e)
            else:
                raise Exception(e)
    def find(self,id = None):
        """
        查询一条记录
        
        返回 字典
        """
        dbs=mysql.mysql()
        if self.__where:
            dbs=dbs.where(self.__where,self.__wheres)
        if self.__field:
            dbs=dbs.field(self.__field)
        if self.__limit:
            dbs=dbs.limit(self.__limit[0],self.__limit[1])
        try :
            return dbs.connect(self.__config).table(self.__sub_table).find(id)
        except Exception as e:
            if not dbs.connect(self.__config).query('show tables like "'+self.__sub_table+'"'):
                try:
                    dbs.connect(self.__config).query("create table "+self.__sub_table+" LIKE "+self.__table+";")
                    return {}
                except Exception as e:
                    raise Exception(e)
            else:
                raise Exception(e)
    def count(self,field="*"):
        """查询数量
        
        返回 int 数字
        """
        dbs=mysql.mysql()
        if self.__where:
            dbs=dbs.where(self.__where,self.__wheres)
        if self.__field:
            dbs=dbs.field(self.__field)
        if self.__limit:
            dbs=dbs.limit(self.__limit[0],self.__limit[1])
        try :
            return dbs.connect(self.__config).table(self.__sub_table).count(field)
        except Exception as e:
            if not dbs.connect(self.__config).query('show tables like "'+self.__sub_table+'"'):
                try:
                    dbs.connect(self.__config).query("create table "+self.__sub_table+" LIKE "+self.__table+";")
                    return 0
                except Exception as e:
                    raise Exception(e)
            else:
                raise Exception(e)
    def update(self,data,affair=False):
        """数据表更新
         
        参数 data 要更新的内容  格式：{"name":"测试","age":20}

        参数 affair 是否开启事务 True表示手动提交事务  False表示自动提交事务 (暂时只能使用默认值)
        """
        dbs=mysql.mysql()
        if self.__where:
            dbs=dbs.where(self.__where,self.__wheres)
        if self.__field:
            dbs=dbs.field(self.__field)
        if self.__limit:
            dbs=dbs.limit(self.__limit[0],self.__limit[1])
        try :
            return dbs.connect(self.__config).table(self.__sub_table).update(data,affair)
        except Exception as e:
            raise Exception(e)
    def delete(self,affair=False):
        """数据表删除

        参数 affair 是否开启事务 True表示手动提交事务  False表示自动提交事务 (暂时只能使用默认值)
        """
        dbs=mysql.mysql()
        if self.__where:
            dbs=dbs.where(self.__where,self.__wheres)
        if self.__field:
            dbs=dbs.field(self.__field)
        if self.__limit:
            dbs=dbs.limit(self.__limit[0],self.__limit[1])
        try :
            return dbs.connect(self.__config).table(self.__sub_table).delete(affair)
        except Exception as e:
            raise Exception(e)
    def insert(self,data):
        """插入数据库 单条插入或多条插入

        参数 dicts 要插入的内容 单条格式：{"name":"测试","age":20}  。     多条格式：[{"name":"测试","age":20},{"name":"测试","age":20}]
        
        参数 affair 是否开启事务 True表示手动提交事务  False表示自动提交事务
        """
        dbs=mysql.mysql()
        try :
            return dbs.connect(self.__config).table(self.__sub_table).insert(data)
        except Exception as e:
            if not dbs.connect(self.__config).query('show tables like "'+self.__sub_table+'"'):
                try:
                    dbs.connect(self.__config).query("create table "+self.__sub_table+" LIKE "+self.__table+";")
                    return dbs.connect(self.__config).table(self.__sub_table).insert(data)
                except Exception as e:
                    raise Exception(e)
            else:
                raise Exception(e)
    def commit(self):
        """事务提交

        增删改后的任务进行提交
        """
        dbs=mysql.mysql()
        dbs.commit()
    def rollback(self):
        """事务回滚

        增删改后的任务进行撤销
        """
        dbs=mysql.mysql()
        dbs.rollback()
    __where=None
    __wheres=()
    def where(self,where = None,*wheres):
        """设置过滤条件

        参数 where：str 字符串 或 列表
       
        传入方式:

        "id","in",2,3,4,5,6,...表示 id in (2,3,4,5,6,...)

        "id",2 表示id='2'

        [("id","gt",6000),"and",("name","like","%超")] 表示 ( id > "6000" and name LIKE "%超" )

        "id","eq",1 表示 id = '1'
        """
        self.__where=where
        self.__wheres=wheres
        return self
    __field='*'
    def field(self,field = "*"):
        """设置过滤条件

        参数 field：str 字符串
        """
        self.__field=field
        return self
    __limit=[]
    def limit(self,offset, length = None):
        """设置查询数量

        参数 offset：int 起始位置

        参数 length：int 查询数量
        """
        self.__limit=[offset,length]
        return self