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
                    onReleased: {
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
                    onReleased: {
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
        anchors.top: channel_settings_row.bottom
        anchors.topMargin: 10
        spacing: 0
        CheckBox{ id: ch_radio_channel_1
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "1" 
                x: ch_radio_channel_1.width / 2 - 3  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_2
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "2" 
                x: ch_radio_channel_1.width / 2 - 3  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_3
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "3" 
                x: ch_radio_channel_1.width / 2 - 3  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_4
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "4" 
                x: ch_radio_channel_1.width / 2 - 3  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_5
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "5" 
                x: ch_radio_channel_1.width / 2 - 3  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_6
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "6" 
                x: ch_radio_channel_1.width / 2 - 3  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_7
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "7" 
                x: ch_radio_channel_1.width / 2 - 3  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_8
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "8" 
                x: ch_radio_channel_1.width / 2 - 3  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_9
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "9" 
                x: ch_radio_channel_1.width / 2 - 3  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_10
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "10" 
                x: ch_radio_channel_1.width / 2 - 7  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_11
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "11" 
                x: ch_radio_channel_1.width / 2 - 7  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_12
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "12" 
                x: ch_radio_channel_1.width / 2 - 7 // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_13
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "13" 
                x: ch_radio_channel_1.width / 2 - 7  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_14
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "14" 
                x: ch_radio_channel_1.width / 2 - 7  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_15
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "15" 
                x: ch_radio_channel_1.width / 2 - 7 // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_16
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "16" 
                x: ch_radio_channel_1.width / 2 - 7  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_17
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "17" 
                x: ch_radio_channel_1.width / 2 - 7  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_18
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "18" 
                x: ch_radio_channel_1.width / 2 - 7  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }
         CheckBox{ id: ch_radio_channel_19
            anchors.verticalCenter: parent.verticalCenter
            checked: true
            Text { text: "19" 
                x: ch_radio_channel_1.width / 2 - 7  // Relative text position to the radio button
                y: 0      
                font.pointSize: 8
                color: "white"
            }
        }

    }
    
    Image{
        x: 800
        y: 10
        source: "images/camera_placeholder.jpg"
    }

    /*
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
    */

}