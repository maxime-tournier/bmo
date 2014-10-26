import QtQuick 1.0

Item {

	width: 0.75 * parent.width
	height: 0.9 * width

	anchors.horizontalCenter: parent.horizontalCenter

	Item {
		anchors.centerIn: parent
		
		width: 1.05 * parent.width
		height: 0.8 * parent.height
		
		Image {
			anchors.centerIn: parent
			anchors.fill: parent
			source: "buttons.png"
		}
	}
	
}
