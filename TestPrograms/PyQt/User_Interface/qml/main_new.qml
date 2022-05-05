import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4

ApplicationWindow{
    id: window 
    width: 1480
    height: 320
    visible: true
    // visibility: "FullScreen"
    // visibility: Window.FullScreen
    Material.theme: Material.Dark // Material.Dark
    Material.accent: Material.LightBlue // Material.LightBlue
    title: qsTr("Audio Beamformer")
    flags: Qt.FramelessWindowHint | Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint
    
    // Divide everythin in Buttons|Main_Window|General_information
    Item{
        id: main_row
        anchors.fill: parent

        // Buttons
        Column{
            id: menu_buttons
            anchors.left: parent.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            width: 150

            Button{
                id: audio_processing_button
                anchors.left: parent.left
                anchors.right: parent.right
                text: qsTr("Audio processing")
                height: menu_buttons.height/3
                autoExclusive: true
                checkable: true
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
           
        }
        // General information
        Item{
            id: general_information_item
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.left: main_window.left
        }
    }
}