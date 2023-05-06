// This Script changes styles for dials SeaSmart.net NMEA 2000 data
// Written 11/01/12
// Chetco Digital Instruments
//


//***************************************************
//  Globals 
//***************************************************
var DialEnd = 1;
var NumOfDials = new Array(1,4,8,12,16,8,8,16,16,16);
var DialSize = new Array(400,300,200,150,200,200,200,200,200,200);
var MaxPages = 1;
var MaxDials = 16;
var DialValid  = new Array(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);

var DialTimes = new Array(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);

// Switch Globals
var SwitchState  = new Array(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
var flashSwitchState  = new Array(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
var gSwitchStates="00000000"
var SwitchPGN = "$PCDIN,01F20E,00000000,00,0000000000FFFFFF*24";
var UpdateSwitch = 0;

var xdr;
var datafile; 
var logdatafile;
var CurrentDialID;
var CurrentCanvasID = 0;
var radialDial  = new Array();

var ClockLCD;

var gsections;
var gareas;

var gDialSections = new Array();
var gDialGradients = new Array();

var DialSettings;
var DialID =0;




// Sets the current page layout
function SetPageLayout(sel) 
{
 
PageLayout = sel.selectedIndex ;

SavePageCookies();

}

// Updates all the gauges on the pages with data returned from a 
// recent GetN2KData
//
function ProcessPageGaugeUpdates(mydata)
{
var CanvasIndex=0;
var N2KValues = new Array();
var DialIndex;

              // Get System Time
              N2KValues = GetPGN126992(mydata, SystemClockPGNID );

              if(N2KValues.length > 0)
                 ClockLCD.setValue(N2KValues.pop());  // Time       

             // calculate current end dail based on start dial and page layout
              //
              DialEnd = getEndDial(DialStart, PageLayout);
    
              // Get PGN data for each dial
              for(DialIndex=DialStart; DialIndex < DialEnd; DialIndex++) //
              {   
                  N2KValues =  GetPGNbyNumber(String(mydata), DialPGNInstance[DialIndex], DialPGNNumber[DialIndex], DialPGNParameter[DialIndex], DialUnits[DialIndex] );
				   UpdateDialValues(CanvasIndex++, N2KValues);
              }

              // Fill in Dial values from Parsed PGNs
              // Update each dial
            //  for(DialIndex=DialStart; DialIndex < DialEnd; DialIndex++) //
            //  {   
             //     UpdateDialValues(CanvasIndex++, N2KValues[DialIndex]);
             // }

}

function ToggleSwitchState(Index, mode) {
var myPGNValue ;

myPGNValue = gSwitchStates.charAt(Index);                                 


	if(mode == 0)
	{
		if (myPGNValue == '0')
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '1' + gSwitchStates.substr(Index +1);
			return 1;
		}
		else if (myPGNValue == '1')
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '0' + gSwitchStates.substr(Index +1);
			return 0;
		}
		else if (myPGNValue == '4')
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '5' + gSwitchStates.substr(Index +1);
			return 1;
		}
		else if (myPGNValue == '5')
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '4' + gSwitchStates.substr(Index +1);
			return 0;
		}
		else
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '0' + gSwitchStates.substr(Index +1);
			return 0;
		}
	}
	else if (mode == 1)
		{
		if (myPGNValue == '0')
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '4' + gSwitchStates.substr(Index +1);
			return 1;
		}
		else if (myPGNValue == '1')
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '5' + gSwitchStates.substr(Index +1);
			return 1;
		}
		else if (myPGNValue == '4')
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '0' + gSwitchStates.substr(Index +1);
			return 0;
		}
		else if (myPGNValue == '5')
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '1' + gSwitchStates.substr(Index +1);
			return 0;
		}
		else
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '0' + gSwitchStates.substr(Index +1);
			return 0;
		}
	}
}

function SetgSwitchState(Index, mode, value) {
var myPGNValue ;

myPGNValue = gSwitchStates.charAt(Index);                                 


	if(mode == 0)
	{
		if (myPGNValue == '0' && value == 1)
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '1' + gSwitchStates.substr(Index +1);
			return 1;
		}
		else if (myPGNValue == '1' && value == 0)
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '0' + gSwitchStates.substr(Index +1);
			return 0;
		}
		else if (myPGNValue == '4' && value == 1)
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '5' + gSwitchStates.substr(Index +1);
			return 1;
		}
		else if (myPGNValue == '5' && value == 0)
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '4' + gSwitchStates.substr(Index +1);
			return 0;
		}
		else
		{
			//gSwitchStates = gSwitchStates.substr(0, Index) + '0' + gSwitchStates.substr(Index +1);
			return value;
		}
	}
	else if (mode == 1)
		{
		if (myPGNValue == '0' && value == 1)
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '4' + gSwitchStates.substr(Index +1);
			return 1;
		}
		else if (myPGNValue == '1' && value == 1)
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '5' + gSwitchStates.substr(Index +1);
			return 1;
		}
		else if (myPGNValue == '4' && value == 0)
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '0' + gSwitchStates.substr(Index +1);
			return 0;
		}
		else if (myPGNValue == '5' && value == 0)
		{
			gSwitchStates = gSwitchStates.substr(0, Index) + '1' + gSwitchStates.substr(Index +1);
			return 0;
		}
		else
		{
			// gSwitchStates = gSwitchStates.substr(0, Index) + '0' + gSwitchStates.substr(Index +1);
			return value;
		}
	}
}

function SetgSwitchStates(Index, value) {
var vSwitchState = new Array();

			switch(Index)
			{
					case 0:
					vSwitchState[0] = SetgSwitchState(1, 0, value);
					break;

					case 1:
					vSwitchState[1] = SetgSwitchState(1, 1, value);
					break;

					case 2:
					vSwitchState[2] = SetgSwitchState(0, 0, value);
					break;

					case 3:
					vSwitchState[3] = SetgSwitchState(0, 1, value);
					break;

					case 4:
					vSwitchState[4] = SetgSwitchState(3, 0, value);
					break;

					case 5:
					vSwitchState[5] = SetgSwitchState(3, 1, value);
					break;

					case 6:
					vSwitchState[6] = SetgSwitchState(2, 0, value);
					break;

					case 7:
					vSwitchState[7] = SetgSwitchState(2, 1, value);
					break;

					case 8:
					vSwitchState[8] = SetgSwitchState(5, 0, value);
					break;

					case 9:
					vSwitchState[9] = SetgSwitchState(5, 1, value);
					break;

					case 10:
					vSwitchState[10] = SetgSwitchState(4, 0, value);
					break;

					case 11:
					vSwitchState[11] = SetgSwitchState(4, 1, value);
					break;

					case 12:
					vSwitchState[12] = SetgSwitchState(7, 0, value);
					break;

					case 13:
					vSwitchState[13] = SetgSwitchState(7, 1, value);
					break;

					case 14:
					vSwitchState[14] = SetgSwitchState(6, 0, value);
					break;

					case 15:
					vSwitchState[15] = SetgSwitchState(6, 1, value);
					break;
	

			}
}

function SetSwitchState(myCurrentCanvas) {

var SwitchInstance;
var myPGNValue ;
var mySwitchID;



myDialID = parseInt(myCurrentCanvas) + parseInt(DialStart);

	if(DialType[myDialID] == 16) // must be a switch and not a  indicator
	{

		mySwitchID = DialPGNParameter[myDialID];

		SwitchInstance = '0' + DialPGNInstance[myDialID].toString(16);

			switch(mySwitchID)
			{
					case 0:
					SwitchState[0] = ToggleSwitchState(1, 0);
					break;

					case 1:
					SwitchState[1] = ToggleSwitchState(1, 1);
					break;

					case 2:
					SwitchState[2] = ToggleSwitchState(0, 0);
					break;

					case 3:
					SwitchState[3] = ToggleSwitchState(0, 1);
					break;

					case 4:
					SwitchState[4] = ToggleSwitchState(3, 0);
					break;

					case 5:
					SwitchState[5] = ToggleSwitchState(3, 1);
					break;

					case 6:
					SwitchState[6] = ToggleSwitchState(2, 0);
					break;

					case 7:
					SwitchState[7] = ToggleSwitchState(2, 1);
					break;

					case 8:
					SwitchState[8] = ToggleSwitchState(5, 0);
					break;

					case 9:
					SwitchState[9] = ToggleSwitchState(5, 1);
					break;

					case 10:
					SwitchState[10] = ToggleSwitchState(4, 0);
					break;

					case 11:
					SwitchState[11] = ToggleSwitchState(4, 1);
					break;

					case 12:
					SwitchState[12] = ToggleSwitchState(7, 0);
					break;

					case 13:
					SwitchState[13] = ToggleSwitchState(7, 1);
					break;

					case 14:
					SwitchState[14] = ToggleSwitchState(6, 0);
					break;

					case 15:
					SwitchState[15] = ToggleSwitchState(6, 1);
					break;
	

			}


			SwitchPGN = "$PCDIN,01F20E,00000000,00,0000000000FFFFFF*24";

				SwitchPGN = SwitchPGN.substr(0, 26) + SwitchInstance + gSwitchStates + SwitchPGN.substr(36);

		UpdateSwitch = 1;

		//alert(radialDial[parseInt(myDialID)]);

		 radialDial[myDialID].setflashing(true);
		 flashSwitchState[myDialID]=1;

	}
}


function GetDialStyleInfo(myCurrentCanvas) {
 
// alert("Ive been clicked");
myDialID = parseInt(myCurrentCanvas) + parseInt(DialStart);
CurrentDialID = myDialID;
CurrentCanvasID = myCurrentCanvas;

///alert(myDialID);

ShowHideTabBar(true);

	//	ele.style.display = "block";


document.getElementById("PageLayout").selectedIndex = PageLayout;

document.getElementById("DialID").selectedIndex = myDialID;
document.getElementById("PGNDialID").selectedIndex = myDialID;
document.getElementById("UpdateInterval").selectedIndex = UpdateInterval/1000;
document.getElementById("PGNTimeout").selectedIndex = DialTimeout;

document.getElementById("DialLabel").value = DialText[myDialID];
document.getElementById("DialUnits").selectedIndex = DialUnits[myDialID];
document.getElementById("MinDial").value = DialMin[myDialID];
document.getElementById("MaxDial").value = DialMax[myDialID];
document.getElementById("Alarm").value = DialAlarm[myDialID];
document.getElementById("AlarmState").value = DialAlarmState[myDialID];

  document.getElementById("PGNNumber").value = DialPGNNumber[myDialID];
  SetPGNParamatersOptionList(DialPGNNumber[myDialID]);
  SetPGNInstanceOptionList(DialPGNNumber[CurrentDialID]);

    document.getElementById("PGNParameterID").selectedIndex = DialPGNParameter[myDialID];
	document.getElementById("PGNInstance").selectedIndex = DialPGNInstance[myDialID];

	//alert(DialFrameType[myDialID]);

	document.getElementById("DialLabel").value = DialText[myDialID];
	document.getElementById("DialType").selectedIndex  = DialType[myDialID];
	document.getElementById("FrameStyle").selectedIndex  = DialFrameType[myDialID];
	document.getElementById("PointerStyle").selectedIndex  = DialPonterType[myDialID];
	document.getElementById("DialBackground").selectedIndex  = DialBackground[myDialID];
	document.getElementById("DialPointerColor").selectedIndex  = DialPointerColor[myDialID];
	document.getElementById("DialLcdColor").selectedIndex  = DialLCDColor[myDialID];
	document.getElementById("ClockLcdColor").selectedIndex  = ClockLCDColor;
	document.getElementById("PageBckColor").selectedIndex  = PageBackGroundColor;

} // end of function GetDialStyleInfo

function ShowHideTabBar(showhide) {

	if(showhide == true)
		document.getElementById("TabBar").style.display = "block";
	else
		document.getElementById("TabBar").style.display = "none";
}

function ShowHideDialParameters(showhide) {

	if(showhide == true)
		document.getElementById("DialStyleParameters").style.display = "block";
	else
		document.getElementById("DialStyleParameters").style.display = "none";
}


function ShowHidePGNs(showhide) {

	if(showhide == true)
		document.getElementById("PGNParameters").style.display = "block";
	else
		document.getElementById("PGNParameters").style.display = "none";
}

function ShowHidePageParams(showhide) {

	if(showhide == true)
		document.getElementById("PageParameters").style.display = "block";
	else
		document.getElementById("PageParameters").style.display = "none";
}

