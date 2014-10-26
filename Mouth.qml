import QtQuick 1.0

// CenteredText {

// 	// text: '‿'
// 	text: '◡'
// 	color: 'black'

// 	width: 0.3 * parent.width
// 	height: 0.1 * parent.height

// 	font.pixelSize: width
	
// 	anchors.centerIn: parent
// 	anchors.verticalCenterOffset: 0.05 * parent.height
// }
Item {
	// anchors.centerIn: parent
	width: parent.width
	height: parent.height

	Image {
		width: 0.1 * parent.width
		height: 0.1 * parent.height
		
		anchors.centerIn: parent
		anchors.verticalCenterOffset: 0.05 * parent.height
		
		fillMode: Image.PreserveAspectCrop
		source: "mouth.png"
	}
}
