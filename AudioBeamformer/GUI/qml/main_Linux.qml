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
    
    Loader{
        anchors.fill: parent
        source: "main.qml"
    }
    Loader{
        source: "backend.qml"
    }
}