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
                    model: ["First", "Second", "Third"]
                }

            }
            Gauge {
                id: ap_source_gauge
                value: 0.5
                anchors.right: parent.right
                anchors.topMargin: 5
                anchors.bottomMargin: 5 
                anchors.top: parent.top
                anchors.bottom: parent.bottom
            }
            Dial{
                id: ap_source_dial
                anchors.top: ap_source_row_input_source.bottom
                anchors.topMargin: 10   
                anchors.horizontalCenter: parent.horizontalCenter
            }
        }

        // Equalizer
        Item{
            id: audio_processing_equalizer_item
            height: audio_processing_settings_row.height
            width: audio_processing_settings_row.width/4
            Label{
                id: ap_equalizer_label
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Equalizer")
            }
            Switch{
                id: ap_equalizer_switch
                text: qsTr("Enable")
                anchors.top: ap_equalizer_label.bottom
                anchors.horizontalCenter: parent.horizontalCenter
                anchors.topMargin: 10
            }


        }

        // Interpolation
        Item{
            id: audio_processing_interpolation_item
            height: audio_processing_settings_row.height
            width: audio_processing_settings_row.width/4
            Label{
                anchors.top: parent.top
                anchors.topMargin: 8
                font.pixelSize: 20  
                anchors.horizontalCenter: parent.horizontalCenter
                text: qsTr("Interpolation")
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