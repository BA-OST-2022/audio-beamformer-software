import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4

ApplicationWindow{
    id: window 
    width: 1480
    height: 320
    visible: true
    // visibility: "FullScreen"
    visibility: Window.FullScreen
    Material.theme: Material.Dark // Material.Dark
    Material.accent: Material.LightBlue // Material.LightBlue
    title: qsTr("Audio Beamformer")
    flags: Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint
    
    
    Item {
        id: general_information
        x: 1428
        y: 0
        width: 50
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0
    }

    Item {
        id: main_menu
        width: 50
        anchors.left: parent.left
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.leftMargin: 0
        anchors.topMargin: 0

        Button {
            id: main_menu_button
            y: 1
            text: qsTr("")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            autoExclusive: false
            checkable: true
        }

        Button {
            id: audio_processing_button
            y: 55
            text: qsTr("")
            anchors.left: parent.left
            anchors.right: parent.right
            checked: false
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            autoExclusive: true
            checkable: true
        }

        Button {
            id: beamforming
            y: 109
            width: 50
            text: qsTr("")
            anchors.left: parent.left
            anchors.right: parent.right
            checked: true
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            autoExclusive: true
            checkable: true
        }

        Button {
            id: camera_button
            y: 164
            text: qsTr("")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            autoExclusive: true
            checkable: true
        }

        Button {
            id: led_button
            y: 218
            text: qsTr("")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            autoExclusive: true
            checkable: true
        }

        Button {
            id: admin_button
            y: 272
            text: qsTr("")
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            autoExclusive: true
            checkable: true
        }
    }
    
    Item {
            id: audio_processing_state
            visible: audio_processing_button.checked
            anchors.left: parent.left
            anchors.right: general_information.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 0
            anchors.leftMargin: 50
            anchors.bottomMargin: 0
            anchors.topMargin: 0

            Column {
                id: audio_processing_column
                height: 400
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.rightMargin: 474
                anchors.leftMargin: 0
                anchors.bottomMargin: 0
                anchors.topMargin: 0

                Item {
                    id: audio_source
                    width: audio_processing_column.width
                    height: audio_processing_column.height/5

                    Row {
                        id: audio_source_row
                        width: 200
                        height: 400
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        leftPadding: 20
                        spacing: 40
                        anchors.rightMargin: 0
                        anchors.leftMargin: 0
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0


                        Label {
                            id: audio_source_label
                            text: qsTr("Audio Source")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        RadioButton {
                            id: audio_source_bluetooth
                            text: qsTr("Bluetooth")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        RadioButton {
                            id: audio_source_mic
                            text: qsTr("Microphone")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        RadioButton {
                            id: radioButton2
                            text: qsTr("Raspberry")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        RadioButton {
                            id: radioButton3
                            text: qsTr("Radio Button")
                            anchors.verticalCenter: parent.verticalCenter
                        }
                    }
                }

                Item {
                    id: equalizer
                    width: audio_processing_column.width
                    height: audio_processing_column.height/5

                    Row {
                        id: equalizer_row
                        width: 200
                        height: 400
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.leftMargin: 0
                        Label {
                            id: equalizer_label
                            text: qsTr("Equalizer")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        RadioButton {
                            id: equalizer_on
                            text: qsTr("On")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        RadioButton {
                            id: equalizer_off
                            text: qsTr("Off")
                            anchors.verticalCenter: parent.verticalCenter
                        }
                        anchors.bottomMargin: 0
                        leftPadding: 20
                        anchors.topMargin: 0
                        spacing: 40
                        anchors.rightMargin: 0
                    }
                }

                Item {
                    id: interpolation
                    width: audio_processing_column.width
                    height: audio_processing_column.height/5

                    Row {
                        id: interpolation_row
                        width: 200
                        height: 400
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.leftMargin: 0
                        Label {
                            id: interpolation_label
                            text: qsTr("Interpolation depth")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        Slider {
                            id: slider
                            width: interpolation_row.width/1.5
                            anchors.verticalCenter: parent.verticalCenter
                            value: 0.5
                        }
                        anchors.bottomMargin: 0
                        leftPadding: 20
                        anchors.topMargin: 0
                        spacing: 40
                        anchors.rightMargin: 0
                    }
                }

                Item {
                    id: modulation_type
                    width: audio_processing_column.width
                    height: audio_processing_column.height/5

                    Row {
                        id: modulation_type_row
                        width: 200
                        height: 400
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        anchors.leftMargin: 0
                        Label {
                            id: modulation_type_label
                            text: qsTr("Modulation type")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        RadioButton {
                            id: equalizer_on1
                            text: qsTr("AM")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        RadioButton {
                            id: equalizer_off1
                            text: qsTr("MAM")
                            anchors.verticalCenter: parent.verticalCenter
                        }
                        anchors.bottomMargin: 0
                        leftPadding: 20
                        anchors.topMargin: 0
                        spacing: 40
                        anchors.rightMargin: 0
                    }
                }

                Item {
                    id: rectangle5
                    width: audio_processing_column.width
                    height: audio_processing_column.height/5
                }
            }
        }
        
         Item {
            id: beamforming_state
            visible: beamforming.checked
            anchors.left: parent.left
            anchors.right: general_information.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 0
            anchors.leftMargin: 50
            anchors.bottomMargin: 0
            anchors.topMargin: 0

            Item {
                id: beamforming_mainwindow
                y: 0
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.rightMargin: 0
                anchors.leftMargin: 0
                anchors.bottomMargin: 0
                anchors.topMargin: 0

                Column {
                    id: beamforming_column
                    height: 400
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.top: parent.top
                    anchors.bottom: parent.bottom
                    anchors.leftMargin: 0

                    Item {
                        id: window_type
                        width: beamforming_column.width
                        height: beamforming_column.height/5
                        Row {
                            id: window_type_row
                            width: 200
                            height: 400
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.leftMargin: 0
                            Label {
                                id: window_type_label
                                text: qsTr("Window type")
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            RadioButton {
                                id: dolph_cheby_button
                                text: qsTr("Dolph-Cheby")
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            RadioButton {
                                id: hamming_button
                                text: qsTr("Hamming")
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            RadioButton {
                                id: hann_button
                                text: qsTr("Hann")
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            RadioButton {
                                id: blackman_button
                                text: qsTr("Blackman")
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            RadioButton {
                                id: window_type_off_button
                                text: qsTr("Off")
                                anchors.verticalCenter: parent.verticalCenter
                            }
                            anchors.bottomMargin: 0
                            leftPadding: 20
                            anchors.topMargin: 0
                            spacing: 40
                            anchors.rightMargin: 0
                        }
                    }

                    Item {
                        id: source_for_direction
                        width: beamforming_column.width
                        height: beamforming_column.height/5

                        Row {
                            id: source_for_direction_row
                            width: 200
                            height: 400
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.leftMargin: 0
                            Label {
                                id: source_of_direction_label
                                text: qsTr("Source for direction")
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            RadioButton {
                                id: source_of_direction_camera
                                text: qsTr("Camera")
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            RadioButton {
                                id: source_of_direction_slider
                                text: qsTr("Slider")
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            RadioButton {
                                id: source_of_direction_pattern
                                text: qsTr("Pattern")
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            RadioButton {
                                id: source_of_direction_off
                                text: qsTr("Off")
                                anchors.verticalCenter: parent.verticalCenter
                            }
                            anchors.bottomMargin: 0
                            leftPadding: 20
                            anchors.topMargin: 0
                            spacing: 40
                            anchors.rightMargin: 0
                        }
                    }

                    Item {
                        id: source_of_direction_helper
                        x: 0
                        width: beamforming_column.width
                        height: beamforming_column.height/5

                        Slider {
                            id: directional_slider
                            visible: source_of_direction_slider.checked
                            anchors.verticalCenter: parent.verticalCenter
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.rightMargin: 0
                            anchors.leftMargin: 0
                            value: 0.5
                        }

                        Row {
                            id: direction_pattern_helper
                            width: 200
                            height: 400
                            visible: source_of_direction_pattern.checked
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            anchors.leftMargin: 0
                            Label {
                                id: direction_pattern_helper_label
                                text: qsTr("Pattern")
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            RangeSlider {
                                id: angle_slider_pattern
                                anchors.verticalCenter: parent.verticalCenter
                                first.value: 0.25
                                second.value: 0.75
                            }

                            SpinBox {
                                id: direction_pattern_step_size
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            SpinBox {
                                id: direction_pattern_step_time
                                anchors.verticalCenter: parent.verticalCenter
                            }

                            anchors.bottomMargin: 0
                            leftPadding: 20
                            anchors.topMargin: 0
                            spacing: 40
                            anchors.rightMargin: 0
                        }
                    }

                    Item {
                        id: channel_on_off
                        width: beamforming_column.width
                        height: beamforming_column.height/5

                        Row {
                            id: channel_on_off_row
                            x: 0
                            anchors.left: parent.left
                            anchors.right: parent.right
                            anchors.top: parent.top
                            anchors.bottom: parent.bottom
                            leftPadding: 20
                            anchors.topMargin: 0
                            anchors.rightMargin: 0
                            anchors.leftMargin: 0
                            spacing: 0
                            anchors.bottomMargin: 0


                            Label {
                                id: channel_on_off_label
                                text: qsTr("Channel On")
                                anchors.verticalCenter: parent.verticalCenter
                            }





                            RadioButton {
                                id: radioButton
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                autoExclusive: false
                                display: AbstractButton.IconOnly
                            }

                            RadioButton {
                                id: radioButton1
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton4
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton5
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton6
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton7
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton8
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton9
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton10
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton11
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton12
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton13
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton14
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton15
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton16
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton17
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton18
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton19
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }

                            RadioButton {
                                id: radioButton20
                                text: qsTr("")
                                anchors.verticalCenter: parent.verticalCenter
                                checked: true
                                display: AbstractButton.IconOnly
                                autoExclusive: false
                            }
                        }
                    }

                    Item {
                        id: beamforming_open_2
                        width: beamforming_column.width
                        height: beamforming_column.height/5
                    }

                    anchors.bottomMargin: 0
                    anchors.topMargin: 0
                    anchors.rightMargin: 453
                }
            }
        }
         Item {
            id: admin_state
            width: 1380
            height: 320
            visible: admin_button.checked
            anchors.left: parent.left
            anchors.right: general_information.left
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 0
            anchors.leftMargin: 50
            anchors.bottomMargin: 0
            anchors.topMargin: 0
            Column {
                id: admin_column
                x: 0
                y: 0
                height: 400
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.bottomMargin: 0
                anchors.topMargin: 0
                anchors.leftMargin: 0
                anchors.rightMargin: 453
                Item {
                    id: window_type1
                    width: admin_column.width
                    height: admin_column.height / 5
                    Row {
                        id: tof_row
                        width: 200
                        height: 400
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        spacing: 40
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        anchors.leftMargin: 0
                        anchors.rightMargin: 0
                        Label {
                            id: tof_label
                            text: qsTr("ToF sensor")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        RadioButton {
                            id: tof_on_button
                            text: qsTr("On")
                            anchors.verticalCenter: parent.verticalCenter
                            checked: true
                        }

                        RadioButton {
                            id: tof_off_button
                            text: qsTr("Off")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        Slider {
                            id: tof_distance_slider
                            visible: tof_on_button.checked
                            anchors.verticalCenter: parent.verticalCenter
                            value: 0.5
                        }

                        leftPadding: 20
                    }
                }

                Item {
                    id: max_volume_admin
                    width: admin_column.width
                    height: admin_column.height / 5
                    Row {
                        id: max_volume_admin_row
                        width: 200
                        height: 400
                        anchors.left: parent.left
                        anchors.right: parent.right
                        anchors.top: parent.top
                        anchors.bottom: parent.bottom
                        spacing: 40
                        anchors.bottomMargin: 0
                        anchors.topMargin: 0
                        anchors.leftMargin: 0
                        anchors.rightMargin: 0

                        leftPadding: 20

                        Label {
                            id: max_volume_label
                            text: qsTr("Max. volume")
                            anchors.verticalCenter: parent.verticalCenter
                        }

                        Slider {
                            id: max_volume_slider
                            width: 500
                            anchors.verticalCenter: parent.verticalCenter
                            value: 0.5
                        }
                    }
                }

                Item {
                    id: source_of_direction_helper1
                    x: 0
                    width: admin_column.width
                    height: admin_column.height / 5
                }

                Item {
                    id: channel_on_off1
                    width: admin_column.width
                    height: admin_column.height / 5
                }

                Item {
                    id: beamforming_open_3
                    width: admin_column.width
                    height: admin_column.height / 5
                }
            }
        }
        
        // This is just a reference how to use Gauges (VU-Meter)
        /*
        Gauge {
            id: gauge 
            minimumValue: 0
            value: 50
            maximumValue: 100
            //anchors.centerIn: parent
        }
        */
}