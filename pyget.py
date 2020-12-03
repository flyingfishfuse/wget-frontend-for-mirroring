#!/usr/bin/python3
# -*- coding: utf-8 -*-
################################################################################
##   Page Mirroring script utilizing python/Wget in a unix-like environment   ##
################################################################################
# Copyright (c) 2020 Adam Galindo                                             ##
#                                                                             ##
# Permission is hereby granted, free of charge, to any person obtaining a copy##
# of this software and associated documentation files (the "Software"),to deal##
# in the Software without restriction, including without limitation the rights##
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell   ##
# copies of the Software, and to permit persons to whom the Software is       ##
# furnished to do so, subject to the following conditions:                    ##
#                                                                             ##
# Licenced under GPLv3                                                        ##
# https://www.gnu.org/licenses/gpl-3.0.en.html                                ##
#                                                                             ##
# The above copyright notice and this permission notice shall be included in  ##
# all copies or substantial portions of the Software.                         ##
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.
################################################################################
import os
import sys
import argparse
import requests
import subprocess

########################################
# Imports for logging and colorization #
########################################

import logging 
try:
	import colorama
	from colorama import init
	init()
	from colorama import Fore, Back, Style
	COLORMEQUALIFIED = True
except ImportError as derp:
	print("[-] NO COLOR PRINTING FUNCTIONS AVAILABLE, Install the Colorama Package from pip")
	COLORMEQUALIFIED = False
    
