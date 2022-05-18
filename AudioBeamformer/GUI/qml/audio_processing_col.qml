import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtCharts 2.15

 // Audio processing
Item{
    id: audio_processing_main_row
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.leftMargin: -10
    visible: audio_processing_button.checked

    // Audio processing settings
    Row{
        id: audio_processing_settings_row
        height: 198
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

            Label{
                id: ap_source_label_combo
                anchors.topMargin: 8
                anchors.top: ap_source_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Input Device")
            }

            ComboBox {
                id: ap_source_combobox
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: ap_source_label_combo.bottom
                anchors.topMargin: 8
                model: backend.sourceList
                width: ap_source_slider.width
                onCurrentIndexChanged: {
                    backend.getSource(ap_source_combobox.currentIndex)
                }
                MouseArea{
                    id: ap_mouse_area
                    anchors.fill: parent
                    preventStealing: true
                    propagateComposedEvents: true
                    onClicked:{
                        ap_source_combobox.model = backend.sourceList
                        ap_source_combobox.popup.open()
                    }
                }
            }

            Label{
                id: ap_source_label_gain
                anchors.top: ap_source_combobox.bottom
                anchors.topMargin: 12
                anchors.horizontalCenter: parent.horizontalCenter
                text: {"Gain: " + (24*(ap_source_slider.value -0.5)).toFixed(1) + " dB"}
            }

            Slider {
                id: ap_source_slider
                stepSize: 1/24
                anchors.top: ap_source_label_gain.bottom
                anchors.topMargin: -2
                value: 0.5
                y: 20
                anchors.horizontalCenter: parent.horizontalCenter
                onValueChanged: {
                    backend.getSourceGain(ap_source_slider.value)
                }

            }
            
            // Timer for Gauge
            Timer {
                // Every 50ms
                interval: 50
                running: true
                repeat: true
                onTriggered: {
                    ap_source_gauge_base.height = Math.min((backend.sourceGainValue + 40) / 50, 0.68)* gauge_background.width
                    ap_source_gauge_middle.height = Math.min((backend.sourceGainValue + 40) / 50-0.68,0.2)* gauge_background.width
                    ap_source_gauge_top.height = Math.min((backend.sourceGainValue + 40) / 50-0.8,0.2)* gauge_background.width
                    }
            }

            Item{
                id: ap_gauge_holder
                anchors.bottom: ap_source_slider.bottom
                anchors.top: ap_source_label_combo.top
                anchors.right: parent.right
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
                    height: parent.height*0.6
                    width: parent.width
                    anchors.bottom:ap_gauge_holder.bottom
                    color: "#38f56e"
                }
                Rectangle{
                    id: ap_source_gauge_middle
                    height: parent.height*0.2
                    width: parent.width
                    anchors.bottom:ap_source_gauge_base.top
                    color: "#f59738"
                }
                Rectangle{
                    id: ap_source_gauge_top
                    height: parent.height
                    width: parent.width
                    anchors.bottom:ap_source_gauge_middle.top
                    color: "#f54b38"
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

            Label{
                    id: ap_equalizer_enable_label
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: ap_equalizer_label.bottom
                    anchors.topMargin: 8
                    text: qsTr("Enable")
            }
            Switch{
                    id: ap_equalizer_switch
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: ap_equalizer_enable_label.bottom
                    anchors.topMargin: 4
                    onReleased: {
                        backend.getEnableEqualizer(ap_equalizer_switch.position)
                    }
            }
            Label{
                    visible: ap_equalizer_switch.checked
                    id: ap_equalizer_combo_label
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: ap_equalizer_switch.bottom
                    anchors.topMargin: 10
                    text: qsTr("Equalizer Profile")
            }
            ComboBox {
                    visible: ap_equalizer_switch.checked
                    id: ap_equalizer_combobox
                    model: backend.equalizerList
                    anchors.horizontalCenter: parent.horizontalCenter
                    width: ap_source_slider.width
                    anchors.top: ap_equalizer_combo_label.bottom
                    anchors.topMargin: 8
                    onCurrentIndexChanged: {
                        backend.getEqualizerProfile(ap_equalizer_combobox.currentIndex)
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


            Label{
                id: ap_interpolation_enable_label
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: ap_interpolation_label.bottom
                anchors.topMargin: 8
                text: qsTr("Enable")
            }

            Switch{
                    id: ap_interpolation_switch
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: ap_interpolation_enable_label.bottom
                    anchors.topMargin: 4
                    onReleased: {
                        backend.getEnableInterpolation(ap_interpolation_switch.position)
                    }
            }

            Label{
                    visible: ap_interpolation_switch.checked
                    id: ap_interpolation_combo_label
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: ap_interpolation_switch.bottom
                    anchors.topMargin: 10
                    text: qsTr("Interpolation levels")
            }

            ComboBox {
                    visible: ap_interpolation_switch.checked
                    id: ap_interpolation_combobox
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: ap_interpolation_combo_label.bottom
                    width: ap_source_slider.width
                    anchors.topMargin: 8
                    model: [2,4,8,16,32,64]
                    onCurrentIndexChanged: {
                        backend.getInterpolationLevel(ap_interpolation_combobox.currentIndex)
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

             Label{
                    id: ap_modulation_label_radio_label
                    anchors.top: ap_modulation_label.bottom
                    anchors.topMargin: 8
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: qsTr("Modulation type")
            }
            Row{
                id: ap_interpolation_row_radio_button
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: ap_modulation_label_radio_label.bottom
                anchors.topMargin: 5
                RadioButton{
                    id: ad_modulation_am
                    text: qsTr("AM")
                    checked: true
                    onClicked:{
                        backend.getModulationType(0)
                    }
                }
                RadioButton{
                    id: ad_modulation_mam
                    text: qsTr("MAM")
                    onClicked:{
                        backend.getModulationType(1)
                    }
                }
            }
            Label{
                id: ap_modulation_slider_label
                visible: ad_modulation_mam.checked
                anchors.top: ap_interpolation_row_radio_button.bottom
                anchors.topMargin: 8
                anchors.horizontalCenter: parent.horizontalCenter
                text: {"MAM Distortion: " + (ap_modulation_slider.value * 100).toFixed() + " %"}
            }
            Slider {
                    id: ap_modulation_slider
                    visible: ad_modulation_mam.checked
                    value: 1
                    anchors.top: ap_modulation_slider_label.bottom
                    anchors.topMargin: 0
                    anchors.horizontalCenter: parent.horizontalCenter
                    onValueChanged: {
                        backend.getMAMGain(ap_modulation_slider.value)
                    }
                    /*
                    Row {
                    anchors.top: parent.bottom
                    anchors.topMargin: -21
                    width: 170
                    spacing: ap_modulation_slider.width / 12 - 2
                    Repeater {
                        id: repeater_ap_source
                        model: 12
                        Rectangle {
                            id: repeat_rectangle_ap_source
                            width: 2; height: 7
                            }
                        }
                    
                    }
                    */
            }
        }
    }
    // Flow-Chart
    Item{
        id: flow_chart_item
        anchors.top: audio_processing_settings_row.bottom
        anchors.bottom: parent.bottom
        anchors.left: parent.left
        anchors.right: parent.right
        Image{
            anchors.top: parent.top
            fillMode: Image.PreserveAspectFit
            source: {
                if (ap_equalizer_switch.checked && ad_modulation_am.checked && ap_interpolation_switch.checked){
                    backend.path_1_1_1
                }
                else if (!ap_equalizer_switch.checked && ad_modulation_am.checked && ap_interpolation_switch.checked){
                    backend.path_0_1_1
                }
                else if (ap_equalizer_switch.checked && ad_modulation_am.checked && !ap_interpolation_switch.checked){
                    backend.path_1_0_1
                }
                else if (ap_equalizer_switch.checked && !ad_modulation_am.checked && ap_interpolation_switch.checked){
                    backend.path_1_1_0
                }
                else if (ap_equalizer_switch.checked && !ad_modulation_am.checked && !ap_interpolation_switch.checked){
                    backend.path_0_1_0
                }
                else if (!ap_equalizer_switch.checked && !ad_modulation_am.checked && ap_interpolation_switch.checked){
                    backend.path_1_0_0
                }
                else if (!ap_equalizer_switch.checked && !ad_modulation_am.checked && !ap_interpolation_switch.checked){
                    backend.path_0_0_0
                }
                else{
                     backend.path_0_0_1
                }
            }
            sourceSize.width: 1206
            sourceSize.height: 122
        }
        Image{
            anchors.right: parent.right
            visible: ad_modulation_am.checked
            anchors.top: parent.top
            fillMode: Image.PreserveAspectFit 
            sourceSize.width: 300
            sourceSize.height: 122
            source: backend.amHolder
            anchors.topMargin:-102
            anchors.rightMargin: 15

        }
       
    }

}