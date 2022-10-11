import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtCharts 2.15

ApplicationWindow{
    property color themeColorOst: "#d72864"
    
    id: window 
    width: 1480
    height: 320
    visible: true
    Material.theme: Material.Dark // Material.Dark
    Material.accent: backend.getThemeType? themeColorOst : Material.Cyan
    title: qsTr("Audio Beamformer")
    flags: Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint
    
     Timer{
        id: main_timer
        interval: 300 
        running: true
        repeat: true
        onTriggered:{
            if (backend.readyState){
                main_timer.running = false
                main_loader.source = "main.qml"
            }
        }
    }
    Loader{
        id: main_loader
        anchors.fill: parent
        source: "loading.qml"
    }
    Loader{
        source: "backend.qml"
    }
}