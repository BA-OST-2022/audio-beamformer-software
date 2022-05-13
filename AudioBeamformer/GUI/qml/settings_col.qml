import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import PyCVQML 1.0
import Filters 1.0

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
            width: settings_row.width/4
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
                text: {"Brightness: " + se_leds_level_slider.value.toFixed(2)}
            }

            Slider {
                id: se_leds_level_slider
                visible: se_led_switch.checked
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
            width: settings_row.width/4
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
                text: {"Sensitivity: " + se_tof_level_slider.value.toFixed(2)}
            }

            Slider {
                id: se_tof_level_slider
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
                interval: 50
                running: true
                repeat: true
                 onTriggered: {
                    se_source_gauge_base.height = Math.min(backend.ToFDistanceLevel , 0.6)* se_gauge_background.width
                    se_source_gauge_middle.height = Math.min(backend.ToFDistanceLevel-0.6,0.2)* se_gauge_background.width
                    se_source_gauge_top.height = Math.min(backend.ToFDistanceLevel-0.8,0.2)* se_gauge_background.width
                }
            }

            Item{
                id: se_gauge_holder
                visible: se_tof_switch.position
                anchors.bottom: se_tof_level_slider.bottom
                anchors.top: se_tof_switch_label.top
                anchors.right: parent.right
                width: 15
                // Background Rectangle
                Rectangle{
                    id: se_gauge_background
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
                    id: se_source_gauge_base
                    height: parent.height*0.6
                    width: parent.width
                    anchors.bottom:se_gauge_holder.bottom
                    color: "#38f56e"
                }
                Rectangle{
                    id: se_source_gauge_middle
                    height: parent.height*0.2
                    width: parent.width
                    anchors.bottom:se_source_gauge_base.top
                    color: "#f59738"
                }
                Rectangle{
                    id: se_source_gauge_top
                    height: parent.height
                    width: parent.width
                    anchors.bottom:se_source_gauge_middle.top
                    color: "#f54b38"
                }
            }

        }

        // Max. Vol
        Item{
            id: settings_volume_item
            height: settings_row.height
            width: settings_row.width/4
            Label{
                id: se_volume_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: {"Max. Volume: " + se_volume_level_slider.value.toFixed(2)}
            }

            Slider {
                id: se_volume_level_slider
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.top: se_volume_label.bottom
                anchors.topMargin: -2
                onValueChanged: {
                        backend.getMaxVolume(se_volume_level_slider.value)
                }
            }

        }

        // Stats
        Item{
            id: settings_stats_item
            height: settings_row.height
            width: settings_row.width/4
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
                }
            }

            // Ambient Temp.
            Row{
                id: se_ambient_temp_row
                anchors.top: se_stats_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10       
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Ambient Temp.")
                }
                Label{
                    id: se_ambient_temp
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            // System Temp.
            Row{
                id: se_system_temp_row
                anchors.top: se_ambient_temp_row.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10       
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("System Temp.")
                }
                Label{
                    id: se_system_temp
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            // CPU Temp.
            Row{
                id: se_cpu_temp_row
                anchors.top: se_system_temp_row.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10       
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("CPU Temp.")
                }
                Label{
                    id: se_cpu_temp
                    anchors.verticalCenter: parent.verticalCenter
                }
            }

            // CPU Load
            Row{
                id: se_cpu_load_row
                anchors.top: se_cpu_temp_row.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10       
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("CPU Load")
                }
                Label{
                    id: se_cpu_load
                    anchors.verticalCenter: parent.verticalCenter
                }
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
                    text: qsTr("Channel enable")
            }
        CheckBox{
            id: channel_1
            checked: true
            Label{
                text: qsTr("1")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_2
            checked: true
            Label{
                text: qsTr("2")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_3
            checked: true
            Label{
                text: qsTr("3")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_4
            checked: true
            Label{
                text: qsTr("4")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_5
            checked: true
            Label{
                text: qsTr("5")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_6
            checked: true
            Label{
                text: qsTr("6")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_7
            checked: true
            Label{
                text: qsTr("7")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_8
            checked: true
            Label{
                text: qsTr("8")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_9
            checked: true
            Label{
                text: qsTr("9")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_10
            checked: true
            Label{
                text: qsTr("10")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_11
            checked: true
            Label{
                text: qsTr("11")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_12
            checked: true
            Label{
                text: qsTr("12")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_13
            checked: true
            Label{
                text: qsTr("13")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_14
            checked: true
            Label{
                text: qsTr("14")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_15
            checked: true
            Label{
                text: qsTr("15")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_16
            checked: true
            Label{
                text: qsTr("16")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_17
            checked: true
            Label{
                text: qsTr("17")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_18
            checked: true
            Label{
                text: qsTr("18")
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }
        CheckBox{
            id: channel_19
            checked: true
            Label{
                text: qsTr("19")
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