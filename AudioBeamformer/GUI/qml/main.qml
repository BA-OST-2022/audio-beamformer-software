import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.5
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtCharts 2.15
import PyCVQML 1.0

Item{
    id: main_row
    anchors.fill: parent
    
    Component.onCompleted:{
        backend.getEnableChannels([1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1])
    }
    
    // Buttons
    Column{
        id: menu_buttons
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 5
        anchors.topMargin: 5
        anchors.bottomMargin: 5
        width: 170

        RoundButton{
            id: audio_processing_button
            anchors.left: parent.left
            anchors.right: parent.right
            text: qsTr("Processing")
            height: menu_buttons.height/3
            autoExclusive: true
            checkable: true
            checked: true
            contentItem: Text {
                text: audio_processing_button.text
                font: audio_processing_button.font
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                color: {audio_processing_button.checked ? "#303030" :"#c8c8c8"}
            }
            onClicked:{
                backend.enableMagicMode(false)
            }
            radius: 8
        }

        RoundButton{
            id: channel_button
            anchors.left: parent.left
            anchors.right: parent.right
            text: "Channels";
            height: menu_buttons.height/3
            autoExclusive: true
            checkable: true
            radius: 8
            contentItem: Text {
                text: channel_button.text
                font: channel_button.font
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                color: {channel_button.checked ? "#303030" :"#c8c8c8"}
            }
            onClicked:{
                backend.enableMagicMode(false)
            }
        }

        RoundButton{
            id: setting_button
            anchors.left: parent.left
            anchors.right: parent.right
            text: qsTr("Settings")
            height: menu_buttons.height/3
            autoExclusive: true
            checkable: true
            radius: 8
            contentItem: Text {
                text: setting_button.text
                font: setting_button.font
                horizontalAlignment: Text.AlignHCenter
                verticalAlignment: Text.AlignVCenter
                color: {setting_button.checked ? "#303030" :"#c8c8c8"}
            }
            onClicked:{
                backend.enableMagicMode(false)
            }
        }
    }

    //Main_Window
    Item{
        id: main_window 
        anchors.left: menu_buttons.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: 1200

        CVCapture
        {
            id: capture
            width: 400
            height: 300
            index: 0
            Component.onCompleted: capture.start()
            Component.onDestruction: capture.stop()
        }

        Loader{
            anchors.fill: parent
            source: "audio_processing_col.qml"
        }

        Loader{
            anchors.fill: parent
            source: "channels_col.qml"
        }

        Loader{
            anchors.fill: parent
            source: "settings_col.qml"
        }

        Loader{
            anchors.fill: parent
            source: "magic_page.qml"
        }
        
    }
    // General information
    Item{
        id: general_information_item
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: 80
        anchors.topMargin: 8
        anchors.bottomMargin: 3
        anchors.rightMargin: 20
        Loader{
            anchors.fill: parent
            source: "general_information.qml"
        }

    }
}

