#!/usr/share/python

#   This python module has been create to generate a m3u8 playlist from local path
#   Copyright (C) 2016  by Mohamed Abdeljelil <abdeljelil.mohamed@gmail.com>
# 
# This script able to find all video in path and its sub foldes and generate a new 
# palylist and it's able to sort the video by creation date, modition date
# last access date and size

import os

# at the end of this script you'll find 
# a exmple for each  type of sort
SORT_BY_CREATION_DATE     = 9 # sort by creation date
SORT_BY_MODIFICATION_DATE = 8 # sort by modification date
SORT_BY_LAST_ACCESS_DATE  = 7 # sort by last access date
SORT_BY_SIZE    = 6 # sort by size

class VideoSeeker(object):
	"""
	Looking for the videos with the defined extensions 
	under the path_root given in the constructor and his sub foldres
	Expample :

		# the path_root is required to instance new object
		vs = VideoSeeker("/media/video")

		# the result is the list of all paths and sub paths contain videos 
		# with the extensions defined in the variable 'EXTENSIONS'
		files = vs.get_videos()	

	"""

	#list of extensions to 
	EXTENSIONS =[
	"webm","mkv","flv","vob","ogv","ogg","drc",'gifv',
	"mng","avi","mov", "qt","wmv","rm","rmvb","asf","mp4", "m4p" , 
	"m4v","mpg", "mp2","mpeg","mpe","mpv","m2v","3gp","3g2","mxf",
	"roq","nsv" ,"f4v" ,"f4p" ,"f4a" ,"f4b"
	]

	def __init__(self,path_root):

		self.path_root = path_root

	def __seeking_file_in_dir(self,path):

		elements  = os.listdir(path)

		files = []
		for element in elements :
			element_path  = os.path.join(path,element)
			if os.path.isfile(element_path) :
				if "." in element :
					extension = element.split(".")[-1]
					if extension in self.EXTENSIONS :
						files.append(element_path)
			else :
				files += self.__seeking_file_in_dir(element_path)
				 
		return files

	def get_videos(self):
		"""
		use it to find all videos with the given root path
		"""

		return self.__seeking_file_in_dir(self.path_root)

class Segment(object):
	"""
	the model of segment in m3u8 file, the attributes in segment are :
	Title : the name of video, in this example we are putting the file name
	Duration : the duration of video (not implemented)
	Uri : the path to video in local
	"""
	def __init__(self,file_path):

		self.file_path = file_path

	def get_title(self):
		"""
		Title of video, in this example we return the name of file
		"""
		base_path,file_name = os.path.split(self.file_path)

		return file_name

	def get_duration(self):
		"""
		TODO: duration not implemented to keep this script simple as possible 
			and to avoid using an extenal package, if you want to add this functionlaty 
			you have to install ffprobe and parse the output with json format.
			Expample of ffprobe command line : 
			ffprobe -v quiet -print_format json -show_format -show_streams <your file>
		Note : ffprobe is integrated in ffmpeg tools.
		"""
		return 20

	def get_uri(self):
		"""
		file path
		"""
		return self.file_path

	def __str__(self):	
		"""
		convert the segment attributes to m3u8 segment info block 
		Example of m3u8 segment block :
		#EXTINF:300,my sample video
		/home/videos/sample/myvideo.mp4
		"""

		title    = self.get_title()
		duration = self.get_duration()
		uri      = self.get_uri()

		return "#EXTINF:{},\"{}\"\n{}".format(duration,title,uri)

class PlayListGenerator(object):

	"""
	create a play list by the list of video given in the constructor
	files paramter is required to create new object of this class

	Example :

	# files : is the list of paths gotten by the class VideoSeeker
	# sort type : is an optinal field default is sort by creation date 
	# for sort type your pick one of sort types defined above
	plg = PlayListGenerator(files,SORT_BY_LAST_ACCESS_DATE)

	# dump the content of m3u8 file in file to run in vlc or any video player 
	# support m3u8 format
	plg.dump("/tmp/plylist_access.m3u8")

	"""

	def __init__(self,files,sort_type=SORT_BY_CREATION_DATE):

		#assert that the files is an list type 
		assert type(files) == list
		#assert that the sort type is an int type
		assert type(sort_type) == int

		self.files     = files
		self.sort_type = sort_type
 	
 	def __sort_files(self):

 		nested_dict = []

 		for file_path in self.files :
 			info = os.stat(file_path)
 			nested_dict.append({"key":info[self.sort_type],"path":file_path})
 
		sorted_list =  sorted(nested_dict, key=lambda x: x["key"], reverse=True)

		return [e["path"] for e in sorted_list ]
 

 	def dumps(self):

 		"""

 		create an m3u8 format with the segments created from the video files
 		and return string 
 		"""

 		full_content = "#EXTM3U\n"
 		full_content += "#EXT-X-PLAYLIST-TYPE:VOD\n"
 		full_content += "#EXT-X-TARGETDURATION:10\n"
 		full_content += "#EXT-X-VERSION:3\n"
 		full_content += "#EXT-X-MEDIA-SEQUENCE:0\n"

 		sorted_files = self.__sort_files()

		for file_path in sorted_files :
			segment = Segment(file_path)
			full_content += str(segment)
			full_content += "\n"

 		full_content += "#EXT-X-ENDLIST"
 		
 		return full_content

 	def dump(self,file_name):

 		"""
 		write the content of m3u8 format in file
 		"""

 		full_content=self.dumps()

 		with open(file_name,"w") as wfile :

 			wfile.write(full_content)

if __name__ == '__main__':

	#seeking for video content
	vs = VideoSeeker("/media/video")
	files = vs.get_videos()

	# create  a playlist sorted by size
	plg = PlayListGenerator(files,SORT_BY_SIZE)
	plg.dump("/tmp/plylist_size.m3u8")

	# create a playlist sorted by creation date
	plg = PlayListGenerator(files,SORT_BY_CREATION_DATE)
	plg.dump("/tmp/plylist_creation.m3u8")

	# create a playlist sorted by modification date
	plg = PlayListGenerator(files,SORT_BY_MODIFICATION_DATE)
	plg.dump("/tmp/plylist_modification.m3u8")

	# create a play list by last access date
	plg = PlayListGenerator(files,SORT_BY_LAST_ACCESS_DATE)
	plg.dump("/tmp/plylist_access.m3u8")
 