function ShowHideAccountParams(showhide) {

	if(showhide == true)
		document.getElementById("AccountParameters").style.display = "block";
	else
		document.getElementById("AccountParameters").style.display = "none";

}
// *****************************************************************************
// Takes returned values from parsed NMEA 2000 data and populates dials values
// DialIndex = Dial to update
// myNewValue = parsed NMEA 2000 value
//
function UpdateDialValues(DialIndex,  myNewDialValue)
{
var myWindDir = new Array();
var ATWindData = new String;
var PitchRollData = new String;
var myPitchRoll = new Array();
var currentTime = new Date();
var currentState;

var i;
//exp.setTime(exp.getTime() + (30 * 24 * 60 * 60 * 1000));
//alert(myNewDialValue);
    //try
	{
		if( myNewDialValue == null || myNewDialValue.length == 0)
		{

		
			// If data was valid but no is not there then disable dial
			// otherwise do nothing since it was already disabled
			if(DialValid[DialIndex] == 0)
			{ 

			//alert(DialTimes[DialIndex]);

				
				if(DialTimes[DialIndex] < DialTimeout )
				{
					DialTimes[DialIndex] = DialTimes[DialIndex] + 1;
					return;
				}

					//alert("data valid before = 0 " + DialIndex + "  " + DialValid);
				radialDial[DialIndex].setShowDialFace(false);

				//radialDial[DialIndex].setValue(0);
				DialValid[DialIndex] = 1;
				//alert("data valid after = 0 " + DialIndex + "  " + DialValid);

			}
		} // end of no new data
		else // data is good 
		{
			// data is good so enable any dials that were previously disabled and show data
			if(DialValid[DialIndex] == 1)
			{
				//alert("data valid = 1 " + DialIndex);
				radialDial[DialIndex].setShowDialFace(true);
				DialValid[DialIndex] = 0;
			}

			DialTimes[DialIndex] = 0;

			if(DialType[DialIndex] == 8) // Wind Direction
			{
				//var myWindDir = new Array();
				
				//var ATWindData = new String;

			//	alert(myNewDialValue + "   " + myNewDialValue.length);

				for(i=0; i< myNewDialValue.length; i++)
				{
						ATWindData = String(myNewDialValue.pop());

						myWindDir = ATWindData.split(":");

					//	alert("myWindDir = " + myWindDir + "  " + myWindDir.length);

						if(myWindDir.length == 2)
						{
							//alert(myWindDir);
							if(myWindDir[1] == "A")
								radialDial[DialIndex].setValueAnimatedLatest(myWindDir[0]);
							else if(myWindDir[1] == "T")
								radialDial[DialIndex].setValueAnimatedAverage(myWindDir[0]);
						}
						else
						{
							if(myNewDialValue.length != 0)
							radialDial[DialIndex].setValueAnimatedLatest(ATWindData);
						}
				}

			}

			else if(DialType[DialIndex] == 10) // Pitch Roll
			{


				PitchRollData = String(myNewDialValue.pop());

				myPitchRoll = PitchRollData.split(":");
				
				if(myPitchRoll.length == 2)
				{
					radialDial[DialIndex].setPitchAnimated(myPitchRoll[0]);
					radialDial[DialIndex].setRollAnimated(myPitchRoll[1]);
				}
				else
				{
					radialDial[DialIndex].setShowDialFace(false);
					radialDial[DialIndex].setPitchAnimated(0);
					radialDial[DialIndex].setRollAnimated(0);
					DialValid[DialIndex] = 1;
				}
			}
			else if(DialType[DialIndex] == 15 || DialType[DialIndex] == 16) // indicator status  0=off 255=0n
			{

				if(myNewDialValue.length != 0)
				{
				

				//alert(myNewDialValue.length + "    " + myNewDialValue);

				
				// possible myNewDialValue values are 0 or 255
				currentState = myNewDialValue.pop();
				//alert(currentState);

					if(currentState >= DialAlarm[DialIndex])
					{
						setLcdColor(DialIndex, parseInt(DialPointerColor[DialIndex]));

							SetgSwitchStates(DialIndex, 1);

						if(SwitchState[DialIndex] == 1)
						 radialDial[DialIndex].setflashing(false);
							

					}
					else if(currentState < DialAlarm[DialIndex])
					{
						setLcdColor(DialIndex,DialLCDColor[DialIndex]);	

						 SetgSwitchStates(DialIndex, 0);

						if(SwitchState[DialIndex] == 0)
						 radialDial[DialIndex].setflashing(false);


					}

					//radialDial[DialIndex].setValueAnimated(myNewDialValue.pop());
				}
			}
			else
			{
					//alert(myNewDialValue.length + "    " + myNewDialValue);
				if(myNewDialValue != null)
				{

					if(myNewDialValue.length != 0)
					radialDial[DialIndex].setValueAnimated(myNewDialValue.pop());
					//radialDial[DialIndex].setValue(myNewDialValue);
				}
			}

		 } // end of good new data
    }
   // catch (err)
    {
    //  alert("we got an error");
    }

}

 function setPGNTimeout(sel) {

	DialTimeout = (sel.options[sel.selectedIndex].value);
}

function setUpdateInterval(sel) {

	UpdateInterval = (sel.options[sel.selectedIndex].value) * 1000;
}

// Sets the current dial Id
  function setDialID(sel) {

	CurrentDialID = parseInt(sel.options[sel.selectedIndex].value);

	document.getElementById("DialID").selectedIndex = CurrentDialID;
	document.getElementById("PGNDialID").selectedIndex = CurrentDialID;
	document.getElementById("PGNTimeout").selectedIndex = DialTimeout;
	document.getElementById("UpdateInterval").selectedIndex = UpdateInterval/1000;

    document.getElementById("PGNNumber").value = DialPGNNumber[CurrentDialID];
	SetPGNParamatersOptionList(DialPGNNumber[CurrentDialID]);
	SetPGNInstanceOptionList(DialPGNNumber[CurrentDialID]);

    document.getElementById("PGNParameterID").selectedIndex = DialPGNParameter[CurrentDialID];

	document.getElementById("DialType").selectedIndex  = DialType[CurrentDialID];
	document.getElementById("DialLabel").value = DialText[CurrentDialID];
	
	document.getElementById("FrameStyle").selectedIndex  = DialFrameType[CurrentDialID];
	document.getElementById("PointerStyle").selectedIndex  = DialPonterType[CurrentDialID];
	document.getElementById("DialBackground").selectedIndex  = DialBackground[CurrentDialID];
	document.getElementById("DialPointerColor").selectedIndex  = DialPointerColor[CurrentDialID];
	document.getElementById("DialLcdColor").selectedIndex  = DialLCDColor[CurrentDialID];
	document.getElementById("ClockLcdColor").selectedIndex  = ClockLCDColor;
	document.getElementById("PageBckColor").selectedIndex  = PageBackGroundColor;

	document.getElementById("DialUnits").selectedIndex = DialUnits[CurrentDialID];
	document.getElementById("MinDial").value = DialMin[CurrentDialID];
	document.getElementById("MaxDial").value = DialMax[CurrentDialID];
	document.getElementById("Alarm").value = DialAlarm[CurrentDialID];
	document.getElementById("AlarmState").value = DialAlarmState[CurrentDialID];
		
    }

// Sets the current dial Label Text
function SetDialLabel(sel) 
{
var myText;
 
var myDialID = document.getElementById("DialID").selectedIndex ;

       myText = sel.value;

	//	alert(myText);
		//	alert(CurrentDialID);

	radialDial[CurrentDialID].setTitleString(myText);
	DialText[CurrentDialID] = myText ;
}

// Sets the current dial Units Text
function updateDialUnits(sel) 
{
var myDialID = document.getElementById("DialID").selectedIndex ;

	
		DialUnits[myDialID] = sel.options[sel.selectedIndex].value;

	SetDialUnits(myDialID, sel.options[sel.selectedIndex].value);
}
// Sets the current dial Units Text
function SetDialUnits(DialID, UnitsID) 
{

//<option value="0">Fahrenheit</option>
//<option value="1">Celsius</option>
//<option value="2">Kelvin</option>
//<option value="3">- - -</option>   
//<option value="4">Knots</option>
//<option value="5">MPH</option>
//<option value="6">KPH</option>
//<option value="7">- - -</option>
//<option value="8">PSI</option>
//<option value="9">KPASCAL</option>
//<option value="10">INHG</option>
//<option value="11">- - -</option>
//<option value="12">TRUE</option>
//<option value="13">MAGNETIC</option>
//<option value="14">- - -</option>
//<option value="15">- - -</option>
//<option value="16">DEGREES</option>
//<option value="17">Radians</option>
//<option value="18">- - -</option>
//<option value="19">- - -</option>
//<option value="20">Liters</option>
//<option value="21">Gallons</option>
//<option value="22">CubicMeter</option>
//<option value="23">- - -</option>
//<option value="24">RPM</option>
//<option value="25">%</option>
//<option value="26">Volts</option>
//<option value="27">Amps</option>       
	

	switch (parseInt(UnitsID)) 
	{
        case 0:
			radialDial[DialID].setUnitString("Fahrenheit");
		break;

		case 1:
			radialDial[DialID].setUnitString("Celsius");
		break;

		case 2:
			radialDial[DialID].setUnitString("Kelvin");
		break;

		case 4:
			radialDial[DialID].setUnitString("Knots");
		break;
		
		case 5:
			radialDial[DialID].setUnitString("MPH");
		break;

		case 6:
			radialDial[DialID].setUnitString("KPH");
		break;

		case 8:
			radialDial[DialID].setUnitString("PSI");
		break;

		case 9:
			radialDial[DialID].setUnitString("KPASCAL");
		break;

		case 10:
			radialDial[DialID].setUnitString("INHG");
		break;

		case 12:
			radialDial[DialID].setUnitString("TRUE");
		break;

		case 13:
			radialDial[DialID].setUnitString("MAGNETIC");
		break;

		case 16:
			radialDial[DialID].setUnitString("DEGREES");
		break;
		
		case 17:
			radialDial[DialID].setUnitString("Radians");
		break;

		case 20:
			radialDial[DialID].setUnitString("Liters");
		break;

		case 21:
			radialDial[DialID].setUnitString("Gallons");
		break;

		case 22:
			radialDial[DialID].setUnitString("CubicMeter");
		break;

		case 24:
			radialDial[DialID].setUnitString("RPM");
		break;

		case 25:
			radialDial[DialID].setUnitString("RPS");
		break;

		case 26:
			radialDial[DialID].setUnitString("%");
		break;

		case 27:
			radialDial[DialID].setUnitString("Volts");
		break;

		case 28:
			radialDial[DialID].setUnitString("Amps");
		break;

		case 30:
			radialDial[DialID].setUnitString("Meters");
		break;

		case 31:
			radialDial[DialID].setUnitString("Feet");
		break;

		case 32:
			radialDial[DialID].setUnitString("Fathoms");
		break;

		case 34:
			radialDial[DialID].setUnitString("Indicator");
		break;

		case 35:
			radialDial[DialID].setUnitString("Switch");
		break;

		case 37:
			radialDial[DialID].setUnitString("undefined");
		break;


	}
       
}


// Sets the current dial Minimum
function SetDialMin(sel) 
{
var myMin;
	var myDialID = document.getElementById("DialID").selectedIndex ;

	//alert(myDialID);

		// reset Units list to last value = undefined
	
	
        myMin = parseInt(sel.value);

	//	alert(myMin);

	DialMin[myDialID] = myMin;
		//	alert(CurrentDialID);

	radialDial[CurrentDialID].setMinValue(myMin);

	createDialSections(myDialID,DialMin[myDialID],DialMax[myDialID]);
	createDialGradients(myDialID,DialMin[myDialID],DialMax[myDialID]);
}

// Sets the current dial Maximum
function SetDialMax(sel) 
{
var myMax;
var myDialID = document.getElementById("DialID").selectedIndex ;
        myMax = parseInt(sel.value);

	//	alert(myDialID);


		//	alert(myMax);
	DialMax[myDialID] = myMax;
	//alert(DialMax[myDialID]);
	radialDial[CurrentDialID].setMaxValue(myMax);
	createDialSections(myDialID,DialMin[myDialID],DialMax[myDialID]);
	createDialGradients(myDialID,DialMin[myDialID],DialMax[myDialID]);

}

// Sets the current dial Alarm
function SetDialAlarm(sel) 
{
var myAlarm;
var myDialID = document.getElementById("DialID").selectedIndex ;
        myAlarm = parseInt(sel.value);

	//	alert(myDialID);


		//	alert(myMax);
	DialAlarm[myDialID] = myAlarm;
	//alert(DialMax[myDialID]);
	radialDial[CurrentDialID].setThreshold(myAlarm);

}

// Selects the current dial Alarm
function SelectAlarmState(sel) 
{
 var myDialID = document.getElementById("DialID").value ;

		DialAlarmState[myDialID] = sel.selectedIndex;

		var myDialID = document.getElementById("DialID").selectedIndex ;

		SetAlarmState(myDialID, parseInt(sel.selectedIndex))
}

// Selects the current dial Alarm
function SetAlarmState(CurrentDialID, AlarmState) {
var i;

        switch (parseInt(AlarmState)) {
        case 0: // Dial Alarm Disabled
            radialDial[CurrentDialID].setAlarmInvert(0);
			radialDial[CurrentDialID].setPlayAlarm(false);
        break;

        case 1: // Dial Alarm active High
          radialDial[CurrentDialID].setAlarmInvert(1);
		  radialDial[CurrentDialID].setPlayAlarm(false);
        break;

        case 2: // Dial Alarm active Low
           radialDial[CurrentDialID].setAlarmInvert(2);
		   radialDial[CurrentDialID].setPlayAlarm(false);
        break;

		case 3: // Dial Alarm active High with sound
            radialDial[CurrentDialID].setAlarmInvert(1);
			radialDial[CurrentDialID].setPlayAlarm(true);
        break;

        case 4: // Dial Alarm active Low with sound
          radialDial[CurrentDialID].setAlarmInvert(2);
		  radialDial[CurrentDialID].setPlayAlarm(true);
        break;

        case 5: // disable all audio
			for(i=0; i<8; i++)
				radialDial[i].setPlayAlarm(false);
         break;



        Default:
			radialDial[CurrentDialID].setAlarmInvert(0);
			radialDial[CurrentDialID].setPlayAlarm(false);
         break;
        }
}

function createDialSections(DialIndex, min, max  )
{
var s0,s1,s2,s3;
var TemperatureSections;


s0 = parseInt(min);
s1 = Math.floor((max - min)* 0.333);
s2 = Math.floor((max - min)* 0.666);
s3 = parseInt(max);

gDialSections[DialIndex] = [steelseries.Section(s0, s1, 'rgba(0, 0, 220, 0.3)'),
			steelseries.Section(s1, s2, 'rgba(0, 220, 0, 0.3)'),
			steelseries.Section(s2, s3, 'rgba(220, 220, 0, 0.3)') ];


}

