import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15

ApplicationWindow{
    id: window 
    width: 1480
    height: 320
    visible: true
    Material.theme: Material.Dark
    Material.accent: Material.LightBlue
    title: qsTr("Audio Beamformer")
    flags: Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint | Qt.CustomizeWindowHint | Qt.MSWindowsFixedSizeDialogHint | Qt.WindowTitleHint
    
    
    Rectangle {
        id: general_information
        x: 1428
        y: 0
        width: 50
        color: "#00ffffff"
        anchors.right: parent.right
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.rightMargin: 0
        anchors.bottomMargin: 0
        anchors.topMargin: 0
    }

    Item {
        id: audio_processing_state
        x: 50
        visible: audio_processing_button.checked
        anchors.top: parent.top
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 0
        anchors.topMargin: 0

        Column {
            id: audio_processing_column
            height: 400
            anchors.left: parent.left
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.bottom: parent.bottom
            anchors.rightMargin: 0
            anchors.leftMargin: 0
            anchors.bottomMargin: 0
            anchors.topMargin: 0

            Row {
                id: audio_source_row
                width: 200
                height: audio_processing_column.height / 5
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.top: parent.top
                leftPadding: 20
                spacing: 40
                anchors.rightMargin: 0
                anchors.leftMargin: 0
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

            Row {
                id: equalizer_row
                y: audio_processing_column.height / 5
                width: 200
                height: audio_processing_column.height / 5
                anchors.left: parent.left
                anchors.right: parent.right
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
                leftPadding: 20
                spacing: 40
                anchors.rightMargin: 0
            }

            Row {
                id: interpolation_row
                y: audio_processing_column.height / 5 * 2
                height: audio_processing_column.height / 5
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.leftMargin: 0
                Label {
                    id: interpolation_label
                    text: qsTr("Interpolation depth")
                    anchors.verticalCenter: parent.verticalCenter
                }

                Slider {
                    id: slider
                    width: 300
                    anchors.verticalCenter: parent.verticalCenter
                    value: 0.5
                }
                leftPadding: 20
                spacing: 40
                anchors.rightMargin: 0
            }

            Row {
                id: modulation_type_row
                y: audio_processing_column.height / 5 * 3
                width: 200
                height: audio_processing_column.height / 5
                anchors.left: parent.left
                anchors.right: parent.right
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
                leftPadding: 20
                spacing: 40
                anchors.rightMargin: 0
            }
        }
    }

    Item {
        id: beamforming_state
        x: 50
        y: 0
        width: 1380
        height: 320
        visible: beamforming.checked
        Rectangle {
            id: beamforming_mainwindow
            y: 0
            color: "#00ffffff"
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

                Row {
                    id: window_type_row
                    y: 0
                    width: 200
                    height: beamforming_column.height / 5
                    anchors.left: parent.left
                    anchors.right: parent.right
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
                    leftPadding: 20
                    spacing: 40
                    anchors.rightMargin: 0
                }

                Row {
                    id: source_for_direction_row
                    y: beamforming_column.height / 5
                    width: 200
                    height: beamforming_column.height / 5
                    anchors.left: parent.left
                    anchors.right: parent.right
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
                    leftPadding: 20
                    spacing: 40
                    anchors.rightMargin: 0
                }

                StackView {
                    id: stackView
                    y: beamforming_column.height / 5 * 2
                    height: beamforming_column.height / 5
                    anchors.left: parent.left
                    anchors.right: parent.right
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0

                    Slider {
                        id: directional_slider
                        x: 0
                        y: 128
                        height: beamforming_column.height / 5
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
                        x: 0
                        y: 0
                        width: 200
                        height: beamforming_column.height / 5
                        visible: source_of_direction_pattern.checked
                        anchors.left: parent.left
                        anchors.right: parent.right
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

                        leftPadding: 20
                        spacing: 40
                        anchors.rightMargin: 0
                    }
                }

                Row {
                    id: channel_on_off_row
                    y: beamforming_column.height / 5 * 3
                    height: beamforming_column.height / 5
                    anchors.left: parent.left
                    anchors.right: parent.right
                    leftPadding: 20
                    anchors.rightMargin: 0
                    anchors.leftMargin: 0
                    spacing: 0

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

                anchors.bottomMargin: 0
                anchors.topMargin: 0
                anchors.rightMargin: 453
            }
        }
    }

    Item {
        id: admin_state
        x: 50
        y: 0
        width: 1380
        height: 320
        visible: admin_button.checked

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

            Row {
                id: tof_row
                width: 200
                height: admin_state.height / 5
                anchors.left: parent.left
                anchors.right: parent.right
                spacing: 40
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

            Row {
                id: max_volume_admin_row
                y: admin_state.height / 5
                width: 200
                height: admin_state.height / 5
                anchors.left: parent.left
                anchors.right: parent.right
                spacing: 40
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
    }

    Rectangle {
        id: main_menu
        width: 50
        color: "#00ffffff"
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
            highlighted: false
            flat: false
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
            checked: false
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
            checked: true
            anchors.leftMargin: 0
            anchors.rightMargin: 0
            autoExclusive: true
            checkable: true
        }
    }

}