import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4

Item{
    id: main_row
    anchors.fill: parent

    // Buttons
    Column{
        id: menu_buttons
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.leftMargin: 20
        width: 140

        Button{
            id: audio_processing_button
            anchors.left: parent.left
            anchors.right: parent.right
            text: qsTr("Audio processing")
            height: menu_buttons.height/3
            autoExclusive: true
            checkable: true
            checked: true
        }

        Button{
            id: channel_button
            anchors.left: parent.left
            anchors.right: parent.right
            text: qsTr("Channels")
            height: menu_buttons.height/3
            autoExclusive: true
            checkable: true
        }

        Button{
            id: setting_button
            anchors.left: parent.left
            anchors.right: parent.right
            text: qsTr("Settings")
            height: menu_buttons.height/3
            autoExclusive: true
            checkable: true
        }
    }

    //Main_Window
    Item{
        id: main_window 
        anchors.left: menu_buttons.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: 1200

        Loader{
            anchors.fill: parent
            source: "audio_processing.qml"
        }

        Loader{
            anchors.fill: parent
            source: "channels.qml"
        }

        Loader{
            anchors.fill: parent
            source: "settings.qml"
        }
        
    }
    // General information
    Item{
        id: general_information_item
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        width: 80
        anchors.rightMargin: 20
        Loader{
            anchors.fill: parent
            source: "general_information.qml"
        }

    }
}

