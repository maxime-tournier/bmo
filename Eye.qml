import QtQuick 1.0

// CenteredText {
// 	text: '◕'
// 	color: 'black'

// 	font.pixelSize: 2 * parent.height
	
// 	width: parent.width
// 	height: parent.height
	
// }

Item {
	anchors.centerIn: parent
	width: parent.width
	height: parent.height

	
	Image {
		anchors.centerIn: parent
		anchors.fill: parent
		fillMode: Image.PreserveAspectCrop
		source: "eye.png"
	}
}
