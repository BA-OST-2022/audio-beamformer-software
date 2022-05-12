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

            // Enable
            Row{
                id: se_led_row_enable
                anchors.top: se_led_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10       
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Enable")
                }

                 Switch{
                    id: se_led_switch
                    anchors.verticalCenter: parent.verticalCenter
                    onReleased: {
                        backend.getEnableLED(se_led_switch.position)
                }
            }

            }
            // Brightness
            Row{
                id: se_led_row_level
                visible: se_led_switch.position
                anchors.top: se_led_row_enable.bottom
                anchors.topMargin: 10       
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Brightness")
                }

                Slider {
                    id: se_leds_level_slider
                    anchors.verticalCenter: parent.verticalCenter
                    onValueChanged: {
                        backend.getLEDBrightness(se_leds_level_slider.value)
                    }
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

            // Enable
            Row{
                id: se_tof_row_enable
                anchors.top: se_tof_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10       
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Enable")
                }

                 Switch{
                    id: se_tof_switch
                    anchors.verticalCenter: parent.verticalCenter
                    onReleased: {
                        backend.getEnableToF(se_tof_switch.position)
                }
            }

            }
            // Distance
            Row{
                id: se_tof_row_distance
                visible: se_tof_switch.position
                anchors.top: se_tof_row_enable.bottom
                anchors.topMargin: 10       
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Distance")
                }

                Slider {
                    id: se_tof_level_slider
                    anchors.verticalCenter: parent.verticalCenter
                    onValueChanged: {
                        backend.getToFDistance(se_tof_level_slider.value)
                    }
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
                anchors.bottom: parent.bottom
                anchors.right: parent.right
                width: 15
                height: 90
                anchors.bottomMargin: 110
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
                    color: "#37d417"
                }
                Rectangle{
                    id: se_source_gauge_middle
                    height: parent.height*0.2
                    width: parent.width
                    anchors.bottom:se_source_gauge_base.top
                    color: "#ffd70f"
                }
                Rectangle{
                    id: se_source_gauge_top
                    height: parent.height
                    width: parent.width
                    anchors.bottom:se_source_gauge_middle.top
                    color: "red"
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
                text: qsTr("Max. Volume")
            }

            Slider {
                    id: se_volume_level_slider
                    orientation: Qt.Vertical
                    anchors.horizontalCenter: parent.horizontalCenter
                    anchors.bottom: parent.bottom
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
        spacing: 5
        anchors.leftMargin: 10
        anchors.bottomMargin: 5
        Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Channel enable")
            }
        CheckBox{
            id: channel_1
            checked: true
        }
        CheckBox{
            id: channel_2
            checked: true
        }
        CheckBox{
            id: channel_3
            checked: true
        }
        CheckBox{
            id: channel_4
            checked: true
        }
        CheckBox{
            id: channel_5
            checked: true
        }
        CheckBox{
            id: channel_6
            checked: true
        }
        CheckBox{
            id: channel_7
            checked: true
        }
        CheckBox{
            id: channel_8
            checked: true
        }
        CheckBox{
            id: channel_9
            checked: true
        }
        CheckBox{
            id: channel_10
            checked: true
        }
        CheckBox{
            id: channel_11
            checked: true
        }
        CheckBox{
            id: channel_12
            checked: true
        }
        CheckBox{
            id: channel_13
            checked: true
        }
        CheckBox{
            id: channel_14
            checked: true
        }
        CheckBox{
            id: channel_15
            checked: true
        }
        CheckBox{
            id: channel_16
            checked: true
        }
        CheckBox{
            id: channel_17
            checked: true
        }
        CheckBox{
            id: channel_18
            checked: true
        }
        CheckBox{
            id: channel_19
            checked: true
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