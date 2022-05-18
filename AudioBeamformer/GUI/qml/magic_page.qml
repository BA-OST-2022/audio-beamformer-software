import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4
import QtCharts 2.15

 // Audio processing
Item{
    id: magic_mode_main
    anchors.left: parent.left
    anchors.right: parent.right
    anchors.top: parent.top
    anchors.bottom: parent.bottom
    anchors.leftMargin: -10
    visible: !audio_processing_button.checked && !channel_button.checked && !setting_button.checked

    Rectangle{
        anchors.fill: parent
    }
}