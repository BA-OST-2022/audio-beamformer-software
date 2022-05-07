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
        height: main_window.height/3*2
        anchors.left: parent.left
        anchors.right: parent.right
        anchors.top: parent.top
        
    }
}