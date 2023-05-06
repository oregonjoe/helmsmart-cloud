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


//SavePageCookies();

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
                 // N2KValues =  GetPGNbyNumber(String(mydata), DialPGNInstance[DialIndex], DialPGNNumber[DialIndex], DialPGNParameter[DialIndex], DialUnits[DialIndex] );
				  N2KValues =  GetPGNbyNumber(mydata, DialPGNInstance[DialIndex], DialPGNNumber[DialIndex], DialPGNParameter[DialIndex], DialUnits[DialIndex] );
				   UpdateDialValues(CanvasIndex++, N2KValues);
              }

              

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
				
				SetHelmSmartSwitch(SwitchPGN);

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

 // document.getElementById("PGNNumber").value = DialPGNNumber[myDialID];
 // SetPGNParamatersOptionList(DialPGNNumber[myDialID]);
 // SetPGNInstanceOptionList(DialPGNNumber[CurrentDialID]);
  var myPGNString = GetPGNTypeFromSeries(DialPGNNumber[myDialID], DialPGNInstance[myDialID],  DialPGNParameter[myDialID]);
  
  	  	 document.getElementById("PGNTypeID").selectedIndex = 0;
		 for(i=0; i< document.getElementById("PGNTypeID").options.length; i++)
		 {
			myEvent = document.getElementById("PGNTypeID").options[i].value;
			
			  if(myEvent.trim() == myPGNString.trim())
					document.getElementById("PGNTypeID").selectedIndex = i;
		} 
    //document.getElementById("PGNParameterID").selectedIndex = DialPGNParameter[myDialID];
	//document.getElementById("PGNInstance").selectedIndex = DialPGNInstance[myDialID];

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

	
}

function ShowHideDialParameters(showhide) {


}


function ShowHidePGNs(showhide) {

	
}

function ShowHidePageParams(showhide) {

	
}

function ShowHideAccountParams(showhide) {

	

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

					if(currentState == 1)
					{
						setLcdColor(DialIndex, parseInt(DialPointerColor[DialIndex]));

							SetgSwitchStates(DialIndex, 1);

						if(SwitchState[DialIndex] == 1)
						 radialDial[DialIndex].setflashing(false);
							

					}
					else if(currentState == 0)
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
    document.getElementById("PGNInstance").selectedIndex = DialPGNInstance[CurrentDialID];
    
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
 
var myDialID = parseInt(document.getElementById("DialID").selectedIndex) ;

       myText = sel.value;

	//	alert(myText);
		//	alert(CurrentDialID);
DialText[myDialID] = myText ;
	
	if(DialType[myDialID] == 15 || DialType[myDialID] == 16)
		radialDial[myDialID].setValue(DialText[myDialID]);
	else if(DialType[myDialID] < 8)
		radialDial[myDialID].setTitleString(myText);
	
	
	
	
}

// Sets the current dial Units Text
function updateDialUnits(sel) 
{
var myDialID = parseInt(document.getElementById("DialID").selectedIndex );

	
		DialUnits[myDialID] = sel.options[sel.selectedIndex].value;

	SetDialUnits(myDialID, sel.options[sel.selectedIndex].value);
}
// Sets the current dial Units Text
function SetDialUnits(DialID, UnitsID) 
{
var myDialID = parseInt(document.getElementById("DialID").selectedIndex) ;
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

		case 33:
			radialDial[DialID].setUnitString("Meters");
		break;

		case 32:
			radialDial[DialID].setUnitString("Feet");
		break;
		
		case 34:
			radialDial[DialID].setUnitString("Miles");
		break;

		case 35:
			radialDial[DialID].setUnitString("Nautical Mile");
		break;
		
		
		case 36:
			radialDial[DialID].setUnitString("Fathoms");
		break;
		
		case 37:
			radialDial[DialID].setUnitString("Time");
		break;

		case 38:
			radialDial[DialID].setUnitString("Date");
		break;

		case 39:
			radialDial[DialID].setUnitString("Hours");
		break;

		case 40:
			radialDial[DialID].setUnitString("Indicator");
		break;
		


		case 41:
			radialDial[DialID].setUnitString("Switch");
		break;
		
		case 42:
			radialDial[DialID].setUnitString("Dimmer");
		break;		
		

		case 43:
			radialDial[DialID].setUnitString("Dimmer Status");
		break;
		
		case 44:
			radialDial[DialID].setUnitString("volts");
		break;

		case 45:
			radialDial[DialID].setUnitString("amps");
		break;		
		
		case 46:
			radialDial[DialID].setUnitString("Inches");
		break;

		case 47:
			radialDial[DialID].setUnitString("millimeters");
		break;		
		
		case 48:
			radialDial[DialID].setUnitString("undefined");
		break;
	


	}
       
}


