import sys
import os
import time
import datetime


from PyQt4 import QtGui, QtCore
from PyQt4.QtCore import *
from PyQt4.QtGui import *

import xml.etree.ElementTree as ET 


def get_matching_messages(message_set, attrib, val):

	matches = []

	for message in message_set:
		if message.__dict__[attrib] == val:
			matches.append(message)

	return matches

class message_box:

	def __init__(self,dir_name):

		self.files = []

		for file in os.listdir("messages"):

			if (os.path.isfile("messages/"+file) and file.find(".xml")!=-1):

				print "Adding "+file+" to message_box..."
				cur_file = file_T()
				cur_file.add_threads("messages/"+file)
				self.files.append(cur_file)

		self.init_cli()

	def init_cli(self):

		print "\n\nMessage_box Message Navigation Tool Menu..."
		print "--> [0] for all sent messages."
		print "--> [1] for all messages sent to x."
		print "--> [9] Quit."

		resp = input("<-- Enter choice: ")

		if resp == 9:
			return

		if resp == 0:
			self.all_sent()

		if resp == 1:
			self.all_to_x()

		self.init_cli()

	def get_all_by_attrib(self, attrib, val):

		matches = []

		for file in self.files:

			for thread in file.threads:

				for message in thread.messages:

					if message.__dict__[attrib] == val:
						matches.append(message)

		return matches


	def all_sent(self):

		msgs = self.get_all_by_attrib('msg_iden', "2")

		for message in msgs:

			message.print_message()

	def all_to_x(self):

		num = input("\t--> Enter the recipient (xxxxxxxxxx): ")

		msgs = self.get_all_by_attrib('msg_iden', "2")

		msgs = get_matching_messages(msgs, 'address', "9085816308")

		for message in msgs:

			message.print_message()



class file_T:

	def __init__(self):

		self.threads = []

	def add_threads(self, filename):

		tree = ET.parse(filename)
		file_src = tree.getroot()

		for thread in file_src:
			thrd = thread_T()
			thrd.add_messages(thread)
			self.threads.append(thrd)

class thread_T:

	def __init__(self):

		self.number = -1
		self.messages = []

	def add_messages(self, thread_src):

		thread_tag = thread_src.tag
		thread_num = thread_src.attrib

		for message in thread_src:

			msg = message_T()
			msg.set_values(message, thread_num)
			self.messages.append(msg)


class message_T:

	def __init__(self):

		self.parent_thread = None

	def set_values(self, msg_src, thread_num):

		self.parent_thread = thread_num

		self.address 	= msg_src.find('address').text
		self.body		= msg_src.find('body').text
		self.date		= msg_src.find('date').text
		self.read 		= msg_src.find('read').text
		self.msg_iden 	= msg_src.find('type').text
		self.locked 	= msg_src.find('locked').text

	def print_message(self,tab_inc=1):

		tab_str = ""

		for _ in range(tab_inc):
			tab_str += "\t"

		tab_str+= "--> "

		print "\n"
		print tab_str+"To: "+self.address
		print tab_str+"Body: "+self.body
		print tab_str+"Date: "+datetime.datetime.fromtimestamp(int(self.date)/1000).strftime('%Y-%m-%d %H:%M:%S')


def main():

	test = message_box("messages")


if __name__ == '__main__':
	main()


