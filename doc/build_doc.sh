# Bau der Doku für SmartHomeNG
#
# Das Skript checkt dazu den Core und die Plugins aus und baut die Dokumentation
#
# Das neu erzeugte Verzeichnis kann gelöscht werden, nachdem die Doku auf 
# den Webserver kopiert wurde
#

KEEP_REPO=True
if [ "$1" == "-f" ] || [ "$2" == "-f" ]; then
  FORCE_CHECKOUT=True
fi

DOC=all
if [ "$1" == "-u" ] || [ "$2" == "-u" ]; then
  DOC=user
fi
if [ "$1" == "-d" ] || [ "$2" == "-d" ]; then
  DOC=developer
fi

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

DIR=$DIR

ACCOUNT=smarthomeNG
REPO=smarthome
LOCALREPO=work
DESTBRANCH=develop

DEVELOPDOC=developer
USERDOC=user


GIT_CHECKOUT=True
echo $DIR/$LOCALREPO/doc
if [ -d "$DIR/$LOCALREPO/doc" ]; then
  if [ "${FORCE_CHECKOUT,,}" != "true" ]; then
    GIT_CHECKOUT=False
  fi
fi

cd $DIR

echo
echo
if [ "${DOC,,}" == "all" ]; then
  echo Erzeugen der vollständigen Dokumentation für SmartHomeNG
  echo ========================================================
fi
echo
if [ "${DOC,,}" == "developer" ]; then
  echo Erzeugen der Entwicklerdokumentation für SmartHomeNG
  echo ====================================================
fi
if [ "${DOC,,}" == "user" ]; then
  echo Erzeugen der Anwenderdokumentation für SmartHomeNG
  echo ==================================================
fi
echo
python3 -c "import sphinx" 2> /dev/null
if [ "$?" == "1" ]; then
  echo Vor Ausführung dieses Skriptes zum Erstellen der $ACCOUNT/$REPO Doku
  echo \(branch $DESTBRANCH\), bitte prüfen ob Sphinx installiert ist.
  echo
  echo Die Installation vorn Sphinx kann mit folgendem Kommando durchgeführt werden:
  echo
  echo -e "\t $ sudo pip3 install sphinx sphinx_rtd_theme recommonmark"
  echo
  exit
fi
echo Dieses Skript erzeugt ein Arbeitsverzeichnis \'$DIR/$LOCALREPO\'
if [ "${KEEP_REPO,,}" != "true" ]; then
  echo und legt die entstandene Dokumentation in \'$DIR/html\' ab.
fi
echo
echo Sollten diese Verzeichnisse bereits existieren, werden die alten
echo Versionen während des Skriptes gelöscht. Der Account unter dem dieses
echo Skript ausgeführt wird, muss Rechte zum anlegen von Verzeichnissen
echo in \'$DIR\' haben.
echo
if [ "${GIT_CHECKOUT,,}" == "true" ]; then
  echo Das Skript clont von github den aktuellen Stand des Branches \'$DESTBRANCH\' aus den
  echo Repositories \'smarthome\' und \'plugins\'.
else
  echo ACHTUNG: Das Skript verwendet einen bereits bestehenden lokalen Clone
  echo der Repositories.

fi
echo
echo Während des Laufes erfolgt die Ausgabe einer Reihe von Warnungen. Das ist
echo normal. Es wurden markdown \(.md\) Dateien gefunden, die bewusst nicht in die
echo Dokumentation aufgenommen wurden. Darauf weisen diese Warnungen hin. 

echo
read -rsp $'Um fortzufahren ENTER drücken, zum Abbruch ^C drücken...\n'


if [ "${GIT_CHECKOUT,,}" == "true" ]; then
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
  echo echo Auschecken des Core von github:
  git clone -b $DESTBRANCH https://github.com/$ACCOUNT/$REPO.git $LOCALREPO

  echo
  echo git status \($REPO\):
  cd $LOCALREPO
  git status

  echo
  echo Auschecken der Plugins von github:
  cd plugins
  git clone -b $DESTBRANCH https://github.com/$ACCOUNT/plugins.git .

  echo
  cd $DIR
  cd $LOCALREPO
  echo git status \(plugins\):
  git status
fi


if [ "${DOC,,}" == "developer" ] || [ "${DOC,,}" == "all" ]; then
  cd $DIR/
  cd $LOCALREPO
  cd doc
  echo
  echo Bau der Entwickler-Dokumentation:
  cd $DEVELOPDOC
  make clean
  make html
  echo
  echo Bau der Entwickler-Dokumentation ist abgeschlossen!
fi

if [ "${DOC,,}" == "user" ] || [ "${DOC,,}" == "all" ]; then
  cd $DIR/
  cd $LOCALREPO
  cd doc
  echo
  echo Bau der Anwender-Dokumentation:
  cd $USERDOC
  make clean
  make html
  echo
  echo Bau der Anwender-Dokumentation ist abgeschlossen!
fi


cd $DIR
  echo

if [ "${KEEP_REPO,,}" == "true" ]; then
  echo Geclontes Repository ist erhalten
fi

if [ "${KEEP_REPO,,}" != "true" ]; then
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
fi
