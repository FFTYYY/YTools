from .fakepath import new_fakefolder
from ..universe.onexit import add_quit_methods
import sqlite3
import os
try:
    from collections import Iterable
except ImportError:
    from collections.abc import Iterable
    
import pickle
from ..universe.exceptions import ArgumentError , YAttributeError

HASH_FOLDER_NAME = "YToolsHash"

class StaticHash:

	def __init__(self , db_name , tb_name = "Hash" ,  keysize = 255):

		self.tb_name = tb_name

		# 获取数据库地址
		folderpath = new_fakefolder( HASH_FOLDER_NAME )
		self.db_path = os.path.join( folderpath , db_name )

		# 连接数据库
		self.connection = sqlite3.connect(self.db_path , check_same_thread = False)
		self.cursor = self.connection.cursor()
		self.closed = False
		add_quit_methods(self.close) #确保退出时关闭

		# 初始化数据库
		self.keysize = keysize
		self.init()

	def close(self):
		if self.closed: #防止反复关闭
			return
		self.closed = True

		self.cursor.close()
		self.connection.close()

	def delete(self):
		'''!! 删除所有记录'''
		self.close()
		os.remove(self.db_path)

	def init(self):
		'''初始化表'''
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS {tablename}
			(
				key varchar({keysize}) PRIMARY KEY, 
				val int
			);
		""".format(tablename = self.tb_name, keysize = self.keysize))
		self.connection.commit()

	def get(self , key):
		'''查询某个key的值，没有则返回None'''

		ret = self.cursor.execute("""
			SELECT val
			FROM {tablename}
			WHERE key = '{key}';
		""".format(tablename = self.tb_name , key = key)).fetchall()

		if len(ret) == 0:
			return None

		return ret[0][0]

	def set(self , key , val , commit = True):
		'''将某个key设为val'''

		#insert或replace
		self.cursor.execute("""
			INSERT OR REPLACE INTO {tablename}
			VALUES ('{key}',{val});
		""".format(tablename = self.tb_name , key = key , val = val))

		if commit:
			self.connection.commit()

	def ensure(self , key , val , commit = True):
		'''如果某个key不存在，则将其设为val'''

		self.cursor.execute("""
			INSERT OR IGNORE INTO {tablename}
			VALUES ('{key}',{val}); 
		""".format(tablename = self.tb_name , key = key , val = val))

		if commit:
			self.connection.commit()

	def plus(self , key , val , commit = True):
		'''将key对应的值加val，并返回加之后的值。需要用户确保其存在'''

		#先update
		self.cursor.execute("""
			UPDATE {tablename}
			SET val = val + {val}
			WHERE key = '{key}';
		""".format(tablename = self.tb_name , key = key , val = val))

		ret_val = self.get(key) #在commit前查询，防止被其他线程修改

		if commit:
			self.connection.commit()

		return ret_val

	def commit(self):
		self.connection.commit()


class DoubleHash(StaticHash):
	'''双向哈希，key和val都是unique的'''

	def __init__(self , db_name , tb_name = "DoubleHash" ,  keysize = 255):
		super().__init__(db_name , tb_name , keysize)

	def init(self):
		'''初始化表'''
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS {tablename}
			(
				key varchar({keysize}) PRIMARY KEY, 
				val int NOT NULL UNIQUE 
			);
		""".format(tablename = self.tb_name, keysize = self.keysize))
		self.connection.commit()

	def ask_val(self , key):
		return self.get(key)

	def ask_key(self , val):
		'''查询某个val对应的key的的值，没有则返回None'''
		ret = self.cursor.execute("""
			SELECT key
			FROM {tablename}
			WHERE val = {val};
		""".format(tablename = self.tb_name , val = val)).fetchall()

		if len(ret) == 0:
			return None

		return ret[0][0]

	def ask(self , key = None, val = None):
		if key is not None:
			return self.ask_val(key)
		if val is None:
			return None
		return self.ask_key(val)