##########################
# Colorization Functions #
##########################
# yeah, about the slashes... do you want invisible \n? 
# Because thats how you avoid invisible \n and concatenation errors
blueprint 			= lambda text: print(Fore.BLUE + ' ' +  text + ' ' + \
	Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
greenprint 			= lambda text: print(Fore.GREEN + ' ' +  text + ' ' + \
	Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
redprint 			= lambda text: print(Fore.RED + ' ' +  text + ' ' + \
	Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)
# inline colorization for lambdas in a lambda
makered				= lambda text: Fore.RED + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makegreen  			= lambda text: Fore.GREEN + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeblue  			= lambda text: Fore.BLUE + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
makeyellow 			= lambda text: Fore.YELLOW + ' ' +  text + ' ' + \
	Style.RESET_ALL if (COLORMEQUALIFIED == True) else None
yellow_bold_print 	= lambda text: print(Fore.YELLOW + Style.BRIGHT + \
	' {} '.format(text) + Style.RESET_ALL) if (COLORMEQUALIFIED == True) else print(text)

###########
# LOGGING #
###########
log_file = '/tmp/logtest'
logging.basicConfig(filename=log_file, format='%(asctime)s %(message)s', filemode='w')
logger		   		= logging.getLogger()
logger.setLevel(logging.DEBUG)
debug_message		= lambda message: logger.debug(blueprint(message)) 
info_message		= lambda message: logger.info(greenprint(message)) 
warning_message 	= lambda message: logger.warning(yellow_bold_print(message)) 
error_message		= lambda message: logger.error(redprint(message)) 
critical_message 	= lambda message: logger.critical(yellow_bold_print(message))

parser = argparse.ArgumentParser(description='page mirroring tool utilizing wget via python scripting')
parser.add_argument('--target',
                                 dest    = 'target',
                                 action  = "store" ,
                                 default = "127.0.0.1" ,
                                 help    = "Website to mirror" )
parser.add_argument('--user-agent',
                                 dest    = 'useragent',
                                 action  = "store" ,
                                 default = 'Mozilla/5.0 (X11; Linux x86_64; rv:28.0) Gecko/20100101  Firefox/28.0' ,
                                 help    = "User agent to bypass crappy limitations" )
parser.add_argument('--directory_prefix',
                                 dest    = 'directory_prefix',
                                 action  = "store" ,
                                 default = './website_mirrors/' ,
                                 help    = "Storage directory to place the downloaded files in, defaults to script working directory" )
#parse arguments from commandline / ARGV[]
arguments         = parser.parse_args()

class GetPage():
    """
    Class that performs the page mirroring, creating a subdirectory with all relevant files
    for display in a browser of your choice
    User agent might need tweaking, defaults to firefox on linux
	
	"""
    def __init__(self):
        self.request_headers    = {'User-Agent' : arguments.useragent }
        self.storage_directory  = arguments.directory_prefix
        self.url_to_grab        = arguments.target
        #example of a command dict, follows pybashy spec
		self.wget_command  = {"wget" : ['wget -nd -H -np -k -p -E --directory-prefix={1}'.format(self.storage_directory),
                                        "[+] Fetching Webpage",
                                        "[+] Page Downloaded",
                                        "[-] Download Failure"]
                            }
    def grab(url):
        #subprocess.call(['wget', '-nd', '-H', '-np', '-k', '-p', '-E', '--directory-prefix={1}'.format(storage_directory), url])
        # instantiate threader if multiple pages given

        page_downloader = ExecutionPool(url)
        page_downloader.step(self.wget_command)

class DownloadPool():
	'''
	This is the download pool threading class for multiple website downloads
	
	Input : 
	    - Wget command
            programmed flags { -nd -H -np -k -p -E }
	    - URL 
		    Default {127.0.0.1}
	
	'''
	def __init__(self, website_to_download):
		# WORKJING ON RIGHT NOW!!!!!
		##################################
		# DO THIS TODAY/ISH!!!!!!!!!!!
		#list of urls to grab if provided a list
		# else, just grab the one
		if isinstance(website_to_download,list):
		    pool = []
		self.script_cwd		   	= Path().absolute()
		self.script_osdir	   	= Path(__file__).parent.absolute()
		self.website_to_grab    = website_to_download

	def step(self, wget_dict : dict):

		try:
			for instruction in wget_dict.values():
				cmd 	= instruction[0]
				info    = instruction[1]
				success = instruction[2]
				fail 	= instruction[3]
				yellow_bold_print(info)
				self.current_command = cmd
				#wget_cmd_exec = self.exec_command(self.current_command)
				wget_cmd_exec  = self.threader(self.exec_command(self.current_command),new_thread_name)
				if wget_cmd_exec.returncode == 0 :
					info_message(success)
				else:
					error_message(fail)
		except Exception as derp:
			return derp
			
	def error_exit(self, message : str, derp : Exception):
		error_message(message = message)
		print(derp.with_traceback)
		sys.exit()	


	def exec_command(self, command, blocking = True, shell_env = True):
		'''TODO: add formatting'''
		try:
			if blocking == True:
				step = subprocess.Popen(command,
										shell=shell_env,
				 						stdout=subprocess.PIPE,
				 						stderr=subprocess.PIPE)
				output, error = step.communicate()
				for output_line in output.decode().split('\n'):
					info_message(output_line)
				for error_lines in error.decode().split('\n'):
					critical_message(error_lines)
				return step
			elif blocking == False:
				# TODO: not implemented yet
				pass
		except Exception as derp:
			yellow_bold_print("[-] Shell Command failed!")
			return derp
		#read, write = os.pipe()
#		step = subprocess.Popen(something_to_set_env, 
#						shell=shell_env, 
#						stdin=read, 
#						stdout=sys.stdout, 
#						stderr=subprocess.PIPE)
#		Note that this is limited to sending a maximum of 64kB at a time,
# 		pretty much an interactive session
#		byteswritten = os.write(write, str(command))
	
	def threader(self, thread_function, name):
		info_message("Thread {}: starting".format(name))
		thread = threading.Thread(target=thread_function, args=(1,))
		thread.start()
		info_message("Thread {}: finishing".format(name))

    def move_shell(self, directory = sys.argv[0]):
        #change shell to script directory by default
        os.chdir(os.path.dirname(directory))

if __name__ == "__main__":
    getpage(target)
#    pagemirror(portalpage)
