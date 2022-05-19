import QtQuick 2.15
import QtQuick.Window 2.15
import QtQuick.Controls 2.15
import QtQuick.Controls.Material 2.15
import QtQuick.Controls.Styles 1.4
import QtQuick.Extras 1.4

Item {
    anchors.fill: parent
    Image{
        id: load_image
        source: backend.loadingImage
        width: 1200
        anchors.top: parent.top
        anchors.topMargin: 20
        anchors.horizontalCenter: parent.horizontalCenter
        fillMode: Image.PreserveAspectFit
    }
    BusyIndicator {
        anchors.bottom: parent.bottom
        anchors.bottomMargin: 75
        running: true
        anchors.horizontalCenter: parent.horizontalCenter
    }
}