// Sets the current dial Minimum
function SetDialMin(sel) 
{
var myMin;
	var myDialID = parseInt(document.getElementById("DialID").selectedIndex) ;

	//alert(myDialID);

		// reset Units list to last value = undefined
	
	
        myMin = parseInt(sel.value);

	//	alert(myMin);

	DialMin[myDialID] = myMin;
		//	alert(CurrentDialID);

	radialDial[myDialID].setMinValue(myMin);

	createDialSections(myDialID,DialMin[myDialID],DialMax[myDialID]);
	createDialGradients(myDialID,DialMin[myDialID],DialMax[myDialID]);
}

// Sets the current dial Maximum
function SetDialMax(sel) 
{
var myMax;
var myDialID = parseInt(document.getElementById("DialID").selectedIndex );
        myMax = parseInt(sel.value);

	//	alert(myDialID);


		//	alert(myMax);
	DialMax[myDialID] = myMax;
	//alert(DialMax[myDialID]);
	radialDial[myDialID].setMaxValue(myMax);
	createDialSections(myDialID,DialMin[myDialID],DialMax[myDialID]);
	createDialGradients(myDialID,DialMin[myDialID],DialMax[myDialID]);

}

// Sets the current dial Alarm
function SetDialAlarm(sel) 
{
var myAlarm;
var myDialID = parseInt(document.getElementById("DialID").selectedIndex) ;
        myAlarm = parseInt(sel.value);

	//	alert(myDialID);


		//	alert(myMax);
	DialAlarm[myDialID] = myAlarm;
	//alert(DialMax[myDialID]);
	radialDial[myDialID].setThreshold(myAlarm);

}

// Selects the current dial Alarm
function SelectAlarmState(sel) 
{
 var myDialID = parseInt(document.getElementById("DialID").value) ;

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


var myDialID = parseInt(document.getElementById("DialID").value) ;


CurrentDialID = myDialID;
CurrentCanvasID = myDialID;

DialType[myDialID] = parseInt(sel.options[sel.selectedIndex].value);

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
		
		case 17:
		
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
			
}

function ChangedPGNTypeID(sel)
{
myDialID = document.getElementById("DialID").selectedIndex ;

 var myseries = sel.options[sel.selectedIndex].value;

 var myserieskey =makePGNfromEvent(myseries, "*")
 
 
 
 myKeys = myserieskey.split(".")
		
		myKey = myKeys[0].split(":");
		DialPGNNumber[myDialID]  = myKey[1];
		
		myKey = myKeys[1].split(":");
		myPGNSource = myKey[1];
		
		myKey = myKeys[2].split(":");
		DialPGNInstance[myDialID] = parseInt(myKey[1]);
		
		//myKey = myKeys[4].split(":");
		//myPGNType = myKey[1];
		
		myKey = myKeys[4].split(":");
		DialPGNParameter[myDialID]  = parseInt(myKey[1]);
		
	
}

function SetPGNNumberOptionList(sel)
{
myDialID = document.getElementById("DialID").selectedIndex ;
DialPGNNumber[myDialID] = sel.options[sel.selectedIndex].value;
	
	
}

function SetPGNInstanceOptionList(selText)
{


}

function SetPGNParamatersOptionList(selText)
{


}

function SetDialPGNInstance(sel)
{

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
/*
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
*/
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
	window.location.reload();
	// document.location.reload(false);
}