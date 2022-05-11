import QtQuick 2.7
import QtQuick.Controls 2.3
import QtQuick.Window 2.3

ApplicationWindow{
    title: qsTr('Quomodo')
    id: mainWindow
    width:  480
    height: 640
    visible: true

    Column {
        anchors.horizontalCenter: parent.horizontalCenter
        spacing: 8
        padding: 8

        Button {
            objectName: "myButton"
            text: qsTr("Work")
            highlighted: true
            onClicked: {
                // call the slot to process the text
                main.textLabel("Next")
            }
        }

        Label {
            id: textResult
            text: qsTr("Time")
            anchors.horizontalCenter: parent.horizontalCenter
        }
    } 

    // Here we take the result of text processing
    Connections {
        target: main

        // Signal Handler 
        onTextResult: {
            // textLabel - was given through arguments=['textLabel']
            textResult.text = textLabel
        }
    }      
}