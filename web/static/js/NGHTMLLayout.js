function CreateCanvasArea(PageLayout)
{

var CanvasArea = document.getElementById("CanvasArea");

//alert('SSHTMLLayout');
switch(parseInt(PageLayout & 0x0F))
{
	case 0: // layout is 1X1
	//alert('1X1');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td width="10%" onclick="setBack();" > </td><td  width="80%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(DialStart);" ondblclick="GetDialStyleInfo(DialStart);" width="201" height="201"></canvas></center></td><td width="10%" onclick="setNext();" > </td>' +
		'</tr>' +
		'<tr><td width="10%" onclick="setBack();" > </td><td ><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td><td width="10%" onclick="setNext();" > </td></tr>' +
		'</table>';

	break;

	case 1: // layout is 2X2
	//alert('2X2');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="201" height="201"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="201" height="201"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="201" height="201"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="201" height="201"></canvas></center></td>' +
		'</tr>' +
		'<tr><td colspan="2"><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td></tr>' +
		'</table>';
	break;

	case 2: // layout is 4X2
	//alert('4X2');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial4" onclick="SetSwitchState(4);" ondblclick="GetDialStyleInfo(4);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial5" onclick="SetSwitchState(5);" ondblclick="GetDialStyleInfo(5);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial6" onclick="SetSwitchState(6);" ondblclick="GetDialStyleInfo(6);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial7" onclick="SetSwitchState(7);" ondblclick="GetDialStyleInfo(7);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr><td colspan="4"><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="80"></canvas></center></td></tr>' +
		'</table>';
	break;

	case 3: // layout is 4X3
	//alert('4X3');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial4" onclick="SetSwitchState(4);" ondblclick="GetDialStyleInfo(4);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial5" onclick="SetSwitchState(5);" ondblclick="GetDialStyleInfo(5);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial6" onclick="SetSwitchState(6);" ondblclick="GetDialStyleInfo(6);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial7" onclick="SetSwitchState(7);" ondblclick="GetDialStyleInfo(7);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial8" onclick="SetSwitchState(8);" ondblclick="GetDialStyleInfo(8);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial9" onclick="SetSwitchState(9);" ondblclick="GetDialStyleInfo(9);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial10" onclick="SetSwitchState(10);" ondblclick="GetDialStyleInfo(10);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial11" onclick="SetSwitchState(11);" ondblclick="GetDialStyleInfo(11);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr><td colspan="4"><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td></tr>' +
		'</table>';
	break;

	case 4: // layout is 4X4
	//alert('4X4');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial4" onclick="SetSwitchState(4);" ondblclick="GetDialStyleInfo(4);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial5" onclick="SetSwitchState(5);" ondblclick="GetDialStyleInfo(5);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial6" onclick="SetSwitchState(6);" ondblclick="GetDialStyleInfo(6);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial7" onclick="SetSwitchState(7);" ondblclick="GetDialStyleInfo(7);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial8" onclick="SetSwitchState(8);" ondblclick="GetDialStyleInfo(8);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial9" onclick="SetSwitchState(9);" ondblclick="GetDialStyleInfo(9);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial10" onclick="SetSwitchState(10);" ondblclick="GetDialStyleInfo(10);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial11" onclick="SetSwitchState(11);" ondblclick="GetDialStyleInfo(11);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial12" onclick="SetSwitchState(12);" ondblclick="GetDialStyleInfo(12);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial13" onclick="SetSwitchState(13);" ondblclick="GetDialStyleInfo(13);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial14" onclick="SetSwitchState(14);" ondblclick="GetDialStyleInfo(14);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial15" onclick="SetSwitchState(15);" ondblclick="GetDialStyleInfo(15);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr><td colspan="4"><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td></tr>' +
		'</table>';
	break;

	case 5: // layout is 8X1
	//alert('8X1');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td  ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="150" height="150"></canvas></center></td>' +
		'<td  ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="150" height="150"></canvas></center></td>' +
		'<td  ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="150" height="150"></canvas></center></td>' +
		'<td  ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="150" height="150"></canvas></center></td>' +
		'<td  ><center><canvas id="canvasRadial4" onclick="SetSwitchState(4);" ondblclick="GetDialStyleInfo(4);" width="150" height="150"></canvas></center></td>' +
		'<td  ><center><canvas id="canvasRadial5" onclick="SetSwitchState(5);" ondblclick="GetDialStyleInfo(5);" width="150" height="150"></canvas></center></td>' +
		'<td  ><center><canvas id="canvasRadial6" onclick="SetSwitchState(6);" ondblclick="GetDialStyleInfo(6);" width="150" height="150"></canvas></center></td>' +
		'<td  ><center><canvas id="canvasRadial7" onclick="SetSwitchState(7);" ondblclick="GetDialStyleInfo(7);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr><td colspan="8"><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td></tr>' +
		'</table>';
	break;

	case 6: // layout is 1X8
	//alert('1X8');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td  ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  ><center><canvas id="canvasRadial4" onclick="SetSwitchState(4);" ondblclick="GetDialStyleInfo(4);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  ><center><canvas id="canvasRadial5" onclick="SetSwitchState(5);" ondblclick="GetDialStyleInfo(5);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  ><center><canvas id="canvasRadial6" onclick="SetSwitchState(6);" ondblclick="GetDialStyleInfo(6);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  ><center><canvas id="canvasRadial7" onclick="SetSwitchState(7);" ondblclick="GetDialStyleInfo(7);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr><td ><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td></tr>' +
		'</table>';
	break;

	case 7: // layout is 8X2
	//alert('8X2');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td  width="12%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial4" onclick="SetSwitchState(4);" ondblclick="GetDialStyleInfo(4);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial5" onclick="SetSwitchState(5);" ondblclick="GetDialStyleInfo(5);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial6" onclick="SetSwitchState(6);" ondblclick="GetDialStyleInfo(6);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial7" onclick="SetSwitchState(7);" ondblclick="GetDialStyleInfo(7);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="12%" ><center><canvas id="canvasRadial8" onclick="SetSwitchState(8);" ondblclick="GetDialStyleInfo(8);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial9" onclick="SetSwitchState(9);" ondblclick="GetDialStyleInfo(9);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial10" onclick="SetSwitchState(10);" ondblclick="GetDialStyleInfo(10);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial11" onclick="SetSwitchState(11);" ondblclick="GetDialStyleInfo(11);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial12" onclick="SetSwitchState(12);" ondblclick="GetDialStyleInfo(12);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial13" onclick="SetSwitchState(13);" ondblclick="GetDialStyleInfo(13);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial14" onclick="SetSwitchState(14);" ondblclick="GetDialStyleInfo(14);" width="150" height="150"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial15" onclick="SetSwitchState(15);" ondblclick="GetDialStyleInfo(15);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr><td colspan="4"><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td></tr>' +
		'</table>';
	break;

	

	case 8: // layout is 2X8
	//alert('2X8');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td  width="50%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="150" height="150"></canvas></center></td>' +
		'<td  width="50%" ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="50%" ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="150" height="150"></canvas></center></td>' +
		'<td  width="50%" ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="50%" ><center><canvas id="canvasRadial4" onclick="SetSwitchState(4);" ondblclick="GetDialStyleInfo(4);" width="150" height="150"></canvas></center></td>' +
		'<td  width="50%" ><center><canvas id="canvasRadial5" onclick="SetSwitchState(5);" ondblclick="GetDialStyleInfo(5);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="50%" ><center><canvas id="canvasRadial6" onclick="SetSwitchState(6);" ondblclick="GetDialStyleInfo(6);" width="150" height="150"></canvas></center></td>' +
		'<td  width="50%" ><center><canvas id="canvasRadial7" onclick="SetSwitchState(7);" ondblclick="GetDialStyleInfo(7);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="50%" ><center><canvas id="canvasRadial8" onclick="SetSwitchState(8);" ondblclick="GetDialStyleInfo(8);" width="150" height="150"></canvas></center></td>' +
		'<td  width="50%" ><center><canvas id="canvasRadial9" onclick="SetSwitchState(9);" ondblclick="GetDialStyleInfo(9);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="50%" ><center><canvas id="canvasRadial10" onclick="SetSwitchState(10);" ondblclick="GetDialStyleInfo(10);" width="150" height="150"></canvas></center></td>' +
		'<td  width="50%" ><center><canvas id="canvasRadial11" onclick="SetSwitchState(11);" ondblclick="GetDialStyleInfo(11);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="50%" ><center><canvas id="canvasRadial12" onclick="SetSwitchState(12);" ondblclick="GetDialStyleInfo(12);" width="150" height="150"></canvas></center></td>' +
		'<td  width="50%" ><center><canvas id="canvasRadial13" onclick="SetSwitchState(13);" ondblclick="GetDialStyleInfo(13);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="50%" ><center><canvas id="canvasRadial14" onclick="SetSwitchState(14);" ondblclick="GetDialStyleInfo(14);" width="150" height="150"></canvas></center></td>' +
		'<td  width="50%" ><center><canvas id="canvasRadial15" onclick="SetSwitchState(15);" ondblclick="GetDialStyleInfo(15);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr><td colspan="2"><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td></tr>' +
		'</table>';
	break;

	case 9: // layout is 16X1
	//alert('16X1');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial4" onclick="SetSwitchState(4);" ondblclick="GetDialStyleInfo(4);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial5" onclick="SetSwitchState(5);" ondblclick="GetDialStyleInfo(5);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial6" onclick="SetSwitchState(6);" ondblclick="GetDialStyleInfo(6);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial7" onclick="SetSwitchState(7);" ondblclick="GetDialStyleInfo(7);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial8" onclick="SetSwitchState(8);" ondblclick="GetDialStyleInfo(8);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial9" onclick="SetSwitchState(9);" ondblclick="GetDialStyleInfo(9);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial10" onclick="SetSwitchState(10);" ondblclick="GetDialStyleInfo(10);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial11" onclick="SetSwitchState(11);" ondblclick="GetDialStyleInfo(11);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial12" onclick="SetSwitchState(12);" ondblclick="GetDialStyleInfo(12);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial13" onclick="SetSwitchState(13);" ondblclick="GetDialStyleInfo(13);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial14" onclick="SetSwitchState(14);" ondblclick="GetDialStyleInfo(14);" width="150" height="150"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial15" onclick="SetSwitchState(15);" ondblclick="GetDialStyleInfo(15);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr><td colspan="16"><center><canvas id="canvasClock"  onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td></tr>' +
		'</table>';
	break;
	
	case 10: // layout is 5X3
	//alert('5X3');
		CanvasArea.innerHTML ='<table  width="100%">' +

		'<tr>' +
		'<td  width="15%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="150" height="150"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="150" height="150"></canvas></center></td>' +
		'<td  colspan="2" width="15%" ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="150" height="150"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="150" height="150"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial4" onclick="SetSwitchState(4);" ondblclick="GetDialStyleInfo(4);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="15%" ><center><canvas id="canvasRadial5" onclick="SetSwitchState(5);" ondblclick="GetDialStyleInfo(5);" width="150" height="150"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial6" onclick="SetSwitchState(6);" ondblclick="GetDialStyleInfo(6);" width="150" height="150"></canvas></center></td>' +
		'<td  colspan="2" width="15%" ><center><canvas id="canvasRadial7" onclick="SetSwitchState(7);" ondblclick="GetDialStyleInfo(7);" width="150" height="150"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial8" onclick="SetSwitchState(8);" ondblclick="GetDialStyleInfo(8);" width="150" height="150"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial9" onclick="SetSwitchState(9);" ondblclick="GetDialStyleInfo(9);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td  width="15%" ><center><canvas id="canvasRadial10" onclick="SetSwitchState(10);" ondblclick="GetDialStyleInfo(10);" width="150" height="150"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial11" onclick="SetSwitchState(11);" ondblclick="GetDialStyleInfo(11);" width="150" height="150"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial12" onclick="SetSwitchState(12);" ondblclick="GetDialStyleInfo(12);" width="50" height="75"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial13" onclick="SetSwitchState(13);" ondblclick="GetDialStyleInfo(13);" width="50" height="75"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial14" onclick="SetSwitchState(14);" ondblclick="GetDialStyleInfo(14);" width="150" height="150"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial15" onclick="SetSwitchState(15);" ondblclick="GetDialStyleInfo(15);" width="150" height="150"></canvas></center></td>' +
		'</tr>' +

		/*
		'<tr>' +
		'<td  width="15%" ><center><canvas id="canvasRadial16" onclick="SetSwitchState(16);" ondblclick="GetDialStyleInfo(16);" width="150" height="50"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial17" onclick="SetSwitchState(17);" ondblclick="GetDialStyleInfo(17);" width="150" height="50"></canvas></center></td>' +
		'<td  colspan="2" width="15%" ><center><canvas id="canvasRadial18" onclick="SetSwitchState(18);" ondblclick="GetDialStyleInfo(18);" width="150" height="50"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial19" onclick="SetSwitchState(19);" ondblclick="GetDialStyleInfo(19);" width="150" height="50"></canvas></center></td>' +
		'<td  width="15%" ><center><canvas id="canvasRadial20" onclick="SetSwitchState(20);" ondblclick="GetDialStyleInfo(20);" width="150" height="50"></canvas></center></td>' +
		'</tr>' +
		*/
		'</table>' +	
		'<table  width="100%">' +		
		'<tr>' +
		'<td  width="12%" ><center><canvas id="canvasRadial16" onclick="SetSwitchState(16);" ondblclick="GetDialStyleInfo(16);" width="150" height="50"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial17" onclick="SetSwitchState(17);" ondblclick="GetDialStyleInfo(17);" width="150" height="50"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial18" onclick="SetSwitchState(18);" ondblclick="GetDialStyleInfo(18);" width="150" height="50"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial19" onclick="SetSwitchState(19);" ondblclick="GetDialStyleInfo(19);" width="150" height="50"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial20" onclick="SetSwitchState(20);" ondblclick="GetDialStyleInfo(20);" width="150" height="50"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial21" onclick="SetSwitchState(21);" ondblclick="GetDialStyleInfo(21);" width="150" height="50"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial22" onclick="SetSwitchState(22);" ondblclick="GetDialStyleInfo(22);" width="150" height="50"></canvas></center></td>' +
		'<td  width="12%" ><center><canvas id="canvasRadial23" onclick="SetSwitchState(23);" ondblclick="GetDialStyleInfo(23);" width="150" height="50"></canvas></center></td>' +
		'</tr>' +

		'<tr><td colspan="8"><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td></tr>' +
		'</table>';
	break;
	
	case 11: // layout is 5X3
	//alert('5X3');
		CanvasArea.innerHTML ='<table  width="100%">' +

		'<tr>' +
		'<td  width="20%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="120" height="120"></canvas></center></td>' +
		'<td  width="20%" ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="140" height="120"></canvas></center></td>' +
		'<td  width="20%" ><center><canvas id="canvasRadial2" onclick="SetSwitchState(2);" ondblclick="GetDialStyleInfo(2);" width="140" height="120"></canvas></center></td>' +
		'<td  width="20%" ><center><canvas id="canvasRadial3" onclick="SetSwitchState(3);" ondblclick="GetDialStyleInfo(3);" width="140" height="120"></canvas></center></td>' +
		'<td  width="20%" ><center><canvas id="canvasRadial4" onclick="SetSwitchState(4);" ondblclick="GetDialStyleInfo(4);" width="120" height="120"></canvas></center></td>' +
		'</tr>' +
		
		'</table>' +	
		'<table  width="100%">' +		
		'<tr>' +
		'<td  width="100%" ><center> <div class="shadow" id="map_canvas" style="width:860px; height:400px; padding: 15px 5px 15px 5px;"  ></div></center></td>' +
		'</tr>' +

		'<tr><td colspan="8"><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" style="width:400px; height:50px; padding: 15px 5px 15px 5px;"></canvas></center></td></tr>' +
		'</table>';
	break;
	
	case 12: // layout is weather data
	//alert('5X3');
		CanvasArea.innerHTML ='<table  width="800px">' +

  		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial0" onclick="GetWeatherPage(0);"  width="201" height="201"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial1" onclick="GetWeatherPage(1);"  width="201" height="201"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial2" onclick="GetWeatherPage(2);"  width="201" height="201"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial3" onclick="GetWeatherPage(3);" width="201" height="201"></canvas></center></td>' +
		'</tr>' +
		'<tr>' +
		'<td colspan="1" width="25%" ><center><canvas id="canvasRadial4" onclick="GetWeatherPage(4);"  width="201" height="401"></canvas></center></td>' +
		'<td colspan="2" width="50%" ><center><canvas id="canvasRadial8" onclick="GetWeatherPage(8);"  width="401" height="401"></canvas></center></td>' +
		'<td colspan="1" width="25%" ><center><canvas id="canvasRadial5" onclick="GetWeatherPage(5);"  width="201" height="401"></canvas></center></td>' +
		
		'</tr>' +
		'<tr>' +
		'<td colspan="1" width="25%" ><center><canvas id="canvasRadial6" onclick="GetWeatherPage(6);"  width="201" height="401"></canvas></center></td>' +
		'<td colspan="2" width="50%" ><center><canvas id="canvasRadial9" onclick="GetWeatherPage(9);"  width="401" height="401"></canvas></center></td>' +
		'<td colspan="1" width="25%" ><center><canvas id="canvasRadial7" onclick="GetWeatherPage(7);"  width="201" height="401"></canvas></center></td>' +
		
		'</tr>' +
		'<tr><td colspan="4"><center><canvas id="canvasClock" onclick="GetConfigPage(0);" width="201" height="101"></canvas></center></td></tr>' +
		'<tr>' +
		'<td colspan="4">' +
		   
		'</td>' +
		'</tr>' +
		'</table>';
	break;
	
	case 13: // layout is 2X1
	//alert('2X1');
		CanvasArea.innerHTML ='<table>' +

		'<tr>' +
		'<td  width="25%" ><center><canvas id="canvasRadial0" onclick="SetSwitchState(0);" ondblclick="GetDialStyleInfo(0);" width="201" height="201"></canvas></center></td>' +
		'<td  width="25%" ><center><canvas id="canvasRadial1" onclick="SetSwitchState(1);" ondblclick="GetDialStyleInfo(1);" width="201" height="201"></canvas></center></td>' +
		'</tr>' +
		'<tr><td colspan="2"><center><canvas id="canvasClock" onclick="GetDialStyleInfo(0);" width="201" height="101"></canvas></center></td></tr>' +
		'<tr><td colspan="2" width="100%  width="25%" ><center><p align="center"><a href="#" onclick="resetFuelTotal(15,15,1);" id="resetFuel" class="persona-button"><span style="display:block; width:120px">Reset Total </span></a></center></td></tr>' +
		'</table>';
	break;

}
}