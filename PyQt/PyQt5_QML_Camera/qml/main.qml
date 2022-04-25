import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow{
    id: window 
    width: 1480
    height: 320
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.LightBlue
    title: qsTr("Audio Beamformer")
    flags: Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint

    // TEXT FIELD USERNAME
    TextField{
        id: usernameField
        width: 300
        text: qsTr("")
        selectByMouse: true
        placeholderText: qsTr("Your username or email")
        verticalAlignment: Text.AlignVCenter        
        anchors.horizontalCenter: parent.horizontalCenter
        //anchors.top: topBar.bottom
        anchors.topMargin: 60
    }

    // TEXT FIELD USERNAME
    TextField{
        id: passwordField
        width: 300
        text: qsTr("")
        selectByMouse: true
        placeholderText: qsTr("Your password")
        verticalAlignment: Text.AlignVCenter        
        anchors.horizontalCenter: parent.horizontalCenter
        anchors.top: usernameField.bottom
        anchors.topMargin: 10
        echoMode: TextInput.Password
    }

    // CHECKBOX SAVE PASS
    CheckBox{
        id: checkBox
        text: qsTr("Save password")
        anchors.top: passwordField.bottom
        anchors.topMargin: 10        
        anchors.horizontalCenter: parent.horizontalCenter   
    }

    // BUTTON LOGIN
    Button{
        id: buttonLogin
        width: 300
        text: qsTr("Login")
        anchors.top: checkBox.bottom
        anchors.topMargin: 10        
        anchors.horizontalCenter: parent.horizontalCenter
        onClicked: backend.checkLogin(usernameField.text, passwordField.text)
    }
    
    ComboBox {
        id: combobox
        model: ["First", "Second", "Third"]
        anchors.top: buttonLogin.bottom
        anchors.topMargin: 10        
        anchors.horizontalCenter: parent.horizontalCenter
    }
    
    Slider {
        id: sliderTest
        //minimumValue: 0
        //maximumValue: 100
        anchors.top: combobox.bottom
        anchors.topMargin: 10        
        anchors.horizontalCenter: parent.horizontalCenter
    }
    
    Image{
        id: cameraImage 
        width: 640
        height: 480
        source: "../images/logo.png"        
        //anchors.horizontalRight: parent.horizontalCenter
        //anchors.top: sliderTest.right
        //anchors.topMargin: 60
    }
    

    Connections {
        target: backend

        // CUSTOM PROPERTIES
        property string username: ""
        property string password: ""
        function onSignalUser(myUser){ username = myUser }
        function onSignalPass(myPass){ password = myPass }
    }    
}
