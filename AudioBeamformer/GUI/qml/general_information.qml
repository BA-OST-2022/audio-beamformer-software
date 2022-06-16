import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtCharts 2.15

Item{
    anchors.fill: parent
    /*
        Rectangle{
        id: alert_rect
        visible: backend.getAlertState
        anchors.fill: parent
        color: "red"
        radius: 10
        anchors.leftMargin: -20
        anchors.rightMargin: -20
        anchors.topMargin: -10
        anchors.bottomMargin: -5

    }
    */

    RoundButton{
            id: main_mute_button
            anchors.bottom: parent.bottom
            anchors.horizontalCenter: parent.horizontalCenter
            checked: true
            text: qsTr("Mute")
            height: 80
            width: 100
            checkable: true
            onReleased: {
                backend.getMuteEnable(main_mute_button.checked)
            }
            contentItem:Image{
                anchors.fill: parent
                anchors.leftMargin: 15
                anchors.topMargin: 15
                anchors.bottomMargin: 15
                anchors.rightMargin: 15
                source: {main_mute_button.checked? backend.getMuteImagePath:backend.getUnmuteImagePath}
                fillMode: Image.PreserveAspectFit
                sourceSize.width: 64
                sourceSize.height: 64
                width: 10
                height: 10
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
     // Timer for Gauge and mute
            Timer {
                // Every 50ms
                interval: 100
                running: true
                repeat: true
                onTriggered: {
                    ap_source_gauge_base.height = Math.min(((backend.sourceGainValue + 20*Math.log(main_volume_slider.value)/Math.log(10)) + 50) / 60, 0.6333)* gauge_background.width * (main_mute_button.checked? 0: 1) * (backend.getAlertState? 0:1)
                    ap_source_gauge_middle.height = Math.min(((backend.sourceGainValue + 20*Math.log(main_volume_slider.value)/Math.log(10)) + 50) / 60-0.6333,0.8333-0.6333)* gauge_background.width * (main_mute_button.checked? 0: 1) * (backend.getAlertState? 0:1)
                    ap_source_gauge_top.height = Math.min(((backend.sourceGainValue + 20*Math.log(main_volume_slider.value)/Math.log(10)) + 50) / 60-0.83333,1-0.8333)* gauge_background.width * (main_mute_button.checked? 0: 1) * (backend.getAlertState? 0:1)
                    main_mute_button.checked = backend.muteEnable;
                    main_volume_slider.value = backend.mainGainValue;
                    //alert_rect.visible = backend.getAlertState;
                    }
            }

            Item{
                id: ap_gauge_holder
                anchors.bottom: main_mute_button.top
                anchors.top: parent.top
                anchors.left: parent.left
                width: 15
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
                    id: ap_source_gauge_base
                    height: 0
                    width: parent.width
                    anchors.bottom:ap_gauge_holder.bottom
                    color: "#38f56e"
                }
                Rectangle{
                    id: ap_source_gauge_middle
                    height: 0
                    width: parent.width
                    anchors.bottom:ap_source_gauge_base.top
                    color: "#f59738"
                }
                Rectangle{
                    id: ap_source_gauge_top
                    height: 0
                    width: parent.width
                    anchors.bottom:ap_source_gauge_middle.top
                    color: "#f54b38"
                }
                Image {
                    anchors.top: ap_gauge_holder.top
                    anchors.topMargin: -1
                    anchors.leftMargin: 5
                    anchors.left: ap_gauge_holder.right
                    height: 0
                    width: 0
                    source: "images/gauge_scale_large.svg"
                    fillMode: Image.PreserveAspectFit
                    antialiasing: true
                    smooth: true
                    Image {
                        id: se_gauge_scale_large_image
                        source: parent.source
                        height: gauge_background.width + 4
                        anchors.top: ap_gauge_holder.top
                        fillMode: Image.PreserveAspectFit
                        antialiasing: true
                        smooth: true
                    }
                }
            }
}