function createDialGradients(DialIndex, min, max  )
{
var s0,s1,s2,s3;

   gDialGradients[DialIndex] = new steelseries.gradientWrapper(  min, max,
                  [ 0, 0.33, 0.66, 0.85, 1],
                  [ new steelseries.rgbaColor(0, 0, 200, 1),
                    new steelseries.rgbaColor(0, 200, 0, 1),
                    new steelseries.rgbaColor(200, 200, 0, 1),
                    new steelseries.rgbaColor(200, 0, 0, 1),
                    new steelseries.rgbaColor(200, 0, 0, 1) ]);

//s0 = parseInt(min);
//s1 = Math.floor((max - min)* 0.333);
//s2 = Math.floor((max - min)* 0.666);
//s3 = parseInt(max);


}
function setDialType(sel) {
var myDialCanvas;


var myDialID = document.getElementById("DialID").value ;

DialType[myDialID] = sel.options[sel.selectedIndex].value;

CreateDialTypes(CurrentCanvasID, parseInt(myDialID), sel.options[sel.selectedIndex].value);

}

function CreateDialTypes(myCanvasIndex, myDialID, myDialType) {
var myDialCanvas;

myDialCanvas = "canvasRadial" + myCanvasIndex;

//alert(myDialID + "Canvas ID = " + myCanvasIndex);

        switch (parseInt(myDialType)) {
		case 0:

			createDialSections(myCanvasIndex,DialMin[myDialID],DialMax[myDialID]);
			

			radialDial[myCanvasIndex] = new steelseries.Radial(myDialCanvas, {
				gaugeType: steelseries.GaugeType.TYPE4,
				size: DialSize[PageLayout],
				section: gDialSections[myDialID],
				useSectionColors: true,
				backgroundVisible: true,
				alarmSound: false,
				//trendVisible: true,
				lcdVisible: true
				});

		//	alert('Dial Max' + DialMax[myDialID] + "  " + myDialID);

			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			SetAlarmState(myCanvasIndex, DialAlarmState[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);

			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);
			
			


		break;

		case 1:


			createDialSections(myCanvasIndex,DialMin[myDialID],DialMax[myDialID]);


				radialDial[myCanvasIndex] = new steelseries.Radial(myDialCanvas, {
				gaugeType: steelseries.GaugeType.TYPE6,
				size: DialSize[PageLayout],
				//section: gDialSections[myDialID],
				useSectionColors: false,
				backgroundVisible: true,
				lcdDecimals: 1,
				alarmSound: false,
				thresholdVisible: false,
				lcdVisible: true
				});
				
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			SetAlarmState(myCanvasIndex, DialAlarmState[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);
		
			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);

			
		break;


		case 2:

			createDialSections(myCanvasIndex,DialMin[myDialID],DialMax[myDialID]);

			radialDial[myCanvasIndex] =  new steelseries.RadialBargraph(myDialCanvas, {
				gaugeType: steelseries.GaugeType.TYPE4,
				size: DialSize[PageLayout],
				section: gDialSections[myDialID],
				useSectionColors: true,
				lcdDecimals: 1,
				lcdVisible: true
				});
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);

			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			//setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			//setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);


		break;


		case 3:
			createDialGradients(myCanvasIndex,DialMin[myDialID],DialMax[myDialID]);
			radialDial[myCanvasIndex] = new steelseries.RadialBargraph(myDialCanvas, {
				gaugeType: steelseries.GaugeType.TYPE4,
				size: DialSize[PageLayout],
				valueGradient: gDialGradients[myDialID],
                useValueGradient: true,
				lcdDecimals: 1,
				lcdVisible: true
				});
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);

			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			//setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			//setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);


		break;


		case 4:
			radialDial[myCanvasIndex] = new steelseries.Linear(myDialCanvas, {
                            threshold: 50,
                            lcdVisible: true
                            });
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);

			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			//setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);


		break;


		case 5:
			radialDial[myCanvasIndex] = new steelseries.LinearBargraph(myDialCanvas, {
                            threshold: 50,
                            lcdVisible: true
                            });
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);

			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			//setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);


		break;


		case 6:
			createDialSections(myCanvasIndex,DialMin[myDialID],DialMax[myDialID]);
			radialDial[myCanvasIndex] = new steelseries.LinearBargraph(myDialCanvas, {
							section: gDialSections[myDialID],
							useSectionColors: true,
                            lcdVisible: true
                            });
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);

			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			//setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			//setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);

		break;


		case 7:
			createDialGradients(myCanvasIndex,DialMin[myDialID],DialMax[myDialID]);
			radialDial[myCanvasIndex] = new steelseries.LinearBargraph(myDialCanvas, {
							valueGradient: gDialGradients[myDialID],
                            useValueGradient: true,
                            lcdVisible: true
                            });
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);

			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			//setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			//setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);


		break;


		case 8:
			radialDial[myCanvasIndex] = new steelseries.WindDirection(myDialCanvas, { size: DialSize[PageLayout], lcdTitleStrings: 'TA' , lcdVisible: true });
			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);
			setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);

		break;

		case 9:
			radialDial[myCanvasIndex] = new steelseries.Compass(myDialCanvas, { size: DialSize[PageLayout] });
			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			//setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);
			//setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);

		break;

		case 10:
			radialDial[myCanvasIndex] = new steelseries.Horizon(myDialCanvas, {size: DialSize[PageLayout] });
			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			//setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
		break;

		case 11:
		//	createDialSections(myCanvasIndex,DialMin[myDialID],DialMax[myDialID]);
				radialDial[myCanvasIndex] = new steelseries.Radial(myDialCanvas, {
				gaugeType: steelseries.GaugeType.TYPE6,
				size: DialSize[PageLayout],
				//section: gDialSections[myDialID],
				useSectionColors: false,
				backgroundVisible: true,
				lcdDecimals: 0,
				alarmSound: false,
				thresholdVisible: false,
				lcdVisible: true
				});
				
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			SetAlarmState(myCanvasIndex, DialAlarmState[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);
		
			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);

			
		break;

		case 12:
	//		createDialSections(myCanvasIndex,DialMin[myDialID],DialMax[myDialID]);
				radialDial[myCanvasIndex] = new steelseries.Radial(myDialCanvas, {
				gaugeType: steelseries.GaugeType.TYPE6,
				size: DialSize[PageLayout],
				//section: gDialSections[myDialID],
				useSectionColors: false,
				backgroundVisible: true,
				lcdDecimals: 2,
				alarmSound: false,
				thresholdVisible: false,
				lcdVisible: true
				});
				
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			SetAlarmState(myCanvasIndex, DialAlarmState[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);
		
			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);	
		break;

		case 13:
	//		createDialSections(myCanvasIndex,DialMin[myDialID],DialMax[myDialID]);
				radialDial[myCanvasIndex] = new steelseries.Radial(myDialCanvas, {
				gaugeType: steelseries.GaugeType.TYPE6,
				size: DialSize[PageLayout],
				//section: gDialSections[myDialID],
				useSectionColors: false,
				backgroundVisible: true,
				lcdDecimals: 4,
				alarmSound: false,
				thresholdVisible: false,
				lcdVisible: true
				});
				
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			SetAlarmState(myCanvasIndex, DialAlarmState[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);
		
			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);	
		break;

		case 14:
	//		createDialSections(myCanvasIndex,DialMin[myDialID],DialMax[myDialID]);
				radialDial[myCanvasIndex] = new steelseries.Radial(myDialCanvas, {
				gaugeType: steelseries.GaugeType.TYPE6,
				size: DialSize[PageLayout],
				//section: gDialSections[myDialID],
				useSectionColors: false,
				backgroundVisible: true,
				lcdDecimals: 6,
				alarmSound: false,
				thresholdVisible: false,
				lcdVisible: true,
				valuesNumeric: false
				});
				
			radialDial[myCanvasIndex].setMinValue(DialMin[myDialID]);
			radialDial[myCanvasIndex].setMaxValue(DialMax[myDialID]);
			radialDial[myCanvasIndex].setThreshold(DialAlarm[myDialID]);
			SetAlarmState(myCanvasIndex, DialAlarmState[myDialID]);
			radialDial[myCanvasIndex].setTitleString(DialText[myDialID]);
			SetDialUnits(myCanvasIndex, DialUnits[myDialID]);
		
			setFrameDesign(myCanvasIndex,DialFrameType[myDialID]);
			setDialBackgroundColor(myCanvasIndex,DialBackground[myDialID]);
			setPointerType(myCanvasIndex,DialPonterType[myDialID]);
			setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);	
		break;

		case 15:
			radialDial[myCanvasIndex] = new steelseries.DisplaySingle(myDialCanvas, {
			width: DialSize[PageLayout],
			height: DialSize[PageLayout]*0.25,
			value: "Switch",
			autoScroll: false,
			valuesNumeric: false
			});

			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);	
			radialDial[myCanvasIndex].setValue(DialText[myDialID]);
		//	radialDial[myCanvasIndex].blink(true);
	//		setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
		break;

		case 16:
			radialDial[myCanvasIndex] = new steelseries.DisplaySingle(myDialCanvas, {
			width: DialSize[PageLayout],
			height: DialSize[PageLayout]*0.25,
			value: "Switch",
			autoScroll: false,
			valuesNumeric: false
			});

			setLcdColor(myCanvasIndex,DialLCDColor[myDialID]);	
			radialDial[myCanvasIndex].setValue(DialText[myDialID]);
	//		setPointerColor(myCanvasIndex,DialPointerColor[myDialID]);
		break;

		}
}

function selectFrameDesign(sel) {

//alert ('selectFrameDesign');

	    var myDialID = document.getElementById("DialID").value ;

		DialFrameType[myDialID] = sel.selectedIndex;

		var myDialID = document.getElementById("DialID").selectedIndex ;

		setFrameDesign(myDialID, parseInt(sel.selectedIndex))
}

function setFrameDesign(CurrentDialID, DialFrameType) {

//alert(CurrentDialID + "  " + DialFrameType);


        switch (parseInt(DialFrameType)) {
        case 0:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.BLACK_METAL);
            break;
        case 1:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.METAL);
            break;
        case 2:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.SHINY_METAL);
            break;
        case 3:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.BRASS);
            break;
        case 4:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.STEEL);
            break;
        case 5:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.CHROME);
            break;
        case 6:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.GOLD);
            break;
        case 7:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.ANTHRACITE);
            break;
        case 8:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.TILTED_GRAY);
            break;
        case 9:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.TILTED_BLACK);
            break;
        case 10:
            radialDial[CurrentDialID].setFrameDesign(steelseries.FrameDesign.GLOSSY_METAL);
            break;
        }
}

function selectPointerType(sel) {
	    var myDialID = document.getElementById("DialID").value ;

		DialPonterType[myDialID] = sel.selectedIndex;

		var myDialID = document.getElementById("DialID").selectedIndex ;

		setPointerType(myDialID, parseInt(sel.selectedIndex))
}

function setPointerType(CurrentDialID, pointerType) {


        switch (parseInt(pointerType)) {
        case 0:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE1);
            break;
        case 1:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE2);
            break;
        case 2:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE3);
            break;
        case 3:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE4);
            break;
        case 4:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE5);
            break;
        case 5:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE6);
            break;
        case 6:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE7);
            break;
        case 7:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE8);
            break;
        case 8:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE9);
            break;
        case 9:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE10);
            break;
        case 10:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE11);
            break;
		case 11:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE12);
            break;
        case 12:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE13);
            break;
        case 13:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE14);
            break;
        case 14:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE15);
            break;
		  case 15:
            radialDial[CurrentDialID].setPointerType(steelseries.PointerType.TYPE16);
            break;
        }
    }

function selectBackgroundColor(sel) {
	    var myDialID = document.getElementById("DialID").value ;

		DialBackground[myDialID] = sel.selectedIndex;

		var myDialID = document.getElementById("DialID").selectedIndex ;

		setDialBackgroundColor(myDialID, parseInt(sel.selectedIndex))
}

function setDialBackgroundColor(CurrentDialID, BackgroundColor) {
	
//	alert(sel);

        switch (parseInt(BackgroundColor)) {
        case 0:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.DARK_GRAY);
            break;
        case 1:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.SATIN_GRAY);
            break;
        case 2:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.LIGHT_GRAY);
            break;
        case 3:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.WHITE);
            break;
        case 4:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.BLACK);
            break;
        case 5:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.BEIGE);
            break;
        case 6:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.BROWN);
            break;
        case 7:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.RED);
            break;
        case 8:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.GREEN);
            break;
        case 9:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.BLUE);
            break;
        case 10:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.ANTHRACITE);
            break;
        case 11:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.MUD);
            break;
        case 12:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.PUNCHED_SHEET);
            break;
        case 13:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.CARBON);
            break;
        case 14:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.STAINLESS);
            break;
        case 15:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.BRUSHED_METAL);
            break;
        case 16:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.BRUSHED_STAINLESS);
            break;
        case 17:
            radialDial[CurrentDialID].setBackgroundColor(steelseries.BackgroundColor.TURNED);
            break;
        }
    }

function selectPointerColor(sel) {
	    var myDialID = document.getElementById("DialID").value ;

		DialPointerColor[myDialID] = sel.selectedIndex;

	//	alert(DialPointerColor[myDialID]);

		var myDialID = document.getElementById("DialID").selectedIndex ;

		if(DialType[CurrentDialID] <  15)
	  {
		setPointerColor(myDialID, parseInt(sel.selectedIndex));
		}
}

