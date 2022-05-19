import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtCharts 2.15
ApplicationWindow{
    id: window 
    width: 1480
    height: 320
    visible: true
    visibility: "FullScreen"
    Material.theme: Material.Dark // Material.Dark
    Material.accent: Material.Cyan // Material.LightBlue
    title: qsTr("Audio Beamformer")
    flags: Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint
    
    Timer{
        id: main_timer
        interval: 300 
        running: true
        repeat: true
        onTriggered:{
            main_loader.active = backend.readyState
            load_loader.active != backend.readyState
            if (backend.readyState){
                main_timer.running = false
            }
        }
    }
    Loader{
        id: load_loader
        active: true
        anchors.fill: parent
        source: "loading.qml"
    }
    Loader{
        id: main_loader
        active: false
        anchors.fill: parent
        source: "main.qml"
    }
    Loader{
        source: "backend.qml"
    }
}