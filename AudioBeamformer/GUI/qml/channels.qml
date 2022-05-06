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

            // Enable
            Row{
                id: ch_beamsteering_row_enable
                anchors.top: ch_beamsteering_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10       
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Enable")
                }

                 Switch{
                    id: ch_beamsteering_switch
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked: {
                        backend.getEnableBeamsteering(ch_beamsteering_switch.position)
                }
            }

            }

            // Beamsteering Source
            Row{
                id: ch_beamsteering_row_source
                visible: ch_beamsteering_switch.position
                anchors.top: ch_beamsteering_row_enable.bottom
                anchors.topMargin: 10       
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Angle source")
                }

                ComboBox {
                    id: ch_beamsteering_combobox
                    model: ["Camera","Manual","Pattern"]
                    onCurrentIndexChanged: {
                        backend.getBeamsteeringSource(ch_beamsteering_combobox.currentIndex)
                    }
                }

            }
            // Beamsteering Pattern
            Row{
                id: ch_beamsteering_row_pattern
                visible: ch_beamsteering_combobox.currentIndex == 2 & ch_beamsteering_switch.position
                anchors.top: ch_beamsteering_row_source.bottom
                anchors.topMargin: 10       
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Pattern")
                }

                ComboBox {
                    id: ch_beamsteering_combobox_pattern
                    model: backend.beamsteeringPatternList
                    onCurrentIndexChanged: {
                        backend.getBeamsteeringPattern(ch_beamsteering_combobox_pattern.currentIndex)
                    }
                }

            }

            Row{
                id: ch_beamsteering_row_angle
                 visible: ch_beamsteering_combobox.currentIndex == 1 & ch_beamsteering_switch.position
                anchors.topMargin: 5
                anchors.bottomMargin: 5 
                anchors.top: ch_beamsteering_row_source.bottom
                anchors.bottom: parent.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10

                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Angle")
                }

                Slider {
                    id: ch_beamsteering_angle_slider
                    anchors.verticalCenter: parent.verticalCenter
                    onValueChanged: {
                        backend.getBeamsteeringManualAngle(ch_beamsteering_angle_slider.value)
                    }
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
            // Enable
            Row{
                id: ch_window_row
                anchors.top: ch_window_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10       
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Enable")
                }

                 Switch{
                    id: ch_window_switch
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked: {
                        backend.getEnableWindow(ch_window_switch.position)
                }
            }

            }
            // Channel window
            Row{
                id: ap_equalizer_row_equalizer_profile
                visible: ch_window_switch.position
                anchors.top: ch_window_row.bottom
                anchors.topMargin: 10       
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Window type")
                }

                ComboBox {
                    id: ch_window_combobox
                    model: backend.windowList
                    onCurrentIndexChanged: {
                        backend.getWindowType(ch_window_combobox.currentIndex)
                    }
                }

            }

        }

    }
    // Channel select
    Row{
        id: channel_select_row
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top

    }
    

    CVItem 
    {
        id: imageWriter
        x: 800
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
        filters: capture_image
        Component.onCompleted: capture.start()
        Component.onDestruction: capture.stop()
    }
    
}