from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from utils.Design_Files.MainFrontEnd import *
import music_tag
import os, sys, time

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
                                WV Files (*.wv);;
                                All Files (*)
                                """
        self.IMAGE_FILTERS = """Jpeg Files (*.jpg *.jpeg );;
                                All Files (*)"""

        ## Variables
        self.album = "" ;self.albumartist = "" ;self.artist = "" ;self.artwork = "" ;self.comment = "" ;self.compilation = ""
        self.composer = "" ;self.discnumber = "" ;self.genre = "" ;self.lyrics = "" ;self.totaldiscs = "" ;self.totaltracks = ""
        self.tracknumber = "" ;self.tracktitle = "" ;self.year = ""
        
        ## Initial Setup
        # header = self.MainUi.tableWidgetAlbum.horizontalHeader()
        # header.setSectionResizeMode(0, QHeaderView.ResizeToContents)
        # header.setSectionResizeMode(1, QHeaderView.ResizeToContents)

        ## Plartform Specific Setup
        if sys.platform == "win32":
            self.defaultMusicPath = f"C:\\Users\\{os.getlogin()}\\Music\\Music\\albums"
            self.defaultPicturesPath = f"C:\\Users\\{os.getlogin()}\\Pictures"
    
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

        metaObj = music_tag.load_file(music_path)

        return metaObj

    def writeMusicInfo(self, musicMetaObj):
        pass

    def populateFields(self, musicMetaObj):

        self.refreshFields()
        
        if self.MainUi.tabWidget.currentIndex() == 0:
            try:
                self.MainUi.titleEditSingle.setText(musicMetaObj["tracktitle"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.albumEditSingle.setText(musicMetaObj["album"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.artistEditSingle.setText(musicMetaObj["albumartist"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.contributorsEditSingle.setText(musicMetaObj["artist"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.GenreEditSingle.setText(musicMetaObj["genre"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.composerEditSingle.setText(musicMetaObj["composer"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.compilationEditSingle.setText(musicMetaObj["compilation"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.commentTextSingle.setText(musicMetaObj["comment"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.yearSpinSingle.setValue(musicMetaObj["year"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.trackNumSpinSingle.setValue(musicMetaObj["tracknumber"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.totalTracksSpinSingle.setValue(musicMetaObj["totaltracks"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.diskNumSpinSingle.setValue(musicMetaObj["discnumber"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.totalDiskSpinSingle.setValue(musicMetaObj["totaldiscs"].first)
            except Exception as e:
                print(e)
        
        elif self.MainUi.tabWidget.currentIndex() == 1:

            try:
                self.MainUi.titleEditAlbum.setText(musicMetaObj["tracktitle"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.albumEntryAlbum.setText(musicMetaObj["album"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.artistEntryAlbum.setText(musicMetaObj["albumartist"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.contributorsEntryAlbum.setText(musicMetaObj["artist"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.GenreEntryAlbum.setText(musicMetaObj["genre"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.composerEntryAlbum.setText(musicMetaObj["composer"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.compilationEntryAlbum.setText(musicMetaObj["compilation"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.commentTextAlbum.setText(musicMetaObj["comment"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.yearSpinAlbum.setValue(musicMetaObj["year"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.trackNumSpinAlbum.setValue(musicMetaObj["tracknumber"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.totalDiskSpinAlbum.setValue(musicMetaObj["totaltracks"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.diskNumSpinAlbum.setValue(musicMetaObj["discnumber"].first)
            except Exception as e:
                print(e)
            try:
                self.MainUi.totalDiskSpinAlbum.setValue(musicMetaObj["totaldiscs"].first)
            except Exception as e:
                print(e)

    def addFileAlbumCMD(self):

        filesPath = QFileDialog.getOpenFileNames(filter=self.FILE_FILTERS, directory=self.defaultMusicPath)[0]
        
        for _file in filesPath:
            
            fileName = os.path.basename(_file)

            rowPosition = self.MainUi.tableWidgetAlbum.rowCount()
            self.MainUi.tableWidgetAlbum.insertRow(rowPosition)

            self.MainUi.tableWidgetAlbum.setItem(rowPosition , 0, QTableWidgetItem(fileName))
            self.MainUi.tableWidgetAlbum.setItem(rowPosition , 1, QTableWidgetItem(_file))

    def removeFileCMD(self):

        if self.MainUi.tableWidgetAlbum.currentIndex().row() != None:
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

        else:
            print("Nothing to remove")

        # self.MainUi.tableWidgetAlbum.clear()

    def destinationAlbumCMD(self):

        fullDir = QFileDialog.getExistingDirectory()
        if fullDir != "":
            self.MainUi.destntryAlbum.setText(fullDir)
            print(fullDir)
        else:
            print("Invalid Directory!")

    def findArtAlbumCMD(self):

        fullDir = QFileDialog.getOpenFileName(directory=self.defaultPicturesPath, filter=self.IMAGE_FILTERS)[0]
        if fullDir != "":
            print(fullDir)
        else:
            print("Invalid Directory!")

    def saveAlbumCMD(self):

        if (os.path.exists(self.MainUi.destntryAlbum.text())): 
            print("Enter valid Storage Path")

    def saveAllAlbumCMD(self):

        itemCount = self.MainUi.tableWidgetAlbum.rowCount()
        musicPathList = [self.MainUi.tableWidgetAlbum.item(row, 1).text() for row in range(0, itemCount)]
        musicNameList = [os.path.basename(musicpath) for musicpath in musicPathList]

        self.getCurrentVarData("album")

        print(self.tracktitle)

        
    def updateDataAlbumCMD(self):
        """ Update the data fields when scrolling throung the music table list. Display the data of the
            curently highlighted row(music)"""

        if self.MainUi.tableWidgetAlbum.currentItem() != None:
            current_row = self.MainUi.tableWidgetAlbum.currentRow()
            music_name = self.MainUi.tableWidgetAlbum.item(current_row, 0).text()
            music_path = self.MainUi.tableWidgetAlbum.item(current_row, 1).text()
            print(f"change>> File Name == {music_name}, path == {music_path}")

            meta_obj = self.getMusicInfo(music_path)
            self.populateFields(meta_obj)

    def refreshFields(self):

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




if __name__ == "__main__":
    w = QApplication([])
    app = Application()
    app.show()
    w.exec_()