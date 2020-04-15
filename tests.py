s = """
        self.album = "" ;self.albumartist = "" ;self.artist = "" ;self.artwork = "" ;self.comment = "" ;self.compilation = "";
        self.composer = "" ;self.discnumber = "" ;self.genre = "" ;self.lyrics = "" ;self.totaldiscs = "" ;self.totaltracks = "";
        self.tracknumber = "" ;self.tracktitle = "" ;self.year = "";
        """.strip().split(";")


for cmd in s:
        base = cmd.split("=")[0]
        print(base.strip())