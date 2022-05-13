import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4

Item{
    anchors.fill: parent
    RoundButton{
            id: main_mute_button
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter

            text: qsTr("Mute")
            height: 80
            width: 100
            checkable: true
            onReleased: {
                backend.getMuteEnable(main_mute_button.checked)
            }
            contentItem:Image{
                source: {main_mute_button.checked? backend.getMuteImagePath:backend.getUnmuteImagePath}
                fillMode: Image.PreserveAspectFit
                sourceSize.width: 124
                sourceSize.height: 124

            }
            Material.background: { main_mute_button.checked?"#f54b38":"#484848"}
            radius: 8
    }

    Slider{
        id: main_volume_slider
        anchors.bottom: main_mute_button.top
        anchors.top: parent.top
        anchors.right: parent.right
        anchors.rightMargin: -20
        orientation: Qt.Vertical
        onValueChanged: {
            backend.getMainGain(main_volume_slider.value)
            }
    }
     // Timer for Gauge
            Timer {
                // Every 50ms
                interval: 50
                running: true
                repeat: true
                onTriggered: {
                    gi_source_gauge_base.height = Math.min(backend.sourceGainValue , 0.6)* gauge_background.width
                    gi_source_gauge_middle.height = Math.min(backend.sourceGainValue-0.6,0.2)* gauge_background.width
                    gi_source_gauge_top.height = Math.min(backend.sourceGainValue-0.8,0.2)* gauge_background.width
                    }
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
                    id: gauge_background
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
                    id: gi_source_gauge_base
                    height: parent.height*0.6
                    width: parent.width
                    anchors.bottom:gi_gauge_holder.bottom
                    color: "#38f56e"
                }
                Rectangle{
                    id: gi_source_gauge_middle
                    height: parent.height*0.2
                    width: parent.width
                    anchors.bottom:gi_source_gauge_base.top
                    color: "#f59738"
                }
                Rectangle{
                    id: gi_source_gauge_top
                    height: parent.height
                    width: parent.width
                    anchors.bottom:gi_source_gauge_middle.top
                    color: "#f54b38"
                }
            }
}