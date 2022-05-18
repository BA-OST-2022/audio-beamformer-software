import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import PyCVQML 1.0
import Filters 1.0

Item{
    id: channels_main_row
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    visible: channel_button.checked

    Row{
        id: channel_settings_row
        height: main_window.height/3*2
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top

        // Beamsteering
        Item{
            id: channels_beamsteering_item
            height: channel_settings_row.height
            width: channel_settings_row.width/4.5
            Label{
                id: ch_beamsteering_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Beamsteering")
            }
            Label{
                id: ch_enable_label
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: ch_beamsteering_label.bottom
                anchors.topMargin: 8
                text: qsTr("Enable")
            }

            Switch{
                    id: ch_beamsteering_switch
                    checked: true
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: ch_enable_label.bottom
                    anchors.topMargin: 5
                    onReleased: {
                        backend.getEnableBeamsteering(ch_beamsteering_switch.position)
                }
            }

            Label{
                    id: ch_beamsteering_source_label
                    anchors.top: ch_beamsteering_switch.bottom
                    anchors.topMargin: 5
                    anchors.horizontalCenter: parent.horizontalCenter
                    visible: ch_beamsteering_switch.position
                    text: qsTr("Angle source")
            }

             ComboBox {
                    id: ch_beamsteering_combobox
                    anchors.top: ch_beamsteering_source_label.bottom
                    anchors.topMargin: 8
                    anchors.horizontalCenter: parent.horizontalCenter
                    visible: ch_beamsteering_switch.position
                    width: ch_beamsteering_angle_slider.width
                    model: ["Camera","Manual","Pattern"]
                    onCurrentIndexChanged: {
                        backend.getBeamsteeringSource(ch_beamsteering_combobox.currentIndex)
                    }
            }
            
             Label{
                    id: ch_beamsteering_pattern_label
                    anchors.top: ch_beamsteering_combobox.bottom
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.topMargin: 8
                    visible: ch_beamsteering_combobox.currentIndex == 2 & ch_beamsteering_switch.position
                    text: qsTr("Pattern")
                }

            ComboBox {
                id: ch_beamsteering_combobox_pattern
                visible: ch_beamsteering_combobox.currentIndex == 2 & ch_beamsteering_switch.position
                anchors.top: ch_beamsteering_pattern_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 8
                width: ch_beamsteering_angle_slider.width
                model: backend.beamsteeringPatternList
                onCurrentIndexChanged: {
                    backend.getBeamsteeringPattern(ch_beamsteering_combobox_pattern.currentIndex)
                }
            }

            Label{
                    id: ch_beamsteering_angle_slider_button
                    anchors.top: ch_beamsteering_combobox.bottom
                    anchors.topMargin: 8
                    anchors.horizontalCenter: parent.horizontalCenter
                    visible: ch_beamsteering_combobox.currentIndex == 1 & ch_beamsteering_switch.position
                    text: {"Angle: " + (ch_beamsteering_angle_slider.value - 0.5).toFixed(2) +  "°"}
                    // Add max and min angle
                }

            Slider {
                id: ch_beamsteering_angle_slider
                anchors.top: ch_beamsteering_angle_slider_button.bottom
                value: 0.5
                anchors.topMargin: -2
                anchors.horizontalCenter: parent.horizontalCenter
                visible: ch_beamsteering_combobox.currentIndex == 1 & ch_beamsteering_switch.position
                onValueChanged: {
                    backend.getBeamsteeringManualAngle(ch_beamsteering_angle_slider.value)
                }
            }
        }

        // Window
        Item{
            id: channel_window_item
            height: channel_settings_row.height
            width: channel_settings_row.width/4.5
            // Title
            Label{
                id: ch_window_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Window")
            }
            Label{
                    id: ch_window_switch_label
                    anchors.top: ch_window_label.bottom
                    anchors.topMargin: 8
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: qsTr("Enable")
                }

            Switch{
                id: ch_window_switch
                anchors.top: ch_window_switch_label.bottom
                anchors.topMargin: 5
                anchors.horizontalCenter: parent.horizontalCenter
                onReleased: {
                    backend.getEnableWindow(ch_window_switch.position)
                    }
            }
            Label{
                    id: ch_window_combobox_label
                    visible: ch_window_switch.checked
                    anchors.top: ch_window_switch.bottom
                    anchors.topMargin: 5
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: qsTr("Window type")
                }

            ComboBox {
                id: ch_window_combobox
                visible: ch_window_switch.checked
                anchors.top: ch_window_combobox_label.bottom
                anchors.topMargin: 8
                anchors.horizontalCenter: parent.horizontalCenter
                model: backend.windowList
                width: ch_beamsteering_angle_slider.width
                onCurrentIndexChanged: {
                    backend.getWindowType(ch_window_combobox.currentIndex)
                }
            }
        }

    }
    
    /*
     Image{
        x: 800
        y: 10
        source: "images/camera_placeholder.jpg"
    }
    */

    CVItem 
    {
        id: imageWriter
        x: 750
        y: 10
        anchors.fill: parent
        image: capture.image
    }
    CVCapture
    {
        id: capture
        width: 400
        height: 300
        index: 0
        //filters: capture_image
        Component.onCompleted: capture.start()
        Component.onDestruction: capture.stop()
    }


}