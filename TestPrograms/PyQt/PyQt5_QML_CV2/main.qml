import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import PyCVQML 1.0
import Filters 1.0

ApplicationWindow
{
    id: window 
    width: 1480
    height: 320
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.LightBlue
    title: qsTr("Audio Beamformer")
    flags: Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint


    CVItem 
    {
        id: imageWriter
        x: 540
        y: 10
        anchors.fill: parent
        image: capture.image
    }
    CVCapture
    {
        id: capture
        width: 400
        height: 300
        index: 0
        filters: capture_image
        Component.onCompleted: capture.start()
        Component.onDestruction: capture.stop()
    }
    
    
    Connections
    {
        target: backend

        // CUSTOM PROPERTIES
        property string username: ""
        property string password: ""
        function onSignalUser(myUser){ username = myUser }
        function onSignalPass(myPass){ password = myPass }
    } 
}