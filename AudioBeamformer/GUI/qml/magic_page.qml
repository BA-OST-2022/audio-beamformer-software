import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtCharts 2.15
import PyCVQML 1.0
import Filters 1.0

 // Audio processing
Item{
    id: magic_mode_main
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.leftMargin: -10
    visible: !audio_processing_button.checked && !channel_button.checked && !setting_button.checked

    Timer{
        interval: 1000
        running: true
        repeat: true
        onTriggered: {
            var red = Math.floor(Math.random()*255)
            var green = Math.floor(Math.random()*255)
            var blue = Math.floor(Math.random()*255)
            nice_text.color = "#" +  red.toString(16) + green.toString(16) + blue.toString(16)
        }
    }

    Image{
        id: elvis_image
        source: backend.elvisionPath
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.leftMargin: 200
        anchors.topMargin: 15
        fillMode: Image.PreserveAspectFit 
        height: 300
    }

    Image{
        id: speech_bubble
        source: backend.speechPath
        anchors.top: parent.top
        anchors.left: parent.left
        anchors.leftMargin: 400
        anchors.topMargin: 150
        fillMode: Image.PreserveAspectFit 
        height: 300
    }

    Text {
    id: nice_text
    anchors.top: parent.top
    anchors.left: elvis_image.right
    anchors.leftMargin: 50
    text: "WONDERLAND"
    font.family: "Comic Sans MS"
    font.pointSize: 24
    color: "red"
}
    CVItem 
    {
        id: imageWriter
        x: 750
        y: 10
        anchors.fill: parent
        image: capture.image
    }

}