import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import PyCVQML 1.0
import Filters 1.0

ApplicationWindow
{
    //width: 800
    //height: 600
    
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
        width: 400
        height: 300
        anchors.fill: parent
        image: capture.image
    }
    
    CVCapture
    {
        id: capture
        index: 0
        filters: capture_image
        Component.onCompleted: capture.start()
        //anchors.topMargin: 10
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