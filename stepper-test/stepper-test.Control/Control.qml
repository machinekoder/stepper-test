import QtQuick 2.0
import QtQuick.Controls 1.1
import QtQuick.Layouts 1.1
import Machinekit.Controls 1.0
import Machinekit.HalRemote.Controls 1.0
import Machinekit.HalRemote 1.0

HalApplicationWindow {
    id: main

    name: "control"
    title: qsTr("Control")

    ColumnLayout {
        anchors.fill: parent
        anchors.margins: 10

        Item {
            Layout.fillHeight: true
        }
        HalSlider {
            Layout.fillWidth: true
            name: "vel-cmd"
            minimum: -1.0
            maximum: 1.0
        }
        HalButton {
            Layout.alignment: Layout.Center
            name: "enable"
            text: "Enable"
            checkable: true
        }
        Item {
            Layout.fillHeight: true
        }
    }
}

