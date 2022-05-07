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
        onTriggered: {gi_main_gauge.height = backend.sourceGainValue * gi_gauge_background.width;gi_main_gauge.color = (backend.sourceGainValue > 0.95) ?  "red": ((backend.sourceGainValue > 0.8) ? "orange" : "#24c5fc")}
    }

    Item{
                id: gi_gauge_holder
                anchors.top: parent.top
                anchors.bottom: main_mute_button.top
                anchors.left: parent.left
                width: 20
                anchors.topMargin: 5
                anchors.bottomMargin: 5
                // Background Rectangle
                Rectangle{
                    id: gi_gauge_background
                    width: parent.height
                    height: parent.width
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    rotation: 90
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: "#424242" }
                        GradientStop { position: 1.0; color: "#595959" }
                    }
                }
                Rectangle{
                    id: gi_main_gauge
                    height: parent.height
                    width: parent.width
                    anchors.bottom:gi_gauge_holder.bottom
                    color: "#24c5fc"
                }
            }
}