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
    Component.onCompleted:{
        //backend.getSource(0)
        ap_source_combobox.model = backend.sourceList
    }

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
                interval: 50
                running: true
                repeat: true
                onTriggered: {
                    ap_source_gauge_base.height = Math.min((backend.sourceGainValue + 50) / 60, 0.6333)* gauge_background.width
                    ap_source_gauge_middle.height = Math.min((backend.sourceGainValue + 50) / 60-0.6333,0.8333-0.6333)* gauge_background.width
                    ap_source_gauge_top.height = Math.min((backend.sourceGainValue + 50) / 60-0.8333,1-0.8333)* gauge_background.width
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
                    height: 0
                    width: parent.width
                    anchors.left: ap_gauge_holder.left
                    anchors.right: ap_gauge_holder.right
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
                    anchors.topMargin: -4
                    anchors.leftMargin: 5
                    anchors.left:ap_gauge_holder.right
                    height: 0
                    width: 0
                    sourceSize.height: gauge_background.width*2.3
                    source: "images/gauge_scale.svg"
                    fillMode: Image.PreserveAspectFit
                    Image {
                        id: se_gauge_scale_source_image
                        source: parent.source
                        height: gauge_background.width + 13
                        sourceSize.height: gauge_background.width*2.3
                        anchors.top: ap_gauge_holder.top
                        fillMode: Image.PreserveAspectFit
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

            Label{
                    id: ap_equalizer_enable_label
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: ap_equalizer_label.bottom
                    anchors.topMargin: 8
                    text: qsTr("Enable")
            }
            Switch{
                    id: ap_equalizer_switch
                    checked: true
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
                        equalizer_plot.source = backend.eqPath + ap_equalizer_combobox.currentIndex + ".svg"
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
                    checked: true
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
                    text: qsTr("Interpolation Levels")
            }

            ComboBox {
                    visible: ap_interpolation_switch.checked
                    id: ap_interpolation_combobox
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.top: ap_interpolation_combo_label.bottom
                    width: ap_source_slider.width
                    anchors.topMargin: 8
                    model: [2,4,8,16,32,64]
                    currentIndex: 5
                    onCurrentIndexChanged: {
                        backend.getInterpolationLevel(Math.pow(2,ap_interpolation_combobox.currentIndex + 1))
                        interpolation_plot.source = backend.interpolPath + (Math.pow(2,ap_interpolation_combobox.currentIndex + 1)).toString() + ".svg"
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
                    text: qsTr("Modulation Type")
            }
            Row{
                id: ap_interpolation_row_radio_button
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: ap_modulation_label_radio_label.bottom
                anchors.topMargin: 5
                RadioButton{
                    id: ad_modulation_mam
                    text: qsTr("MAM")
                    checked: true
                    onClicked:{
                        backend.getModulationType(1)
                    }
                }
                RadioButton{
                    id: ad_modulation_am
                    text: qsTr("AM")
                    onClicked:{
                        backend.getModulationType(0)
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
                    value: 0.2
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
        // Equalizer
        Image{
            id: equalizer_plot
            visible: ap_equalizer_switch.checked
            anchors.top: parent.top
            anchors.left: parent.left
            anchors.topMargin:18
            anchors.leftMargin: 368
            fillMode: Image.PreserveAspectFit
            source: {backend.eqPath + "0.svg"}
            width: 170
            //height: 90            
        }
        
        // Interpolation
        Image{
            id: interpolation_plot
            visible: ap_interpolation_switch.checked
            anchors.top: parent.top
            anchors.right: parent.right
            anchors.topMargin:18
            anchors.rightMargin: 365
            fillMode: Image.PreserveAspectFit
            source: {backend.interpolPath + "64.svg"}
            width: 182
            height: 90      
            Label{
                anchors.top: parent.top
                visible: ap_interpolation_switch.checked && ap_interpolation_combobox.currentValue >= 32
                anchors.left: parent.left
                anchors.topMargin: 44
                anchors.leftMargin: 68
                text: "N = " + ap_interpolation_combobox.currentValue
            }      
        }
        
        // MAM Label
        Label{
            visible: !ad_modulation_am.checked
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: 206
            anchors.topMargin: 17
            text: "Signal"
        }
        Label{
            visible: !ad_modulation_am.checked
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: 195
            anchors.topMargin: 92
            text: "Distortion"
        }

        // AM Label
         Label{
            visible: ad_modulation_am.checked
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: 220
            anchors.topMargin: -18
            text: "1"
        }
        Label{
            visible: ad_modulation_am.checked
            anchors.right: parent.right
            anchors.top: parent.top
            anchors.rightMargin: 124
            anchors.topMargin: -18
            text: "Carrier"
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