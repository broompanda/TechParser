__author__ = 'upasana'
import datetime
import DB_Utility as db


class Counters(object):
	def __init__(self, counters, path2):
		'''
		Get the output of relevant counters and show clock.
		Keep these variables as a list
		'''
		self.counters = counters
		self.showclock = self.getclock(path2)
		self.dict = {}
		cnt_Jericho_db = db.get_from_db("SELECT counter_name, counter_desc FROM jericho_counters")
		cnt_Arad_db = db.get_from_db("SELECT counter_name, counter_desc FROM arad_counters")
		cnt_Jericho = {counter_name:counter_desc for counter_name, counter_desc in cnt_Jericho_db }
		cnt_Arad = {counter_name:counter_desc for counter_name, counter_desc in cnt_Arad_db }



	def getcounters(self):
		'''
		Convert relevant counters into dist
		'''
		header = None
		for line in self.counters:
			if "(* indicates overflow)" in line:
				header = line.split('Counters (* indicates overflow)')[0]
				if header not in self.dict:
					self.dict[header] = []

			elif header:
				self.dict[header].append(line.strip().split(':'))



	def getclock(self, path2):
		with open(path2, 'r') as fileobj2:
			return datetime.datetime.strptime(fileobj2.readlines()[4].rstrip(), "%a %b %d %H:%M:%S %Y")

	def compare_counters(self):
		'''
		Check for increments in a week
		'''
		#print self.dict
		for key in self.dict :
			for i in range(0,len(self.dict[key])-1):
				first_heard = datetime.datetime.strptime((self.dict[key][i][2]+self.dict[key][i][3]+self.dict[key][i][4]).strip(), "%Y-%m-%d %H%M%S")
				last_heard = datetime.datetime.strptime((self.dict[key][i][5]+self.dict[key][i][6]+self.dict[key][i][7]).strip(), "%Y-%m-%d %H%M%S")

				if (((self.showclock - first_heard).days < 7) or ((self.showclock - last_heard)).days < 7):
					pass
				else:
					pass
					self.dict[key][i] = 'remove'


		for key in self.dict:
			'''
			Remove unwanted counters
			'''
			for i in range(self.dict[key].count("remove")):
				self.dict[key].remove("remove")

		for key in self.dict:
			print "\n" + key
			for i in range(0,len(self.dict[key])-1):
					print ':'.join(self.dict[key][i])

	def get_counters2(self):
		self.dict = {}
		header = None
		for line in self.counters:
			if "(* indicates overflow)" in line:
				header = line.split('Counters (* indicates overflow)')[0]
				header = header.strip()
				if header not in self.dict:
					self.dict[header] = {}

			elif header:
				elements_nostrip = (line.strip()).split(':')
				elements = [element.strip() for element in elements_nostrip]
				counter_name =elements[0]
				self.dict[header][counter_name]={}
				self.dict[header][counter_name]['count'] = elements[1]
				self.dict[header][counter_name]['start_time'] = datetime.datetime.strptime(elements[2]+elements[3]+elements[4], "%Y-%m-%d %H%M%S")
				self.dict[header][counter_name]['last_time'] = datetime.datetime.strptime(elements[5]+elements[6]+elements[7], "%Y-%m-%d %H%M%S")


	def compare_counters2(self):
			'''
			Check for increments in a week
			'''

			filtered_errors = {}
			filtered_counters = {}
			for chip in self.dict :
				filtered_counters[chip] = {}

				for counter in self.dict[chip]:
					if ((((self.showclock - self.dict[chip][counter]['start_time'])).days < 7) or ((self.showclock - self.dict[chip][counter]['last_time'])).days < 7):
						filtered_counters[chip][counter] = self.dict[chip][counter]
						chip_dict= {}
						chip_dict[chip]=self.dict[chip][counter]
						if filtered_errors.get(counter,0) == 0:

							filtered_errors[counter] = [chip_dict]
						else:
							filtered_errors[counter].append(chip_dict)


			print "Below are the counters of interest from the last 7 days"
			for counter in filtered_errors:
				desc_string = ""
				print "\n============================================================================="
				print "Counter name: " +str(counter)
				print "============================================================================="
				print "This counter is seen in the following chip/s on the switch"
				for chip in filtered_errors[counter] :
					print chip.keys()[0] +" occurred " + chip[chip.keys()[0]]['count'] + " time/s"


				if 'Jericho' in filtered_errors[counter][0].keys()[0]:
					desc_string = cnt_Jericho[counter]
				elif 'Arad' in filtered_errors[counter][0].keys()[0]:
					desc_string = cnt_Arad[counter]
				else :
					print "Unrecognized chip" + str()
				print "This counter indicates " + str(desc_string)






def main(counters):
	checkCounters(counters)

def checkCounters(counters, clock_output):
	to_parse = Counters(counters, clock_output)
	to_parse.getcounters()
	to_parse.compare_counters()
	to_parse.get_counters2()
	to_parse.compare_counters2()



counters = {}

if __name__ == '__main__':
	main(counters)







