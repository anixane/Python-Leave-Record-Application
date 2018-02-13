from easygui import *
import MySQLdb

title='LEAVE RECORD'
try:
	p=MySQLdb.connect('localhost','root','dbms123','TLEAVE')  #connecting to the database
	cur=p.cursor()    
except:
	p=MySQLdb.connect('localhost','root','dbms123')
	cur=p.cursor() 
	msgbox('Database has not yet been created',title)  #message in case of failure in establishing connection

res=''
##########################################################################################################################################
#code for the status
def status():
	tid = ''
	try:
		while tid=='':
			tid = enterbox('Enter ID',title)
		query1 = 'SELECT * FROM OLEAVE WHERE TID ='+`tid`	#here we are using stored procedures, storing the entire query in one string and using it over again and again
		query2 = 'SELECT * FROM PLEAVE WHERE TID ='+`tid`
		try:
			cur.execute(query1)  #executing stored procedures
			rows = cur.fetchall()

			res = 'Official Leaves\n\t\t\tTID\t\t\tDate\t\t\tType of Leave\t\t\tLocation\n\n'
			for row in rows:
				for eachVal in row:
					res += '\t\t\t'+str(eachVal)
				res += '\n'
			res += '\n'
		
		except:
			print '',

		try:
			cur.execute(query2)
			rows = cur.fetchall()
			res += 'Personal Leaves\n\t\t\tTID\t\t\tDate\t\t\tParticular\t\t\tReason\n\n'
			
			for row in rows:
				for eachVal in row:
					res += '\t\t\t'+str(eachVal)
				res += '\n'
			textbox('I found this information',title,res)
			res = ''
			if len(rows) == 0:
				msgbox('Invalid ID Or No leave taken',title)
				return
		except:
			print '',
	except:
		print '',
p.commit()
###################################################################################################
def entry():
	try:
		global title,cur,res
		check = 'Please enter leave details:'
		detailList = ["Username","Password"]
		feildValues = multpasswordbox("LOGIN",title,detailList)
		query1 = 'SELECT * FROM TEACHER WHERE USERNAME='+`feildValues[0]`+' AND PASSWORD='+`feildValues[1]`
		print query1
		try:
			cur.execute(query1)
			queryResult = cur.fetchone()
			if queryResult == None:
				msgbox('Invalid username or password, TRY AGAIN',title)
			else:
				tid = queryResult[0]
				choices = ['Official Leave','Personal leave']
				choice = indexbox('Login successful for '+tid,title,choices)
				if choice == 0:
					entryFeilds = ['Date(YYYY-MM-DD)','Particlar','Location']
					while True:
						obtainedValues = multenterbox(check,title,entryFeilds)
						if obtainedValues == None:
							if ynbox('Press Yes to enter information or No to cancel',title):
								continue
							else:
								return
						flag = 0
						check = ''
						for i in range(len(obtainedValues)):
							if obtainedValues[i] == '':
								check += entryFeilds[i]+' is a required feild\n\n'
								flag = 1
						if flag == 1:
							continue
						else:
							break
					try:
						cur.execute('INSERT INTO OLEAVE(TID,ODATE,PARTICULAR,LOC) VALUES(%s,%s,%s,%s)',(tid,obtainedValues[0],obtainedValues[1],obtainedValues[2]))
					except:
						msgbox('Improper entries detected',title)
			
				if choice == 1:
					entryFeilds = ['Date(YYYY-MM-DD)','Type of Leave','Reason']
					while True:
						obtainedValues = multenterbox(check,title,entryFeilds)
						if obtainedValues == None:
							if ynbox('Press Yes to enter information or No to cancel',title):
								continue
							else:
								return
						flag = 0
						check = ''
						for i in range(len(obtainedValues)):
							if obtainedValues[i] == '':
								check += entryFeilds[i]+' is a required feild\n\n'
								flag = 1
						if flag == 1:
							continue
						else:
							break
					try:
						cur.execute('INSERT INTO PLEAVE(TID,PDATE,LTYPE,REASON) VALUES(%s,%s,%s,%s)',(tid,obtainedValues[0],obtainedValues[1],obtainedValues[2]))
					except:
						msgbox('Improper entries detected',title)


		except:
			exceptionbox()
	except:
		print '',	
p.commit()
####################################################################################################################
def ADMIN():
	try:
		global title,cur,res
		if(passwordbox('Enter your password','Authentication')=='dhanya'):
			choices = ['Enter your own query','Create user','Exit','Recreate Database']
			choice = indexbox("Choose",title,choices)
			if choice == 0:
				query = enterbox('Enter your Query',title)
				try:
					cur.execute(query)
					rows = cur.fetchall()
					for row in rows:
						for eachVal in row:
							res += '\t\t'+str(eachVal)
						res += '\n'
					textbox('I found this information',title,res)
					res = ''
			
				except:
					msgbox('Improper query detected')
			elif choice == 1:
				entryFeilds = ['ID','Name','Designation','dept','Username','Password']
				check = 'Enter information'
				while True:
					obtainedValues = multpasswordbox(check,title,entryFeilds)
					if obtainedValues == None:
						if ynbox('Press Yes to enter information or No to cancel',title):
							continue
						else:
							return
					check = ''
					flag = 0
					for i in range(len(obtainedValues)):
						if obtainedValues[i] == '':
							check += entryFeilds[i]+' is a required feild\n\n'
							flag = 1
					if flag == 1:
						continue
					else:
						break
				try:
					cur.execute('INSERT INTO TEACHER (TID,NAME,DESG,DEPT,USERNAME,PASSWORD) VALUES(%s,%s,%s,%s,%s,%s)', (obtainedValues[0],obtainedValues[1],obtainedValues[2],obtainedValues[3],obtainedValues[4],obtainedValues[5]))
				except:
					exceptionbox()
			
			elif choice == 3:
				if(ynbox('Are You Sure You Want to recreate the database','Caution')):
					if(ccbox("I HEREBY CONFIRM THAT I'M RESPONSIBLE FOR DATABASE DELETION",'CAUTION')):
						try:
							cur.execute('DROP DATABASE IF EXISTS TLEAVE')
							cur.execute('CREATE DATABASE TLEAVE')
							p=MySQLdb.connect('localhost','root','dbms123','TLEAVE')
							cur=p.cursor()
#here we are using triggers, on entering password, the program creates in the database itself.
							cur.execute('CREATE TABLE TEACHER(TID VARCHAR(30) PRIMARY KEY,NAME VARCHAR(30) NOT NULL,DESG VARCHAR(30), DEPT VARCHAR(30) NOT NULL,USERNAME VARCHAR(30) UNIQUE, PASSWORD VARCHAR(30))')
							cur.execute('CREATE TABLE OLEAVE(TID VARCHAR(30) REFERENCES TEACHER(TID),ODATE DATE,PARTICULAR VARCHAR(256),LOC VARCHAR(256),PRIMARY KEY(TID,ODATE))')
							cur.execute('CREATE TABLE PLEAVE(TID VARCHAR(30) REFERENCES TEACHER(TID),PDATE DATE,LTYPE VARCHAR(256),REASON VARCHAR(256),PRIMARY KEY(TID,PDATE))')
						except:
							exceptionbox()					
					else:
						print '',
				else:
					print '',
		else:
			msgbox('Wrong Password')
	except:
		print '',	


while 1:
    msg='Hello! choose'
    choices=['Status','Entry','Admin','Exit']
    choice=indexbox(msg,title,choices)
    if choice==0:
        status()
    if choice==1:
        entry()
    if choice==2:
        ADMIN() 
    if choice==3:
       break
           
p.commit()
