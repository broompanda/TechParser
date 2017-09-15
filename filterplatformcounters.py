'''Checks for counters in Arad or Jericho or mixed mode system'''
import clockcomparison
import DB_Utility as db

class showTech(object):
	
	def __init__(self,fileName):
		self.fileName = fileName

	def getCounter(self,fileName):
		'''extracts counters for multiple chips and discards chips with no NZ counters of interest'''

		cnt_Jericho_db = db.get_from_db("SELECT counter_name  FROM jericho_counters")
		cnt_Arad_db = db.get_from_db("SELECT counter_name  FROM arad_counters")


		'''cnt_Jericho=["Egq Ehp Discard Packet Cnt","Egq Pqp Discard Mc Packet Cnt","Egq Pqp Discard Uc Packet Cnt",
		"Epe Discarded Packet Cnt","Deleted Credit Cnt","Ipt Deleted Big Latency Pkt Cnt","Deleted Pkt Cnt","Discarded Pkt Cnt",
		"Matched Packets Discarded in the Deq Process","Counts Matched Packets Discarded at Enq Pipe"]

		cnt_Arad = ["Ehp Discard Packet","Pqp Discard Multicast Packet","Epe Packet","Egq Pkt","Queue Total Discarded Packet",
		"Queue Deleted Packet"]
		'''
		cnt_Jericho = [counter[0] for counter  in cnt_Jericho_db]
		cnt_Arad = [counter[0] for counter  in cnt_Arad_db]


		with open(fileName) as f:
			content = f.readlines()
		content = [x.strip("\n") for x in content]
		content = [x.strip("\r") for x in content]
		cnt = []
		counters = []

		for i in content:
			if 'Arad' in i:
				print i
			if "(* indicates overflow)" in i:
				chip = i
				writeChip = 1
				if "Jericho" in i:
					cnt = cnt_Jericho
				else:
					cnt = cnt_Arad
			for x in cnt:        
				if  ((x in i)):
					if (writeChip):
						counters.append(chip)
						writeChip = 0
					counters.append(i)
		return counters

	def callNextModule(self,counters, clock_output):
		for i in counters:
			with open('blah.txt','a') as f:
				f.write(i)
				f.write('\n')

		clockcomparison.checkCounters(counters, clock_output)

def filter(fileName, clock_output):

	techObject = showTech(fileName)
	counters = techObject.getCounter(fileName)
	techObject.callNextModule(counters, clock_output)


def main():
	filter("test")

if __name__ == "__main__":
	main()

