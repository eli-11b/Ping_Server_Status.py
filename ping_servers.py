import subprocess
import csv
def ping(hostname):
	p=subprocess.Popen('ping ' + hostname, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

	pingStatus = 'ok';

	for line in p.stdout:
		output = line.rstrip().decode('UTF-8')

		if (output.endswith('unreachable.')):
			#no route from the local system. Packets sent were never put on the wire.
			pingStatus = "unreachable"

		elif (output.startswith('Ping request could not find host')):
			pingStatus = 'host_not_found'
			break
		if(output.startswith('Request timed out.')):
			#No Echo Reply messages were received within the default time of 1 second
			pingStatus = 'timed_out'
			break
		return	pingStatus

def printPingResult(hostname):
	statusofPing = ping(hostname)

	if (statusofPing == 'host_not_found'):
		writeToFile('!server-not-found.txt', hostname)
	elif(statusofPing == 'unreachable'):
		writeToFile('!unreachable.txt',hostname)
	elif(statusofPing == 'timed_out'):
		writeToFile('!timed_out.txt',hostname)
	elif(statusofPing == 'ok'):
		writeToFile('!ok.txt', hostname)


def writeToFile(filename, data):
	with open(filename, 'a') as output:
		output.write(data + '\n')


file = open('servers.txt')

try:
	reader = csv.reader(file)

	for item in reader:
		printPingResult(item[0].strip())

finally:
	file.close()