class HighDimHash(StaticHash):
	'''高维哈希，前m维是键，后n维是值'''

	def __init__(self , db_name , tb_name = "HighDimHash", keydim = 2 , valdim = 1 , always_tuple = False):
		'''
			keydim：键空间的维度
			valdim：值空间的维度
			always_tuple：如果为False，则在只有值只有一个元素时返回值而不是元组。默认False
		'''


		self.always_tuple = always_tuple

		self.keydim = keydim
		self.valdim = valdim

		self.key_list = ["key_{idx}".format(idx = i) for i in range(self.keydim)]
		self.val_list = ["val_{idx}".format(idx = i) for i in range(self.valdim)]

		super().__init__(db_name , tb_name , keysize = None)

	def name_value_list(self , namelist , vallist , sep = ","):
		'''将一系列名和一系列值转化为像『a=xx,b=xx』这样的字符串'''
		return sep.join( ["%s=%d" % (nam,val) for nam,val in zip(namelist , vallist)] )

	def init(self):
		'''初始化表'''
		self.cursor.execute('''
			CREATE TABLE IF NOT EXISTS {tablename}
			(
				{keys},
				{vals},
				PRIMARY KEY({primary_keys})
			);
		'''.format(tablename = self.tb_name, 
			keys = ",\n".join( ["%s int" % x for x in self.key_list] ) , 
			vals = ",\n".join( ["%s int" % x for x in self.val_list] ) , 
			primary_keys = ",".join(self.key_list), 
		))
		self.connection.commit()

	def get(self , keys):
		'''
			注意此处keys应是m维列表
			查询某个keys的值，没有则返回None
		'''

		keys , _ = self.check_kv(keys)

		if len(keys) != self.keydim:
			raise ArgumentError("get" , "len(keys)" , len(keys) , 
				class_name = "HighDimHash" , note_str = "key dim invalid")

		ret = self.cursor.execute("""
			SELECT {vals}
			FROM {tablename}
			WHERE {key_list};
		""".format(tablename = self.tb_name , 
			vals 	 = ",".join(self.val_list) ,
			key_list = self.name_value_list(self.key_list , keys , sep = " AND ") , 
		)).fetchall()

		if len(ret) == 0:
			return None

		if self.valdim == 1 and not self.always_tuple:
			return ret[0][0] # 返回唯一的一个值
		return ret[0] #返回元组

	def get_partial(self , keys):
		'''
			注意此处keys应是m维列表
			此处keys中的某些维度允许是None，表示查询这一维度任意的结果。
			返回一个列表表示所有的结果，列表元素是(keys , vals)
		'''

		keys , _ = self.check_kv(keys)

		if len(keys) != self.keydim:
			raise ArgumentError("get_partial" , "len(keys)" , len(keys) , 
				class_name = "HighDimHash" , note_str = "key dim invalid")

		ret = self.cursor.execute("""
			SELECT {keys} , {vals}
			FROM {tablename}
			WHERE {key_list};
		""".format(tablename = self.tb_name , 
			vals = ",".join(self.val_list) ,
			keys = ",".join(self.key_list) ,
			key_list = " AND ".join( ["%s=%d" % (nam,val) for nam,val in zip(self.key_list , keys) if val is not None] )
		)).fetchall()

		ret = [ [ x[:self.keydim] , x[self.keydim:] ] for x in ret] # 把keys分为一组，vals分为一组

		return ret #返回元组

	def check_kv(self , keys , vals = None):
		if len(keys) != self.keydim:
			raise RuntimeError("key dim invalid")


		if vals is not None:
			if self.valdim == 1 and not isinstance(vals , Iterable):
				vals = [vals] 

			if len(vals) != self.valdim:
				raise ArgumentError("check_kv" , "len(keys)" , len(keys) , 
					class_name = "HighDimHash" , note_str = "key dim invalid")

		return keys , vals

	def set(self , keys , vals , commit = True):
		'''将某个key设为val'''
		keys , vals = self.check_kv(keys , vals)

		self.cursor.execute("""
			INSERT OR REPLACE INTO {tablename}
			VALUES ({keys},{vals}); 
		""".format(tablename = self.tb_name , 
			keys = ",".join([str(x) for x in keys]) , 
			vals = ",".join([str(x) for x in vals]) , 
		))

		if commit:
			self.connection.commit()

	def ensure(self , keys , vals , commit = True):
		'''如果某个key不存在，则将其设为val'''
		keys , vals = self.check_kv(keys , vals)

		self.cursor.execute("""
			INSERT OR IGNORE INTO {tablename}
			VALUES ({keys},{vals}); 
		""".format(tablename = self.tb_name , 			
			keys = ",".join([str(x) for x in keys]) , 
			vals = ",".join([str(x) for x in vals]) , 
		))

		if commit:
			self.connection.commit()

	def plus(self , keys , vals , commit = True):
		'''将key对应的值加val，并返回加之后的值。需要用户确保其存在'''
		
		if self.valdim != 1:
			raise YAttributeError("plus" , "valdim" , self.valdim , 
				class_name = "HighDimHash" , note_str = "Highdim Table can only plus when valdim == 1")

			raise RuntimeError("HIghdim Table can only plus when valdim == 1")

		keys , vals = self.check_kv(keys , vals)
		val = vals[0]

		#先update
		self.cursor.execute("""
			UPDATE {tablename}
			SET {val_name} = {val_name} + {val}
			WHERE {key_list};
		""".format(tablename = self.tb_name , val_name = self.val_list[0] , val = val , 
			key_list = self.name_value_list(self.key_list , keys , sep = " AND ") 
		))

		ret_val = self.get(keys) #在commit前查询，防止被其他线程修改

		if commit:
			self.connection.commit()

		return ret_val


class StaticBlob(StaticHash):

	def __init__(self , db_name , tb_name = "BlobHash" , keysize = 255):
		super().__init__(db_name , tb_name , keysize)

	def close(self):
		if self.closed: #防止反复关闭
			return
		self.closed = True

		self.cursor.close()
		self.connection.close()

	def init(self):
		'''初始化表'''
		self.cursor.execute("""
			CREATE TABLE IF NOT EXISTS {tablename}
			(
				key varchar({keysize}) PRIMARY KEY, 
				val blob
			);
		""".format(tablename = self.tb_name, keysize = self.keysize))
		self.connection.commit()

	def get(self , key):
		'''查询某个key的值，没有则返回None'''

		ret = self.cursor.execute("""
			SELECT val
			FROM {tablename}
			WHERE key = '{key}';
		""".format(tablename = self.tb_name , key = key)).fetchall()

		if len(ret) == 0:
			return None

		return pickle.loads(ret[0][0])

	def set(self , key , val , commit = True):
		'''将某个key设为val'''

		#insert或replace
		self.cursor.execute("""
			INSERT OR REPLACE INTO {tablename}
			VALUES ('{key}',?);
		""".format(tablename = self.tb_name , key = key) , [sqlite3.Binary(pickle.dumps(val))])

		if commit:
			self.connection.commit()

	def ensure(self , key , val , commit = True):
		'''如果某个key不存在，则将其设为val'''

		self.cursor.execute("""
			INSERT OR IGNORE INTO {tablename}
			VALUES ('{key}',?); 
		""".format(tablename = self.tb_name , key = key) , [sqlite3.Binary(pickle.dumps(val))])

		if commit:
			self.connection.commit()


	def commit(self):
		self.connection.commit()
