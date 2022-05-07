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
            
            // Timer for Input Source
            Timer {
                // Every 500ms
                interval: 500
                running: true
                repeat: true
                onTriggered: ap_source_combobox.model = backend.sourceList
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
                anchors.topMargin: 5
                anchors.bottomMargin: 5 
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.left: parent.left
                anchors.leftMargin: 10
                spacing: 5

                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Gain")
                }

                Slider {
                    id: ap_source_slider
                    anchors.verticalCenter: parent.verticalCenter
                    onValueChanged: {
                        backend.getSourceGain(ap_source_slider.value)
                    }
                }

            }
            // Timer for Gauge
            Timer {
                // Every 50ms
                interval: 50
                running: true
                repeat: true
                onTriggered: {ap_source_gauge.height = backend.sourceGainValue * gauge_background.width;ap_source_gauge.color = (backend.sourceGainValue > 0.95) ?  "red": ((backend.sourceGainValue > 0.8) ? "orange" : "#24c5fc")}
            }

            Item{
                id: ap_gauge_holder
                anchors.top: parent.top
                anchors.bottom: parent.bottom
                anchors.right: parent.right
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
                    id: ap_source_gauge
                    height: parent.height
                    width: parent.width
                    anchors.bottom:ap_gauge_holder.bottom
                    color: "#24c5fc"
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
                id: ap_modulation_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Modulation")
            }
            // ModulationType
            Row{
                id: ap_modulation_row_type
                anchors.top: ap_modulation_label.bottom
                anchors.topMargin: 10       
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Modulation type")
                }
                RadioButton{
                    id: ad_modulation_am
                    text: qsTr("AM")
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked:{
                        backend.getModulationType(0)
                    }
                }
                RadioButton{
                    id: ad_modulation_mam
                    text: qsTr("MAM")
                    anchors.verticalCenter: parent.verticalCenter
                    onClicked:{
                        backend.getModulationType(1)
                    }
                }

            }
            // MAM Distortion term
            Row{
                id: ap_modulation_row_gain_distortion
                visible: ad_modulation_mam.checked
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.topMargin: 5
                anchors.bottomMargin: 5 
                anchors.top: ap_modulation_row_type.bottom
                spacing: 10

                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("MAM Distortion")
                }

                Slider {
                    id: ap_modulation_slider
                    anchors.verticalCenter: parent.verticalCenter
                    onValueChanged: {
                        backend.getMAMGain(ap_modulation_slider.value)
                    }
                }

            }
        }
    }
    // Flow-Chart
    Item{
        id: flow_chart_item

    }
}