function setPointerColor(CurrentDialID, DialPointerColor) {

	   // test for radial dials
	  if(DialType[CurrentDialID] < 4 || DialType[CurrentDialID] > 10)
	  {

			switch (parseInt(DialPointerColor)) {
			case 0:
			
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.RED);
				break;
			case 1:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.GREEN);
				break;
			case 2:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.BLUE);
				break;
			case 3:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.ORANGE);
				break;
			case 4:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.YELLOW);
				break;
			case 5:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.CYAN);
				break;
			case 6:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.MAGENTA);
				break;
			case 7:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.WHITE);
				break;
			case 8:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.GRAY);
				break;
			case 9:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.BLACK);
				break;
			case 10:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.RAITH);
				break;
			case 11:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.GREEN_LCD);
				break;
			case 12:
				radialDial[CurrentDialID].setPointerColor(steelseries.ColorDef.JUG_GREEN);
				break;
			}
		}
		else if(DialType[CurrentDialID] >= 4 && DialType[CurrentDialID] <= 10)
	  {

	 // alert(CurrentDialID + "  " + DialPointerColor);

	  			switch (parseInt(DialPointerColor)) {
			case 0:
			
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.WHITE);
				break;
			case 1:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.BLUE);
				break;
			case 2:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.ORANGE);
				break;
			case 3:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.RED);
				break;
			case 4:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.YELLOW);
				break;
			case 5:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.GRAY);
				break;
			case 6:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.BLACK);
				break;
			case 7:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.GREEN);
				break;
			case 8:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.BLUE);
				break;
			case 9:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.BLUE);
				break;
			case 10:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.BLUE);
				break;
			case 11:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.BLUE);
				break;
			case 12:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.GREEN_LCD);
				break;
			case 13:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.GREEN_LCD);
				break;
			case 14:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.BLUE);
				break;
			case 15:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.RED);
				break;
			case 16:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.BLUE);
				break;
			case 17:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.MAGENTA);
				break;
			case 18:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.BLACK);
				break;
			case 19:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.JUG_GREEN);
				break;
			case 20:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.WHITE);
				break;
			case 21:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.CYAN);
				break;
			case 22:
				radialDial[CurrentDialID].setValueColor(steelseries.ColorDef.WHITE);
				break;





			}
		}
    }

function selectLcdColor(sel) {
	    var myDialID = document.getElementById("DialID").value ;

		DialLCDColor[myDialID] = sel.selectedIndex;

		var myDialID = document.getElementById("DialID").selectedIndex ;

		setLcdColor(myDialID, parseInt(sel.selectedIndex))
}

 function setLcdColor(CurrentDialID, LCDColor) {

        switch (parseInt(LCDColor)) {
        case 0:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.BEIGE);
            break;
        case 1:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.BLUE);
            break;
        case 2:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.ORANGE);
            break;
        case 3:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.RED);
            break;
        case 4:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.YELLOW);
            break;
        case 5:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.WHITE);
            break;
        case 6:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.GRAY);
            break;
        case 7:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.BLACK);
            break;
        case 8:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.GREEN);
            break;
        case 9:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.BLUE2);
            break;
        case 10:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.BLUE_BLACK);
            break;
        case 11:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.BLUE_DARKBLUE);
            break;
        case 12:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.BLUE_GRAY);
            break;
        case 13:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.STANDARD);
            break;
        case 14:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.STANDARD_GREEN);
            break;
        case 15:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.BLUE_BLUE);
            break;
        case 16:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.RED_DARKRED);
            break;
        case 17:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.DARKBLUE);
            break;
        case 18:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.LILA);
            break;
        case 19:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.BLACKRED);
            break;
        case20:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.DARKGREEN);
            break;

        case 21:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.AMBER);
            break;
        case 22:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.LIGHTBLUE);
            break;

		case 23:
            radialDial[CurrentDialID].setLcdColor(steelseries.LcdColor.SECTIONS);
            break;
        }
    }

function selectClockLcdColor(sel) {
	    var myDialID = document.getElementById("DialID").value ;

		// clock display is dial=8
	 ClockLCDColor = sel.selectedIndex;


		setClockLcdColor(parseInt(sel.selectedIndex))
}

function setClockLcdColor(ClockLCDColor) {


	
        switch (parseInt(ClockLCDColor)) {
         case 0:
           ClockLCD.setLcdColor(steelseries.LcdColor.BEIGE);
            break;
        case 1:

            ClockLCD.setLcdColor(steelseries.LcdColor.BLUE);
            break;
        case 2:
            ClockLCD.setLcdColor(steelseries.LcdColor.ORANGE);
            break;
        case 3:
            ClockLCD.setLcdColor(steelseries.LcdColor.RED);
            break;
        case 4:
           ClockLCD.setLcdColor(steelseries.LcdColor.YELLOW);
            break;
        case 5:
            ClockLCD.setLcdColor(steelseries.LcdColor.WHITE);
            break;
        case 6:
            ClockLCD.setLcdColor(steelseries.LcdColor.GRAY);
            break;
        case 7:
            ClockLCD.setLcdColor(steelseries.LcdColor.BLACK);
            break;
        case 8:
            ClockLCD.setLcdColor(steelseries.LcdColor.GREEN);
            break;
        case 9:
           ClockLCD.setLcdColor(steelseries.LcdColor.BLUE2);
            break;
        case 10:
            ClockLCD.setLcdColor(steelseries.LcdColor.BLUE_BLACK);
            break;
        case 11:
            ClockLCD.setLcdColor(steelseries.LcdColor.BLUE_DARKBLUE);
            break;
        case 12:
            ClockLCD.setLcdColor(steelseries.LcdColor.BLUE_GRAY);
            break;
        case 13:
           ClockLCD.setLcdColor(steelseries.LcdColor.STANDARD);
            break;
        case 14:
           ClockLCD.setLcdColor(steelseries.LcdColor.STANDARD_GREEN);
            break;
        case 15:
            ClockLCD.setLcdColor(steelseries.LcdColor.BLUE_BLUE);
            break;
        case 16:
            ClockLCD.setLcdColor(steelseries.LcdColor.RED_DARKRED);
            break;
        case 17:
            ClockLCD.setLcdColor(steelseries.LcdColor.DARKBLUE);
            break;
        case 18:
            ClockLCD.setLcdColor(steelseries.LcdColor.LILA);
            break;
        case 19:
            ClockLCD.setLcdColor(steelseries.LcdColor.BLACKRED);
            break;
        case20:
            ClockLCD.setLcdColor(steelseries.LcdColor.DARKGREEN);
            break;
        case 21:
           ClockLCD.setLcdColor(steelseries.LcdColor.DARKGREEN);
            break;
        case 22:
            ClockLCD.setLcdColor(steelseries.LcdColor.AMBER);
            break;
        case 23:
            ClockLCD.setLcdColor(steelseries.LcdColor.LIGHTBLUE);
            break;
        }
    }

function selectPageColor(sel) {
	
		PageBackGroundColor = sel.options[sel.selectedIndex].value;

		setPageColor(sel.options[sel.selectedIndex].value)
}

 function setPageColor(PageBackgroundColor) {


        switch (PageBackgroundColor) {
        case "aqua":
            PageBackGroundColor  = "aqua";
            break;
        case "gray":
            PageBackGroundColor  = "gray";
            break;
        case "navy":
            PageBackGroundColor  = "navy";
            break;
        case "silver":
           PageBackGroundColor  = "silver";
            break;
        case "black":
            PageBackGroundColor  = "black";
            break;
        case "green":
            PageBackGroundColor  = "green";
            break;
        case "olive":
           PageBackGroundColor  = "olive";
            break;
        case "teal":
           PageBackGroundColor  = "teal";
            break;
        case "blue":
            PageBackGroundColor  = "blue";
            break;
        case "lime":
            PageBackGroundColor  = "lime";
            break;
        case "purple":
            PageBackGroundColor  = "purple";
            break;
        case "fuchsia":
            PageBackGroundColor  = "fuchsia";
            break;
        case "maroon":
            PageBackGroundColor  = "maroon";
            break;
        case "red":
            PageBackGroundColor  = "red";
            break;
        case "yellow":
           PageBackGroundColor  = "yellow";
            break;
        case "white":
            PageBackGroundColor  = "white";
            break;
		default:
		 PageBackGroundColor  = "black";
        break;

      
        }
    }

function updateBackColor(color)
{
        PageBackGroundColor  = '#'+color;

		PageBackGroundColor = PageBackGroundColor;
}

function CloseDialParameters()
{
 
	document.getElementById("DialStyleParameters").style.display = "none";
	document.getElementById("PGNParameters").style.display = "none";
	document.getElementById("PageParameters").style.display = "none";
	document.getElementById("AccountParameters").style.display = "none"		
	document.getElementById("TabBar").style.display = "none";
}

function CloseTabs()
{
 
	document.getElementById("DialStyleParameters").style.display = "none";
	document.getElementById("PGNParameters").style.display = "none";
	document.getElementById("PageParameters").style.display = "none";
	document.getElementById("AccountParameters").style.display = "none"		
	document.getElementById("TabBar").style.display = "none";
}

function SetAccountFolderName(sel)
{
var mytext = "nothing";

var exp = new Date();
exp.setTime(exp.getTime() + (30 * 24 * 60 * 60 * 1000));

//sel.options[sel.selectedIndex].value

mytext = sel.value;

//alert(mytext);



AccountDataFolder = mytext;

document.getElementById("ServerLocal").checked = false;
		document.getElementById("ServerWeb").checked = false;
		document.getElementById("ServerGlobal").checked = false;

//SetCookie('SSP1Account', AccountDataFolder + ":" + AccountType + ":" + ConfigOptions, exp); 

}

function ParseDialCookie(DialID, DialSettingsCookie)
{

	//alert('parsing cookies');
	//alert(DialSettingsCookie);

	if(DialSettingsCookie != null)
    {
    var myDialSettingsSubStrings = new Array();
		//alert('got a cookies');
		// parse the cookie string
		myDialSettingsSubStrings= DialSettingsCookie.split(":");

		// test to see if we get a cookie else use defaults
		if(myDialSettingsSubStrings.length !=0)
		{
			//alert('valid cookie');
			//alert(myDialSettingsSubStrings.length);
			// test to see if get all the parameters else use the defaults
			if(myDialSettingsSubStrings.length == 15)
			{
			// for(i=0; i < myDialSettingsSubStrings.length; i++)
			 //  alert(myDialSettingsSubStrings[i]);
       
				DialType[DialID]   = myDialSettingsSubStrings[0];
				DialPGNInstance[DialID]  =  myDialSettingsSubStrings[1];
				DialPGNNumber[DialID]  =  myDialSettingsSubStrings[2];
				DialPGNParameter[DialID]   = myDialSettingsSubStrings[3];
				DialUnits[DialID]   = myDialSettingsSubStrings[4];
				DialMin[DialID]   = myDialSettingsSubStrings[5];
				DialMax[DialID]   = myDialSettingsSubStrings[6];
				DialAlarm[DialID]  =  myDialSettingsSubStrings[7];
				DialAlarmState[DialID]  =  myDialSettingsSubStrings[8];
				DialText[DialID]  = myDialSettingsSubStrings[9];
				DialFrameType[DialID]   = myDialSettingsSubStrings[10];
				DialBackground[DialID]   = myDialSettingsSubStrings[11];
				DialLCDColor[DialID]  = myDialSettingsSubStrings[12];
				DialPointerColor[DialID]   = myDialSettingsSubStrings[13];
				DialPonterType[DialID]  =  myDialSettingsSubStrings[14];
			}
		}
    }

//	alert(DialFrameType[0]);
}

function SaveDialCookies()
{
var mytext = "nothing";
var DialSettings = new Array();

var exp = new Date();
exp.setTime(exp.getTime() + (30 * 24 * 60 * 60 * 1000));

for(i=0; i<MaxDials; i++)
{

DialSettings[i] =	DialType[i] + ":" +
					DialPGNInstance[i] + ":" +
					DialPGNNumber[i] + ":" +
					DialPGNParameter[i] + ":" +
					DialUnits[i] + ":" +
					DialMin[i] + ":" +
					DialMax[i] + ":" +
					DialAlarm[i] + ":" +
					DialAlarmState[i] + ":" +
					DialText[i] + ":" +
					DialFrameType[i] + ":" +
					DialBackground[i] + ":" +
					DialLCDColor[i] + ":" +
					DialPointerColor[i] + ":" +
					DialPonterType[i];

SetCookie(CookiePrefix +'Dial' + i + 'Settings', DialSettings[i] , exp); 

}

document.location.reload(false);


}

function ParsePageSettingsCookie( PageSettingsCookie)
{

	//alert('parsing cookies');
	//alert(PageSettingsCookie);

	if(PageSettingsCookie != null)
    {
    var myPageSettingsSubStrings = new Array();
		//alert('got a cookies');
		// parse the cookie string
		myPageSettingsSubStrings= PageSettingsCookie.split(":");

		// test to see if we get a cookie else use defaults
		if(myPageSettingsSubStrings.length !=0)
		{
			//alert('valid cookie');
		
			// test to see if get all the parameters else use the defaults
			if(myPageSettingsSubStrings.length == 9)
			{
				PageLayout   = myPageSettingsSubStrings[0];
				DialStart  =  parseInt(myPageSettingsSubStrings[1]);
				PageBackGroundColor  =  myPageSettingsSubStrings[2];
				PageForeGroundColor   = myPageSettingsSubStrings[3];
				ClockLCDColor   = myPageSettingsSubStrings[4];
				SystemClockPGNID   = myPageSettingsSubStrings[5];
				UpdateInterval   = myPageSettingsSubStrings[6];
				DialTimeout   = myPageSettingsSubStrings[7];
				xmlDescription   = myPageSettingsSubStrings[8];
			}
		}
    }

	//alert(PageLayout);
}

