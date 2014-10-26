import QtQuick 1.0
 
Rectangle {
	
	id: body
    width: 200
    height: 290
    color: "#23b1a5"


	Item {
		id: face

		width: 0.75 * parent.width
		height: 0.8 * width

		anchors.centerIn: body
		anchors.verticalCenterOffset:  -0.22 * parent.height

		Image {
			anchors.centerIn: parent
			anchors.fill: parent
			source: "face.png"
		}
		

		Item {
			width: parent.width
			height: parent.height
			
			anchors.centerIn: parent
			anchors.verticalCenterOffset: -0.15 * parent.height

		
			
			EyeSocket {
				id: leyesocket
				anchors.horizontalCenterOffset: -0.22 * face.width

				Item {
					width: 0
					height: 0
					objectName: 'leftCenter'
					anchors.centerIn: parent
				}
				
				Eye {
					id: leye
					objectName: 'leye'
				}

			}

			EyeSocket {
				id: reyesocket
				anchors.horizontalCenterOffset: 0.22 * face.width

				Item {
					width: 0
					height: 0
					objectName: 'rightCenter'
					anchors.centerIn: parent
				}
				
				
				Eye {
					id: reye
					objectName: 'reye'
				}

			}

			Mouth {
				id: mouth
				x: 0.5 * (leye.x + reye.x)
				y: 0.5 * (leye.y + reye.y) + 0.05 * parent.height
				
			}

		}
	}

	Buttons {
		anchors.top: face.bottom
		
	}
	
}

