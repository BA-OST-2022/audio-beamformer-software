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
    Timer{
        interval: 10000
        running: true
        repeat: true
        onTriggered: {
            if (Math.random() > 0.6)
            {
                speech_bubble_thierry.visible = true
                speech_bubble_thierry_text.text = backend.quoteList[parseInt(Math.random()*backend.quoteList.length)]
            }
            else{
                speech_bubble_thierry.visible = false   
            }
            if (Math.random() > 0.6)
            {
                speech_bubble_florian.visible = true
                speech_bubble_florian_text.text = backend.quoteList[parseInt(Math.random()*backend.quoteList.length)]
            }
            else{
                speech_bubble_florian.visible = false
            }
            if (Math.random() > 0.9)
            {
                speech_bubble_elvision.visible = true
            }
            else{
                speech_bubble_elvision.visible = false
            }
        }
    }
    Image{
        id: speech_bubble_thierry
        source: backend.speechPath
        x: 390
        y: 26   
        visible: false
        fillMode: Image.PreserveAspectFit
        width: 130*2; height: 100*2
        sourceSize.width: 130*2
        sourceSize.height: 100*2
        Text{
            id: speech_bubble_thierry_text
            text: "Welcome"
            width: 145
            height: 70   
            x: 80
            y: 68
            wrapMode: Text.WordWrap
            font.family: "Comic Sans MS"
            font.pointSize: 10
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
        }
    }

    
    Image{
        id: speech_bubble_florian
        source: backend.speechFlipPath
        visible: false
        x: 65
        y: 37
        fillMode: Image.PreserveAspectFit 
        width: 130*2; height: 100*2
        sourceSize.width: 130*2
        sourceSize.height: 100*2
        Text{
            id: speech_bubble_florian_text
            text: "Welcome"
            width: 145
            height: 70   
            x: 15
            y: 65
            wrapMode: Text.WordWrap
            font.family: "Comic Sans MS"
            font.pointSize: 10
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
        }
    }

    Image{
        id: speech_bubble_elvision
        source: "images/SpeechBubble_Small.svg"
        height: 80
        width: 100
        visible: false
        sourceSize.width: 160
        sourceSize.height: 200
        x: 310
        y: 130
        Text{
            text: "Miau"
            height: 30
            width: 80
            font.family: "Comic Sans MS"
            font.pointSize: 10
            y: 46
            x: 10
            verticalAlignment: Text.AlignVCenter
            horizontalAlignment: Text.AlignHCenter
        }
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