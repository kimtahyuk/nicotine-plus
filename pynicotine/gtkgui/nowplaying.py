# Copyright (C) 2006 daelstorm <daelstorm@gmail.com>
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation; either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

import gtk, gobject
import os, commands, sys, re
from pynicotine.utils import _

class NowPlaying:
	def __init__(self, frame, create = True, accel_group = None):
		self.frame = frame
		if accel_group is None:
			self.accel_group = gtk.AccelGroup()
		else:
			self.accel_group = accel_group
		if create:
			self.NowPlaying = gtk.Window(gtk.WINDOW_TOPLEVEL)
			self.NowPlaying.set_title(_("NowPlaying"))
			self.NowPlaying.set_position(gtk.WIN_POS_NONE)
			self.NowPlaying.add_accel_group(self.accel_group)
			#self.NowPlaying.show()
			self.NowPlaying.connect("destroy", self.quit)
        		self.NowPlaying.connect("delete_event", self.quit)
	
		self.vbox1 = gtk.VBox(False, 5)
		self.vbox1.show()
		self.vbox1.set_spacing(5)
	
		self.label6 = gtk.Label(_("Display what your Media Player is playing in Chat with the /now command"))
		self.label6.set_alignment(0, 0.5)
		self.label6.set_padding(5, 3)
		self.label6.set_line_wrap(True)
		self.label6.show()
		self.vbox1.pack_start(self.label6, False, False, 0)
	
		self.hbox1 = gtk.HBox(False, 5)
		self.hbox1.show()
		self.hbox1.set_spacing(5)
		self.hbox1.set_border_width(3)
		
		self.label2 = gtk.Label(_(""))
	
		self.NP_infopipe = gtk.RadioButton()
		self.NP_infopipe.set_active(False)
		self.NP_infopipe.set_label(_("XMMS / Infopipe"))
		self.NP_infopipe.show()
		self.NP_infopipe.connect("clicked", self.OnNPPlayer)
	
		self.hbox1.pack_start(self.NP_infopipe, False, False, 0)
	
		self.NP_amarok = gtk.RadioButton(self.NP_infopipe)
		self.NP_amarok.set_active(False)
		self.NP_amarok.set_label(_("Amarok"))
		self.NP_amarok.show()
		self.NP_amarok.connect("clicked", self.OnNPPlayer)
	
		self.hbox1.pack_start(self.NP_amarok, False, False, 0)
	
		self.NP_mpd = gtk.RadioButton(self.NP_infopipe)
		self.NP_mpd.set_active(False)
		self.NP_mpd.set_label(_("MPD via mpc"))
		self.NP_mpd.show()
		self.NP_mpd.connect("clicked", self.OnNPPlayer)
	
		self.hbox1.pack_start(self.NP_mpd, False, False, 0)
	
		self.vbox1.pack_start(self.hbox1, False, True, 0)
	
		self.hbox2 = gtk.HBox(False, 5)
		self.hbox2.show()
		self.hbox2.set_spacing(5)
		self.hbox2.set_border_width(3)
	
		#self.NP_mp3blaster = gtk.RadioButton(self.NP_infopipe)
		#self.NP_mp3blaster.set_active(False)
		#self.NP_mp3blaster.set_label(_("MP3Blaster"))
		#self.NP_mp3blaster.show()
		#self.NP_mp3blaster.connect("clicked", self.OnNPPlayer)
		## mp3blaster disabled
		#self.NP_mp3blaster.set_sensitive(False)
	
		#self.hbox2.pack_start(self.NP_mp3blaster, False, False, 0)
	
		self.NP_bmpx = gtk.RadioButton(self.NP_infopipe)
		self.NP_bmpx.set_active(False)
		self.NP_bmpx.set_label(_("BMPx"))
		self.NP_bmpx.show()
		self.NP_bmpx.connect("clicked", self.OnNPPlayer)
	
		self.hbox2.pack_start(self.NP_bmpx, False, False, 0)
	
		self.NP_rhythmbox = gtk.RadioButton(self.NP_infopipe)
		self.NP_rhythmbox.set_active(False)
		self.NP_rhythmbox.set_label(_("Rhythmbox"))
		self.NP_rhythmbox.show()
		self.NP_rhythmbox.connect("clicked", self.OnNPPlayer)
		
	
		self.hbox2.pack_start(self.NP_rhythmbox, False, False, 0)
	
		self.NP_other = gtk.RadioButton(self.NP_infopipe)
		self.NP_other.set_active(False)
		self.NP_other.set_label(_("Other"))
		self.NP_other.show()
		self.NP_other.connect("clicked", self.OnNPPlayer)
	
		self.hbox2.pack_start(self.NP_other, False, False, 0)
	
		self.vbox1.pack_start(self.hbox2, False, True, 0)
	
		self.hbox5 = gtk.HBox(False, 5)
		self.hbox5.show()
		self.hbox5.set_spacing(5)
		self.hbox5.set_border_width(3)
	
		self.label5 = gtk.Label(_("Player Command:"))
		self.label5.set_padding(0, 0)
		self.label5.set_line_wrap(False)
		self.label5.show()
		self.hbox5.pack_start(self.label5, False, False, 0)
	
		self.NPCommand = gtk.Entry()
		self.NPCommand.set_text("")
		self.NPCommand.set_editable(True)
		self.NPCommand.show()
		self.NPCommand.set_visibility(True)
		self.hbox5.pack_start(self.NPCommand, True, True, 0)
	
		self.vbox1.pack_start(self.hbox5, False, False, 0)
	
		self.hbox4 = gtk.HBox(False, 5)
		self.hbox4.show()
		self.hbox4.set_spacing(5)
		self.hbox4.set_border_width(3)
	
		self.label3 = gtk.Label(_("Legend:"))
		self.label3.set_alignment(0, 0.5)
		self.label3.set_padding(5, 5)
		self.label3.set_line_wrap(False)
		self.label3.show()
		self.hbox4.pack_start(self.label3, False, False, 0)
	
		
		
		self.label2.set_alignment(0, 0.5)
		self.label2.set_padding(0, 0)
		self.label2.set_line_wrap(False)
		self.label2.show()
		self.hbox4.pack_start(self.label2, False, False, 0)
	
		self.vbox1.pack_start(self.hbox4, False, False, 0)
	
		self.label4 = gtk.Label(_("Now playing format:"))
		self.label4.set_alignment(0, 0.5)
		self.label4.set_padding(5, 5)
		self.label4.set_line_wrap(False)
		self.label4.show()
		self.vbox1.pack_start(self.label4, False, False, 0)
	
		self.NPFormat_List = gtk.ListStore(gobject.TYPE_STRING)
		self.NPFormat = gtk.ComboBoxEntry()
		self.NPFormat.show()
		self.defaultlist = [ "$n", "$a - $t", "[$a] $t", "Now $s: [$a] $t", "Now $s: $n", "$a - $b - $t", "$a - $b - $t ($l/$rKBps) from $y $c" ]
		if self.frame.np.config.sections["players"]["npformat"] != "":
			self.NPFormat.child.set_text(self.frame.np.config.sections["players"]["npformat"])
		if self.frame.np.config.sections["players"]["npformatlist"] != []:
			if self.frame.np.config.sections["players"]["npformat"] == "":
				self.NPFormat.child.set_text(self.frame.np.config.sections["players"]["npformatlist"][0])
			for item in self.frame.np.config.sections["players"]["npformatlist"]:
				self.NPFormat_List.append([item])
		if self.frame.np.config.sections["players"]["npformat"] == "":
			self.NPFormat.child.set_text(self.defaultlist[0])

		for item in self.defaultlist:
			self.NPFormat_List.append([item])
		

	
		self.NPFormat.set_model(self.NPFormat_List)
		self.NPFormat.set_text_column(0)
		self.NPFormat.child.connect("activate", self.OnAddFormat)
		self.vbox1.set_border_width(5)
		self.vbox1.pack_start(self.NPFormat, False, False, 0)
		
		self.hbox6 = gtk.HBox(False, 5)
		self.hbox6.show()
		self.hbox6.set_spacing(5)
		
		self.label6 = gtk.Label(_("Example:"))
		self.label6.set_alignment(0, 0.5)
		self.label6.set_padding(5, 5)
		self.label6.set_line_wrap(False)
		self.label6.show()
		
		self.label7 = gtk.Label(_(""))
		self.label7.set_alignment(0, 0.5)
		self.label7.set_padding(5, 5)
		self.label7.set_line_wrap(False)
		self.label7.show()
		self.hbox6.pack_start(self.label6, False, False, 0)
		self.hbox6.pack_start(self.label7, False, False, 0)
		self.vbox1.pack_start(self.hbox6, False, False, 0)
	
	
		self.hbox3 = gtk.HBox(False, 5)
		self.hbox3.show()
		self.hbox3.set_spacing(5)
	
		self.NPCancel = gtk.Button(None, gtk.STOCK_CANCEL)
		self.NPCancel.show()
		self.NPCancel.connect("clicked", self.OnNPCancel)
	
		self.hbox3.pack_end(self.NPCancel, False, False, 0)
	
		self.NPSave = gtk.Button(None, gtk.STOCK_SAVE)
		self.NPSave.show()
		self.NPSave.connect("clicked", self.OnNPSave)
	
		self.hbox3.pack_end(self.NPSave, False, False, 0)
		
		self.NPTest = gtk.Button()
		self.NPTest.show()
		self.NPTest.connect("clicked", self.OnNPTest)
		
		self.alignment16 = gtk.Alignment(0.5, 0.5, 0, 0)
		self.alignment16.show()
	
		self.hbox36 = gtk.HBox(False, 2)
		self.hbox36.show()
		self.hbox36.set_spacing(2)
	
		self.image16 = gtk.Image()
		self.image16.set_padding(0, 0)
		self.image16.set_from_stock(gtk.STOCK_JUMP_TO, 4)
		self.image16.show()
		self.hbox36.pack_start(self.image16, False, False, 0)
	
		self.label45 = gtk.Label(_("Test"))
		self.label45.set_padding(0, 0)
		self.label45.set_line_wrap(False)
		self.label45.show()
		self.hbox36.pack_start(self.label45, False, False, 0)
	
		self.alignment16.add(self.hbox36)
		self.NPTest.add(self.alignment16)
	
		self.hbox3.pack_end(self.NPTest, False, False, 0)
	
		self.vbox1.pack_start(self.hbox3, False, True, 0)
		self.title_clear()
		self.OnNPPlayer(None)
	
		if create:
			self.NowPlaying.add(self.vbox1)
		
		self.SetPlayer(self.frame.np.config.sections["players"]["npplayer"])
		
	def title_clear(self):
		self.label7.set_text("")
		self.title = { "title": "", "artist": "", "comment": "", "year": "", "album": "", "track":"", "length": "", "nowplaying": "", "status": "", "bitrate": "", "filename": ""}
		
	def SetPlayer(self, player):
		if player == "infopipe":
			self.NP_infopipe.set_active(1)
		elif player == "amarok":
			self.NP_amarok.set_active(1)
		elif player == "mpd":
			self.NP_mpd.set_active(1)
		#elif player == "mp3blaster":
		#	self.NP_mp3blaster.set_active(1)
		elif player == "rhythmbox":
			self.NP_rhythmbox.set_active(1)
		elif player == "bmpx":
			self.NP_bmpx.set_active(1)
		elif player == "other":
			self.NP_other.set_active(1)
			
	def OnAddFormat(self, widget):
		text = self.NPFormat.child.get_text().strip()
		if text.isspace() or text == "":
			return
		items = self.frame.np.config.sections["players"]["npformatlist"]
		if text in self.defaultlist:
			return
		if text in items:
			items.remove(text)
		items.insert(0, text)
		self.frame.np.config.sections["players"]["npformat"] = text
		del items[15:]
		self.frame.np.config.writeConfig()
		# Repopulate the combo list
		self.NPFormat.get_model().clear()
		templist = []
		for i in items:
			if i not in templist:
				templist.append(i)
		templist += self.defaultlist
		for i in templist:
			self.NPFormat.append_text(i)
			
	def OnNPPlayer(self, widget):
		set = 0 
		if self.NP_infopipe.get_active():
			self.label2.set_text(_("$n Now Playing\n$l Length\n$r Bitrate\n$s Status"))
			set = 1
		if self.NP_mpd.get_active():
			self.label2.set_text(_("$n Now Playing\n$t Title\n$a Artist\n$b Album\n$k Track Number\n$f Filename"))
			set = 1
		if self.NP_amarok.get_active():
			self.label2.set_text(_("$n Now Playing\n$l Length\n$r Bitrate\n$s Status\n$t Title\n$a Artist\n$b Album\n$c Comment\n$k Track Number\n$y Year\n$f Filename"))
			set = 1
		if self.NP_rhythmbox.get_active():
			self.label2.set_text(_("$n Now Playing\n$l Length\n$r Bitrate\n$s Status\n$t Title\n$a Artist\n$b Album\n$c Comment\n$k Track Number\n$y Year\n$f Filename (URI)"))
			set = 1
		if self.NP_bmpx.get_active():
			self.label2.set_text(_("$n Now Playing\n$l Length\n$r Bitrate\n$t Title\n$a Artist\n$b Album\n$k Track Number\n$y Year\n$f Filename (URI)"))
			set = 1
		if self.NP_other.get_active():
			self.label2.set_text(_("$n Now Playing"))
			self.NPCommand.set_sensitive(True)
			set = 1
		else:
			self.NPCommand.set_sensitive(False)
		if not set:
			self.label2.set_text(_(""))
			
	def OnNPCancel(self, widget):
		self.quit(None)
		
	def quit(self, widget):
		self.NowPlaying.hide()
		
	def OnNPTest(self, widget):
		self.DisplayNowPlaying(None, test=1)
		
	def OnNPSave(self, widget):
		if self.NP_infopipe.get_active():
			player = "infopipe"
		elif self.NP_amarok.get_active():
			player = "amarok"
		elif self.NP_mpd.get_active():
			player = "mpd"
		#elif self.NP_mp3blaster.get_active():
		#	player = "mp3blaster"
		elif self.NP_rhythmbox.get_active():
			player = "rhythmbox"
		elif self.NP_bmpx.get_active():
			player = "bmpx"
		elif self.NP_other.get_active():
			player = "other"
			
		self.frame.np.config.sections["players"]["npplayer"] = player
		self.frame.np.config.sections["players"]["npothercommand"] = self.NPCommand.get_text()
		self.frame.np.config.sections["players"]["npformat"] = self.NPFormat.child.get_text()
		self.frame.np.config.writeConfig()
		self.quit(None)
		
	def DisplayNowPlaying(self, widget, test=None):
		self.title_clear()
		if self.NP_infopipe.get_active():
			result = self.xmms()
		elif self.NP_amarok.get_active():
			result = self.amarok()
		elif self.NP_mpd.get_active():
			result = self.mpd()
		#elif self.NP_mp3blaster.get_active():
		#	result = self.mp3blaster()
		elif self.NP_rhythmbox.get_active():
			result = self.rhythmbox()
		elif self.NP_bmpx.get_active():
			result = self.bmpx()
		elif self.NP_other.get_active():
			result = self.other()
		if not result:
			return None

		#print self.title
		title = self.NPFormat.child.get_text()
		title = title.replace("$t", self.title["title"])
		title = title.replace("$a", self.title["artist"])
		title = title.replace("$b", self.title["album"])
		title = title.replace("$c", self.title["comment"])
		title = title.replace("$n", self.title["nowplaying"])
		title = title.replace("$k", self.title["track"])
		title = title.replace("$l", self.title["length"])
		title = title.replace("$y", self.title["year"])
		title = title.replace("$r", self.title["bitrate"])
		title = title.replace("$s", self.title["status"])
		title = title.replace("$f", self.title["filename"])
		
		if test:
			self.label7.set_text(title)
			return None
		if title:
			#print title
			return title
		
	
	def get_custom_widget(self, id, string1, string2, int1, int2):
		w = gtk.Label(_("(custom widget: %s)") % id)
		return w
	
	def audacious(self):
		return None
	
	def bmpx(self):
		try:
			import dbus
			import dbus.glib
			bus = dbus.SessionBus()
		except Exception, e:
			print "NowPlaying Error while loading dbus", e	
		try:
			bmp_object = bus.get_object('org.beepmediaplayer.bmp', '/Core')
			bmp_iface = dbus.Interface(bmp_object, 'org.beepmediaplayer.bmp')
		except Exception, e:
			print "NowPlaying Error while accessing bmpx dbus interface", e
		try:
			if bmp_iface.GetCurrentSource() == -1:
				return None
			metadata = bmp_iface.GetMetadataFromSource(bmp_iface.GetCurrentSource())
			self.title["bitrate"] = str(metadata["bitrate"])
			self.title["track"] = str(metadata["tracknumber"])
			self.title["title"] = metadata["title"]
			self.title["artist"] = metadata["artist"]
			self.title["length"] = self.get_length_time(metadata["time"])
			self.title["nowplaying"] = metadata["artist"] + " - " +metadata["title"] 
			self.title["year"] = str(metadata["date"])
			self.title["album"] = metadata["album"]
			self.title["filename"] = metadata["location"]
			return 1 
		except Exception, e:
			print "NowPlaying Error during RPC", e
			return None
		
	
	def mpd(self):
		format = self.NPFormat.child.get_text()
		if "$a" in format:
			output = self.mpd_command("%artist%")
			if output:
				self.title["artist"] = output
		if "$t" in format:
			output = self.mpd_command("%title%")
			if output:
				self.title["title"] = output
		if "$n" in format:
			output = self.mpd_command("%artist%\ \-\ %title%")
			if output:
				self.title["nowplaying"] = output
		if "$f" in format:
			output = self.mpd_command("%file%")
			if output:
				self.title["filename"] = output
		if "$b" in format:
			output = self.mpd_command("%album%")
			if output:
				self.title["album"] = output	

		return 1
	def mpd_command(self, command):
		output = commands.getoutput("mpc --format %s" % command).split('\n')[0]
		if output == '' or output.startswith("MPD_HOST") or output.startswith("volume: "):
			return None
		return output
	def amarok(self):
		slist = self.NPFormat.child.get_text()
		
		if "$n" in slist:
			output = self.amarok_command("nowPlaying")
			if output: self.title["nowplaying"] = output
		if "$t" in slist:
			output = self.amarok_command("title")
			if output: self.title["title"] = output
		if "$l" in slist:
			output = self.amarok_command("totalTime")
			if output: self.title["length"] = output
		if "$a" in slist:
			output = self.amarok_command("artist")
			if output: self.title["artist"] = output
		if "$b" in slist:
			output = self.amarok_command("album")
			if output:
				self.title["length"] = output
		if "$c" in slist:
			output = self.amarok_command("comment")
			if output: self.title["comment"] = output
		if "$k" in slist:
			output = self.amarok_command("track")
			if output: self.title["track"] = output
		if "$y" in slist:
			output = self.amarok_command("year")
			if output: self.title["year"] = output
		if "$r" in slist:
			output = self.amarok_command("bitrate")
			if output: self.title["bitrate"] = output
		if "$f" in slist:
			output = self.amarok_command("path")
			if output: self.title["filename"] = output
		if "$s" in slist:
			output = self.amarok_command("status")
			if output:
				status = output
				if status == "0":
					self.title["status"] = "stopped"
				elif status == "1":
					self.title["status"] = "paused"
				elif status == "2":
					self.title["status"] = "playing"
				else:
					self.title["status"] = "unknown"
		return 1
		
				
	def amarok_command(self, command):
		output = commands.getoutput("dcop amarok player %s" % command).split('\n')[0]
		if output == 'call failed':
			output = None
		return output
		
	def mp3blaster(self):
		return None
	
	def rhythmbox(self):
		try:
			import dbus
			import dbus.glib
			bus = dbus.SessionBus()
		except Exception, e:
			print "NowPlaying Error loading dbus", e
			return None
		try:
			rbshellobj = bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Shell')
			self.rbshell = dbus.Interface(rbshellobj, 'org.gnome.Rhythmbox.Shell')
			rbplayerobj = bus.get_object('org.gnome.Rhythmbox', '/org/gnome/Rhythmbox/Player')
			rbplayer = dbus.Interface(rbplayerobj, 'org.gnome.Rhythmbox.Player')
 		except Exception, e:
			print "NowPlaying Error opening Rhythmbox interface on dbus", e
			return None

		try:
			metadata = self.rbshell.getSongProperties(rbplayer.getPlayingUri())
			self.title["bitrate"] = str(metadata["bitrate"])
			self.title["track"] = str(metadata["track-number"])
			self.title["title"] = metadata["title"]
			self.title["artist"] = metadata["artist"]
			self.title["comment"] = metadata["description"]
			self.title["length"] = self.get_length_time(metadata["duration"])
			self.title["nowplaying"] = metadata["artist"] + " - " +metadata["title"] 
			self.title["year"] = str(metadata["year"])
			self.title["album"] = metadata["album"]
			self.title["filename"] = metadata["location"]
			if rbplayer.getPlaying(): 
				self.title["status"] = "playing"
			else:
				self.title["status"] = "paused"
			return 1
		except:
			return None
		
	def get_length_time(self, length):
		if length != '' and length != None:
			minutes = int(length)/60
			seconds = str( int(length) - (60 * minutes))
			if len(seconds) < 2:
				seconds = '0' + seconds
			length = str(minutes)+":"+str(seconds)
		else:
			length = "0:00"
		return length	
		

	def other(self):
		try: 
			othercommand = self.NPCommand.get_text()
			if othercommand == "":
				return None
			output = commands.getoutput("%s" % othercommand)
			if output.startswith("sh: "):
				raise Exception, output
			else:
				self.title["nowplaying"] = output 
			return 1
		except Exception, e:
			print "NowPlaying Error running command %s" %  othercommand, e
			return None
	
	def xmms(self):
		if not os.path.exists("/tmp/xmms-info"):
			return None
		try:
			fsock = open("/tmp/xmms-info")
			do = fsock.readlines()
			infolist = []
			for i in do:
				if i != "":
					infolist.append( i.strip("\n") )
			#protocol  = infolist[0][29:]
			#version = infolist[1][25:]
			status = infolist[2][8:]
			#playlist_count = infolist[3][20:]
			#playlist_position = infolist[4][20:]
			#millisec_position = infolist[5][15:]
			position = infolist[6][10:]
			#millisec_time = infolist[7][15:]
			time = infolist[8][6:]
			bitrate = str(int(infolist[9][17:])/1024)
			frequency = infolist[10][20:]
			channels = infolist[11][10:]
			title = infolist[12][7:]
			filename = infolist[13][7:]
			self.title = { "title": "",  "artist": "", "comment": "", "year": "", "album": "", "track":"", "nowplaying": title, "length": time, "bitrate": bitrate, "channels": channels, "position": position, "filename": filename, "status": status}
			fsock.close()
			return 1
		except:
			return None
		