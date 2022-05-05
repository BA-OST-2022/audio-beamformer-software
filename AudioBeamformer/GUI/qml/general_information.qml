import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4

Item{
    anchors.fill: parent
    Button{
            id: main_mute_button
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.bottom: parent.bottom
            text: qsTr("Mute")
            height: 80
            checkable: true
            onClicked: {
                backend.getMuteEnable(main_mute_button.checked)
            }
    }

    Slider{
        id: main_volume_slider
        anchors.bottom: main_mute_button.top
        anchors.top: parent.top
        anchors.right: parent.right
        orientation: Qt.Vertical
        onValueChanged: {
            backend.getMainGain(main_volume_slider.value)
            }
    }
    Timer {
        // Every 50ms
        interval: 50
        running: true
        repeat: true
        onTriggered: gi_main_gauge.value = backend.mainGainValue
    }

           Gauge {
                id: gi_main_gauge
                anchors.top: parent.top
                anchors.bottom: main_mute_button.top
                anchors.left: parent.left
                anchors.topMargin: 5
                minimumValue: 0
                value: 50
                maximumValue: 100
            }
}