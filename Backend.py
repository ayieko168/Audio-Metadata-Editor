from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPixmap
from utils.Design_Files.MainFrontEnd import *
import music_tag
import os, sys, time, shutil, re

class Application(QMainWindow):

    def __init__(self):

        super().__init__()
        self.MainUi = Ui_MainWindow()
        self.MainUi.setupUi(self)

        ## CONNECTIONS
        self.MainUi.openButtonSingle.clicked.connect(self.openButtonSingleCMD)
        self.MainUi.addFileAlbum.clicked.connect(self.addFileAlbumCMD)
        self.MainUi.removeFileButtonAlbum.clicked.connect(self.removeFileCMD)
        self.MainUi.removeAllAlbum.clicked.connect(self.removeAllCMD)
        self.MainUi.destuttonAlbum.clicked.connect(self.destinationAlbumCMD)
        self.MainUi.findArtButtonAlbum.clicked.connect(self.findArtAlbumCMD)
        self.MainUi.saveButtonAlbum.clicked.connect(self.saveAlbumCMD)
        self.MainUi.saveAllButtonAlbum.clicked.connect(self.saveAllAlbumCMD)
        self.MainUi.exitButtonAlbum.clicked.connect(lambda: print("exit"))
        self.MainUi.tableWidgetAlbum.currentItemChanged.connect(self.updateDataAlbumCMD)
        self.MainUi.saveButtonSingle.clicked.connect(self.saveSingleCMD)
        self.MainUi.findArtButtonSingle.clicked.connect(self.findArtSingleCMD)

        ## CONSTANTS
        self.FILE_FILTERS = """ Audio Files (*.aac *.aiff *.dsf *.flac *.m4a *.mp3 *.ogg *.opus *.wav *.wv);;
                                AAC Files (*.aac);;
                                AIFF Files (*.aiff);;
                                DSF Files (*.dsf);;
                                FLAC Files (*.flac);;
                                M4A Files (*.m4a);;
                                MP3 Files (*.mp3);;
                                OGG Files (*.ogg);;
                                OPUS Files (*.opus);;
                                WAV Files (*.wav);;
                                WV Files (*.wv)
                                """
        self.IMAGE_FILTERS = """Jpeg Files (*.jpg *.jpeg );;
                                All Files (*)"""

        ## SETUPS
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.updateAlbumMetas)
        self.timer.start(100)

        ## Variables
        self.album = "" ;self.albumartist = "" ;self.artist = "" ;self.artwork = "" ;self.comment = "" ;self.compilation = ""
        self.composer = "" ;self.discnumber = 0 ;self.genre = "" ;self.lyrics = "" ;self.totaldiscs = 0 ;self.totaltracks = 0
        self.tracknumber = 0 ;self.tracktitle = "" ;self.year = 0
        self.metadata_dictinary = {}  # keys=muic_names and values=the music's metadata

        ## Plartform Specific Setup
        if (sys.platform == "win32") or (sys.platform == "cygwin"):
            self.defaultMusicPath = f"C:\\Users\\{os.getlogin()}\\Music\\Music\\albums"
            self.defaultPicturesPath = f"C:\\Users\\{os.getlogin()}\\Pictures"
        elif sys.platform == "linux":
            self.defaultMusicPath = f"/{os.getlogin()}/Music"
            self.defaultPicturesPath = f"/{os.getlogin()}/Pictures"

    def updateAlbumMetas(self):

        if self.MainUi.tabWidget.currentIndex() == 1:
            self.getCurrentVarData("album")
            if self.MainUi.tableWidgetAlbum.item(self.MainUi.tableWidgetAlbum.currentRow(), 0) is not None:
                # print("Update Meta divt ", self.metadata_dictinary)
                curent_music_path = self.MainUi.tableWidgetAlbum.item(self.MainUi.tableWidgetAlbum.currentRow(), 1).text()
                curent_music_name = os.path.basename(curent_music_path)
                current_music_meta_object = self.metadata_dictinary[curent_music_name]
                print(f"Editing Values of {curent_music_name}, Self Value = {self.totaltracks}, meta Value = {current_music_meta_object['totaltracks']}")
                self.writeMusicInfo(current_music_meta_object)

    def openButtonSingleCMD(self):

        fullpPath = QFileDialog.getOpenFileName(filter=self.FILE_FILTERS, directory=self.defaultMusicPath)[0]
        print(fullpPath)

        if fullpPath != "":
            self.MainUi.filePathEntrySingle.setText(fullpPath)
            f = self.getMusicInfo(fullpPath)
            self.populateFields(f)
            print(f)
        else:
            print("Invalid File Path!")

    def getMusicInfo(self, music_path):
        """return the meta music object"""

        return music_tag.load_file(music_path)

    def findArtSingleCMD(self):

        fullpPath = QFileDialog.getOpenFileName(filter=self.IMAGE_FILTERS, directory=self.defaultPicturesPath)[0]
        print(fullpPath)

        if fullpPath != "":

            pixmap = QPixmap(fullpPath)
            pixmap = pixmap.scaled(200, 200)
            self.MainUi.artLabelSingle.setPixmap(pixmap)
            self.MainUi.artLabelSingle.setToolTip(fullpPath)

            self.artwork = fullpPath

        else:
            print("Invalid File Path!")

    def writeMusicInfo(self, musicMetaObJ_Write):

        if self.album != "":
            try:
                musicMetaObJ_Write['album'] = str(self.album)
            except Exception as e:
                print("album ERROR", e)
        if self.albumartist != "":
            try:
                musicMetaObJ_Write['albumartist'] = self.albumartist
            except Exception as e:
                print("albumartist ERROR", e)
        if self.artist != "":
            try:
                musicMetaObJ_Write['artist'] = self.artist
            except Exception as e:
                print("artist ERROR", e)
        if self.artwork != "":
            if os.path.exists(self.artwork):
                with open(self.artwork, 'rb') as img_in:
                    musicMetaObJ_Write['artwork'] = img_in.read()

        if self.comment != "":
            try:
                musicMetaObJ_Write['comment'] = self.comment
            except Exception as e:
                print("comment ERROR", e)
        if self.compilation != "":
            try:
                musicMetaObJ_Write['compilation'] = self.compilation
            except Exception as e:
                print("compilation ERROR", e)
        if self.composer != "":
            try:
                musicMetaObJ_Write['composer'] = self.composer
            except Exception as e:
                print("composer ERROR", e)
        if self.discnumber is not None:
            try:
                musicMetaObJ_Write['discnumber'] = str(self.discnumber)
            except Exception as e:
                print("discnumber ERROR", e)
        if self.genre != "":
            try:
                musicMetaObJ_Write['genre'] = self.genre
            except Exception as e:
                print("genre ERROR", e)
        if self.lyrics != "":
            try:
                musicMetaObJ_Write['lyrics'] = self.lyrics
            except Exception as e:
                print("lyrics ERROR", e)
        if self.totaldiscs is not None:
            try:
                musicMetaObJ_Write['totaldiscs'] = str(self.totaldiscs)
            except Exception as e:
                print("totaldiscs ERROR", e)
        if self.totaltracks is not None:
            try:
                musicMetaObJ_Write['totaltracks'] = str(self.totaltracks)
            except Exception as e:
                print("totaltracks ERROR", e)
        if self.tracknumber is not None:
            try:
                musicMetaObJ_Write['tracknumber'] = str(self.tracknumber)
            except Exception as e:
                print("tracknumber ERROR", e)
        if self.tracktitle != "":
            try:
                musicMetaObJ_Write['tracktitle'] = self.tracktitle
            except Exception as e:
                print("tracktitle ERROR", e)
        if self.year != 0:
            try:
                musicMetaObJ_Write['year'] = str(self.year)
            except Exception as e:
                print("year write ERROR", e)

    def populateFields(self, musicMetaObJ_Pop):

        self.refreshFields()

        if self.MainUi.tabWidget.currentIndex() == 0:  # The Single tab
            try:
                self.MainUi.titleEditSingle.setText(musicMetaObJ_Pop["tracktitle"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.albumEditSingle.setText(musicMetaObJ_Pop["album"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.artistEditSingle.setText(musicMetaObJ_Pop["albumartist"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.contributorsEditSingle.setText(musicMetaObJ_Pop["artist"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.GenreEditSingle.setText(musicMetaObJ_Pop["genre"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.composerEditSingle.setText(musicMetaObJ_Pop["composer"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.compilationEditSingle.setText(musicMetaObJ_Pop["compilation"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.commentTextSingle.setText(musicMetaObJ_Pop["comment"].first)
            except Exception as e:
                print(e)
            try:
                if int(musicMetaObJ_Pop["year"].first) is not None:
                    self.MainUi.yearSpinSingle.setValue(musicMetaObJ_Pop["year"].first)
            except Exception as e:
                print("year ERROR ", e)
            try:
                self.MainUi.trackNumSpinSingle.setValue(musicMetaObJ_Pop["tracknumber"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.totalTracksSpinSingle.setValue(musicMetaObJ_Pop["totaltracks"].first)
            except Exception as e:
                print("populate error totlatracks", e)
            try:
                self.MainUi.diskNumSpinSingle.setValue(musicMetaObJ_Pop["discnumber"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.totalDiskSpinSingle.setValue(musicMetaObJ_Pop["totaldiscs"].first)
            except Exception as e:
                print(e)
            try:
                art = musicMetaObJ_Pop["artwork"]
                if art.first is not None:
                    raw_img = art.first.raw_thumbnail([200, 200])
                    with open("test_img.jpg", 'wb') as img_out:
                        img_out.write(raw_img)

                        pixmap = QPixmap("test_img.jpg")
                        self.MainUi.artLabelSingle.setPixmap(pixmap)

                    self.cleanImages()
                else:
                    self.MainUi.artLabelSingle.clear()

            except Exception as e:
                print("art ERROR ", e)

        elif self.MainUi.tabWidget.currentIndex() == 1:

            try:
                self.MainUi.titleEditAlbum.setText(musicMetaObJ_Pop["tracktitle"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.albumEntryAlbum.setText(musicMetaObJ_Pop["album"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.artistEntryAlbum.setText(musicMetaObJ_Pop["albumartist"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.contributorsEntryAlbum.setText(musicMetaObJ_Pop["artist"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.GenreEntryAlbum.setText(musicMetaObJ_Pop["genre"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.composerEntryAlbum.setText(musicMetaObJ_Pop["composer"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.compilationEntryAlbum.setText(musicMetaObJ_Pop["compilation"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.commentTextAlbum.setText(musicMetaObJ_Pop["comment"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.yearSpinAlbum.setValue(musicMetaObJ_Pop["year"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.trackNumSpinAlbum.setValue(musicMetaObJ_Pop["tracknumber"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.totalDiskSpinAlbum.setValue(musicMetaObJ_Pop["totaltracks"].first)
            except Exception as e:
                print("populate error totlatracks", e)
            try:
                self.MainUi.diskNumSpinAlbum.setValue(musicMetaObJ_Pop["discnumber"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.totalDiskSpinAlbum.setValue(musicMetaObJ_Pop["totaldiscs"].first)
            except Exception as e:
                print(e)
            try:
                art = musicMetaObJ_Pop["artwork"]
                if art.first is not None:
                    raw_img = art.first.raw_thumbnail([200, 200])
                    with open("test_img.jpg", 'wb') as img_out:
                        img_out.write(raw_img)

                        pixmap = QPixmap("test_img.jpg")
                        self.MainUi.artLabelAlbum.setPixmap(pixmap)

                    self.cleanImages()
                else:
                    self.MainUi.artLabelAlbum.clear()

            except Exception as e:
                print(e)

    def addFileAlbumCMD(self):

        filesPath = QFileDialog.getOpenFileNames(filter=self.FILE_FILTERS, directory=self.defaultMusicPath)[0]

        for _file in filesPath:

            fileName = os.path.basename(_file)

            rowPosition = self.MainUi.tableWidgetAlbum.rowCount()
            self.MainUi.tableWidgetAlbum.insertRow(rowPosition)

            self.MainUi.tableWidgetAlbum.setItem(rowPosition, 0, QTableWidgetItem(fileName))
            self.MainUi.tableWidgetAlbum.setItem(rowPosition, 1, QTableWidgetItem(_file))

            self.metadata_dictinary[fileName] = self.getMusicInfo(_file)

        print(self.metadata_dictinary)

    def removeFileCMD(self):
        """remove the current row with focus, if no focus, remove any row"""

        if self.MainUi.tableWidgetAlbum.currentIndex().row() != None:

            try:
                row_data = self.MainUi.tableWidgetAlbum.currentItem().text()
                music_name = os.path.basename(row_data)
                del self.metadata_dictinary[music_name]
                print(self.metadata_dictinary)
            except Exception as e:
                print("Remove ERROR ", e)


            item_row = self.MainUi.tableWidgetAlbum.currentIndex().row()
            self.MainUi.tableWidgetAlbum.removeRow(item_row)

        else:
            print("Nothing to remove")

    def removeAllCMD(self):

        row_count = self.MainUi.tableWidgetAlbum.rowCount()
        print("row count is ", row_count)

        if row_count != 0:
            for _ in range(0, (row_count+1)):
                print("removing row ", self.MainUi.tableWidgetAlbum.rowCount()-1)
                self.MainUi.tableWidgetAlbum.removeRow(self.MainUi.tableWidgetAlbum.rowCount()-1)

            self.metadata_dictinary = {}
            self.refreshFields()

        else:
            print("Nothing to remove")

        # self.MainUi.tableWidgetAlbum.clear()

    def destinationAlbumCMD(self):

        destPath = QFileDialog.getExistingDirectory(self, directory=self.defaultMusicPath)
        if destPath != "":
            self.MainUi.destntryAlbum.setText(destPath)
            print(destPath)
        else:
            print("Invalid Directory!")

    def findArtAlbumCMD(self):

        fullpPath = QFileDialog.getOpenFileName(filter=self.IMAGE_FILTERS, directory=self.defaultPicturesPath)[0]

        if fullpPath != "":

            pixmap = QPixmap(fullpPath)
            pixmap = pixmap.scaled(200, 200)
            self.MainUi.artLabelAlbum.setPixmap(pixmap)
            self.MainUi.artLabelAlbum.setToolTip(fullpPath)

            self.artwork = fullpPath

        else:
            print("Invalid File Path!")

    def saveAlbumCMD(self):
        """similar to save all but moves the edited music files to <DESTINATION> Hence creating an album with <ALBUM NAME>"""

        # verify that the created path exists else, exit
        if not os.path.exists(self.MainUi.destntryAlbum.text()):
            print("Enter valid Storage Path!")
            return
        album_destination_path = self.MainUi.destntryAlbum.text()
        print(f"Destination set to {album_destination_path}")

        # ask for the album name
        album_name, resp = QInputDialog.getText(self, "Whats The Album Name?", "Album Name: ")

        # Verify that the user agreed to the name.
        if not resp:
            print("Fatal! You exited without chosing an Album Name.")
            return
        elif album_name == "":
            print("Fatal! You havent entered a valid name.")
            return
        elif len([x for x in re.compile(r"^[\w\-. ]+$").finditer(album_name)]) <= 0:
            print("Fatal! You havent entered a valid name.")
            return

        print(f"Album Name set to >> {album_name.title()}")

        # Verify that There are music files selected
        if self.MainUi.tableWidgetAlbum.rowCount() <= 0:
            print("Exiting! You havent selected any music files for the Album.")
            return

        # Create The Album
        print("Creating the album...")
        itemCount = self.MainUi.tableWidgetAlbum.rowCount()
        musicPathList = list(set([self.MainUi.tableWidgetAlbum.item(row, 1).text() for row in range(0, itemCount)]))
        musicNameList = list(set([os.path.basename(musicpath) for musicpath in musicPathList]))
        edited_musicNames = list(set([self.MainUi.tableWidgetAlbum.item(row, 0).text() for row in range(0, itemCount)]))
        edited_musicPaths = list(set([os.path.dirname(new_path) + os.path.sep + ".".join(new_name.split(".")[:-1]) + os.path.splitext(new_path)[-1] for new_path in musicPathList for new_name in edited_musicNames]))
        edited_musicPaths_Album = list(set([album_destination_path + os.path.sep + album_name.title() + os.path.sep + ".".join(new_name.split(".")[:-1]) + os.path.splitext(new_path)[-1] for new_path in musicPathList for new_name in edited_musicNames]))

        new_name = os.path.basename(edited_musicPaths_Album[-1])
        album_path = os.path.dirname(edited_musicPaths_Album[-1])

        # Save the new files to the album directory
        print("All cnanges made to renamed file will be lost, try renaming the files and saving them then editing the metadata after")
        self.metadata_dictinary = {}
        for old, new in list(zip(musicPathList, edited_musicPaths_Album)):
            print(f"Old >> {old},  New >> {new}")
            # create the album directory if non existant
            if not os.path.exists(os.path.dirname(new)):
                print("making dest dirrs")
                os.makedirs(os.path.dirname(new))
            # copy files
            print(f"copy file, old>>{old}, new>>{new}")
            shutil.copy2(old, new)
        # update table widget with new name and path
        print("update table widget with new names and paths")
        for _file in os.listdir(album_path):
            fileName = os.path.basename(_file)
            rowPosition = self.MainUi.tableWidgetAlbum.rowCount()
            self.MainUi.tableWidgetAlbum.insertRow(rowPosition)
            self.MainUi.tableWidgetAlbum.setItem(rowPosition, 0, QTableWidgetItem(fileName))
            self.MainUi.tableWidgetAlbum.setItem(rowPosition, 1, QTableWidgetItem(_file))
        print("Done refresh table widget Ops.")

        ## refreshing the operation lists
        itemCount = self.MainUi.tableWidgetAlbum.rowCount()
        musicPathList = list(set([self.MainUi.tableWidgetAlbum.item(row, 1).text() for row in range(0, itemCount)]))
        musicNameList = list(set([os.path.basename(musicpath) for musicpath in musicPathList]))
        edited_musicNames = list(set([self.MainUi.tableWidgetAlbum.item(row, 0).text() for row in range(0, itemCount)]))
        edited_musicPaths = list(set([os.path.dirname(new_path) + os.path.sep + ".".join(new_name.split(".")[:-1]) + os.path.splitext(new_path)[-1] for new_path in musicPathList for new_name in edited_musicNames]))
        edited_musicPaths_Album = list(set([album_destination_path + os.path.sep + album_name.title() + os.path.sep + ".".join(new_name.split(".")[:-1]) + os.path.splitext(new_path)[-1] for new_path in musicPathList for new_name in edited_musicNames]))

        ## refresh changed filename meta objects
        print("creating new meta objects and meta dict")
        for new in musicPathList:
            old_name = os.path.basename(old)
            new_name = os.path.basename(new)

            self.metadata_dictinary[new_name] = self.getMusicInfo(new)
            print("Added Meta divt ", self.metadata_dictinary)

        ## Save the Edited metadata To disk
        print("Done Refreshing, Now Saving the edited metadatas")
        for pth, metaObj in self.metadata_dictinary.items():
            metaObj.save()
            pass
        print("Done Saving metadata\nDone All Ops.")

    def saveAllAlbumCMD(self):

        """save all the edited metadata and file names to disk without creating any new folders"""

        itemCount = self.MainUi.tableWidgetAlbum.rowCount()
        musicPathList = [self.MainUi.tableWidgetAlbum.item(row, 1).text() for row in range(0, itemCount)]
        musicNameList = [os.path.basename(musicpath) for musicpath in musicPathList]
        edited_musicNames = [self.MainUi.tableWidgetAlbum.item(row, 0).text() for row in range(0, itemCount)]
        edited_musicPaths = [os.path.dirname(new_path)+os.path.sep+".".join(new_name.split(".")[:-1])+os.path.splitext(new_path)[-1] for new_path in musicPathList for new_name in edited_musicNames]

        ## Save Cahnged File names to disk and change the list values with the current ones
        if not musicNameList == edited_musicNames:
            print("A Name changed")
            msg = QMessageBox.question(self, "QUESTION",
                                       "I seams you have renamed some file names, do you want to rename the file?",
                                       " More Info title", "More Info Data",
                                       QMessageBox.Yes | QMessageBox.No)

            if msg == QMessageBox.Yes:
                print("yesss")
                print("\aAll cnanges made to renamed file will be lost, try renaming the files and saving them then editing the metadata after")
                for old, new in list(zip(musicPathList, edited_musicPaths)):
                    if (old != new):
                        print(f"Old >> {old},  New >> {new}")
                        new_name = os.path.basename(new)
                        # rename file
                        print("rename file")
                        os.rename(old, new)
                        # update lists with new file
                        print("update lists with new file")
                        itemCount = self.MainUi.tableWidgetAlbum.rowCount()
                        musicPathList = [self.MainUi.tableWidgetAlbum.item(row, 1).text() for row in range(0, itemCount)]
                        edited_musicNames = [self.MainUi.tableWidgetAlbum.item(row, 0).text() for row in range(0, itemCount)]
                        edited_musicPaths = [os.path.dirname(new_path)+os.path.sep+".".join(new_name.split(".")[:-1])+os.path.splitext(new_path)[-1] for new_path in musicPathList for new_name in edited_musicNames]
                        # update table widget with new name and path
                        print("update table widget with new names and paths")
                        self.removeFileCMD()
                        rowPosition = self.MainUi.tableWidgetAlbum.rowCount()
                        self.MainUi.tableWidgetAlbum.insertRow(rowPosition)
                        self.MainUi.tableWidgetAlbum.setItem(rowPosition, 0, QTableWidgetItem(new_name))
                        self.MainUi.tableWidgetAlbum.setItem(rowPosition, 1, QTableWidgetItem(new))
                        print("Done Rename Ops.")
            else:
                print("noooooooo")

        ## refresh changed filename meta objects
        print("Now Refreshing metadata dict with new re-named file objects")
        for old, new in list(zip(musicPathList, edited_musicPaths)):
            if old != new:
                old_name = os.path.basename(old)
                new_name = os.path.basename(new)

                print(f"Removing old>{old_name} and adding new>{new_name} to the meta dict")
                old_meta = self.metadata_dictinary[old_name]
                self.metadata_dictinary[new_name] = self.metadata_dictinary.pop(old_name)
                self.metadata_dictinary[new_name] = self.getMusicInfo(new)
                print("Edited Meta divt ", self.metadata_dictinary)

        ## Save the Edited metadata To disk
        print("Done Refreshing, Now Saving the edited metadatas")
        for pth, metaObj in self.metadata_dictinary.items():
            metaObj.save()
            pass
        print("Done Saving metadata\nDone All Ops.")

    def saveSingleCMD(self):

        print("\n Setting Paths")
        music_path = self.MainUi.filePathEntrySingle.text()
        music_meta = self.getMusicInfo(music_path)

        self.getCurrentVarData()
        self.writeMusicInfo(music_meta)

        music_meta.save()
        self.populateFields(music_meta)
        print("done all ops\n")

    def updateDataAlbumCMD(self):
        """ Update the data fields when scrolling throung the music table list. Display the data of the
            curently highlighted row(music)"""

        if self.MainUi.tableWidgetAlbum.currentItem() != None:
            current_row = self.MainUi.tableWidgetAlbum.currentRow()
            music_path = self.MainUi.tableWidgetAlbum.item(current_row, 1).text()
            music_name = os.path.basename(music_path)
            print(f"change>> File Name == {music_name}, path == {music_path}")

            # meta_obj = self.getMusicInfo(music_path)
            meta_obj = self.metadata_dictinary[music_name]
            self.populateFields(meta_obj)

    def refreshFields(self):

        """Reset all fields to empty remove any text and images"""

        if self.MainUi.tabWidget.currentIndex() == 0:

            self.MainUi.titleEditSingle.setText("")
            self.MainUi.albumEditSingle.setText("")
            self.MainUi.artistEditSingle.setText("")
            self.MainUi.contributorsEditSingle.setText("")
            self.MainUi.GenreEditSingle.setText("")
            self.MainUi.composerEditSingle.setText("")
            self.MainUi.compilationEditSingle.setText("")
            self.MainUi.commentTextSingle.setText("")
            self.MainUi.yearSpinSingle.setValue(0)
            self.MainUi.trackNumSpinSingle.setValue(0)
            self.MainUi.totalTracksSpinSingle.setValue(0)
            self.MainUi.diskNumSpinSingle.setValue(0)
            self.MainUi.totalDiskSpinSingle.setValue(0)
            self.MainUi.artLabelSingle.clear()

        elif self.MainUi.tabWidget.currentIndex() == 1:

            self.MainUi.titleEditAlbum.setText("")
            self.MainUi.albumEntryAlbum.setText("")
            self.MainUi.artistEntryAlbum.setText("")
            self.MainUi.contributorsEntryAlbum.setText("")
            self.MainUi.GenreEntryAlbum.setText("")
            self.MainUi.composerEntryAlbum.setText("")
            self.MainUi.compilationEntryAlbum.setText("")
            self.MainUi.commentTextAlbum.setText("")
            self.MainUi.yearSpinAlbum.setValue(0)
            self.MainUi.trackNumSpinAlbum.setValue(0)
            self.MainUi.totalTracksAlbum.setValue(0)
            self.MainUi.diskNumSpinAlbum.setValue(0)
            self.MainUi.totalDiskSpinAlbum.setValue(0)
            self.MainUi.artLabelAlbum.clear()

    def getCurrentVarData(self, _from="single"):
        """update the global variables with the curently set variable data ie album name from the album entry"""

        if _from == "single":

            self.tracktitle = self.MainUi.titleEditSingle.text()
            self.album = self.MainUi.albumEditSingle.text()
            self.albumartist = self.MainUi.artistEditSingle.text()
            self.artist = self.MainUi.contributorsEditSingle.text()
            self.genre = self.MainUi.GenreEditSingle.text()
            self.composer = self.MainUi.composerEditSingle.text()
            self.compilation = self.MainUi.compilationEditSingle.text()
            self.comment = self.MainUi.commentTextSingle.toPlainText()
            self.year = self.MainUi.yearSpinSingle.value()
            self.tracknumber = self.MainUi.trackNumSpinSingle.value()
            self.totaltracks = self.MainUi.totalTracksSpinSingle.value()
            self.discnumber = self.MainUi.diskNumSpinSingle.value()
            self.totaldiscs = self.MainUi.totalDiskSpinSingle.value()

        elif _from == "album":

            self.tracktitle = self.MainUi.titleEditAlbum.text()
            self.album = self.MainUi.albumEntryAlbum.text()
            self.albumartist = self.MainUi.artistEntryAlbum.text()
            self.artist = self.MainUi.contributorsEntryAlbum.text()
            self.genre = self.MainUi.GenreEntryAlbum.text()
            self.composer = self.MainUi.composerEntryAlbum.text()
            self.compilation = self.MainUi.compilationEntryAlbum.text()
            self.comment = self.MainUi.commentTextAlbum.toPlainText()
            self.year = self.MainUi.yearSpinAlbum.value()
            self.tracknumber = self.MainUi.trackNumSpinAlbum.value()
            self.totaltracks = self.MainUi.totalTracksAlbum.value()
            self.discnumber = self.MainUi.diskNumSpinAlbum.value()
            self.totaldiscs = self.MainUi.totalDiskSpinAlbum.value()

    def cleanImages(self):
        """Remove the temporarily created art image"""

        os.remove("test_img.jpg")


if __name__ == "__main__":
    w = QApplication([])
    app = Application()
    app.show()
    w.exec_()