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
        height: main_window.height/4
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
                onTriggered: se_tof_label_curr_distance.text = backend.ToFDistance
            }

            // Current distance 
            Row{
                id: se_tof_row_curr_distance
                visible: se_tof_switch.position
                anchors.top: se_tof_row_distance.bottom
                anchors.topMargin: 10       
                anchors.horizontalCenter: parent.horizontalCenter
                spacing: 10
                Label{
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Current distance")
                }

                Label{
                    id: se_tof_label_curr_distance
                    anchors.verticalCenter: parent.verticalCenter
                    text: qsTr("Current distance")
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
                    anchors.bottomMargin: -settings_volume_item.height * 2
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
}