function SavePageCookies()
{
var mytext = "nothing";
var PageSettings;

var exp = new Date();
exp.setTime(exp.getTime() + (30 * 24 * 60 * 60 * 1000));

PageSettings =	PageLayout + ":" +
				DialStart + ":" +
				PageBackGroundColor + ":" +
				PageForeGroundColor + ":" +
				ClockLCDColor + ":" +
				SystemClockPGNID + ":" +
				UpdateInterval + ":" +
				DialTimeout + ":" +
				xmlDescription;

//alert(DialSettings[0]);

SetCookie(CookiePrefix + 'PageSettings', PageSettings , exp); 

document.location.reload(false);

}


function InitializePGNNumberOptionList(current)
{
			document.getElementById("PGNNumber").options.length = 0;

			document.getElementById("PGNNumber").options[0] = new Option("PGN127488 - Engine Rapid", "127488");
			document.getElementById("PGNNumber").options[1] = new Option("PGN127489 - Engine Dynamic", "127489");
			document.getElementById("PGNNumber").options[2] = new Option("PGN127508 - Battery Status", "127508");
			document.getElementById("PGNNumber").options[3] = new Option("PGN127505 - Fluid Level", "127505");
			document.getElementById("PGNNumber").options[4] = new Option("PGN127493 - Transmission", "127493");
			document.getElementById("PGNNumber").options[5] = new Option("PGN130311 - Environmental", "130311");
			document.getElementById("PGNNumber").options[6] = new Option("PGN130323 - Meteorlogical", "130323");
			document.getElementById("PGNNumber").options[7] = new Option("PGN130306 - Wind Data", "130306");
			document.getElementById("PGNNumber").options[8] = new Option("PGN127250 - Heading", "127250");
			document.getElementById("PGNNumber").options[9] = new Option("PGN127257 - Attitude", "127257");
			document.getElementById("PGNNumber").options[10] = new Option("PGN127251 - Rate of Turn", "127251");
			document.getElementById("PGNNumber").options[11] = new Option("PGN130312 - Temperature", "130312");
			document.getElementById("PGNNumber").options[12] = new Option("PGN127245 - Rudder", "127245");
			document.getElementById("PGNNumber").options[13] = new Option("PGN127501 - Switch Status", "127501");
			document.getElementById("PGNNumber").options[14] = new Option("PGN127502 - Switch Control", "127502");
			document.getElementById("PGNNumber").options[15] = new Option("PGN129026 - COG & SOG", "129026");
			document.getElementById("PGNNumber").options[16] = new Option("$IIMWD    - Wind Data North", "IIMWD");
			document.getElementById("PGNNumber").options[17] = new Option("$IIMWV    - Wind Data Relative", "IIMWV");
			document.getElementById("PGNNumber").options[18] = new Option("$IIVWR    - Wind Data Relative", "IIVWR");
			document.getElementById("PGNNumber").options[19] = new Option("$HCHDG    - Heading", "HCHDG");
			document.getElementById("PGNNumber").options[20] = new Option("$IIVHW    - Water Heading & Speed", "IIVHW");
			document.getElementById("PGNNumber").options[21] = new Option("$IIVTG    - Track COG & SOG", "IIVTG");			
			document.getElementById("PGNNumber").options[22] = new Option("$IIROT    - Rate of Turn", "IIROT");			
			document.getElementById("PGNNumber").options[23] = new Option("$YXXDR    - Pitch/Roll", "YXXDR");			
			document.getElementById("PGNNumber").options[24] = new Option("$GPGLL    - Position Data", "GPGLL");
			document.getElementById("PGNNumber").options[25] = new Option("$GPRMC    - Navigation Data", "GPRMC");
			document.getElementById("PGNNumber").options[26] = new Option("$SDDBT    - Depth", "SDDBT");
			document.getElementById("PGNNumber").options[27] = new Option("$SDMTW    - Water Temp", "SDMTW");
			document.getElementById("PGNNumber").options[28] = new Option("$WIMDA    - Meteorological", "WIMDA");
}

function SetPGNNumberOptionList(sel)
{
var myDialID;

	myDialID = document.getElementById("DialID").selectedIndex ;

	//alert(myDialID);

	DialPGNNumber[myDialID] = sel.options[sel.selectedIndex].value;



   switch (sel.options[sel.selectedIndex].value) 
	{
        case "127488":
			SetPGNParamatersOptionList("127488");
			SetPGNInstanceOptionList("127488");
		break

		case "127489":
			SetPGNParamatersOptionList("127489");
			SetPGNInstanceOptionList("127489");
		break

		 case "127508":
			SetPGNParamatersOptionList("127508");
			SetPGNInstanceOptionList("127508");
		break

		 case "127505":
			SetPGNParamatersOptionList("127505");
			SetPGNInstanceOptionList("127505");
		break

		 case "127493":
			SetPGNParamatersOptionList("127493");
			SetPGNInstanceOptionList("127493");
		break
		
		case "130311":
			SetPGNParamatersOptionList("130311");
			SetPGNInstanceOptionList("130311");
		break

		case "130323":
			SetPGNParamatersOptionList("130323");
			SetPGNInstanceOptionList("130323");
		break

		 case "130306":
			SetPGNParamatersOptionList("130306");
			SetPGNInstanceOptionList("130306");
		break

		 case "127250":
			SetPGNParamatersOptionList("127250");
			SetPGNInstanceOptionList("127250");
		break

		 case "127257":
			SetPGNParamatersOptionList("127257");
			SetPGNInstanceOptionList("127257");
		break

		 case "127251":
			SetPGNParamatersOptionList("127251");
			SetPGNInstanceOptionList("127251");
		break

		 case "130312":
			SetPGNParamatersOptionList("130312");
			SetPGNInstanceOptionList("130312");
		break

		case "127245":
			SetPGNParamatersOptionList("127245");
			SetPGNInstanceOptionList("127245");
		break

		case "127501":
			SetPGNParamatersOptionList("127501");
			SetPGNInstanceOptionList("127501");
		break

		 case "129026":
			SetPGNParamatersOptionList("129026");
			SetPGNInstanceOptionList("129026");
		break

		case "127501":
			SetPGNParamatersOptionList("127501");
			SetPGNInstanceOptionList("127501");
		break

		case "127502":
			SetPGNParamatersOptionList("127502");
			SetPGNInstanceOptionList("127502");
		break

		case "IIMWD":
			SetPGNParamatersOptionList("IIMWD");
			SetPGNInstanceOptionList("IIMWD");
		break


		case "IIMWV":
			SetPGNParamatersOptionList("IIMWV");
			SetPGNInstanceOptionList("IIMWV");
		break

		case "IIVWR":
			SetPGNParamatersOptionList("IIVWR");
			SetPGNInstanceOptionList("IIVWR");
		break

		case "HCHDG":
			SetPGNParamatersOptionList("HCHDG");
			SetPGNInstanceOptionList("HCHDG");
		break

		case "IIVHW":
			SetPGNParamatersOptionList("IIVHW");
			SetPGNInstanceOptionList("IIVHW");
		break

		case "IIVTG":
			SetPGNParamatersOptionList("IIVTG");
			SetPGNInstanceOptionList("IIVTG");
		break

		case "IIROT":
			SetPGNParamatersOptionList("IIROT");
			SetPGNInstanceOptionList("IIROT");
		break

		case "YXXDR":
			SetPGNParamatersOptionList("YXXDR");
			SetPGNInstanceOptionList("YXXDR");
		break

		case "GPGLL":
			SetPGNParamatersOptionList("GPGLL");
			SetPGNInstanceOptionList("GPGLL");
		break

		case "GPRMC":
			SetPGNParamatersOptionList("GPRMC");
			SetPGNInstanceOptionList("GPRMC");
		break

		case "SDDBT":
			SetPGNParamatersOptionList("SDDBT");
			SetPGNInstanceOptionList("SDDBT");
		break

		case "SDMTW":
			SetPGNParamatersOptionList("SDMTW");
			SetPGNInstanceOptionList("SDMTW");
		break

		case "WIMDA":
			SetPGNParamatersOptionList("WIMDA");
			SetPGNInstanceOptionList("WIMDA");
		break



		case "":
			SetPGNParamatersOptionList("Undefined");
			SetPGNInstanceOptionList("Undefined");
		break

		case "Undefined":
			SetPGNParamatersOptionList("Undefined");
			SetPGNInstanceOptionList("Undefined");
		break

		default:
			SetPGNParamatersOptionList("Undefined");
			SetPGNInstanceOptionList("Undefined");
		break



		}

	//alert(myDialID);
		// reset parameter list to first value
		document.getElementById("PGNParameterID").selectedIndex = 0;

		// reset Units list to last value = undefined
		document.getElementById("DialUnits").selectedIndex = 37;
		DialUnits[myDialID] = 37;

		// reset parameter index to 0
		DialPGNParameter[myDialID] = 0;

		radialDial[myDialID].setUnitString("undefined");
	
}

function SetPGNInstanceOptionList(selText)
{

document.getElementById("PGNInstance").options.length = 0;

	switch (selText)
	{
		case "127505":
			document.getElementById("PGNInstance").options[0] = new Option("00-Fuel", 0);
			document.getElementById("PGNInstance").options[1] = new Option("01-Fuel", 1);
			document.getElementById("PGNInstance").options[2] = new Option("02-Fuel", 2);
			document.getElementById("PGNInstance").options[3] = new Option("03-Fuel", 3);
			document.getElementById("PGNInstance").options[4] = new Option("04-Fuel", 4);
			document.getElementById("PGNInstance").options[5] = new Option("05-Fuel", 5);
			document.getElementById("PGNInstance").options[6] = new Option("06-Fuel", 6);
			document.getElementById("PGNInstance").options[7] = new Option("07-Fuel", 7);
			document.getElementById("PGNInstance").options[8] = new Option("08-Fuel", 8);
			document.getElementById("PGNInstance").options[9] = new Option("09-Fuel", 9);
			document.getElementById("PGNInstance").options[10] = new Option("10-Fuel", 10);
			document.getElementById("PGNInstance").options[11] = new Option("11-Fuel", 11);
			document.getElementById("PGNInstance").options[12] = new Option("12-Fuel", 12);
			document.getElementById("PGNInstance").options[13] = new Option("13-Fuel", 13);
			document.getElementById("PGNInstance").options[14] = new Option("14-Fuel", 14);
			document.getElementById("PGNInstance").options[15] = new Option("15-Fuel", 15);

			document.getElementById("PGNInstance").options[16] = new Option("16-Fresh Water", 16);
			document.getElementById("PGNInstance").options[17] = new Option("17-Fresh Water", 17);
			document.getElementById("PGNInstance").options[18] = new Option("18-Fresh Water", 18);
			document.getElementById("PGNInstance").options[19] = new Option("19-Fresh Water", 19);
			document.getElementById("PGNInstance").options[20] = new Option("20-Fresh Water", 20);
			document.getElementById("PGNInstance").options[21] = new Option("21-Fresh Water", 21);
			document.getElementById("PGNInstance").options[22] = new Option("22-Fresh Water", 22);
			document.getElementById("PGNInstance").options[23] = new Option("23-Fresh Water", 23);
			document.getElementById("PGNInstance").options[24] = new Option("24-Fresh Water", 24);
			document.getElementById("PGNInstance").options[25] = new Option("25-Fresh Water", 25);
			document.getElementById("PGNInstance").options[26] = new Option("26-Fresh Water", 26);
			document.getElementById("PGNInstance").options[27] = new Option("27-Fresh Water", 27);
			document.getElementById("PGNInstance").options[28] = new Option("28-Fresh Water", 28);
			document.getElementById("PGNInstance").options[29] = new Option("29-Fresh Water", 29);
			document.getElementById("PGNInstance").options[30] = new Option("30-Fresh Water", 30);
			document.getElementById("PGNInstance").options[31] = new Option("31-Fresh Water", 31);

			document.getElementById("PGNInstance").options[32] = new Option("32-Waste Water", 32);
			document.getElementById("PGNInstance").options[33] = new Option("33-Waste Water", 33);
			document.getElementById("PGNInstance").options[34] = new Option("34-Waste Water", 34);
			document.getElementById("PGNInstance").options[35] = new Option("35-Waste Water", 35);
			document.getElementById("PGNInstance").options[36] = new Option("36-Waste Water", 36);
			document.getElementById("PGNInstance").options[37] = new Option("37-Waste Water", 37);
			document.getElementById("PGNInstance").options[38] = new Option("38-Waste Water", 38);
			document.getElementById("PGNInstance").options[39] = new Option("39-Waste Water", 39);
			document.getElementById("PGNInstance").options[40] = new Option("40-Waste Water", 40);
			document.getElementById("PGNInstance").options[41] = new Option("41-Waste Water", 41);
			document.getElementById("PGNInstance").options[42] = new Option("42-Waste Water", 42);
			document.getElementById("PGNInstance").options[43] = new Option("43-Waste Water", 43);
			document.getElementById("PGNInstance").options[44] = new Option("44-Waste Water", 44);
			document.getElementById("PGNInstance").options[45] = new Option("45-Waste Water", 45);
			document.getElementById("PGNInstance").options[46] = new Option("46-Waste Water", 46);
			document.getElementById("PGNInstance").options[47] = new Option("47-Waste Water", 47);



			//document.getElementById("PGNInstance").options[16] = new Option("1-Fuel", 16);
			//document.getElementById("PGNInstance").options[17] = new Option("1-Fresh Water", 17);
			//document.getElementById("PGNInstance").options[18] = new Option("1-Waste Water", 18);
			//document.getElementById("PGNInstance").options[19] = new Option("1-Live Well", 19);
			//document.getElementById("PGNInstance").options[20] = new Option("1-Oil", 20);
			//document.getElementById("PGNInstance").options[21] = new Option("1-Black Water", 21);
			//document.getElementById("PGNInstance").options[22] = new Option("1-Reserved", 22);
		break

		case "130311":
			document.getElementById("PGNInstance").options[0] = new Option("Sea Temp", 0);
			document.getElementById("PGNInstance").options[1] = new Option("Outside", 1);
			document.getElementById("PGNInstance").options[2] = new Option("Inside", 2);
			document.getElementById("PGNInstance").options[3] = new Option("Engine Room", 3);
			document.getElementById("PGNInstance").options[4] = new Option("Cabin", 4);

		break;

		

		case "127250":
			document.getElementById("PGNInstance").options[0] = new Option("True", 0);
			document.getElementById("PGNInstance").options[1] = new Option("Magnetic", 1);

		break;

		

		case "130306":
			document.getElementById("PGNInstance").options[0] = new Option("True", 0);
			document.getElementById("PGNInstance").options[1] = new Option("Magnetic", 1);
			document.getElementById("PGNInstance").options[2] = new Option("Apparent", 2);
			document.getElementById("PGNInstance").options[3] = new Option("Ground", 3);
			document.getElementById("PGNInstance").options[4] = new Option("Water", 4);
			document.getElementById("PGNInstance").options[5] = new Option("Reserved", 5);
			document.getElementById("PGNInstance").options[6] = new Option("Error", 6);
			document.getElementById("PGNInstance").options[7] = new Option("Null", 7);
			document.getElementById("PGNInstance").options[8] = new Option("T/M/A", 8);
			//document.getElementById("PGNInstance").options[9] = new Option("Mag/App", 9);
		break;

		case "127501":
			document.getElementById("PGNInstance").options[0] = new Option("0", 0);
			document.getElementById("PGNInstance").options[1] = new Option("1", 1);
			document.getElementById("PGNInstance").options[2] = new Option("2", 2);
			document.getElementById("PGNInstance").options[3] = new Option("3", 3);
			document.getElementById("PGNInstance").options[4] = new Option("4", 4);
			document.getElementById("PGNInstance").options[5] = new Option("5", 5);	
			document.getElementById("PGNInstance").options[6] = new Option("6", 6);
			document.getElementById("PGNInstance").options[7] = new Option("7", 7);
			document.getElementById("PGNInstance").options[8] = new Option("8", 8);
			document.getElementById("PGNInstance").options[9] = new Option("9", 9);
			document.getElementById("PGNInstance").options[10] = new Option("10", 10);
		break;
	
		case "127502":
			document.getElementById("PGNInstance").options[0] = new Option("0", 0);
			document.getElementById("PGNInstance").options[1] = new Option("1", 1);
			document.getElementById("PGNInstance").options[2] = new Option("2", 2);
			document.getElementById("PGNInstance").options[3] = new Option("3", 3);
			document.getElementById("PGNInstance").options[4] = new Option("4", 4);
			document.getElementById("PGNInstance").options[5] = new Option("5", 5);	
			document.getElementById("PGNInstance").options[6] = new Option("6", 6);
			document.getElementById("PGNInstance").options[7] = new Option("7", 7);
			document.getElementById("PGNInstance").options[8] = new Option("8", 8);
			document.getElementById("PGNInstance").options[9] = new Option("9", 9);
			document.getElementById("PGNInstance").options[10] = new Option("10", 10);
		break;

		case "IIMWD":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "IIMWV":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "IIVWR":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "HCHDG":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "IIVHW":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "IIVTG":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "IIROT":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "YXXDR":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "GPGLL":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "GPRMC":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "SDDBT":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;

		case "SDMTW":
			document.getElementById("PGNInstance").options[0] = new Option("*", 0);
		break;



		default:
			document.getElementById("PGNInstance").options[0] = new Option("0", 0);
			document.getElementById("PGNInstance").options[1] = new Option("1", 1);
			document.getElementById("PGNInstance").options[2] = new Option("2", 2);
			document.getElementById("PGNInstance").options[3] = new Option("3", 3);
			document.getElementById("PGNInstance").options[4] = new Option("4", 4);
			document.getElementById("PGNInstance").options[5] = new Option("5", 5);	
			document.getElementById("PGNInstance").options[6] = new Option("6", 6);
			document.getElementById("PGNInstance").options[7] = new Option("7", 7);
			document.getElementById("PGNInstance").options[8] = new Option("8", 8);
			document.getElementById("PGNInstance").options[9] = new Option("9", 9);
			document.getElementById("PGNInstance").options[10] = new Option("10", 10);
		break

	}

}

