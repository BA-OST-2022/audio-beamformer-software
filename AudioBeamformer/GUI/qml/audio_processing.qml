 import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4

 // Audio processing
Item{
    id: audio_processing_main_row
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    visible: audio_processing_button.checked

    // Audio processing settings
    Row{
        id: audio_processing_settings_row
        height: main_window.height/3*2
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top

        // Source 
        Item{
            id: audio_processing_source_item
            height: audio_processing_settings_row.height
            width: audio_processing_settings_row.width/4

            // Source label
            Label{
                id: ap_source_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Source")
            }

            // ComboBox
            Row{
                id: ap_source_row_input_source
                anchors.top: ap_source_label.bottom
                anchors.topMargin: 10       
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Input Source")
                }

                ComboBox {
                    id: ap_source_combobox
                    model: backend.sourceList
                    onCurrentIndexChanged: {
                        backend.getSource(ap_source_combobox.currentIndex)
                    }
                }

            }

            // Slider
            Row{
                id: ap_source_row_gain_source
                anchors.right: parent.right
                anchors.topMargin: 5
                anchors.bottomMargin: 5 
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                spacing: 10

                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Volume")
                }

                 Slider {
                    id: ap_source_slider
                    anchors.verticalCenter: parent.verticalCenter
                    onValueChanged: {
                        backend.getSourceGain(ap_source_slider.value)
                    }
                }

            }
           
        }

        // Equalizer
        Item{
            id: audio_processing_equalizer_item
            height: audio_processing_settings_row.height
            width: audio_processing_settings_row.width/4
            // Title
            Label{
                id: ap_equalizer_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Equalizer")
            }
            // Enable
            Row{
                id: ap_equalizer_row_enable
                anchors.top: ap_equalizer_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10       
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Enable")
                }

                 Switch{
                    id: ap_equalizer_switch
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked: {
                        backend.getEnableEqualizer(ap_equalizer_switch.position)
                }
            }

            }
            // Equalizer Profile
            Row{
                id: ap_equalizer_row_equalizer_profile
                visible: ap_equalizer_switch.position
                anchors.top: ap_equalizer_row_enable.bottom
                anchors.topMargin: 10       
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Equalizer Profile")
                }

                ComboBox {
                    id: ap_equalizer_combobox
                    model: backend.equalizerList
                    onCurrentIndexChanged: {
                        backend.getEqualizerProfile(ap_equalizer_combobox.currentIndex)
                    }
                }

            }

        }

        // Interpolation
        Item{
            id: audio_processing_interpolation_item
            height: audio_processing_settings_row.height
            width: audio_processing_settings_row.width/4
            Label{
                id: ap_interpolation_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Interpolation")
            }

            // Enable
            Row{
                id: ap_interpolation_row_enable
                anchors.top: ap_interpolation_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10       
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Enable")
                }

                 Switch{
                    id: ap_interpolation_switch
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked: {
                        backend.getEnableInterpolation(ap_interpolation_switch.position)
                }
            }

            }
            // Interpolation level
            Row{
                id: ap_interpolation_row_level
                visible: ap_interpolation_switch.position
                anchors.top: ap_interpolation_row_enable.bottom
                anchors.topMargin: 10       
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Interpolation levels")
                }

                ComboBox {
                    id: ap_interpolation_combobox
                    model: [2,4,8,16,32,64]
                    onCurrentIndexChanged: {
                        backend.getInterpolationLevel(ap_interpolation_combobox.currentIndex)
                    }
                }

            }

        }

        // Modulation
        Item{
            id: audio_processing_modulation_item
            height: audio_processing_settings_row.height
            width: audio_processing_settings_row.width/4
            Label{
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Modulation")
            }
        }
    }
    // Flow-Chart
    Item{
        id: flow_chart_item

    }
}