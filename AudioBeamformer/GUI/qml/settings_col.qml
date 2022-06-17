import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import PyCVQML 1.0
import Filters 1.0
import QtCharts 2.15

Item{
    id: settings_main_row
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    visible: setting_button.checked

    Row{
        id: settings_row
        height: main_window.height/4*3
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        // LED
        Item{
            id: settings_led_item
            height: settings_row.height
            width: settings_row.width/5
            Label{
                id: se_led_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("LED")
            }

            Label{
                    id: se_led_switch_label
                    anchors.topMargin: 8
                    anchors.top: se_led_label.bottom
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: qsTr("Enable")
            }

            Switch{
                id: se_led_switch
                checked: true
                anchors.topMargin: 5
                anchors.top: se_led_switch_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                onReleased: {
                    backend.getEnableLED(se_led_switch.position)
                }
            }

    

            Label{
                id: se_leds_level_slider_label
                visible: se_led_switch.checked
                anchors.topMargin: 5
                anchors.top: se_led_switch.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                text: {"Brightness: " + (se_leds_level_slider.value*100).toFixed(0) + " %"}
            }

            Slider {
                id: se_leds_level_slider
                visible: se_led_switch.checked
                value: 1
                anchors.topMargin: -2
                anchors.top: se_leds_level_slider_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                onValueChanged: {
                    backend.getLEDBrightness(se_leds_level_slider.value)
                }
            }
        }

        // ToF Sensor
         Item{
            id: settings_tof_item
            height: settings_row.height
            width: settings_row.width/5
            Label{
                id: se_tof_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("ToF Sensor")
            }

            Label{
                id: se_tof_switch_label
                anchors.top: se_tof_label.bottom
                anchors.topMargin: 8
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Enable")
            }

            Switch{
                id: se_tof_switch
                checked: true
                anchors.top: se_tof_switch_label.bottom
                anchors.topMargin: 5
                anchors.horizontalCenter: parent.horizontalCenter
                onReleased: {
                    backend.getEnableToF(se_tof_switch.position)
                }
            }

            Label{
                id: se_tof_level_slider_label
                anchors.top: se_tof_switch.bottom
                anchors.topMargin: 5
                visible: se_tof_switch.checked
                anchors.horizontalCenter: parent.horizontalCenter
                text: {"Sensitivity: " + (se_tof_level_slider.value * 100).toFixed(0) + " %"}
            }

            Slider {
                id: se_tof_level_slider
                value: 0.5
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: se_tof_level_slider_label.bottom
                anchors.topMargin: -2
                visible: se_tof_switch.checked
                onValueChanged: {
                    backend.getToFDistance(se_tof_level_slider.value)
                }
            }

            Timer {
                // Every 50ms
                interval: 100
                running: true
                repeat: true
                 onTriggered: {
                    se_source_gauge_base.width = backend.ToFDistanceLevel * se_gauge_background.width
                    audio_player_enable.checked = backend.getPlayerState
                }
            }

            Item{
                id: se_gauge_holder
                visible: se_tof_switch.position
                anchors.top: se_tof_level_slider.bottom
                anchors.topMargin: 7
                anchors.horizontalCenter: parent.horizontalCenter
                height: 15
                width: se_tof_level_slider.width - se_tof_level_slider.implicitHandleWidth
                // Background Rectangle
                Rectangle{
                    id: se_gauge_background
                    width: parent.width
                    height: parent.height
                    anchors.verticalCenter: parent.verticalCenter
                    anchors.horizontalCenter: parent.horizontalCenter
                    rotation: 0
                    gradient: Gradient {
                        GradientStop { position: 0.0; color: "#424242" }
                        GradientStop { position: 1.0; color: "#595959" }
                    }
                }
                Rectangle{
                    id: se_source_gauge_base
                    height: se_gauge_background.height
                    width: se_gauge_background.width
                    anchors.left:se_gauge_background.left
                    anchors.verticalCenter:se_gauge_background.verticalCenter
                    color: "#80DEEA"
                }
                Image {
                    anchors.top: se_gauge_background.bottom
                    anchors.topMargin: 5
                    anchors.leftMargin: -9
                    anchors.left:se_gauge_background.left
                    width:se_gauge_background.width + 39
                    source: "images/gauge_scale_percent.svg"
                    fillMode: Image.PreserveAspectFit
                    antialiasing: true
                    smooth: true
                    Image {
                        id: se_gauge_scale_image
                        source: parent.source
                        width: 0
                        height: 0
                        antialiasing: true
                        smooth: true
                    }
                }
            }

        }

        // Max. Vol
        Item{
            id: settings_volume_item
            height: settings_row.height
            width: settings_row.width/5
            Label{
                id: se_volume_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: {"Max. Volume: " + (se_volume_level_slider.value * 100).toFixed(0) + " %"}
            }

            Slider {
                id: se_volume_level_slider
                anchors.horizontalCenter: parent.horizontalCenter
                value: 1
                anchors.top: se_volume_label.bottom
                anchors.topMargin: -2
                onValueChanged: {
                        backend.getMaxVolume(se_volume_level_slider.value)
                }
            }
            

            Label{
                id: audio_player_label
                anchors.top: se_volume_level_slider.bottom
                anchors.topMargin: 1
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: {"Audio Player"}
            }
            
             Label{
                     id: audio_player_combo_label
                     anchors.horizontalCenter: parent.horizontalCenter
                     anchors.top: audio_player_label.bottom
                     anchors.topMargin: 10
                     text: qsTr("Song List:")
             }
             ComboBox {
                     id: audio_player_combo
                     model: backend.getAudioFiles
                     anchors.horizontalCenter: parent.horizontalCenter
                     width: se_volume_level_slider.width - se_volume_level_slider.implicitHandleWidth
                     anchors.top: audio_player_combo_label.bottom
                     anchors.topMargin: 3
                     onCurrentIndexChanged: {
                         backend.audioFileIndex(audio_player_combo.currentIndex)
                     }
             }
             RoundButton{
                 id: audio_player_enable
                 checkable: true
                 checked: false
                 width: se_volume_level_slider.width
                 height: se_volume_level_slider.width / 4
                 anchors.horizontalCenter: parent.horizontalCenter
                 anchors.top: audio_player_combo.bottom
                 anchors.topMargin: 5
                  contentItem:Image{
                      anchors.fill: parent
                      anchors.topMargin: 10
                      anchors.bottomMargin: 10
                      anchors.leftMargin: 2
                      anchors.rightMargin: 2
                      sourceSize.width: 32
                      sourceSize.height: 32
                      source: {audio_player_enable.checked? backend.pausePath:backend.playPath}
                      fillMode: Image.PreserveAspectFit
                      width: 5
                      height: 5
                  }
                Material.background: { audio_player_enable.checked?"#484848":"#484848"}
                 onClicked:{
                     backend.enablePlayer(audio_player_enable.checked)
                 }
             }

        }

        // Beamfocusing
        Item{
            id: settings_beamfocusing_item
            height: settings_row.height
            width: settings_row.width/5
            Label{
                id: se_bf_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Beamfocusing")
            }

            Label{
                    id: se_bf_switch_label
                    anchors.topMargin: 8
                    anchors.top: se_bf_label.bottom
                    anchors.horizontalCenter: parent.horizontalCenter
                    text: qsTr("Enable")
            }

            Switch{
                id: se_bf_switch
                checked: false
                anchors.topMargin: 5
                anchors.top: se_bf_switch_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                onReleased: {
                    backend.enableBeamfocusing(se_bf_switch.position)
                }
            }

    

            Label{
                id: se_distance_level_slider_label
                visible: se_bf_switch.checked
                anchors.topMargin: 5
                anchors.top: se_bf_switch.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                text: {"Distance: " + (1 + 9*se_bf_level_slider.value).toFixed(1) + " m"}
            }

            Slider {
                id: se_bf_level_slider
                visible: se_bf_switch.checked
                value: 1/18 * 8
                stepSize: 1/18
                anchors.topMargin: -2
                anchors.top: se_distance_level_slider_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                onValueChanged: {
                    backend.getFocusDistance(se_bf_level_slider.value)
                }
            }
        }

        // Stats
        Item{
            id: settings_stats_item
            height: settings_row.height
            width: settings_row.width/5
            Label{
                id: se_stats_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Stats")
            }

            Timer {
                // Every 1s
                interval: 1000
                running: true
                repeat: true
                onTriggered: {
                    se_ambient_temp.text = backend.AmbientTemperature
                    se_system_temp.text = backend.SystemTemperature
                    se_cpu_temp.text = backend.CPUTemperature
                    se_cpu_load.text = backend.CPULoad
                    blue_device_count.text = backend.deviceCount
                    blue_device_list.text = backend.deviceList
                }
            }

            // Ambient Temp.
            Item{
                id: se_ambient_temp_row
                anchors.top: se_stats_label.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.topMargin: 10     
                anchors.leftMargin: 20  
                Label{
                    anchors.left: parent.left
                    text: qsTr("Ambient Temp.")
                }
                Label{
                    id: se_ambient_temp
                    anchors.left: parent.left
                    anchors.leftMargin: 120
                }
            }

            // System Temp.
            Item{
                id: se_system_temp_row
                anchors.top: se_ambient_temp_row.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.topMargin: 20       
                anchors.leftMargin: 20  
                Label{
                    anchors.left: parent.left
                    text: qsTr("System Temp.")
                }
                Label{
                    id: se_system_temp
                    anchors.left: parent.left
                    anchors.leftMargin: 120
                }
            }

            // CPU Temp.
            Item{
                id: se_cpu_temp_row
                anchors.top: se_system_temp_row.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.topMargin: 20       
                anchors.leftMargin: 20 
                Label{
                    anchors.left: parent.left
                    text: qsTr("CPU Temp.")
                }
                Label{
                    id: se_cpu_temp
                    anchors.left: parent.left
                    anchors.leftMargin: 120
                }
            }

            // CPU Load
            Item{
                id: se_cpu_load_row
                anchors.top: se_cpu_temp_row.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.topMargin: 20       
                anchors.leftMargin: 20 
                Label{
                    anchors.left: parent.left
                    text: qsTr("CPU Load")
                }
                Label{
                    id: se_cpu_load
                    anchors.left: parent.left
                    anchors.leftMargin: 120
                }
            }

            // Bluetooth Device Count
            Item{
                id: blue_device_count_row
                anchors.top: se_cpu_load_row.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.topMargin: 20       
                anchors.leftMargin: 20 
                Label{
                    anchors.left: parent.left
                    text: qsTr("Bluetooth Devices")
                }
                Label{
                    id: blue_device_count
                    anchors.left: parent.left
                    anchors.leftMargin: 120
                }
            }
            // Bluetooth Device List
            Item{
                id: blue_device_list_row
                anchors.top: blue_device_count_row.bottom
                anchors.left: parent.left
                anchors.right: parent.right
                anchors.topMargin: 20       
                anchors.leftMargin: 20 
                Label{
                    id: blue_device_list
                    anchors.left: parent.left
                    anchors.leftMargin: 10
                    text: backend.deviceList

                }
            
            }
        }
    }
    // Enable Magic Timer
    Timer{
        interval: 2000
        running: true
        repeat: true
        onTriggered: {
             if (!channel_1.checked && !channel_2.checked && channel_3.checked && !channel_4.checked && !channel_5.checked && !channel_6.checked && !channel_7.checked && !channel_8.checked && !channel_9.checked && !channel_10.checked && !channel_11.checked && !channel_12.checked && !channel_13.checked && channel_14.checked && channel_15.checked && !channel_16.checked && !channel_17.checked && !channel_18.checked && !channel_19.checked){
                channel_1.checked= true
                channel_2.checked= true
                channel_3.checked= true
                channel_4.checked= true
                channel_5.checked= true
                channel_6.checked= true
                channel_7.checked= true
                channel_8.checked= true
                channel_9.checked= true
                channel_10.checked= true
                channel_11.checked= true
                channel_12.checked= true
                channel_13.checked= true
                channel_14.checked= true
                channel_15.checked= true
                channel_16.checked= true
                channel_17.checked= true    
                channel_18.checked= true
                channel_19.checked= true
                audio_processing_button.checked = false
                channel_button.checked = false
                setting_button.checked = false
                backend.enablePlayer(false)
                audio_player_enable.checked = false
                backend.enableMagicMode(true)
             }
        }
    }
    Timer{
        interval: 200
        running: true
        repeat: true
        onTriggered: {
            backend.getEnableChannels([channel_1.checked,channel_2.checked,
                                        channel_3.checked,channel_4.checked,
                                        channel_5.checked,channel_6.checked,
                                        channel_7.checked,channel_8.checked,
                                        channel_9.checked,channel_10.checked,
                                        channel_11.checked,channel_12.checked,
                                        channel_13.checked,channel_14.checked,
                                        channel_15.checked,channel_16.checked,
                                        channel_17.checked,channel_18.checked,
                                        channel_19.checked])
        }
    }
    
    Row{
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.bottom: parent.bottom
        height: 50
        spacing: 3.5
        anchors.leftMargin: 10
        anchors.bottomMargin: 5
        Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Channel Enable")
            }
        CheckBox{
            id: channel_1
            checked: true
            Label{
                text: qsTr("1")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_2
            checked: true
            Label{
                text: qsTr("2")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_3
            checked: true
            Label{
                text: qsTr("3")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_4
            checked: true
            Label{
                text: qsTr("4")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_5
            checked: true
            Label{
                text: qsTr("5")
                 anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_6
            checked: true
            Label{
                text: qsTr("6")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_7
            checked: true
            Label{
                text: qsTr("7")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_8
            checked: true
            Label{
                text: qsTr("8")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_9
            checked: true
            Label{
                text: qsTr("9")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_10
            checked: true
            Label{
                text: qsTr("10")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_11
            checked: true
            Label{
                text: qsTr("11")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_12
            checked: true
            Label{
                text: qsTr("12")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_13
            checked: true
            Label{
                text: qsTr("13")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_14
            checked: true
            Label{
                text: qsTr("14")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_15
            checked: true
            Label{
                text: qsTr("15")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_16
            checked: true
            Label{
                text: qsTr("16")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_17
            checked: true
            Label{
                text: qsTr("17")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_18
            checked: true
            Label{
                text: qsTr("18")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_19
            checked: true
            Label{
                text: qsTr("19")
                anchors.top: parent.top
                anchors.topMargin: -4
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        Button{
            text: qsTr("Enable all")
            onClicked:{
                channel_1.checked= true
                channel_2.checked= true
                channel_3.checked= true
                channel_4.checked= true
                channel_5.checked= true
                channel_6.checked= true
                channel_7.checked= true
                channel_8.checked= true
                channel_9.checked= true
                channel_10.checked= true
                channel_11.checked= true
                channel_12.checked= true
                channel_13.checked= true
                channel_14.checked= true
                channel_15.checked= true
                channel_16.checked= true
                channel_17.checked= true
                channel_18.checked= true
                channel_19.checked= true
            }
        }
        Button{
            text: qsTr("Disable all")
            onClicked:{
                channel_1.checked= false
                channel_2.checked= false
                channel_3.checked= false
                channel_4.checked= false
                channel_5.checked= false
                channel_6.checked= false
                channel_7.checked= false
                channel_8.checked= false
                channel_9.checked= false
                channel_10.checked= false
                channel_11.checked= false
                channel_12.checked= false
                channel_13.checked= false
                channel_14.checked= false
                channel_15.checked= false
                channel_16.checked= false
                channel_17.checked= false
                channel_18.checked= false
                channel_19.checked= false
            }
        }
    }
}