function SetPGNParamatersOptionList(selText)
{

document.getElementById("PGNParameterID").options.length = 0;

	switch (selText)
	{
        case "127488":
			document.getElementById("PGNParameterID").options[0] = new Option("RPM", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Boost", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Trim", 2);
		break

		case "127489":
			document.getElementById("PGNParameterID").options[0] = new Option("Oil Pressure", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Oil Temp", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Engine Temp", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Alt Volts", 3);
			document.getElementById("PGNParameterID").options[4] = new Option("Fuel Rate", 4);
			document.getElementById("PGNParameterID").options[5] = new Option("Engine Hours", 5);
			document.getElementById("PGNParameterID").options[6] = new Option("Coolant Pressure", 6);
			document.getElementById("PGNParameterID").options[7] = new Option("Fuel Pressure", 7);
			document.getElementById("PGNParameterID").options[8] = new Option("Check Engine", 8);
			document.getElementById("PGNParameterID").options[9] = new Option("Over Temp", 9);
			document.getElementById("PGNParameterID").options[10] = new Option("Low Oil Pres", 10);
			document.getElementById("PGNParameterID").options[11] = new Option("Low Oil Level", 11);
			document.getElementById("PGNParameterID").options[12] = new Option("Low Sys Volt", 12);
			document.getElementById("PGNParameterID").options[13] = new Option("Low Coolant Level", 13);
		break

		 case "127508":
			document.getElementById("PGNParameterID").options[0] = new Option("Battery Volt", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Current", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Temperature", 2);
		break

		 case "127505":
			document.getElementById("PGNParameterID").options[0] = new Option("Level", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Capacity", 1);
		break

		 case "127493":
			document.getElementById("PGNParameterID").options[0] = new Option("Gear", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Pressure", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Temperature", 2);
		break

		case "130311":
			document.getElementById("PGNParameterID").options[0] = new Option("Temperature", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Humidity", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Barometric", 2);
		break

		 case "130323":
			document.getElementById("PGNParameterID").options[0] = new Option("Date", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Time", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Lat", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Long", 3);
			document.getElementById("PGNParameterID").options[4] = new Option("Wind Speed", 4);
			document.getElementById("PGNParameterID").options[5] = new Option("Wind Dir", 5);
			document.getElementById("PGNParameterID").options[6] = new Option("Wind GUst", 6);
			document.getElementById("PGNParameterID").options[7] = new Option("Barometric", 7);
			document.getElementById("PGNParameterID").options[8] = new Option("Air Temp", 8);
			document.getElementById("PGNParameterID").options[9] = new Option("Station ID", 9);
			document.getElementById("PGNParameterID").options[10] = new Option("Station Name", 10);
		break

		 case "130306":
			document.getElementById("PGNParameterID").options[0] = new Option("Wind Speed", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Wind Direction", 1);
		break

		case "127250":
			document.getElementById("PGNParameterID").options[0] = new Option("Heading", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Deviation", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Variation", 2);
		break

		case "127257":
			document.getElementById("PGNParameterID").options[0] = new Option("Yaw", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Pitch", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Roll", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Pitch/Roll", 3);
		break

		case "130312":
			document.getElementById("PGNParameterID").options[0] = new Option("Sea Temp", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Outside", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Inside", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Engine Room", 3);
			document.getElementById("PGNParameterID").options[4] = new Option("Cabin", 4);
			document.getElementById("PGNParameterID").options[5] = new Option("Live Well", 5);
			document.getElementById("PGNParameterID").options[6] = new Option("Bait Well", 6);
			document.getElementById("PGNParameterID").options[7] = new Option("Refigeration", 7);
			document.getElementById("PGNParameterID").options[8] = new Option("Heating", 8);
			document.getElementById("PGNParameterID").options[9] = new Option("Dew Point", 9);
			document.getElementById("PGNParameterID").options[10] = new Option("Wind Chill A", 10);
			document.getElementById("PGNParameterID").options[11] = new Option("Wind Chill T", 11);
			document.getElementById("PGNParameterID").options[12] = new Option("Heat Index", 12);
			document.getElementById("PGNParameterID").options[13] = new Option("Freezer", 13);
	
			document.getElementById("PGNParameterID").options[14] = new Option("128", 128);
			document.getElementById("PGNParameterID").options[15] = new Option("129", 129);
			document.getElementById("PGNParameterID").options[16] = new Option("130", 130);
			document.getElementById("PGNParameterID").options[17] = new Option("131", 131);
			document.getElementById("PGNParameterID").options[18] = new Option("132", 132);
			document.getElementById("PGNParameterID").options[19] = new Option("133", 133);
			document.getElementById("PGNParameterID").options[20] = new Option("134", 134);
			document.getElementById("PGNParameterID").options[21] = new Option("135", 135);
			document.getElementById("PGNParameterID").options[22] = new Option("136", 136);
			document.getElementById("PGNParameterID").options[23] = new Option("137", 137);
			document.getElementById("PGNParameterID").options[24] = new Option("138", 138);
		break

		case "127245":
			document.getElementById("PGNParameterID").options[0] = new Option("Rudder", 0);
		
		break

		case "127251":
			document.getElementById("PGNParameterID").options[0] = new Option("Rate of Turn", 0);
		
		break


		case "129026":
			document.getElementById("PGNParameterID").options[0] = new Option("COG", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("SOG", 1);
		
		break

		case "127501":
			document.getElementById("PGNParameterID").options[0] = new Option("Indicator 0", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Indicator 1", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Indicator 2", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Indicator 3", 3);
			document.getElementById("PGNParameterID").options[4] = new Option("Indicator 4", 4);
			document.getElementById("PGNParameterID").options[5] = new Option("Indicator 5", 5);
			document.getElementById("PGNParameterID").options[6] = new Option("Indicator 6", 6);
			document.getElementById("PGNParameterID").options[7] = new Option("Indicator 7", 7);
			document.getElementById("PGNParameterID").options[8] = new Option("Indicator 8", 8);
			document.getElementById("PGNParameterID").options[9] = new Option("Indicator 9", 9);
			document.getElementById("PGNParameterID").options[10] = new Option("Indicator 10", 10);
			document.getElementById("PGNParameterID").options[11] = new Option("Indicator 11", 11);
			document.getElementById("PGNParameterID").options[12] = new Option("Indicator 12", 12);
			document.getElementById("PGNParameterID").options[13] = new Option("Indicator 13", 13);
			document.getElementById("PGNParameterID").options[14] = new Option("Indicator 14", 14);
			document.getElementById("PGNParameterID").options[15] = new Option("Indicator 15", 15);
			document.getElementById("PGNParameterID").options[16] = new Option("Indicator 16", 16);
			document.getElementById("PGNParameterID").options[17] = new Option("Indicator 17", 17);
			document.getElementById("PGNParameterID").options[18] = new Option("Indicator 18", 18);
			document.getElementById("PGNParameterID").options[19] = new Option("Indicator 19", 19);
			document.getElementById("PGNParameterID").options[10] = new Option("Indicator 20", 20);
			document.getElementById("PGNParameterID").options[11] = new Option("Indicator 21", 21);
			document.getElementById("PGNParameterID").options[12] = new Option("Indicator 22", 22);
			document.getElementById("PGNParameterID").options[13] = new Option("Indicator 23", 23);
			document.getElementById("PGNParameterID").options[14] = new Option("Indicator 24", 24);
			document.getElementById("PGNParameterID").options[15] = new Option("Indicator 25", 25);
			document.getElementById("PGNParameterID").options[16] = new Option("Indicator 26", 26);
			document.getElementById("PGNParameterID").options[17] = new Option("Indicator 27", 27);
			document.getElementById("PGNParameterID").options[18] = new Option("Indicator 28", 28);
		break

		
		case "127502":
			document.getElementById("PGNParameterID").options[0] = new Option("Switch 0", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Switch 1", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Switch 2", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Switch 3", 3);
			document.getElementById("PGNParameterID").options[4] = new Option("Switch 4", 4);
			document.getElementById("PGNParameterID").options[5] = new Option("Switch 5", 5);
			document.getElementById("PGNParameterID").options[6] = new Option("Switch 6", 6);
			document.getElementById("PGNParameterID").options[7] = new Option("Switch 7", 7);
			document.getElementById("PGNParameterID").options[8] = new Option("Switch 8", 8);
			document.getElementById("PGNParameterID").options[9] = new Option("Switch 9", 9);
			document.getElementById("PGNParameterID").options[10] = new Option("Switch 10", 10);
			document.getElementById("PGNParameterID").options[11] = new Option("Switch 11", 11);
			document.getElementById("PGNParameterID").options[12] = new Option("Switch 12", 12);
			document.getElementById("PGNParameterID").options[13] = new Option("Switch 13", 13);
			document.getElementById("PGNParameterID").options[14] = new Option("Switch 14", 14);
			document.getElementById("PGNParameterID").options[15] = new Option("Switch 15", 15);
			document.getElementById("PGNParameterID").options[16] = new Option("Switch 16", 16);
			document.getElementById("PGNParameterID").options[17] = new Option("Switch 17", 17);
			document.getElementById("PGNParameterID").options[18] = new Option("Switch 18", 18);
			document.getElementById("PGNParameterID").options[19] = new Option("Switch 19", 19);
			document.getElementById("PGNParameterID").options[10] = new Option("Switch 20", 20);
			document.getElementById("PGNParameterID").options[11] = new Option("Switch 21", 21);
			document.getElementById("PGNParameterID").options[12] = new Option("Switch 22", 22);
			document.getElementById("PGNParameterID").options[13] = new Option("Switch 23", 23);
			document.getElementById("PGNParameterID").options[14] = new Option("Switch 24", 24);
			document.getElementById("PGNParameterID").options[15] = new Option("Switch 25", 25);
			document.getElementById("PGNParameterID").options[16] = new Option("Switch 26", 26);
			document.getElementById("PGNParameterID").options[17] = new Option("Switch 27", 27);
			document.getElementById("PGNParameterID").options[18] = new Option("Switch 28", 28);
		break

		case "IIMWD":
			document.getElementById("PGNParameterID").options[0] = new Option("Wind Direction T", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Wind Direction M", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Wind Speed Knots", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Wind Speed M/S", 3);
		break

		case "IIMWV":
			document.getElementById("PGNParameterID").options[0] = new Option("Wind Direction R", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Wind Direction T", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Wind Speed Knots", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Wind Speed Km/hr", 3);
			document.getElementById("PGNParameterID").options[4] = new Option("Wind Speed Mi/hr", 4);
			document.getElementById("PGNParameterID").options[5] = new Option("Wind Speed M/sec", 5);
		break


		case "IIVWR":
			document.getElementById("PGNParameterID").options[0] = new Option("Wind Direction Apparant", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Wind Speed Knots", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Wind Speed Mi/hr", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Wind Speed Km/hr", 3);
		break

		case "HCHDG":
			document.getElementById("PGNParameterID").options[0] = new Option("Heading Magnetic", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Heading True", 1);
		break

		case "IIVHW":
			document.getElementById("PGNParameterID").options[0] = new Option("Water Direction T", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Water Direction M", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Water Speed Knots", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Water Speed Km/hr", 3);
		break

		case "IIVTG":
			document.getElementById("PGNParameterID").options[0] = new Option("Track T", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Track M", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Track Speed Knots", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Track Speed Km/hr", 3);
		break

		case "IIROT":
			document.getElementById("PGNParameterID").options[0] = new Option("RateOfTurn", 0);
		break

		case "YXXDR":
			document.getElementById("PGNParameterID").options[0] = new Option("Pitch", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Roll", 1);
		break

		case "GPGLL":
			document.getElementById("PGNParameterID").options[0] = new Option("Latitude", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Longitude", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Time", 2);
		break

		case "GPRMC":
			document.getElementById("PGNParameterID").options[0] = new Option("Time", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Latitude", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Longitude", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Speed/Ground", 3);
			document.getElementById("PGNParameterID").options[4] = new Option("Track", 4);
			document.getElementById("PGNParameterID").options[5] = new Option("Date", 5);
			document.getElementById("PGNParameterID").options[6] = new Option("Variation", 6);
		break

		case "SDDBT":
			document.getElementById("PGNParameterID").options[0] = new Option("Depth Feet", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Depth Meters", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Depth Fathoms", 2);
		break

		case "SDMTW":
			document.getElementById("PGNParameterID").options[0] = new Option("Temp C", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Temp F", 1);
		break

		case "WIMDA":
			document.getElementById("PGNParameterID").options[0] = new Option("Baro InHg", 0);
			document.getElementById("PGNParameterID").options[1] = new Option("Baro Bars", 1);
			document.getElementById("PGNParameterID").options[2] = new Option("Air Temp C", 2);
			document.getElementById("PGNParameterID").options[3] = new Option("Water Temp", 3);
			document.getElementById("PGNParameterID").options[4] = new Option("Humidity R", 4);
			document.getElementById("PGNParameterID").options[5] = new Option("Humidity A", 5);
			document.getElementById("PGNParameterID").options[6] = new Option("Dew Point", 6);
			document.getElementById("PGNParameterID").options[7] = new Option("Wind Dir T", 7);
			document.getElementById("PGNParameterID").options[8] = new Option("Wind Dir M", 8);
			document.getElementById("PGNParameterID").options[9] = new Option("Wind Speed Knots", 9);
			document.getElementById("PGNParameterID").options[10] = new Option("Wind Speed M/s", 10);
		break



	   default:
			document.getElementById("PGNParameterID").options[0] = new Option("Undefined", 0);	
		break

	}


}

function SetDialPGNInstance(sel)
{
var myDialID;

	myDialID = document.getElementById("DialID").selectedIndex ;

	//alert(myDialID);

	DialPGNInstance[myDialID] = sel.options[sel.selectedIndex].value;

		// reset Units list to last value = undefined
		//document.getElementById("DialUnits").selectedIndex = 30;
		//DialUnits[myDialID] = 30;
}

function SetClockPGNInstance(sel)
{


	// Clock display is Dial ID = 8
	SystemClockPGNID = sel.options[sel.selectedIndex].value;

	
}

function SetDialPGNParameter(sel)
{
var myDialID;

	myDialID = document.getElementById("DialID").selectedIndex ;

	//alert(myDialID);

	DialPGNParameter[myDialID] = sel.options[sel.selectedIndex].value;

		// reset Units list to last value = undefined
		document.getElementById("DialUnits").selectedIndex = 30;
		DialUnits[myDialID] = 30;
}

// Function to get the settings of the user
function getCookieVal(offset) {
    var endstr = document.cookie.indexOf(";", offset);
    if (endstr == -1)
        endstr = document.cookie.length;
    return unescape(document.cookie.substring(offset, endstr));
}

// Function to get the settings of the user
function GetCookie(name) {
//alert(name);

    var arg = name + "=";
    var alen = arg.length;
    var clen = document.cookie.length;
    var i = 0;
    while (i < clen) {
        var j = i + alen;
        if (document.cookie.substring(i, j) == arg)
            return getCookieVal(j);
        i = document.cookie.indexOf(" ", i) + 1;
        if (i == 0) break;
    }
    return null;
}

// Function to remember the settings
function SetCookie(name, value) {
    var argv = SetCookie.arguments;
    var argc = SetCookie.arguments.length;
    var expires = (argc > 2) ? argv[2] : null;
    var path = (argc > 3) ? argv[3] : null;
    var domain = (argc > 4) ? argv[4] : null;
    var secure = (argc > 5) ? argv[5] : false;
    document.cookie = name + "=" + escape(value) +
	((expires == null) ? "" : ("; expires=" + expires.toGMTString())) +
	((path == null) ? "" : ("; path=" + path)) +
	((domain == null) ? "" : ("; domain=" + domain)) +
	((secure == true) ? "; secure" : "");
}

// Function to remove the settings
function DeleteCookie(name) {
    var exp = new Date();
    exp.setTime(exp.getTime() - 1);
    var cval = GetCookie(name);
    document.cookie = name + "=" + cval + "; expires=" + exp.toGMTString();
}
// Function to ser server radial buttons
function SetServerType(id) {
var exp = new Date();
exp.setTime(exp.getTime() + (30 * 24 * 60 * 60 * 1000));

// alert(' SetServerType = ' + id);

	switch(id){

	case 0: // Local SeaSmart.net adapter
		//alert("0");
		datafile = window.location.href.substring(0,
		window.location.href.lastIndexOf("/") + 1) +
		"GetNMEAData";
		document.getElementById("ServerLocal").checked = true;
		document.getElementById("ServerWeb").checked = false;
		document.getElementById("ServerGlobal").checked = false;
		AccountType = 0;
	break;

	case 1: // Web Server based data folder
	//alert("1");
		datafile = window.location.href.substring(0,
		window.location.href.lastIndexOf("/") + 1) +
		"DATA/" +  AccountDataFolder +"/PushSmartData.htm";
		document.getElementById("ServerLocal").checked = false;
		document.getElementById("ServerWeb").checked = true;
		document.getElementById("ServerGlobal").checked = false;
		AccountType = 1;
	break;

	case 2: // Global based data folder
	//alert("2");
		 datafile = "http://" + AccountDataFolder;
		// alert(datafile);
		document.getElementById("ServerLocal").checked = false;
		document.getElementById("ServerWeb").checked = false;
		document.getElementById("ServerGlobal").checked = true;
		AccountType = 2;
	break;

	default: // Web Server based data folder
//alert("default");
		datafile = window.location.href.substring(0,
		window.location.href.lastIndexOf("/") + 1) +
		"DATA/000000000000/PushSmartData.htm";
		document.getElementById("ServerLocal").checked = false;
		document.getElementById("ServerWeb").checked = true;
		document.getElementById("ServerGlobal").checked = false;
		AccountType = 1;
	break;

	}

	//alert("datafile = " + datafile);

	SetCookie(CookiePrefix +'Account', AccountDataFolder + ":" + AccountType + ":" + ConfigOptions, exp); 

	CloseDialParameters();

}

function getEndDial(myDialStart, myPageLayout)
{
var myEndDial;
var myNumOfDials;

 //   alert(myDialStart + " " + myPageLayout);

myNumOfDials = NumOfDials[myPageLayout];

myEndDial = myDialStart + myNumOfDials;

// alert(myEndDial + " " + myNumOfDials);

if(myEndDial >= MaxDials)
myEndDial = MaxDials;

return myEndDial;

}

function setBack()
{
//alert("ive been clicked back");
}

function setNext()
{

//alert("ive been clicked next");

var myEndDial;
var myNumOfDials;
    var DialIndex=0;
    var CanvasIndex=0;


myNumOfDials = NumOfDials[PageLayout];

if((DialStart + myNumOfDials) < MaxDials)
	DialStart = DialStart + 1;
else
	DialStart = 0;

//	document.location.reload(false);

    DialEnd = getEndDial(DialStart, PageLayout);

 for(DialIndex=DialStart; DialIndex < DialEnd; DialIndex++) //
    {           
      CreateDialTypes(CanvasIndex++, DialIndex, DialType[DialIndex]);
    }

	SavePageCookies();

}
function SavePage()
{
	DialStart = 0;
	SavePageCookies();
}
function ResetPageParameters()
{

	DialStart = 0;

	DeleteCookie(CookiePrefix + 'PageSettings'); 

	for(i=0; i<MaxDials; i++)
	{
		DeleteCookie(CookiePrefix +'Dial' + i + 'Settings'); 

	}

	document.location.reload(false);
}


function ApplyAllDialParameters()
{
var DialIndex;
var myCurrentIndex;

//	DialStart = 0;
//	SavePageCookies();

myCurrentIndex = document.getElementById("DialID").selectedIndex;

 for(DialIndex=0; DialIndex < MaxDials; DialIndex++) //
    {           

	//	alert(DialIndex + "  " + myCurrentIndex);

		DialFrameType[DialIndex] = DialFrameType[myCurrentIndex];
		DialPonterType[DialIndex] = DialPonterType[myCurrentIndex];
		DialBackground[DialIndex] = DialBackground[myCurrentIndex];
		DialPointerColor[DialIndex] = DialPointerColor[myCurrentIndex];
		DialLCDColor[DialIndex] = DialLCDColor[myCurrentIndex];
		
    }

	for(DialIndex=0; DialIndex < NumOfDials[PageLayout]; DialIndex++) //
    {           
		setFrameDesign(DialIndex, DialFrameType[myCurrentIndex]);
		setPointerType(DialIndex, DialPonterType[myCurrentIndex]);
		setDialBackgroundColor(DialIndex, DialBackground[myCurrentIndex]);
		setPointerColor(DialIndex, DialPointerColor[myCurrentIndex]);
		setLcdColor(DialIndex, DialLCDColor[myCurrentIndex]);
    }

}

function ShowParameters()
{
var i;
var gParameters;
var HTMLText;


myWindow=window.open('','','scrollbars=yes, resizable=yes, width=600,height=400')
HTMLText = "//***************************************************<br>";
HTMLText = HTMLText + "//  Account Global Defaults<br>";
HTMLText = HTMLText + "//***************************************************<br>&nbsp;<br>";
myWindow.document.write(HTMLText)

gParameters = "";
gParameters = gParameters + "var AccountType = " +  AccountType + "; <br>";
gParameters = gParameters + "var AccountDataFolder = " +  '"' + AccountDataFolder + '"' + "; <br>";
gParameters = gParameters + "var ConfigOptions = " +  ConfigOptions + "; <br>";
gParameters = gParameters + "&nbsp; <br>";

myWindow.document.write(gParameters)


HTMLText = "//***************************************************<br>";
HTMLText = HTMLText + "//  Page Parameters Global Defaults<br>";
HTMLText = HTMLText + "//***************************************************<br>&nbsp;<br>";
myWindow.document.write(HTMLText)

gParameters = "";
gParameters = gParameters + "var PageID = " +  PageID + "; <br>";
gParameters = gParameters + "var CookiePrefix = " +  '"' + CookiePrefix + '"' + "; <br>";
gParameters = gParameters + "var PageLayout = " +  PageLayout + "; <br>";
gParameters = gParameters + "var DialStart = " +  DialStart + "; <br>";
gParameters = gParameters + "var PageBackGroundColor = " +  '"' + PageBackGroundColor + '"' + "; <br>";
gParameters = gParameters + "var PageForeGroundColor = " +  '"' + PageForeGroundColor + '"' + "; <br>";
gParameters = gParameters + "var ClockLCDColor = " +  ClockLCDColor + "; <br>";
gParameters = gParameters + "var SystemClockPGNID = " +  SystemClockPGNID + "; <br>";
gParameters = gParameters + "var UpdateInterval = " +  UpdateInterval + "; <br>";
gParameters = gParameters + "var DialTimeout = " +  DialTimeout + "; <br>";
gParameters = gParameters + "var xmlDescription = " +   '"' +  xmlDescription  +   '"'  + "; <br>";
gParameters = gParameters + "&nbsp; <br>";

myWindow.document.write(gParameters)

HTMLText = "//***************************************************<br>";
HTMLText = HTMLText + "//  Dial Parameters Global Defaults<br>";
HTMLText = HTMLText + "//***************************************************<br>&nbsp;<br>";
myWindow.document.write(HTMLText)

gParameters = "var DialType  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialType[i] + "," }
gParameters = gParameters + DialType[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);

gParameters = "var DialPGNInstance  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialPGNInstance[i] + "," }
gParameters = gParameters + DialPGNInstance[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);


gParameters = "var DialPGNNumber  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + '"' + DialPGNNumber[i] + '"' + "," }
gParameters = gParameters + '"' + DialPGNNumber[i] + '"';
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);

gParameters = "var DialPGNParameter  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialPGNParameter[i] + "," }
gParameters = gParameters + DialPGNParameter[i]
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);


gParameters = "var DialUnits  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialUnits[i] + "," }
gParameters = gParameters + DialUnits[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);


gParameters = "var DialMin  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialMin[i] + "," }
gParameters = gParameters + DialMin[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);


gParameters = "var DialMax  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialMax[i] + "," }
gParameters = gParameters + DialMax[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);


gParameters = "var DialAlarm  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialAlarm[i] + "," }
gParameters = gParameters + DialAlarm[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);


gParameters = "var DialAlarmState  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialAlarmState[i] + "," }
gParameters = gParameters + DialAlarmState[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);


gParameters = "var DialText  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + '"' + DialText[i] + '"' + "," }
gParameters = gParameters + '"' + DialText[i] + '"';
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);

gParameters = "var DialFrameType  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialFrameType[i] + "," }
gParameters = gParameters + DialFrameType[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);

gParameters = "var DialBackground  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialBackground[i] + "," }
gParameters = gParameters + DialBackground[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);

gParameters = "var DialLCDColor  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialLCDColor[i] + "," }
gParameters = gParameters + DialLCDColor[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);

gParameters = "var DialPointerColor  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialPointerColor[i] + "," }
gParameters = gParameters + DialPointerColor[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);

gParameters = "var DialPonterType  = new Array(";
for(i=0; i<MaxDials-1; i++){ gParameters = gParameters + DialPonterType[i] + "," }
gParameters = gParameters + DialPonterType[i];
gParameters = gParameters + "); <br>"
myWindow.document.write(gParameters);


 myWindow.focus()
}

function escapeHTML( string )
{
    var pre = document.createElement('pre');
    var text = document.createTextNode( string );
    pre.appendChild(text);
    return pre.innerHTML;
}

function ParseXMLData(xmlDoc) {
//var xmlDials=xmlDoc.getElementsByTagName("dial");
var xmlDials;
var xmlPages=xmlDoc.getElementsByTagName("PageSettings");
var xmlDialId;

	if(xmlPages.length <= 0)
	return;

	document.getElementById("XMLFilesSelect").options.length = 0;
	document.getElementById("XMLFilesSelect").options[0] = new Option("Use defaults", 0);
    document.getElementById("XMLFilesSelect").options[1] = new Option("Use Cookies", 1);

	for(i=0; i<xmlPages.length; i++)
    {
		tempXMLdata= xmlPages[i].getElementsByTagName("xmlDescription")[0].childNodes[0].nodeValue;
		

		document.getElementById("XMLFilesSelect").options[i+2] = new Option("XML-" + tempXMLdata, i+2);
		
		//alert(tempXMLdata);
	}

	if(ConfigOptions <= (xmlPages.length + 2))
		document.getElementById("XMLFilesSelect").selectedIndex = ConfigOptions;
	else
		document.getElementById("XMLFilesSelect").selectedIndex = 0;

	if((ConfigOptions <= (xmlPages.length + 2)) && ConfigOptions > 1)
	{
	    
		PageID = xmlPages[ConfigOptions-2].getElementsByTagName("PageID")[0].childNodes[0].nodeValue;
		CookiePrefix = xmlPages[ConfigOptions-2].getElementsByTagName("CookiePrefix")[0].childNodes[0].nodeValue;
		PageLayout = xmlPages[ConfigOptions-2].getElementsByTagName("PageLayout")[0].childNodes[0].nodeValue;
		DialStart = xmlPages[ConfigOptions-2].getElementsByTagName("DialStart")[0].childNodes[0].nodeValue;
		PageBackGroundColor = xmlPages[ConfigOptions-2].getElementsByTagName("PageBackGroundColor")[0].childNodes[0].nodeValue;
		PageForeGroundColor = xmlPages[ConfigOptions-2].getElementsByTagName("PageForeGroundColor")[0].childNodes[0].nodeValue;
		ClockLCDColor = xmlPages[ConfigOptions-2].getElementsByTagName("ClockLCDColor")[0].childNodes[0].nodeValue;
		SystemClockPGNID = xmlPages[ConfigOptions-2].getElementsByTagName("SystemClockPGNID")[0].childNodes[0].nodeValue;
		UpdateInterval = xmlPages[ConfigOptions-2].getElementsByTagName("UpdateInterval")[0].childNodes[0].nodeValue;
		DialTimeout = xmlPages[ConfigOptions-2].getElementsByTagName("DialTimeout")[0].childNodes[0].nodeValue;
		xmlDescription = xmlPages[ConfigOptions-2].getElementsByTagName("xmlDescription")[0].childNodes[0].nodeValue;

		xmlPages=xmlDoc.getElementsByTagName("page");
		xmlDials=xmlPages[ConfigOptions-2].getElementsByTagName("dial");
	//alert(xmlDials.length);

		for(i=0; i<xmlDials.length; i++)
	    {
			  xmlDialId= xmlDials[i].getElementsByTagName("DialID")[0].childNodes[0].nodeValue;
			  DialType[xmlDialId] = xmlDials[i].getElementsByTagName("DialType")[0].childNodes[0].nodeValue;
			  DialPGNInstance[xmlDialId] = xmlDials[i].getElementsByTagName("DialPGNInstance")[0].childNodes[0].nodeValue;	
			  DialPGNNumber[xmlDialId] = xmlDials[i].getElementsByTagName("DialPGNNumber")[0].childNodes[0].nodeValue;
			  DialPGNParameter[xmlDialId] = xmlDials[i].getElementsByTagName("DialPGNParameter")[0].childNodes[0].nodeValue;	
			  DialUnits[xmlDialId] = xmlDials[i].getElementsByTagName("DialUnits")[0].childNodes[0].nodeValue;
			  DialMin[xmlDialId] = xmlDials[i].getElementsByTagName("DialMin")[0].childNodes[0].nodeValue;	
			  DialMax[xmlDialId] = xmlDials[i].getElementsByTagName("DialMax")[0].childNodes[0].nodeValue;
			  DialAlarm[xmlDialId] = xmlDials[i].getElementsByTagName("DialAlarm")[0].childNodes[0].nodeValue;	
			  DialAlarmState[xmlDialId] = xmlDials[i].getElementsByTagName("DialAlarmState")[0].childNodes[0].nodeValue;
			  DialText[xmlDialId] = xmlDials[i].getElementsByTagName("DialText")[0].childNodes[0].nodeValue;	
			  DialFrameType[xmlDialId] = xmlDials[i].getElementsByTagName("DialFrameType")[0].childNodes[0].nodeValue;
			  DialBackground[xmlDialId] = xmlDials[i].getElementsByTagName("DialBackground")[0].childNodes[0].nodeValue;	
			  DialLCDColor[xmlDialId] = xmlDials[i].getElementsByTagName("DialLCDColor")[0].childNodes[0].nodeValue;
			  DialPointerColor[xmlDialId] = xmlDials[i].getElementsByTagName("DialPointerColor")[0].childNodes[0].nodeValue;	
			  DialPonterType[xmlDialId] = xmlDials[i].getElementsByTagName("DialPonterType")[0].childNodes[0].nodeValue;	

	     //alert(tempXMLdata);
	    }
   }

}

function ShowParametersXML()
{
var i;
var gParameters;

var Tab1 = "&nbsp;&nbsp;&nbsp;";
var Tab2 = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
var Tab3 = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";
var Tab4 = "&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;";



var myHTMLString;



//&lt;SSXML&gt;
myHTMLString = "</SSXML>";

myHTMLString = escapeHTML(myHTMLString);

//alert (myHTMLString);

myWindow=window.open('','','scrollbars=yes, resizable=yes, width=600,height=400');
//myWindow.document.write("<p>XML Config</p>");

myWindow.document.write(escapeHTML("<?xml version=\"1.0\" encoding=\"ISO-8859-1\"?>")+ "<br>");
myWindow.document.write(escapeHTML("<!-- Edited by Chetco Digital Instruments, Inc. copyright 2012 -->") + "<br>");
//myWindow.document.write(escapeHTML("<SSXML>")+ "<br>");
//myWindow.document.write(escapeHTML("  <page>")+ "<br>");
//myWindow.document.write(escapeHTML("    <dial>")+ "<br>");

	myHTMLString = "&lt;SSXML&gt; <br>";
	myWindow.document.write(myHTMLString);
	
for(j=0; j<1; j++)
{		
	myHTMLString = Tab1 + "&lt;page&gt; <br>";

	myHTMLString = myHTMLString + Tab2 +"&lt;PageSettings&gt; <br>";
	myHTMLString = myHTMLString + Tab3 + "&lt;PageID&gt;" + j + "&lt;/PageID&gt;" + "<br>"
	myHTMLString = myHTMLString + Tab3 + "&lt;CookiePrefix&gt;" + CookiePrefix + "&lt;/CookiePrefix&gt;" + "<br>"

	myHTMLString = myHTMLString + Tab3 + "&lt;PageLayout&gt;" + PageLayout + "&lt;/PageLayout&gt;" + "<br>"
	myHTMLString = myHTMLString + Tab3 + "&lt;DialStart&gt;" + DialStart + "&lt;/DialStart&gt;" + "<br>"
	myHTMLString = myHTMLString + Tab3 + "&lt;PageBackGroundColor&gt;" + PageBackGroundColor + "&lt;/PageBackGroundColor&gt;" + "<br>"
	myHTMLString = myHTMLString + Tab3 + "&lt;PageForeGroundColor&gt;" + PageForeGroundColor + "&lt;/PageForeGroundColor&gt;" + "<br>"
	myHTMLString = myHTMLString + Tab3 + "&lt;ClockLCDColor&gt;" + ClockLCDColor + "&lt;/ClockLCDColor&gt;" + "<br>"
	myHTMLString = myHTMLString + Tab3 + "&lt;SystemClockPGNID&gt;" + SystemClockPGNID + "&lt;/SystemClockPGNID&gt;" + "<br>"
	myHTMLString = myHTMLString + Tab3 + "&lt;UpdateInterval&gt;" + UpdateInterval + "&lt;/UpdateInterval&gt;" + "<br>"
	myHTMLString = myHTMLString + Tab3 + "&lt;DialTimeout&gt;" + DialTimeout + "&lt;/DialTimeout&gt;" + "<br>"
	myHTMLString = myHTMLString + Tab3 + "&lt;xmlDescription&gt;" + xmlDescription + "&lt;/xmlDescription&gt;" + "<br>"
	myHTMLString = myHTMLString + Tab2 + "&lt;/PageSettings&gt; <br>";
	myWindow.document.write(myHTMLString);

		for(i=0; i<MaxDials; i++)
		{
			myHTMLString = Tab2 +"&lt;dial&gt; <br>";
			myHTMLString = myHTMLString + Tab3 + "&lt;DialID&gt;" + i + "&lt;/DialID&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialType&gt;" + DialType[i] + "&lt;/DialType&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialPGNInstance&gt;" + DialPGNInstance[i] + "&lt;/DialPGNInstance&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialPGNNumber&gt;" + DialPGNNumber[i] + "&lt;/DialPGNNumber&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialPGNParameter&gt;" + DialPGNParameter[i] + "&lt;/DialPGNParameter&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialUnits&gt;" + DialUnits[i] + "&lt;/DialUnits&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialMin&gt;" + DialMin[i] + "&lt;/DialMin&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialMax&gt;" + DialMax[i] + "&lt;/DialMax&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialAlarm&gt;" + DialAlarm[i] + "&lt;/DialAlarm&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialAlarmState&gt;" + DialAlarmState[i] + "&lt;/DialAlarmState&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialText&gt;" + DialText[i] + "&lt;/DialText&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialFrameType&gt;" + DialFrameType[i] + "&lt;/DialFrameType&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialBackground&gt;" + DialBackground[i] + "&lt;/DialBackground&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialLCDColor&gt;" + DialLCDColor[i] + "&lt;/DialLCDColor&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&nbsp;&lt;DialPointerColor&gt;" + DialPointerColor[i] + "&lt;/DialPointerColor&gt;" + "<br>"
			myHTMLString = myHTMLString + Tab3 + "&lt;DialPonterType&gt;" + DialPonterType[i] + "&lt;/DialPonterType&gt;" + "<br>"	
			myHTMLString = myHTMLString + Tab2 + "&lt;/dial&gt; <br>";

			myWindow.document.write(myHTMLString);	
		}

	myHTMLString = Tab1 + "&lt;/page&gt; <br>"

	myWindow.document.write(myHTMLString);

}


	myHTMLString = "&lt;/SSXML&gt; <br>";
	myWindow.document.write(myHTMLString);



 myWindow.focus();
}


function SetXMLFileOptionList(id, selText)
{

}

function selectXMLFile(sel)
{
var exp = new Date();
exp.setTime(exp.getTime() + (30 * 24 * 60 * 60 * 1000));
	

  ConfigOptions = document.getElementById("XMLFilesSelect").selectedIndex;

 // alert(ConfigOptions);

	SetCookie(CookiePrefix +'Account', AccountDataFolder + ":" + AccountType + ":" + ConfigOptions, exp);

	CloseDialParameters();

	 document.location.reload(false);
}