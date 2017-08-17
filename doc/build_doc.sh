# Bau der Doku für SmartHomeNG
#
# Das Skript checkt dazu den Core und die Plugins aus und baut die Dokumentation
#
# Das neu erzeugte Verzeichnis kann gelöscht werden, nachdem die Doku auf 
# den Webserver kopiert wurde
#

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

ACCOUNT=smarthomeNG
REPO=smarthome
LOCALREPO=build_doc_work
DESTBRANCH=develop

cd $DIR

echo
echo
echo Vor Ausführung dieses Skriptes zum Erstellen der $ACCOUNT/$REPO Doku
echo \(branch $DESTBRANCH\), bitte prüfen ob Sphinx installiert ist.
echo
echo Die Installation vorn Sphinx kann mit folgendem Kommando durchgeführt werden:
echo
echo -e "\t $ sudo pip3 install sphinx sphinx_rtd_theme recommonmark"
echo
echo Dieses Skript erzeugt ein Arbeitsverzeichnis \'$LOCALREPO\'
echo und legt die entstandene Dokumentation in \'$DIR/html\' ab.
echo
echo Sollten diese Verzeichnisse bereits existieren, werden die alten
echo Versionen während des Skriptes gelöscht. Der Account unter dem dieses
echo Skript ausgeführt wird, muss Rechte zum anlegen von Verzeichnissen
echo in \'$DIR\' haben.
echo
echo Während des Laufes erfolgt die Ausgabe einer Reihe von Warnungen. Das ist
echo normal. Es wurden markdown \(.md\) Dateien gefunden, die bewusst nicht in die
echo Dokumentation aufgenommen wurden. Darauf weisen diese Warnungen hin. 

echo
read -rsp $'Um fortzufahren ENTER drücken, zum Abbruch ^C drücken...\n'


echo
if [ -d "$LOCALREPO" ]; then
  echo Lösche altes Arbeitsverzeichnis \'$LOCALREPO\'
  rm -rf $LOCALREPO
fi

if [ ! -d "$LOCALREPO" ]; then
  echo Erzeuge temporäres Arbeitsverzeichnis \'$LOCALREPO\'
  mkdir $LOCALREPO
fi

echo
echo echo Auschecken des Core von github
git clone -b $DESTBRANCH https://github.com/$ACCOUNT/$REPO.git $LOCALREPO

echo
echo git status \($REPO\):
cd $LOCALREPO
git status

echo
echo Auschecken der Plugins von github
cd plugins
git clone -b $DESTBRANCH https://github.com/$ACCOUNT/plugins.git .

echo
cd $LOCALREPO
echo git status \(plugins\):
git status

echo
echo Bau der Dokumentation...
cd ../doc
make clean
make html
echo
echo Bau der Dokumentation ist abgeschlossen!

cd $DIR
echo
if [ -d "$DIR/html" ]; then
  echo Lösche das existierende Verzeichnis $DIR/html
  rm -rf $DIR/html
fi
echo Verschiebe die neu gebaute Doku zu $DIR/html
mv $LOCALREPO/doc/build/html $DIR

echo Lösche das temporäre Arbeitsverzeichnis $LOCALREPO
rm -rf $LOCALREPO

echo
echo
echo
echo Zur Veröffentlichung der Doku \(Branch $DESTBRANCH\):
echo
echo   Bitte jetzt noch den Inhalt des Verzeichnisses \'$DIR/html\' 
echo   auf den webserver www.smarthomeNG.de in das Verzeichnis /dev kopieren
echo

