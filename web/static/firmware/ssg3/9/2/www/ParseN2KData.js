// This Script parses SeaSmart.net NMEA 2000 data
// Written 11/01/12
// Chetco Digital Instruments
//
var TEMPFAHRENHEIT	= 0x0000;	// MASK = 0x0003
var TEMPCELCUIS		= 0x0001;	// MASK = 0x0003
var TEMPKELVIN		= 0x0002;	// MASK = 0x0003

var SPEEDKNOTS		= 0x0000;	// MASK = 0x000C
var SPEEDMPH		= 0x0004;	// MASK = 0x000C
var SPEEDKPH		= 0x0008;	// MASK = 0x000C

var PRESSUREPSI		= 0x0000;	// MASK = 0x0030
var PRESSUREKPH		= 0x0010;	// MASK = 0x0030
var PRESSUREINHG	= 0x0020;	// MASK = 0x0030

var REFERENCETRUE	= 0x0000;	// MASK = 0x00C0
var REFERENCEMAG	= 0x0040;	// MASK = 0x00C0

var ANGLEDEGREES	= 0x0000;	// MASK = 0x0300
var ANGLERADIANS	= 0x0100;	// MASK = 0x0300

var VOLUMELITERS	= 0x0000;	// MASK = 0x0C00
var VOLUMEGALLON	= 0x0400;	// MASK = 0x0C00
var VOLUMECUMETER	= 0x0800;	// MASK = 0x0C00

// converts PGN value to NMEA 2000 temperature converted to specified units
function parseN2KTemperature(myPGNValue,myUnitsFlags, Scale)
{
        if (myPGNValue == 0xFFFF) 
		{
			return null;
		}
        else 
		{	
			if(myUnitsFlags == 1) // degrees C
				return Math.floor((myPGNValue * Scale * 0.01) - 273);
			else if(myUnitsFlags  == 2) // degrees Kelvin
				return Math.floor(myPGNValue * Scale * 0.01 );
			else // default is degrees F
				return Math.floor((myPGNValue * Scale *  0.018 ) - 459);
		}	
	
}


// converts PGN value to NMEA 2000 pressure converted to specified units
function parseN2KPressure(myPGNValue,myUnitsFlags, Scale)
{
        if (myPGNValue == 0xFFFF) 
		{
			return null;
		}
        else 
		{	

			if(myUnitsFlags  == 8) // PSI
				return Math.floor((myPGNValue * Scale * 0.0145037738007) ) ;  
			else if(myUnitsFlags == 9) // kPa
				return Math.floor(myPGNValue * Scale * 0.1)  ;  //0.01 kPA
			else if(myUnitsFlags  == 10) // inHg
				return (myPGNValue * Scale * 0.0295229).toFixed(2); 
			else // default mbar
				return Math.floor(myPGNValue * Scale * 1.0);

		}	
	
}

// converts PGN value to NMEA 2000 volts converted to specified units
function parseN2KVoltsAmps(myPGNValue,myUnitsFlags, Scale)
{
        if (myPGNValue == 0x7FFF) 
		{
			return null;
		}
        else 
		{	
			return (myPGNValue * Scale * 0.01 ).toFixed(2); 
		}	
	
}


// converts PGN value to NMEA 2000 Level converted to specified units
function parseN2KLevel(myPGNValue,myUnitsFlags, Scale)
{
        if (myPGNValue == 0x7FFF) 
		{
			return null;
		}
        else 
		{	
			return (myPGNValue * Scale * 0.004).toFixed(2);

		}	
	
}

// converts PGN value to NMEA 2000 Flow Rate converted to specified units
function parseN2KFlowRate(myPGNValue, myUnitsFlags, Scale)
{
        if (myPGNValue == 0x7FFF) 
		{
			return null;
		}
        else 
		{	
			if(myUnitsFlags == 19) // liters/hr
				return (myPGNValue * Scale * 0.10).toFixed(2);
			else if(myUnitsFlags  == 18) // gallons/hr
				return (myPGNValue * Scale * 0.0264172).toFixed(2);
			else // default cubic meters/hr
				return (myPGNValue * Scale * 0.0001).toFixed(2);	 		
		}	
	
}


// converts PGN value to NMEA 2000 Fluid Capicity converted to specified units
function parseN2KFluidCapacity(myPGNValue, myUnitsFlags, Scale)
{
        if (myPGNValue == 0x7FFF) 
		{
			return null;
		}
        else 
		{	
			if(myUnitsFlags == 19) // liters/hr
				return Math.floor(myPGNValue * Scale * 1.00);
			else if(myUnitsFlags  == 18) // gallons/hr
				return Math.floor(myPGNValue * Scale * 0.264172);
			if(myUnitsFlags == 20) // liters/hr
				return Math.floor(myPGNValue * Scale * 1.00);
			else if(myUnitsFlags  == 21) // gallons/hr
				return Math.floor(myPGNValue * Scale * 0.264172);				
			else // default cubic meters/hr
				return Math.floor(myPGNValue * Scale * 0.001);		 		
		}	
	
}



// GetPGNbyNumber
// 
// myN2Kdata   -> DataString
// myPGNInstance  -> INstance Number
// myPGNNumber  -> PGN
//
function GetPGNbyNumber(myN2KdataArray, DialIndex, myPGNInstance, myPGNNumber, myParameterIndex, myUnitsFlags, myflashSwitch )
{
var flashSwitch;

if(arguments.length == 5) {
flashSwitch = true;
}
else {
flashSwitch = myflashSwitch;
}

var myN2Kdata = new Array();

var myN2KValues = new Array();

    for(i=0; i< myN2KdataArray.length; i++)
    {
	
		myN2Kdata = myN2KdataArray[i];
        if(myN2Kdata.length == 4)
         {
			
        if(parseInt(myN2Kdata[0],16) == parseInt(myPGNNumber))
        {

            switch(myPGNNumber)
            {
                case "127488":
					var N2KValue = GetPGN127488(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
					
                break

                case"127489":
					var N2KValue = GetPGN127489(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                case"127508":
					var N2KValue = GetPGN127508(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                case"127506":
					var N2KValue = GetPGN127506(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                case"127505":
					var N2KValue = GetPGN127505(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                case"127493":
					var N2KValue = GetPGN127493(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                case"130311":
					var N2KValue = GetPGN130311(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                case"130314":
					var N2KValue = GetPGN130314(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                case"130323":
					var N2KValue = GetPGN130323(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                case"130306":
					var N2KValue =GetPGN130306(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                case"127250":
					var N2KValue = GetPGN127250(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                case"127257":
					var N2KValue = GetPGN127257(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				case"65292":
					var N2KValue = GetPGN65292(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				

				case"65262":
					var N2KValue = GetPGN65262(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				
				case"65263":
					var N2KValue = GetPGN65263(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
			
				case"65271":
					var N2KValue = GetPGN65271(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				case"65272":
					var N2KValue = GetPGN65272(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				
				
				case"65276":
					var N2KValue = GetPGN65276(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break


				case"61444":
					var N2KValue = GetPGN61444(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				
				
				
				
				
				
				
				
				
				
				
				
				
				case"65014":
					var N2KValue = GetPGN65014(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				case"65011":
					var N2KValue = GetPGN65011(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				
				case"65008":
					var N2KValue = GetPGN65008(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break	


				case"65017":
					var N2KValue = GetPGN65017(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				case"65005":
					var N2KValue = GetPGN65005(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				case"65027":
					var N2KValue = GetPGN65027(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				case"65024":
					var N2KValue = GetPGN65024(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				
				case"65021":
					var N2KValue = GetPGN65021(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break	


				case"65030":
					var N2KValue = GetPGN65030(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				case"65018":
					var N2KValue = GetPGN65018(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				// Custom Dimmer
				case"65286":
					var N2KValue = GetPGN65286(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break				
				
				
				case"65287":
					var N2KValue = GetPGN65287(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				// AC Volt/Amps detail
				case"65288":
					var N2KValue = GetPGN65288(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

				
				
                // water depth
                case"128267":
					var N2KValue = GetPGN128267(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                // water speed
                case"128259":
					var N2KValue = GetPGN128259(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                // Environmential Temperature 0x1FD08
                case"130312":
					var N2KValue = GetPGN130312(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				
				// Environmential Temperature 0x1FD0A
                case"130316":
					var N2KValue = GetPGN130316(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                // Rudder 0x1FD08
                case"127245":
					var N2KValue = GetPGN127245(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                // Rate of Turn 0x1F10D
                case"127251":
					var N2KValue = GetPGN127251(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;
                break

                // Switch Status 0x1F20D
                case"127501":
					var N2KValue = GetPGN127501(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags, DialIndex, flashSwitch);
					if(N2KValue.length != 0)
						return N2KValue;
                break
				// SOG COG
                case"129026":
					var N2KValue = GetPGN129026(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;

                break
				// Position Rapid
				case"129025":
					var N2KValue = GetPGN129025(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;

                break
				
				//GNSS Position data
				case"129029":
					var N2KValue = GetPGN129029(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;

                break
				
				
				//Trip Parameters Engine
				case"127497":
					var N2KValue = GetPGN127497(myN2KdataArray[i],myPGNInstance,myParameterIndex,myUnitsFlags);
					if(N2KValue.length != 0)
						return N2KValue;

                break
				
/*
                case"IIMWD":
                myN2KValues=GetIIMWD(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"IIMWV":
                myN2KValues=GetIIMWV(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"IIVWR":
                myN2KValues=GetIIVWR(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"HCHDG":
                myN2KValues=GetHCHDG(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"IIVHW":
                myN2KValues=GetIIVHW(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"IIVTG":
                myN2KValues=GetIIVTG(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"IIROT":
                myN2KValues=GetIIROT(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"YXXDR":
                myN2KValues=GetYXXDR(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"GPGLL":
                myN2KValues=GetGPGLL(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"GPRMC":
                myN2KValues=GetGPRMC(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"SDDBT":
                myN2KValues=GetSDDBT(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"SDMTW":
                myN2KValues=GetSDMTW(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

                case"WIMDA":
                myN2KValues=GetWIMDA(myN2Kdata,myPGNInstance,myParameterIndex,myUnitsFlags);
                break

*/
                default:

                break;
				}
			}
        }
     }

return myN2KValues;


}




//
// System Time
//
function GetPGN126992(myN2Kdata, SystemClockPGNID ) {
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    var myPGNInstance;
    var myPGN;
    var myPGNValue;
   
    var vGN2KTime = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
    var myTimeStr = new String();

	    var vGYear;
    var vGMonth;
    var vGDay;
    var vGHour;
    var vGMin;
    var vGSec;

    var NGTDate = new Date(0);

//mySubStrings = myN2Kdata.split("$PCDIN,01F010,");

   // myArrayLength = mySubStrings.length;

      vGYear = 0;
      vGHour = 0;

      // Get all the elements and parse into variables
      //for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr =  myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
			
             myTimeStr = myHexStr.substr(7, 8);
             myHexStr = myHexStr.substr((22-12-7), 1);
             myPGNInstance = parseInt("0x" + myHexStr);

		//	 alert('clock = ' + SystemClockPGNID);

             if (myPGNInstance == SystemClockPGNID) 
             {
                  myHexStr = myN2Kdata[3];

					// look for checksum character in the correct place or skip if(myHexStr.substr(28-12 ,1) == '*')
					{
                                 myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);
                                 myPGNValue = parseInt(myHexStr);

                                 vGDay = (myPGNValue * 86400) * 1000;


                                 myHexStr = myN2Kdata[3];
                                 myHexStr = "0x" + myHexStr.substr((33-12-7), 2) + myHexStr.substr((31-12-7), 2);

                                 myPGNValue = parseInt(myHexStr);

                                 vGHour = myPGNValue + (myPGNValue * 65536);


                                 myHexStr = myN2Kdata[3];
                                 myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);
                                 myPGNValue = parseInt(myHexStr);

                                 vGSec = vGHour + (myPGNValue);
                                 vGSec = Math.floor(vGSec / 10);

								 vGSec = Math.floor(vGSec + vGDay);
                                 NGTDate.setTime(vGSec);
                         
	                             //N2KTimeEPOCH = Date.parse(N2KTimeStr);		
                                   vGN2KTime.push([NGTDate.toUTCString(), myTimeStamp]);
                             
                              } // String greater then 28
                         } // Time Instance
			 } //good checksum character
         } // PGN126992 Array Loop

	return vGN2KTime;
		//return "this is a test";

} // end of function GetPGN 126992
//
// GNSS System Time
//
function GetPGN129029TS(myN2Kdata, SystemClockPGNID ) {
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    var myPGNInstance;
    var myPGN;
    var myPGNValue;
   
    var vGN2KTime = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
    var myTimeStr = new String();

	    var vGYear;
    var vGMonth;
    var vGDay;
    var vGHour;
    var vGMin;
    var vGSec;

    var NGTDate = new Date(0);

//mySubStrings = myN2Kdata.split("$PCDIN,01F010,");

   // myArrayLength = mySubStrings.length;

      vGYear = 0;
      vGHour = 0;
         myHexStr =myN2Kdata[3];;  
			 // look for checksum character in the correct place or skip var myIndex = myHexStr.indexOf('*');
			 
			if(myIndex > 0)
			{
				var checksum = parseInt("0x" + myHexStr.substr((myIndex +1) ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,myIndex));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr =  myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
			
            // myTimeStr = myHexStr.substr(7, 8);
           //  myHexStr = myHexStr.substr((22-12-7), 1);
           //  myPGNInstance = parseInt(myHexStr);



            // if (myPGNInstance == SystemClockPGNID) 
             {
                  myHexStr = myN2Kdata[3];

					// look for checksum character in the correct place or skip 
					//if(myHexStr.substr(28-12 ,1) == '*')
					{
                                 myHexStr = "0x" + myHexStr.substr((4), 2) + myHexStr.substr((2), 2);
                                 myPGNValue = parseInt(myHexStr);

                                 vGDay = (myPGNValue * 86400) * 1000;


                                 myHexStr = myN2Kdata[3];
                                 myHexStr = "0x" + myHexStr.substr((12), 2) + myHexStr.substr((10), 2);

                                 myPGNValue = parseInt(myHexStr);

                                 vGHour = myPGNValue + (myPGNValue * 65536);


                                 myHexStr = myN2Kdata[3];
                                 myHexStr = "0x" + myHexStr.substr((8), 2) + myHexStr.substr((6), 2);
                                 myPGNValue = parseInt(myHexStr);

                                 vGSec = vGHour + (myPGNValue);
                                 vGSec = Math.floor(vGSec / 10);

								 vGSec = Math.floor(vGSec + vGDay);
                                 NGTDate.setTime(vGSec);
                         
	                             //N2KTimeEPOCH = Date.parse(N2KTimeStr);		
                                   vGN2KTime.push([NGTDate.toUTCString(), myTimeStamp]);
                             
                              } // String greater then 28
                         } // Time Instance
			 } //good checksum character
 

	return vGN2KTime;
		//return "this is a test";

} // end of function GetPGN 126992
// Engine Parameters Dynamic
// PGN 127488 [0x01F200] Environmential Parameters
// myParameterIndex = 0  -> Tachometer
// myParameterIndex = 1  -> Boost
// myParameterIndex = 2  -> Trim
//
function GetPGN127488(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
	var myTimeStamp;
    var myTimeStampStr;
	
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F200,");
	mySubStrings = myN2Kdata[3];
	
    //myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

            // myHexStr = mySubStrings[myIndex];
			 myHexStr = myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
				var myTimeStamp;
				var myTimeStampStr;
	
				//myTimeStampStr = myHexStr.substr(0 ,6)
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;


			 myHexStr = "0x" + myHexStr.substr(0 ,2) ;
		     myInstance = parseInt(myHexStr);
				

			
				if(myInstance == myPGNInstance) // field 0 Tachometer 
				{                      
					if(myParameterIndex == 0)
					  {
						  // field 0 Tachometer
						  myHexStr = "0x" + myN2Kdata[3].substr(4, 2) + myN2Kdata[3].substr(2, 2);

						  myPGNValue = parseInt(myHexStr);
						  
						  if(myPGNValue != 0xFFFF)
							myPGNData.push([(myPGNValue * 0.25), myTimeStamp]) ;
						  
						  
					 }
					 else if(myParameterIndex == 1)  // get Boost pressure
					{						
                        // field 1
						myHexStr = "0x" + myN2Kdata[3].substr(8, 2) + myN2Kdata[3].substr(6, 2);

						myPGNValue = parseN2KTemperature(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					}
							 
                    else if(myParameterIndex == 2) //Trim %
					{
					
						myHexStr = "0x" + myN2Kdata[3].substr(10, 2);

						myPGNValue = parseN2KLevel(parseInt(myHexStr),myUnitsFlags, 250);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					}
                          
          
			} // Instance match
		}// good checksum
	} // 127488 Array Loop

	return myPGNData;

} // end of function GetPGN 127489

// Engine Parameters Dynamic
// PGN 127489 [0x01F201] Environmential Parameters
// myParameterIndex = 0  -> Oil Pressure
// myParameterIndex = 1  -> Oil Temp
// myParameterIndex = 2  -> Engine Temp
// myParameterIndex = 3  -> Volts
// myParameterIndex = 4  -> Fuel rate
// myParameterIndex = 5  -> Engine Hours
// myParameterIndex = 6  -> Fuel Pressure
// myParameterIndex = 7  -> Coolant Pressure
//
function GetPGN127489(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(52 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(53 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,52));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
             // get instance
			 myHexStr = "0x" + myHexStr.substr(0 ,2) ;
		     myInstance = parseInt(myHexStr);
				

			
				if(myInstance == myPGNInstance) // Outside Temp and Baro
				{                      


                      myPGNValue = parseInt(myHexStr);

                      if(myParameterIndex == 0) //field 0 Oil Pressure
					  {
						myHexStr = "0x" + myN2Kdata[3].substr(4, 2) + myN2Kdata[3].substr(2, 2);

						myPGNValue = parseN2KPressure(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);

					  }
                           
					else if(myParameterIndex == 1) // get OIL temperature
					{
						myHexStr = "0x" + myN2Kdata[3].substr(8, 2) + myN2Kdata[3].substr(6, 2);

						myPGNValue = parseN2KTemperature(parseInt(myHexStr),myUnitsFlags, 10);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
						
                     }
					 else if(myParameterIndex == 2) // get temperature
					{
                        myHexStr = "0x" + myN2Kdata[3].substr(12, 2) + myN2Kdata[3].substr(10, 2);
                         
						myPGNValue = parseN2KTemperature(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					}
                       
					else if(myParameterIndex == 3) // get Voltage
					{
                        myHexStr = "0x" + myN2Kdata[3].substr(16, 2) + myN2Kdata[3].substr(14, 2);
                         
						myPGNValue = parseN2KVoltsAmps(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					}
                            
					else if(myParameterIndex == 4) // get Fuel Rate
					{
                        myHexStr = "0x" + myN2Kdata[3].substr(20, 2) + myN2Kdata[3].substr(18, 2);
                         
						myPGNValue = parseN2KFlowRate(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
                    }
					
                   	else if(myParameterIndex == 5) // get hour meter
					{
                             // field 5 Engine Hours					
                             myHexStrLB =  myN2Kdata[3];
                             myHexStrLB = myHexStrLB.substr((43-12-7), 2) + myHexStrLB.substr((41-12-7), 2);

                             myHexStr = myN2Kdata[3];
                             myHexStr = myHexStr.substr((47-12-7), 2) + myHexStr.substr((45-12-7), 2);

                             myHexStr = "0x" + myHexStr + myHexStrLB;

                             myPGNValue = parseInt(myHexStr);

                             if (myPGNValue == parseInt("0x7FFFFFFF")) 
							 {

                             }
                             else 
							 {
                                 var vGHour = Math.floor(myPGNValue / 3600);
                                 var vGMin = myPGNValue - vGHour * 3600;
                                  vGMin = Math.floor(vGMin / 60);

							
									myPGNData.push([vGHour + "." + vGMin, myTimeStamp]);
								}
                                 
                     }
					 else if(myParameterIndex == 6)  // get coolant pressure
					{
						myHexStr = "0x" + myN2Kdata[3].substr(32, 2) + myN2Kdata[3].substr(30, 2);

						myPGNValue = parseN2KPressure(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					}

					else if(myParameterIndex == 7)  // get fuel pressure
					{
						myHexStr = "0x" + myN2Kdata[3].substr(36, 2) + myN2Kdata[3].substr(34, 2);

						myPGNValue = parseN2KPressure(parseInt(myHexStr),myUnitsFlags, 10);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					}

                          
          
				 } // Instance match
		} // good checksum
	} // 127489 Array Loop

	return myPGNData;
		

} // end of function GetPGN 127489

// Transmission Parameters Dynamic
// PGN 127493 [0x01F205] Environmential Parameters
// myParameterIndex = 0  -> Gear Position
// myParameterIndex = 1  -> Oil Pressure
// myParameterIndex = 2  -> Oil Temp

//
function GetPGN127493(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F205,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
      //for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1]
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
             myHexStr = "0x" + myHexStr.substr(0 ,2) ;

		     myInstance = parseInt(myHexStr);
			 if(myInstance == myPGNInstance) // field 1 Oil Pressure
			{   
			 
				if(myParameterIndex == 1)// field 1 Oil Pressure
				{
					myHexStr = "0x" + myN2Kdata[3].substr(6, 2) + myN2Kdata[3].substr(4, 2);

					myPGNValue = parseN2KPressure(parseInt(myHexStr),myUnitsFlags, 1);
					if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);

				}       
				else if(myParameterIndex == 2) // get temperature
				{
					myHexStr = "0x" + myN2Kdata[3].substr(10, 2) + myN2Kdata[3].substr(8, 2);

					myPGNValue = parseN2KTemperature(parseInt(myHexStr),myUnitsFlags, 10);
					if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
                }

							 
           
                          
          
        } // Instance match
	  } // good checksum
	} // 127493 Array Loop

	return myPGNData;
		
} // end of function GetPGN 127493

// Fluid Parameters
// PGN 127505 [0x01F211] Fluid Parameters
// myPGNINstance = Instance and type
// Type = myPGNINstance & 0x0F
// Instance = myPGNINstance & 0xF0
// myParameterIndex = 0  -> Level %
// myParameterIndex = 1  -> Capacity
// 
//
function GetPGN127505(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

//	mySubStrings = myN2Kdata.split("$PCDIN,01F211,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			

				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr =  myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
             myHexStr = "0x" + myHexStr.substr(0 ,2);

		     myInstance = parseInt(myHexStr);
				
			if(myInstance == myPGNInstance) // 
			{                      
                if(myParameterIndex == 0)// field 0 Fluid Level
				{
					myHexStr = "0x" + myN2Kdata[3].substr(4, 2) + myN2Kdata[3].substr(2, 2);

					myPGNValue = parseN2KLevel(parseInt(myHexStr),myUnitsFlags, 1);
					if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					
				}
                else if(myParameterIndex == 1)  // get Capacity
				{       
                    myHexStr = "0x" + myN2Kdata[3].substr(12, 2) +  myN2Kdata[3].substr(10, 2)  + myN2Kdata[3].substr(8, 2) +  myN2Kdata[3].substr(6, 2);;
					
					myPGNValue = parseN2KCapicaty(parseInt(myHexStr),myUnitsFlags, 0.1);
					if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
				}

					
                          
          
        } // Instance match
	  } // good checksum
	} // 127505 Array Loop

	return myPGNData;

} // end of function GetPGN 127505

// Ststus Parameters
// PGN 127506 [0x01F212] DC Detailed
// myPGNINstance = Instance and type
// Type = myPGNINstance & 0x0F
// Instance = myPGNINstance & 0xF0
// myParameterIndex = 0  -> Voltage
// myParameterIndex = 1  -> Current
// myParameterIndex = 1  -> Temp
// 
//
function GetPGN127506(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F212,");

    //myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(18 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(19 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,18));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				
             myHexStr = "0x" + myHexStr.substr(14-12 ,2) ;

		     myInstance = parseInt(myHexStr);
				
				if(myInstance == myPGNInstance) // 
				{                      
					if(myParameterIndex == 0)
					{
                      // field 0 State of Charge
						myHexStr = myN2Kdata[3];
                      myHexStr =  myHexStr.substr(18-12, 2);
					  if(myHexStr != "FF")
					  {
						  myPGNValue = parseInt(myHexStr, 16);

					
								myHexStr =((myPGNValue * 1.0) ) ;
								myPGNData.push([myHexStr, myTimeStamp]) ;
						  }
					}
					else if(myParameterIndex == 1)
					{
					  // field 1 State of Health
						myHexStr = myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr(20-12, 2) ;
					  if(myHexStr != "FF")
					  {
						  myPGNValue = parseInt(myHexStr, 16);

						
								myHexStr =((myPGNValue * 1.0) ) ;
								myPGNData.push([myHexStr, myTimeStamp]) ;
						  }
					  }
					  
					else if(myParameterIndex == 2)  // get Time Remain
					{
									
                      // field 2 Time Remain
 
						myHexStr = myN2Kdata[3];
                       myHexStr = myHexStr.substr(24, 2) + myHexStr.substr(22-12, 2);
					  if(myHexStr != "FFFF")
					  {
						   myPGNValue = parseInt(myHexStr, 16);

						
						
								myHexStr =((myPGNValue * 1.0) ) ;
								
								myPGNData.push([myHexStr, myTimeStamp]) ;
							}
					  }
					  
					else if(myParameterIndex == 3)  // get Ripple Voltage
					{					  
						// field 3 Ripple Voltage
						if(myHexStr != "FFFF")
					  {    
						   myHexStr = myN2Kdata[3];
						   myHexStr = myHexStr.substr(28-12, 2) + myHexStr.substr(26-12, 2);

						   myPGNValue = parseInt(myHexStr, 16);


							
						
								myHexStr =((myPGNValue * 0.0001) ) ;
								
								myPGNData.push([myHexStr, myTimeStamp]) ;
							}
						}
                          
          
        } // Instance match
	  } // good checksum
	} // 127506 Array Loop

	return myPGNData;

} // end of function GetPGN 127506

// Ststus Parameters
// PGN 127508 [0x01F214] Battery Status
// myPGNINstance = Instance and type
// Type = myPGNINstance & 0x0F
// Instance = myPGNINstance & 0xF0
// myParameterIndex = 0  -> Voltage
// myParameterIndex = 1  -> Current
// myParameterIndex = 1  -> Temp
// 
//
function GetPGN127508(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F214,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
      //for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				
             myHexStr = "0x" + myHexStr.substr(0 ,2) ;
		     myInstance = parseInt(myHexStr);
				
			if(myInstance == myPGNInstance) // 
			{                      
				if(myParameterIndex == 0)
				{
					myHexStr = "0x" + myN2Kdata[3].substr(4, 2) + myN2Kdata[3].substr(2, 2);
                         
					myPGNValue = parseN2KVoltsAmps(parseInt(myHexStr),myUnitsFlags, 1);
					if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					
				} 
				else if(myParameterIndex == 1)  // get Current
				{	
					myHexStr = "0x" + myN2Kdata[3].substr(8, 2) + myN2Kdata[3].substr(6, 2);
                         
					myPGNValue = parseN2KVoltsAmps(parseInt(myHexStr),myUnitsFlags, 1);
					if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
				}	
				else if(myParameterIndex == 2) // get temperature
				{
					myHexStr = "0x" + myN2Kdata[3].substr(12, 2) + myN2Kdata[3].substr(10, 2);
                         
					myPGNValue = parseN2KTemperature(parseInt(myHexStr),myUnitsFlags, 1);
					if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
				}        
			} // Instance match
	  } // good checksum
	} // 127508 Array Loop

	return myPGNData;

} // end of function GetPGN 127508

	
// Ststus Parameters
// PGN 127497 [0x01F209] Trip Parameters Engine
// myPGNINstance = Instance and type
// Type = myPGNINstance & 0x0F
// Instance = myPGNINstance & 0xF0
// myParameterIndex = 0  -> Fuel Used
// myParameterIndex = 1  -> Fuel Rate Average
// myParameterIndex = 2  -> Fuel Rate, Economy
// myParameterIndex = 3  -> Instantaneous Fuel Rate, Economy
// 
//
function GetPGN127497(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

			//	<option value="20">Liters</option>
			//	<option value="21">Gallons</option>
			//	<option value="22">CubicMeter</option>


      // Get all the elements and parse into variables
      //for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(18 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(19 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,18));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
			//$PCDIN,01F209,E2K27Q0B,AA,00 1C24 1A02 1A02 36 00*47				
             myHexStr = "0x" + myHexStr.substr(0 ,2) ;

		     myInstance = parseInt(myHexStr);

				if(myInstance == myPGNInstance) // 
				{                      
					if(myParameterIndex == 0)  // field 0 Trip fuel used
					{
						myHexStr = "0x" + myN2Kdata[3].substr(4, 2) + myN2Kdata[3].substr(2, 2);
					  
						myPGNValue = parseN2KFluidCapacity(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					} 
					else if(myParameterIndex == 1)  // get Fuel Rate, Average
					{	

						myHexStr = "0x" + myN2Kdata[3].substr(8, 2) + myN2Kdata[3].substr(6, 2);
                         
						myPGNValue = parseN2KFlowRate(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
								
					}
					else if(myParameterIndex == 2) // get Fuel Rate, Economy
					{
						myHexStr = "0x" + myN2Kdata[3].substr(12, 2) + myN2Kdata[3].substr(10, 2);
                         
						myPGNValue = parseN2KFlowRate(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					}
					
					else if(myParameterIndex == 3) // get Instantaneous Fuel Economy
					{
						myHexStr = "0x" + myN2Kdata[3].substr(16, 2) + myN2Kdata[3].substr(14, 2);
                         
						myPGNValue = parseN2KFlowRate(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					}
                          
          
        } // Instance match
	  } // good checksum
	} // 127497 Array Loop

	return myPGNData;

} // end of function GetPGN 127508


// Weather station data
// PGN 130311 [0x01FD07] Environmential Parameters
// myParameterIndex = 0  -> Air Temp
// myParameterIndex = 1  -> Humidity
// myParameterIndex = 2  -> Barometric Pressure
// myUnitsFlags = 0  -> Degrees F
// myUnitsFlags = 1  -> Degrees C
//
function GetPGN130311(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01FD07,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr =myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			

				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				
				myHexStr = "0x" + myHexStr.substr(3 ,1) ;

				myWindRef = parseInt(myHexStr);
				// Get Temperature Reference
				// 0 = Sea emp
				// 1 = Outside Temp
				// 2 = Inside Temp
				// 3 = Engine Room Temp
				// 4 = Main Cabin Temp

			
				if(myWindRef == myPGNInstance) // Outside Temp and Baro
				{          
					if(myParameterIndex == 2)
					{
						myHexStr = "0x" + myN2Kdata[3].substr(14, 2) + myN2Kdata[3].substr(12, 2);
								 
						myPGNValue = parseN2KPressure(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					 }
					 
					else if(myParameterIndex == 1) // get Humidity %
					{
						myHexStr = "0x" + myN2Kdata[3].substr(10, 2) + myN2Kdata[3].substr(8, 2);
								 
						myPGNValue = parseN2KTemperature(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					}

					else if(myParameterIndex == 0) // get temperature
					{
						myHexStr = "0x" + myN2Kdata[3].substr(6, 2) + myN2Kdata[3].substr(4, 2);
								 
						myPGNValue = parseN2KTemperature(parseInt(myHexStr),myUnitsFlags, 1);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					}  
						
          
			} // Outside temp and baro
		} // good checksum
	} // 130311 Array Loop

	return myPGNData;
		//return "this is a test";

} // end of function GetPGN 130311


// Temperature data
// PGN 130312 [0x01FD08] Temperature Parameters
// myParameterIndex = 0  -> Temperature
// myParameterIndex = 1  -> Set Temperature

// myUnitsFlags = 0  -> Degrees F
// myUnitsFlags = 1  -> Degrees C
//
function GetPGN130312(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myTempRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

//	mySubStrings = myN2Kdata.split("$PCDIN,01FD08,");

 //   myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = myN2Kdata[3];;

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				
			 myHexStr = "0x" + myHexStr.substr(2 ,2) ;

		     myInstance = parseInt(myHexStr);
				
				if(myInstance == myPGNInstance) // 
				{                      
				  myHexStr = myN2Kdata[3];;
				  myHexStr = "0x" + myHexStr.substr(4 ,2) ;
				  myTempRef = parseInt(myHexStr);

				myTempRef = parseInt(myHexStr);
				// Get Temperature Reference
				// 0 = Sea emp
				// 1 = Outside Temp
				// 2 = Inside Temp
				// 3 = Engine Room Temp
				// 4 = Main Cabin Temp
          
				if(myParameterIndex == myTempRef) // get temperature
				{
					myHexStr = "0x" + myN2Kdata[3].substr(8, 2) + myN2Kdata[3].substr(6, 2);
								 
					myPGNValue = parseN2KTemperature(parseInt(myHexStr),myUnitsFlags, 1);
					if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
					
				} // Temperature
			} // good instance
		} // good checksum
	} // 130312 Array Loop

	return myPGNData;
		//return "this is a test";

} // end of function GetPGN 130312


// Temperature Extended
// PGN 130316 [0x01FD0C] Environmential Parameters
// myParameterIndex = 0  -> Temperature
// myParameterIndex = 1  -> Set Temperature

// myUnitsFlags = 0  -> Degrees F
// myUnitsFlags = 1  -> Degrees C
//
function GetPGN130316(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myTempRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

//	mySubStrings = myN2Kdata.split("$PCDIN,01FD08,");

 //   myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = myN2Kdata[3];;

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				
			 myHexStr = "0x" + myHexStr.substr((21-12-7) ,2) ;

		     myInstance = parseInt(myHexStr);
				
				if(myInstance == myPGNInstance) // 
				{                      
				  myHexStr = myN2Kdata[3];;
				  myHexStr = "0x" + myHexStr.substr((23-12-7) ,2) ;
				  myTempRef = parseInt(myHexStr);

					myTempRef = parseInt(myHexStr);
					// Get Temperature Reference
					// 0 = Sea emp
					// 1 = Outside Temp
					// 2 = Inside Temp
					// 3 = Engine Room Temp
					// 4 = Main Cabin Temp
          
					if(myParameterIndex == myTempRef) // get temperature
					{
						myHexStr = "0x"  + myN2Kdata[3].substr(10, 2) + myN2Kdata[3].substr(8, 2) + myN2Kdata[3].substr(6, 2);
									 
						myPGNValue = parseN2KTemperature(parseInt(myHexStr),myUnitsFlags, 100);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
						
					} // Temperature
			} // good instance
		} // good checksum
	} // 130316 Array Loop

	return myPGNData;
		//return "this is a test";

} // end of function GetPGN 130316

// Actual Pressure
// PGN 130314 [0x01FD0A] Environmential Parameters
// myParameterIndex = 0  -> Actual Pressure
//
function GetPGN130314(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myTempRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01FD0A,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = myN2Kdata[3];;

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				
			 myHexStr = "0x" + myHexStr.substr((21-12-7) ,2) ;

		     myInstance = parseInt(myHexStr);
				
				if(myInstance == myPGNInstance) // 
				{                      
				  myHexStr = myN2Kdata[3];;
				  myHexStr = "0x" + myHexStr.substr((23-12-7) ,2) ;
				  myTempRef = parseInt(myHexStr);

					myTempRef = parseInt(myHexStr);
					// Get pressure Reference
					// 0 = atmosphere
					// 1 = water
					// 2 = steam
					// 3 = compressed air
					// 4 = hydraulic
          
					 if(myParameterIndex == myTempRef) // get pressure
					 {
						myHexStr = "0x"  + myN2Kdata[3].substr(12, 2) + myN2Kdata[3].substr(10, 2) + myN2Kdata[3].substr(8, 2) + myN2Kdata[3].substr(6, 2);
									 
						myPGNValue = parseN2KPressure(parseInt(myHexStr),myUnitsFlags, 100);
						if ( myPGNValue != null) myPGNData.push([myPGNValue, myTimeStamp]);
						
					} // pressure
			} // good instance
		} // good checksum
	} // 130314 Array Loop

	return myPGNData;
		//return "this is a test";

} // end of function GetPGN 130314

// Weather station data
// PGN 130323 [0x01FD13] Environmential Parameters
// myParameterIndex = 0  -> Air Temp
// myParameterIndex = 1  -> Humidity
// myParameterIndex = 2  -> Barometric Pressure
// myUnitsFlags = 0  -> Degrees F
// myUnitsFlags = 1  -> Degrees C
//
function GetPGN130323(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01FD13,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = myN2Kdata[3];;

	  	 // look for checksum character in the correct place or skip 
		//	if(myHexStr.substr(72 ,1) == '*')
			{
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
					
				{        
				
				
					myHexStr = myN2Kdata[3];;
					// get Lat
					myHexStr = "0x" + myHexStr.substr((32-12),2) + myHexStr.substr((30-12),2) + myHexStr.substr((28-12),2) + myHexStr.substr((26-12),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue > 2147483648)
						myPGNValue = -(4294967295 - myPGNValue); 

					  if(myParameterIndex == 2)
					  {
							myHexStr =myPGNValue*.0000001 ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
					  }
				  

				  	myHexStr = myN2Kdata[3];; 
					// get long
					myHexStr = "0x" + myHexStr.substr((40-12),2) + myHexStr.substr((38-12),2) + myHexStr.substr((36-12),2) + myHexStr.substr((34-12),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue > 2147483648)
						myPGNValue = -(4294967295 - myPGNValue); 

					  if(myParameterIndex == 3)
					  {
							myHexStr =myPGNValue*.0000001 ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
					  }


			         myHexStr = "0x" + myHexStr.substr((50-12) ,2) ;
				  myWindRef = parseInt(myHexStr);

					myWindRef = parseInt(myHexStr);
					// Get Heading Reference value
					// 0x00 = Theoretical Wind (ground referenced, referenced to True North; calculated using COG/SOG)
					// 0x01 = Theoretical Wind (ground referenced, referenced to Magnetic North; calculated using COG/SOG)
					// 0x02 = Apparent Wind (relative to the vessel centerline)
					// 0x03 = Theoretical (Calculated to Centerline of the vessel, refernced to ground; calculated using COG/SOG)
					// 0x04 = Theoretical (Calculated to Centerline of the vessel, refernced to water; calculated using Heading/Speed through Water)
					// 0x05 = Reserved
					// 0x06 = Error
					// 0x07 = Null

			 //alert(myPGNInstance);
				if(((myWindRef & 0x0007) == myPGNInstance) || ( myPGNInstance == 8))// Use Reference
				{          
                    
					myHexStr = myN2Kdata[3];;         
                    // Get WInd Direction
					myHexStr = "0x" + myHexStr.substr((48-12),2) + myHexStr.substr((46-12),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 65535)
					{
						
					} // invalid value
					else
					{
					   myDegreesMagN = Math.floor(myPGNValue * 57.2957795 * .0001); // converted to degrees
						if(myDegreesMagN >= 360)
							myDegreesMagN = myDegreesMagN - 360;

					  if(myParameterIndex == 5) // Wind Direction
					  {
					 // alert(myPGNInstance);
						if(myPGNInstance == 8)
						{
							if((myWindRef & 0x0007) == 0) // Wind ref to True North
								myPGNData.push([myDegreesMagN + ":T", myTimeStamp]) ;
							else if((myWindRef & 0x0007) == 1) // Wind ref to Mag North
								myPGNData.push([myDegreesMagN + ":M", myTimeStamp]) ;
							else if((myWindRef & 0x0007) == 2) // Wind ref to Apparent
								myPGNData.push([myDegreesMagN + ":A", myTimeStamp]) ;

								

						}
						else
						{
							//alert(myDegreesMagN);
							myPGNData.push([myDegreesMagN, myTimeStamp]);
						}
					  }
		    
					} // valid value

					 // get Wind Speed
					myHexStr = myN2Kdata[3];;
					myHexStr = "0x" + myHexStr.substr((44-12),2) + myHexStr.substr((42-12),2) ;
					myPGNValue = parseInt(myHexStr);

					if(myPGNValue == 65535)
					{
						
					}
					else
					{
						
					    if(myParameterIndex == 4) // Wind Speed
					   {
						  if(myUnitsFlags  == 4) // Knots
							myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots
						  else if(myUnitsFlags  == 5) // MPH
							myPGNValue  = myPGNValue * 2.23694 * .01; // converted to MPH
						else if(myUnitsFlags  == 6) // KPH
							myPGNValue  = myPGNValue * 3.6 * .01; // converted to KPH
						  else if(myUnitsFlags  == 7) // KPH
							myPGNValue  = myPGNValue * 1.0 * .01; // converted to KPH
						  else //  default knots
							myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots

						if(myPGNInstance == 8)
						{
							if((myWindRef & 0x0007) == 0) // Speed ref to True North
								myPGNData.push([myPGNValue + ":T", myTimeStamp]) ;
							else if((myWindRef & 0x0007) == 1) // Speed ref to Mag North
								myPGNData.push([myPGNValue + ":M", myTimeStamp]) ;
							else if((myWindRef & 0x0007) == 2) // Speed ref to Apparent
								myPGNData.push([myPGNValue + ":A", myTimeStamp]) ;
						}
						else
							myPGNData.push([myPGNValue, myTimeStamp]);
						     
					   }
				}

          
			} // Wind Reference
                    
					myHexStr = myN2Kdata[3];;      
                    
					// get baro
					myHexStr = "0x" + myHexStr.substr((58-12),2) + myHexStr.substr((56-12),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 32767)
					{
						
					}
					else
					{
					 

					  if(myParameterIndex == 7)
					  {
						if(myUnitsFlags  == 8) // PSI
						{
							myHexStr =((myPGNValue * 0.0145037738007) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags  == 9) // kPa
						{
							myHexStr =((myPGNValue * 0.1) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags  == 10) // inHg
						{
							myHexStr =((myPGNValue * 0.0295229) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else // default is PSI
						{
							myHexStr =((myPGNValue * 0.0145037738007) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}

					  }
		    
					 }

		
          
					// get temperature
					myHexStr = myN2Kdata[3];;
					myHexStr = "0x" + myHexStr.substr((62-12),2) + myHexStr.substr((60-12),2) ;
					myPGNValue = parseInt(myHexStr);

					// Air temp Scale for degrees F PGN130311
					//AirTempScale = 0.018;
					//AirTempOffset = 459;

					// Air temp Scale for degrees C PGN130311
					//AirTempScale = 0.01;
					//AirTempOffset = 273;

					 if(myParameterIndex == 8) // get temperature
					 {
						if(myUnitsFlags  == 1) // degrees C
							myPGNData.push([Math.floor(((myPGNValue * 0.01) - 273)), myTimeStamp]);
						else if(myUnitsFlags  == 2) // degrees Kelvin
							myPGNData.push([Math.floor(((myPGNValue * 0.01) )), myTimeStamp]);
						else // default is degrees F
							myPGNData.push([Math.floor(((myPGNValue * 0.018) - 459)), myTimeStamp]);
					}
          
			} // Outside temp and baro
		} // good checksum
	} // 130323 Array Loop

	return myPGNData;
		//return "this is a test";

} // end of function GetPGN 130323


// Heading
// PGN 127250 [0x01F112] Environmential Parameters
// myParameterIndex = 0  -> Heading Magnetic North
// myParameterIndex = 1  -> Heading True North
// myUnitsFlags = 0  -> Degrees F
// myUnitsFlags = 1  -> Degrees C
//
function GetPGN127250(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 
	var myDegreesTrueN;
	var myDegreesMagN;

//	mySubStrings = myN2Kdata.split("$PCDIN,01F112,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
    //  for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr =  myN2Kdata[3];;

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr =  myN2Kdata[1];;
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				
             myHexStr = "0x" + myHexStr.substr((33-12-7) ,2) ;
				  myWindRef = parseInt(myHexStr);

					myWindRef = parseInt(myHexStr);
					// Get Heading Reference value
					// 0 = True Reference to North
					// 1 = ?? requires GPS fix
					// 2 = Apparent
					// 3 = ??? requires GPS fix 
					// 4 = reference to water speed
					//alert(myWindRef)
			
				if((myWindRef & 0x03) == myPGNInstance) // True/Magnetic Fix
				{          
                  	if(myParameterIndex == 0)
					{  
					  
					myHexStr =  myN2Kdata[3];;         
                    
					myHexStr = "0x" + myHexStr.substr((23-12-7),2) + myHexStr.substr((21-12-7),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 32767)
					{
						
					}
					else
					{
					   myDegreesMagN = Math.floor(myPGNValue * 57.2957795 * .0001); // converted to degrees
						if(myDegreesMagN >= 360)
							myDegreesMagN = myDegreesMagN - 360;

		
						//if(myUnitsFlags  == 13) // Heading Magnetic
						myPGNData.push([myDegreesMagN, myTimeStamp]) ;
					  }
		    
					 }
					 
					else if(myParameterIndex == 1) // deviation
					{
					myHexStr =  myN2Kdata[3];;
					myHexStr = "0x" + myHexStr.substr((27-12-7),2) + myHexStr.substr((25-12-7),2) ;
					myPGNValue = parseInt(myHexStr);

					if(myPGNValue == 65535)
					{
						
					}
					else
					{
						if(myPGNValue > 32767 )
						myPGNValue  = -(65536 - myPGNValue);

						myPGNValue  = (myPGNValue * 57.2957795 * .0001); // converted to degrees

				
					
						  
						     myPGNData.push([myPGNValue, myTimeStamp]) ;
					   }

				}

					else if(myParameterIndex == 2)
					{
						 
					myHexStr =  myN2Kdata[3];;
					myHexStr = "0x" + myHexStr.substr((31-12-7),2) + myHexStr.substr((29-12-7),2) ;
					myPGNValue = parseInt(myHexStr);

					if(myPGNValue == 65535)
					{
						
					}
					else
					{
						if(myPGNValue > 32767 )
						myPGNValue  = -(65536 - myPGNValue);

						myPGNValue  = (myPGNValue * 57.2957795 * .0001); // converted to degrees

						myDegreesTrueN  = myDegreesMagN + myPGNValue;  
					 //  if(myParameterIndex == 0)
					  // {
					//	  if(myUnitsFlags  == 13) // Heading Magnetic
					//	     myPGNData.push(myDegreesTrueN) ;
					 //  }
					 
						     myPGNData.push([myPGNValue, myTimeStamp]) ;
					   }

				}
          
			} // Magnetic Fix
		} //good checksum
	} // 127250 Array Loop

	return myPGNData;

} // end of function GetPGN 127250


// Wind Data
// PGN 130306 [0x01FD02] Environmential Parameters
// myParameterIndex = 0  -> Wind Speed
// myParameterIndex = 1  -> Wind Direction
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetPGN130306(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 
	var myDirectionTrue;
	var myDirectionApparent;
	var mySpeedTrue;
	var mySpeedApparent;

	var myDegreesMagN;
	var myDegreesTrueN;

	//mySubStrings = myN2Kdata.split("$PCDIN,01FD02,");

   // myArrayLength = mySubStrings.length;

	//alert(mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = myN2Kdata[3];;
			// alert(myHexStr);
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			

				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
             myHexStr = "0x" + myHexStr.substr((29-12-7) ,2) ;
				  myWindRef = parseInt(myHexStr);

					myWindRef = parseInt(myHexStr);
					// Get Heading Reference value
					// 0x00 = Theoretical Wind (ground referenced, referenced to True North; calculated using COG/SOG)
					// 0x01 = Theoretical Wind (ground referenced, referenced to Magnetic North; calculated using COG/SOG)
					// 0x02 = Apparent Wind (relative to the vessel centerline)
					// 0x03 = Theoretical (Calculated to Centerline of the vessel, refernced to ground; calculated using COG/SOG)
					// 0x04 = Theoretical (Calculated to Centerline of the vessel, refernced to water; calculated using Heading/Speed through Water)
					// 0x05 = Reserved
					// 0x06 = Error
					// 0x07 = Null

			 //alert(myPGNInstance);
				if(((myWindRef & 0x0007) == myPGNInstance) || ( myPGNInstance == 8))// Use Reference
				{          
                    
					myHexStr = myN2Kdata[3];;        
                    // Get WInd Direction
					myHexStr = "0x" + myHexStr.substr((27-12-7),2) + myHexStr.substr((25-12-7),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 65535)
					{
						
					} // invalid value
					else
					{
					   myDegreesMagN = Math.floor(myPGNValue * 57.2957795 * .0001); // converted to degrees
						if(myDegreesMagN >= 360)
							myDegreesMagN = myDegreesMagN - 360;

					  if(myParameterIndex == 1) // Wind Direction
					  {
					 // alert(myPGNInstance);
						if(myPGNInstance == 8)
						{
							if((myWindRef & 0x0007) == 0) // Wind ref to True North
								myPGNData.push([myDegreesMagN + ":T", myTimeStamp]) ;
							else if((myWindRef & 0x0007) == 1) // Wind ref to Mag North
								myPGNData.push([myDegreesMagN + ":M", myTimeStamp]) ;
							else if((myWindRef & 0x0007) == 2) // Wind ref to Apparent
								myPGNData.push([myDegreesMagN + ":A", myTimeStamp]) ;

								

						}
						else
						{
							//alert(myDegreesMagN);
							myPGNData.push([myDegreesMagN, myTimeStamp]);
						}
					  }
		    
					} // valid value

					 // get Wind Speed
					myHexStr = myN2Kdata[3];;
					myHexStr = "0x" + myHexStr.substr((23-12-7),2) + myHexStr.substr((21-12-7),2) ;
					myPGNValue = parseInt(myHexStr);

					if(myPGNValue == 65535)
					{
						
					}
					else
					{
						
					    if(myParameterIndex == 0) // Wind Speed
					   {
						  if(myUnitsFlags  == 4) // Knots
							myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots
						  else if(myUnitsFlags  == 5) // MPH
							myPGNValue  = myPGNValue * 2.23694 * .01; // converted to MPH
						  else if(myUnitsFlags  == 6) // KPH
							myPGNValue  = myPGNValue * 3.6 * .01; // converted to KPH
						 else if(myUnitsFlags  == 7) // KPH
							myPGNValue  = myPGNValue * 1.0 * .01; // converted to KPH
						  else //  default knots
							myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots

						if(myPGNInstance == 8)
						{
							if((myWindRef & 0x0007) == 0) // Speed ref to True North
								myPGNData.push([myPGNValue + ":T", myTimeStamp]) ;
							else if((myWindRef & 0x0007) == 1) // Speed ref to Mag North
								myPGNData.push([myPGNValue + ":M", myTimeStamp]) ;
							else if((myWindRef & 0x0007) == 2) // Speed ref to Apparent
								myPGNData.push([myPGNValue + ":A", myTimeStamp]) ;
						}
						else
							myPGNData.push([myPGNValue, myTimeStamp]);
						     
					   }
				}

          
			} // Wind Reference
		} // good checksum
	} // 130306 Array Loop

	return myPGNData;

} // end of function GetPGN 130306
     

// Vessel Attitude
// PGN 127257 [0x01F119] Vesel Attitude
// myParameterIndex = 0  -> YAW
// myParameterIndex = 1  -> Pitch
// myParameterIndex = 2  -> Roll
//
function GetPGN127257(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 
	var myPitch;
	var myRoll;

	//mySubStrings = myN2Kdata.split("$PCDIN,01F119,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

			myHexStr = myN2Kdata[3];;      
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;   
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				if(myParameterIndex == 0) // Yaw
				{				      
                    // Get Yaw
					myHexStr = "0x" + myHexStr.substr((23-12-7),2) + myHexStr.substr((21-12-7),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 65535)
					{
						
					}
					else
					{

					if(myPGNValue > 32767 )
					myPGNValue  = -(65536 - myPGNValue);
					myPGNValue  = (myPGNValue * 57.2957795 * .0001); // converted to degrees


						myPGNData.push([myPGNValue, myTimeStamp]) ;
					  }
		    
				}
				
				
				else if(myParameterIndex == 1) // Pitch
				{
					 myHexStr = myN2Kdata[3];;             
                    // Get Pitch
					myHexStr = "0x" + myHexStr.substr((27-12-7),2) + myHexStr.substr((25-12-7),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 65535)
					{
						
					}
					else
					{

					if(myPGNValue > 32767 )
					myPGNValue  = -(65536 - myPGNValue);
					myPitch  = (myPGNValue * 57.2957795 * .0001); // converted to degrees

				
						myPGNData.push([myPitch, myTimeStamp]) ;
					  }
		    
					 }
					 
					 
					else if(myParameterIndex == 2) // Roll
					{
					myHexStr = myN2Kdata[3];;        
                    // Get Roll
					myHexStr = "0x" + myHexStr.substr((31-12-7),2) + myHexStr.substr((29-12-7),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 65535)
					{
						
					}
					else
					{

					if(myPGNValue > 32767 )
					myPGNValue  = -(65536 - myPGNValue);
					myRoll  = (myPGNValue * 57.2957795 * .0001); // converted to degrees

				
						myPGNData.push([myRoll, myTimeStamp]) ;
					  }
		    
					 }

				else if(myParameterIndex == 3) // Roll
				{
					//myPGNData.push(myRoll) ;
					myPGNData.push([myPitch + ":" + myRoll, myTimeStamp]) ;
				}
		} // good checksum
	} // 127257 Array Loop

	return myPGNData;

} // end of function GetPGN 127257

// Rate of Turn
// PGN 127251 [0x01F113] Rate of Turn
// myParameterIndex = 0  -> ROT
//
function GetPGN127251(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 
	var myPitch;
	var myRoll;

	//mySubStrings = myN2Kdata.split("$PCDIN,01F113,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

			myHexStr = myN2Kdata[3];;  
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
				
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;  
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
                    // Get Rate of Turn
 myHexStrLB = myN2Kdata[3];;  
                     myHexStrLB = myHexStrLB.substr((23-12-7), 2) + myHexStrLB.substr((21-12-7), 2);

                     myHexStr = myN2Kdata[3];;  
                     myHexStr = myHexStr.substr((27-12-7), 2) + myHexStr.substr((25-12-7), 2);

                     myHexStr = "0x" + myHexStr + myHexStrLB;

                     myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 0x7FFFFFFF)
					{
						
					}
					else
					{

					if(myPGNValue > 0x7FFFFFFF )
						myPGNValue  = -(0xFFFFFFFF - myPGNValue);

					myPGNValue  = (myPGNValue * .00010743446497); // converted to degrees/min
					//myPGNValue  = (myPGNValue * 3.1248083 * .00000001); // converted to radians/sec

					  if(myParameterIndex == 0) // rate of turn
					  {
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					  }
		    
					}

					
		} // good checksum
	} // 127251 Array Loop

	return myPGNData;

} // end of function GetPGN 127251

// Ruddder Angle
// PGN 127245 [0x01F10D] Rudder Angle
// myParameterIndex = 0  -> Angle
//
function GetPGN127245(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();

	//mySubStrings = myN2Kdata.split("$PCDIN,01F10D,");

    //myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

			myHexStr = myN2Kdata[3];;  
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;  
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				//PCDIN,01F10D,E0Q1FF0K,AA,00F8FF7F7414FFFF
				myHexStr = "0x" + myN2Kdata[3].substr((0) ,2) ;
				myInstance = parseInt(myHexStr);
				
				if(myInstance == myPGNInstance) // 
				{   
					      
                    // Get Rudder Angle
					myHexStr = "0x" + myN2Kdata[3].substr((10),2) + myN2Kdata[3].substr((8),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 65535)
					{
						
					}
					else
					{

					if(myPGNValue > 32767 )
					myPGNValue  = -(65536 - myPGNValue);
					myPGNValue  = (myPGNValue * 57.2957795 * .0001); // converted to degrees

					  if(myParameterIndex == 0) // Rudder angle
					  {
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					  }
		    
					 }

					
			} // Instance match
					
		} // good checksum
	} // 127245 Array Loop

	return myPGNData;

} // end of function GetPGN 127245

// Water Depth
// PGN 128267 [0x01F50B] Water Depth
// myParameterIndex = 0  -> Depth meters
//
function GetPGN128267(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();

	//mySubStrings = myN2Kdata.split("$PCDIN,01F50B,");

    //myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
      //for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

			myHexStr = myN2Kdata[3];;  
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;  
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				//myHexStr = "0x" + myHexStr.substr((19-7) ,2) ;
				//myInstance = parseInt(myHexStr);
				
				//if(myInstance == myPGNInstance) // 
				{   
					      
                    // Get depth
					myHexStr = "0x" + myHexStr.substr((27-12-7),2) + myHexStr.substr((25-12-7),2)+ myHexStr.substr((23-12-7),2) + myHexStr.substr((21-12-7),2) ;
					myPGNValue = parseInt(myHexStr);
          
					

					if(myUnitsFlags  == 32) // feet
							myPGNValue  = myPGNValue * 3.28084 * .01; // converted to feet
					else if(myUnitsFlags  == 36) // fathoms
							myPGNValue  = myPGNValue * 0.546806649 * .01; // converted to fathoms
					else //  default knots
							myPGNValue  = myPGNValue * 1.0 * .01; // converted to meters
				
					myPGNData.push([myPGNValue, myTimeStamp]) ;
					  		    

					
			} // Instance match
					
		} // good checksum
	} // 128267 Array Loop

	return myPGNData;

} // end of function GetPGN 128267


// Water Speed
// PGN 128259 [0x01F503] Environmential Parameters
// myParameterIndex = 0  -> Speed Water Reference
// myParameterIndex = 1  -> Speed Ground Reference
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetPGN128259(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myCOGRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 
	var myDegreesTrueN;
	var myDegreesMagN;

	//mySubStrings = myN2Kdata.split("$PCDIN,01F503,");

    //myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr =myN2Kdata[3];;  

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			

				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;  
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				myHexStr = "0x" + myHexStr.substr((29-12-7) ,2) ;

					myCOGRef = parseInt(myHexStr);
					// Get Heading Reference value
					// 0x00 = Paddel Wheel
					// 0x01 = Pitot tube
					// 0x02 = Doppler
					// 0x03 = Correlation
					// 0x04 = EM Log

			
				if((myCOGRef & 0x00FF) != 255 && (myCOGRef & 0x00FF) == myPGNInstance) // Use Reference
				{          
 					if(myParameterIndex == 0) // Speed Over water
					{                   
					myHexStr = myN2Kdata[3];;          
                    // Get speed water reference
					myHexStr = "0x" + myHexStr.substr((23-12-7),2) + myHexStr.substr((21-12-7),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 65535)
					{
						
					}
					else
					{
						

						  if(myUnitsFlags  == 4) // Knots
							myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots
					 else if(myUnitsFlags  == 5) // MPH
							myPGNValue  = myPGNValue * 2.23694 * .01; // converted to MPH
						else if(myUnitsFlags  == 6) // KPH
							myPGNValue  = myPGNValue * 3.6 * .01; // converted to KPH
					 else if(myUnitsFlags  == 7) // KPH
							myPGNValue  = myPGNValue * 1.0 * .01; // converted to KPH
					 else //  default knots
							myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots

					 myPGNData.push([myPGNValue, myTimeStamp]) ;
					   }
					}
					
					
					else if(myParameterIndex == 1) // Speed Over Ground
					{
					 // get Speed ground reference
					myHexStr = myN2Kdata[3];;  
					myHexStr = "0x" + myHexStr.substr((27-12-7),2) + myHexStr.substr((25-12-7),2) ;
					myPGNValue = parseInt(myHexStr);

					if(myPGNValue == 65535)
					{
						
					}
					else
					{
						
					
						  if(myUnitsFlags  == 4) // Knots
							myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots
					 else if(myUnitsFlags  == 5) // MPH
							myPGNValue  = myPGNValue * 2.23694 * .01; // converted to MPH
					 else if(myUnitsFlags  == 6) // KPH
							myPGNValue  = myPGNValue * 1.0 * .01; // converted to KPH
					 else //  default knots
							myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots

					 myPGNData.push([myPGNValue, myTimeStamp]) ;
					   }
					}

          
        } // COG Reference
	  } // good checksum
	} // 128259 Array Loop

	return myPGNData;

} // end of function GetPGN 128259


// COG and SOG
// PGN 129026 [0x01F802] Environmential Parameters
// myParameterIndex = 0  -> Course over Ground
// myParameterIndex = 1  -> Speed over Ground
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetPGN129026(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myCOGRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 
	var myDegreesTrueN;
	var myDegreesMagN;

	//mySubStrings = myN2Kdata.split("$PCDIN,01F802,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
				
			

              myHexStr =myN2Kdata[3];;  

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;  
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
             myHexStr = "0x" + myHexStr.substr((21-12-7) ,2) ;
				  myCOGRef = parseInt(myHexStr);

					myCOGRef = parseInt(myHexStr);
					// Get Heading Reference value
					// 0x00 = True
					// 0x01 = Magnetic
					// 0x02 = Error
					// 0x03 = Null

			
				if((myCOGRef & 0x0003) == myPGNInstance) // Use Reference
				{          
                    if(myParameterIndex == 0) // Wind Direction
					{
					myHexStr = myN2Kdata[3];;           
                    // Get Course Over Ground
					myHexStr = "0x" + myHexStr.substr((25-12-7),2) + myHexStr.substr((23-12-7),2) ;
					myPGNValue = parseInt(myHexStr);
          
					if(myPGNValue == 65535)
					{
						
					}
					else
					{
					   myDegreesMagN = Math.floor(myPGNValue * 57.2957795 * .0001); // converted to degrees
						if(myDegreesMagN >= 360)
							myDegreesMagN = myDegreesTrueN - 360;

					
						
						myPGNData.push([myDegreesMagN, myTimeStamp]) ;
					  }
		    
					 }
					 
					 
					else if(myParameterIndex == 1) // Speed Over Ground
					{
					 // get  Speed
					myHexStr = myN2Kdata[3];;  
					myHexStr = "0x" + myHexStr.substr((29-12-7),2) + myHexStr.substr((27-12-7),2) ;
					myPGNValue = parseInt(myHexStr);

					if(myPGNValue == 65535)
					{
						
					}
					else
					{
						
				
						  if(myUnitsFlags  == 4) // Knots
							myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots
						  else if(myUnitsFlags  == 5) // MPH
							myPGNValue  = myPGNValue * 2.23694 * .01; // converted to MPH
						  else if(myUnitsFlags  == 6) // KPH
							myPGNValue  = myPGNValue * 3.6 * .01; // converted to KPH
						else if(myUnitsFlags  == 7) // KPH
							myPGNValue  = myPGNValue * 1.0 * .01; // converted to KPH
						  else //  default knots
							myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots

						     myPGNData.push([myPGNValue, myTimeStamp]) ;
					   }
				}

          
        } // COG Reference
	  } // good checksum
	} // 129026 Array Loop

	return myPGNData;

} // end of function GetPGN 129026


// Position Rapid
// PGN 129025 [0x01F801] Position Rapid
// myParameterIndex = 0  -> Don't Care
// myUnitsFlags = 0  -> Degrees
// myUnitsFlags = 4  -> radians
//
function GetPGN129025(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myCOGRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 
	var myDegreesTrueN;
	var myDegreesMagN;

	//mySubStrings = myN2Kdata.split("$PCDIN,01F802,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
				
			

              myHexStr =myN2Kdata[3];;  

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;  
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				

         
                    if(myParameterIndex == 0) // Lattitude
					{
					myHexStr = myN2Kdata[3];;           
                    // Get Lattitude
					myHexStr =  myHexStr.substr((25-12-7),2) + myHexStr.substr((23-12-7),2) + myHexStr.substr((21-12-7),2) + myHexStr.substr((19-12-7),2) ;
					myPGNValue = parseInt(myHexStr,16);
          
					if(myHexStr == "0x7FFFFFFF")
					{
						
					}
					else
					{
					  if(myHexStr.charCodeAt(0) > 0x37)
						{
							myDegreesMagN = -((4294967295 - myPGNValue)  * Math.pow(10,-7)); // converted to degrees
						}
						else
						{
							myDegreesMagN = (myPGNValue * Math.pow(10,-7)); // converted to degrees
						}
				

						myPGNData.push([myDegreesMagN, myTimeStamp]) ;
					  }
		    
					 }
					 
					 
					else if(myParameterIndex == 1) // longitude
					{
					 // get  Speed
					myHexStr = myN2Kdata[3];;  
					myHexStr =  myHexStr.substr((33-12-7),2) + myHexStr.substr((31-12-7),2) + myHexStr.substr((29-12-7),2) + myHexStr.substr((27-12-7),2) ;
					myPGNValue = parseInt(myHexStr,16);

					if(myHexStr == "0x7FFFFFFF")
					{
						
					}
					else
					{
						
						if(myHexStr.charCodeAt(0) > 0x37)
						{
							myDegreesMagN = -((4294967295 - myPGNValue)  * Math.pow(10,-7)); // converted to degrees
						}
						else
						{
							myDegreesMagN = (myPGNValue  * Math.pow(10,-7)); // converted to degrees
						}
					
	

						myPGNData.push([myDegreesMagN, myTimeStamp]) ;
						
					   }
				}

          

	  } // good checksum
	} // 129025 Array Loop

	return myPGNData;

} // end of function GetPGN 129025


// GNSS Position
// PGN 129029 [0x01F805] GNSS POsition
// myParameterIndex = 0  -> LAT
// myParameterIndex = 1  -> LNG
// myParameterIndex = 2  -> Altitude
// myUnitsFlags = 30  -> Meters
// myUnitsFlags = 31  -> Feet

//
function GetPGN129029(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myCOGRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 
	var myDegreesTrueN;
	var myDegreesMagN;

	//mySubStrings = myN2Kdata.split("$PCDIN,01F802,");

   // myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
				
			

              myHexStr =myN2Kdata[3];;  

			 // look for checksum character in the correct place or skip 
			 var myIndex = myHexStr.indexOf('*');
			 
			if(myIndex > 0)
			{
				var checksum = parseInt("0x" + myHexStr.substr((myIndex +1) ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,myIndex));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;  
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
             myHexStr = "0x" + myHexStr.substr((63) ,1) ;
				  myCOGRef = parseInt(myHexStr);

					myCOGRef = parseInt(myHexStr);
					// Get Heading Reference value
					// 0x00 = True
					// 0x01 = Magnetic
					// 0x02 = Error
					// 0x03 = Null

			
				if((myCOGRef & 0x0003) == myPGNInstance) // Use Reference
				{          
                    if(myParameterIndex == 0) // Lattitude
					{
					myHexStr = myN2Kdata[3];;           
                    // lattidude
					myHexLBStr = myHexStr.substr(20,2) + myHexStr.substr(18,2) + myHexStr.substr(16,2) + myHexStr.substr(14,2) ;
					myPGNValue = parseInt(myHexLBStr, 16);
					
					myHexStr =  myHexStr.substr(28,2) + myHexStr.substr(26,2) + myHexStr.substr(24,2) + myHexStr.substr(22,2) ;
					
					myPGNValue = parseInt(myHexStr, 16);
          
					if(myHexStr == "0x7FFF")
					{
						
					}
					else
					{
						if(myHexStr.charCodeAt(0) > 0x37)
						{
							myDegreesMagN = -(((4294967295 - myPGNValue) * 4294967296 + parseInt(myHexLBStr, 16))  * Math.pow(10,-16)); // converted to degrees
						}
						else
						{
							myDegreesMagN = ((myPGNValue  * 4294967296 + parseInt(myHexLBStr, 16))* Math.pow(10,-16)); // converted to degrees
						}
							
						myPGNData.push([myDegreesMagN, myTimeStamp]) ;
					  }
		    
					 }
					 
					if(myParameterIndex == 1) // Longitude
					{
					myHexStr = myN2Kdata[3];;           
                    // Longitude
					myHexLBStr = myHexStr.substr(36,2) + myHexStr.substr(34,2) + myHexStr.substr(32,2) + myHexStr.substr(30,2) ;
					myPGNValue = parseInt(myHexLBStr, 16);
					
					myHexStr = myHexStr.substr(44,2) + myHexStr.substr(42,2) + myHexStr.substr(40,2) + myHexStr.substr(38,2) ;
					myPGNValue = parseInt(myHexStr, 16);
          
					if(myHexStr == "0x7FFF")
					{
						
					}
					else
					{
						if(myHexStr.charCodeAt(0) > 0x37)
						{
							myDegreesMagN = -(((4294967295 - myPGNValue) * 4294967296 + parseInt(myHexLBStr, 16))  * Math.pow(10,-16)); // converted to degrees
						}
						else
						{
							myDegreesMagN = ((myPGNValue  * 4294967296 + parseInt(myHexLBStr, 16)) * Math.pow(10,-16)); // converted to degrees
						}
			
					
						
						myPGNData.push([myDegreesMagN, myTimeStamp]) ;
					  }
		    
					 }
					 
					 
					else if(myParameterIndex == 2) // Altitude
					{
					myHexStr = myN2Kdata[3];;           
					myHexLBStr = myHexStr.substr(52,2) + myHexStr.substr(50,2) + myHexStr.substr(48,2) + myHexStr.substr(46,2);
					myHexStr =  myHexStr.substr(60,2) + myHexStr.substr(58,2) + myHexStr.substr(56,2) + myHexStr.substr(54,2) ;
					myPGNValue = parseInt(myHexStr, 16);
          
					if(myHexStr == "0x7FFF")
					{
						
					}

					else
					{
						
						if(myHexStr.charCodeAt(0) > 0x37)
						{
						  if(myUnitsFlags  == 31) // feet
							myPGNValue  = -((4294967295 - myPGNValue) * 4294967296 + parseInt(myHexLBStr, 16)) * 3.28084 * Math.pow(10,-6); // converted to Knots

						  else //  default meters
							myPGNValue  = -((4294967295 - myPGNValue) * 4294967296 + parseInt(myHexLBStr, 16))  * Math.pow(10,-6); // converted to meters
						}
						else
						{
						  if(myUnitsFlags  == 31) // feet
							myPGNValue  = ((myPGNValue) * 4294967296 + parseInt(myHexLBStr, 16)) * 3.28084 * Math.pow(10,-6); // converted to Knots

						  else //  default meters
							myPGNValue  = (( myPGNValue) * 4294967296 + parseInt(myHexLBStr, 16))  * Math.pow(10,-6); // converted to meters
						}

						     myPGNData.push([myPGNValue, myTimeStamp]) ;
					 }
				}

          
        } // COG Reference
	  } // good checksum
	} // 129029 Array Loop

	return myPGNData;

} // end of function GetPGN 129029



// Switch Status
// PGN 127501 [0x01F20D] Switch Status
// myParameterIndex = 0  -> Switch0
// myParameterIndex = 1  -> Switch1
//
//
// myParameterIndex = 28  -> Switch28
//
function GetPGN127501(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags, DialIndex, myflashSwitch )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();

	//mySubStrings = myN2Kdata.split("$PCDIN,01F20D,");

   // myArrayLength = mySubStrings.length;

	

      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

			myHexStr = myN2Kdata[3];;   
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
							
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];;  
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				
				myHexStr = "0x" + myHexStr.substr((19-12-7) ,2) ;
				myInstance = parseInt(myHexStr);
				//alert(myInstance);
				if(myInstance == myPGNInstance) // 
				{   
					  switch(parseInt(myParameterIndex))
					  {
						  case 0:  // get switch 0
							myHexStr = myN2Kdata[3];;   
							myHexStr = "0x" + myHexStr.substr((21-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x03 ) == 0x01)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x03 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
						
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}
			
						  break

						case 1:  // get switch 1
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((21-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x0C ) == 0x04)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x0C ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}
						  break

					 case 2:  // get switch 2
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((21-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x30 ) == 0x10)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x30 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}

						  break

					 case 3:  // get switch 3
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((21-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0xC0 ) == 0x40)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0xC0 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}

						
						  break

					 case 4:  // get switch 4
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((23-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x03 ) == 0x01)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x03 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}

						  break

						case 5:  // get switch 5
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((23-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x0C ) == 0x04)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x0C ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}

						  break

					 case 6:  // get switch 6
							myHexStr = myN2Kdata[3];;   
							myHexStr = "0x" + myHexStr.substr((23-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x30 ) == 0x10)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x30 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}

						  break

					 case 7:  // get switch 7
							myHexStr = myN2Kdata[3];;   
							myHexStr = "0x" + myHexStr.substr((23-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0xC0 ) == 0x40)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0xC0 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}
	
						  break

					 case 8:  // get switch 8
							myHexStr = myN2Kdata[3];;   
							myHexStr = "0x" + myHexStr.substr((25-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x03 ) == 0x01)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x03 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}

						  break

						case 9:  // get switch 9
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((25-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x0C ) == 0x04)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x0C ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}

						  break

					 case 10:  // get switch 10
							myHexStr = myN2Kdata[3];;   
							myHexStr = "0x" + myHexStr.substr((25-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x30 ) == 0x10)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x30 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}

						  break

					 case 11:  // get switch 11
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((25-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0xC0 ) == 0x40)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0xC0 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}

						  break

					 case 12:  // get switch 12
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((27-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x03 ) == 0x01)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x03 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
						if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}

						  break

						case 13:  // get switch 13
							myHexStr = myN2Kdata[3];;   
							myHexStr = "0x" + myHexStr.substr((27-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x0C ) == 0x04)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x0C ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}
						  break

					 case 14:  // get switch 14
							myHexStr = myN2Kdata[3];;   
							myHexStr = "0x" + myHexStr.substr((27-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x30 ) == 0x10)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x30 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}	

						  break

					 case 15:  // get switch 15
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((27-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0xC0 ) == 0x40)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0xC0 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
							if(myflashSwitch == true) {						
								radialDial[DialIndex].setflashing(false);
								flashSwitchState[DialIndex]=0;
							}
						  break

					 case 16:  // get switch 16
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((29-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x03 ) == 0x01)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x03 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								

			
						  break

						case 17:  // get switch 17
							myHexStr = myN2Kdata[3];;   
							myHexStr = "0x" + myHexStr.substr((29-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x0C ) == 0x04)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x0C ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								

						  break

					 case 18:  // get switch 18
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((29-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x30 ) == 0x10)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x30 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
						  break

					 case 19:  // get switch 19
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((29-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0xC0 ) == 0x40)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0xC0 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
						  break

					 case 20:  // get switch 20
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((31-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x03 ) == 0x01)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x03 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
			
						  break

						case 21:  // get switch 21
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((31-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x0C ) == 0x04)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x0C ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
						  break

					 case 22:  // get switch 22
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((31-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x30 ) == 0x10)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x30 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
						  break

					 case 23:  // get switch 23
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((31-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0xC0 ) == 0x40)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0xC0 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
						  break

					 case 24:  // get switch 24
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((33-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x03 ) == 0x01)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x03 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
			
						  break

						case 25:  // get switch 25
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((33-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x0C ) == 0x04)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x0C ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
						  break

					 case 26:  // get switch 26
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((33-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0x30 ) == 0x10)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0x30 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
						  break

					 case 27:  // get switch 27
							myHexStr = myN2Kdata[3];;  
							myHexStr = "0x" + myHexStr.substr((33-12-7),2);
							myPGNValue = parseInt(myHexStr);

							if((myPGNValue & 0xC0 ) == 0x40)
								myPGNData.push([255, myTimeStamp]) ;
							else if((myPGNValue & 0xC0 ) == 0x00)
								myPGNData.push([0, myTimeStamp]) ;
							else
								myPGNData.push([256, myTimeStamp]) ;
								
								
						  break
		    
					 } // end switch

					
				} // Instance match
					
		} // good checksum
	} // 127501 Array Loop

	return myPGNData;

} // end of function GetPGN 127501



// J1939 PGN 61444 (0x0F004) Electronic Engine Controller 1
// myParameterIndex = 0  ->  Engine torque mode 
// myParameterIndex = 1  -> Driver Demand Torque  (-125% to 125%) 1%/bit   
// myParameterIndex = 2  -> Actual Torque  (-125% to 125%) 1%/bit 
// myParameterIndex = 3  -> RPM LB (0-8031) 0.125 rpm/bit 
// myParameterIndex = 4  -> Source address

//
function GetPGN61444(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				

				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      
                   

                      // Engine Coolant Temperature
 myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((0), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // Engine torque mode
					{
                      // field Engine Coolant Temperature
 myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								  
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
								}
                     }
					 
					 if(myParameterIndex == 1) // Driver Demand Torque
					{
                      // field   Engine Fuel Temperature Temperature
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((2), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
	
										myPGNData.push([Math.floor(((myPGNValue * 1.0) - 125)), myTimeStamp]);
								}
                     }
                           
					else if(myParameterIndex == 2) // Actual Torque
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((4), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {

									myPGNData.push([Math.floor(((myPGNValue * 1.0) - 125)), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // RPM 
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((8), 2) + myHexStr.substr((6), 2);
                             myPGNValue = parseInt(myHexStr);

		
									myPGNData.push([Math.floor(((myPGNValue * 0.125) )), myTimeStamp]);
					}
                       
					else if(myParameterIndex == 4) // Source address
					{
                             // field 3 Alternator Volts
                             myHexStr =  myN2Kdata[3];
                             myHexStr = "0x" +  myHexStr.substr((10), 2);

                             myPGNValue = parseInt(myHexStr);

				
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
					}
                            
					else if(myParameterIndex == 5) // get Engine Intercooler Thermostat Opening
					{
                             // field 4 Fuel Rate
                             myHexStr =  myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((14), 2) ;

                             myPGNValue = parseInt(myHexStr);

							
								myPGNData.push([((myPGNValue * 1.0) - 125), myTimeStamp]);
                    }
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 61444 Array Loop

	return myPGNData;
		

} // end of function GetPGN 61444




// J1939 Engine Temperature
// PGN 65262 [0x0FEEE] Engine Temperature
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 2  -> Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset 
// myParameterIndex = 3  -> Engine Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 4  -> Engine Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   

//
function GetPGN65262(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;

				

				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

                      // Engine Coolant Temperature
 myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // Engine Coolant Temperature
					{
                      // field Engine Coolant Temperature
 myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							{
									if(myUnitsFlags == 1) // degrees C
										myPGNData.push([Math.floor(((myPGNValue * 1.0) - 40)), myTimeStamp]);
									else if(myUnitsFlags  == 2) // degrees Kelvin
										myPGNData.push([Math.floor(((myPGNValue * 1.0) + 233)), myTimeStamp]);
									else // default is degrees F
										myPGNData.push([Math.floor(((myPGNValue * 1.8) - 40)), myTimeStamp]);	
							}
                     }
					 
					 if(myParameterIndex == 1) // Fuel Temperature
					{
                      // field   Engine Fuel Temperature Temperature
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((21-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
									if(myUnitsFlags == 1) // degrees C
										myPGNData.push([Math.floor(((myPGNValue * 1.0) - 40)), myTimeStamp]);
									else if(myUnitsFlags  == 2) // degrees Kelvin
										myPGNData.push([Math.floor(((myPGNValue * 1.0) + 233)), myTimeStamp]);
									else // default is degrees F
										myPGNData.push([Math.floor(((myPGNValue * 1.8) - 40)), myTimeStamp]);	
							}
                     }
                           
					else if(myParameterIndex == 2) // get OIL temperature
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
							
							if(myUnitsFlags  == 1) // degrees C
								myPGNData.push([Math.floor(((myPGNValue * 0.03125) - 273)), myTimeStamp]);
							else if(myUnitsFlags  == 2) // degrees Kelvin
								myPGNData.push([Math.floor(((myPGNValue * 0.03125) )), myTimeStamp]);
							else // default is degrees F
								myPGNData.push([Math.floor(((myPGNValue * 0.05625) - 459)), myTimeStamp]);		
								}
                     }
					 else if(myParameterIndex == 3) // get Engine Turbocharger Oil Temperature
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
							if(myUnitsFlags  == 1) // degrees C
								myPGNData.push([Math.floor(((myPGNValue * 0.03125) - 273)), myTimeStamp]);
							else if(myUnitsFlags  == 2) // degrees Kelvin
								myPGNData.push([Math.floor(((myPGNValue * 0.03125) )), myTimeStamp]);
							else // default is degrees F
								myPGNData.push([Math.floor(((myPGNValue * 0.05625) - 459)), myTimeStamp]);		
					}
                       
					else if(myParameterIndex == 4) // get Engine Intercooler Temperature
					{
                             // field 3 Alternator Volts
                             myHexStr =  myN2Kdata[3];
                             myHexStr = "0x" +  myHexStr.substr((31-12-7), 2);

                             myPGNValue = parseInt(myHexStr);

							if(myUnitsFlags  == 1) // degrees C
								myPGNData.push([Math.floor(((myPGNValue * 0.03125) - 273)), myTimeStamp]);
							else if(myUnitsFlags  == 2) // degrees Kelvin
								myPGNData.push([Math.floor(((myPGNValue * 0.03125) )), myTimeStamp]);
							else // default is degrees F
								myPGNData.push([Math.floor(((myPGNValue * 0.05625) - 459)), myTimeStamp]);		
					}
                            
					else if(myParameterIndex == 5) // get Engine Intercooler Thermostat Opening
					{
                             // field 4 Fuel Rate
                             myHexStr =  myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((33-12-7), 2) ;

                             myPGNValue = parseInt(myHexStr);

							
								myPGNData.push([((myPGNValue * .04)), myTimeStamp]);
                    }
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65262 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65262 Engine



// J1939 PGN 65271 (0x0FEF7) Vehicle Electrical Power
// myParameterIndex = 0  -> Net Battery Current (-125 to 125 Amps) 1 Amp/bit
// myParameterIndex = 1  -> Alternator Current (-125 to 125 Amps) 1 Amp/bit  
// myParameterIndex = 2  -> Charging Voltage LSB (0-3212 V) 0.05 V/bit
// myParameterIndex = 3  -> Battery Voltage LSB (0-3212 V) 0.05 V/bit
// myParameterIndex = 4  -> Keyswitch Voltage LSB (0-3212 V) 0.05 V/bit
//
function GetPGN65271(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

                      
                      myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // Net Battery Current (-125 to 125 Amps) 1 Amp/bit
					{
                      
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
					
										myPGNData.push([Math.floor(((myPGNValue * 1.0) - 125)), myTimeStamp]);
								}
                     }
					 
					 if(myParameterIndex == 1) // Alternator Current (-125 to 125 Amps) 1 Amp/bit
					{
                      
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((21-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
							
				
										myPGNData.push([Math.floor(((myPGNValue * 1.0) - 125)), myTimeStamp]);
								}
                     }
                           
					else if(myParameterIndex == 2) // Charging Voltage LSB (0-3212 V) 0.05 V/bit
					{
                     
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
							
		
										myPGNData.push([Math.floor(((myPGNValue * 0.05) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Battery Voltage LSB (0-3212 V) 0.05 V/bit
					{
							 
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
					
									myPGNData.push([Math.floor(((myPGNValue * 0.05) )), myTimeStamp]);
					}
                       
					else if(myParameterIndex == 4) //  Keyswitch Voltage LSB (0-3212 V) 0.05 V/bit 
					{
                             
                             myHexStr =  myN2Kdata[3];
                              myHexStr = "0x" + myHexStr.substr((33-12-7), 2) + myHexStr.substr((31-12-7), 2);

                             myPGNValue = parseInt(myHexStr);

				
										myPGNData.push([Math.floor(((myPGNValue * 0.05) )), myTimeStamp]);
					}
                            
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65271 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65271 Battery



// J1939 PGN 65276  (0x0FEFC) Dash Display
// myParameterIndex = 0  -> Net Battery Current (-125 to 125 Amps) 1 Amp/bit
// myParameterIndex = 1  -> Alternator Current (-125 to 125 Amps) 1 Amp/bit  
// myParameterIndex = 2  -> Charging Voltage LSB (0-3212 V) 0.05 V/bit
// myParameterIndex = 3  -> Battery Voltage LSB (0-3212 V) 0.05 V/bit
// myParameterIndex = 4  -> Keyswitch Voltage LSB (0-3212 V) 0.05 V/bit
//
function GetPGN65276(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				

				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      
                  

                      
                      myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // Washer Fluid Level (0-100%) 0.4%/bit
					{
                      // field Engine Coolant Temperature
 myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((0), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
					
										myPGNData.push([Math.floor(((myPGNValue *0.4) )), myTimeStamp]);
								}
                     }
					 
					 if(myParameterIndex == 1) // Fuel Level  (0-100%) 0.4%/bit
					{
                      
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((2), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
							
				
									myPGNData.push([Math.floor(((myPGNValue * 0.4) )), myTimeStamp]);
								}
                     }
                           
					else if(myParameterIndex == 2) // Fuel Filter Differential Pressure (0-500 kPa) 2 kPA/bit
					{
                      
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" +   myHexStr.substr((4), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
							
		
										myPGNData.push([Math.floor(((myPGNValue * 0.5) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Oil Filter Differential Pressure (0-125 kPa) 0.5 kPA/bit
					{
							 
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((6), 2);
                             myPGNValue = parseInt(myHexStr);

                         
					
									myPGNData.push([Math.floor(((myPGNValue * 0.5) )), myTimeStamp]);
					}
                       
					else if(myParameterIndex == 4) //  Cargo Ambient Temp LSB 
					{
                             
                             myHexStr =  myN2Kdata[3];
                              myHexStr = "0x" + myHexStr.substr((10), 2) + myHexStr.substr((8), 2);

                             myPGNValue = parseInt(myHexStr);

										
							if(myUnitsFlags  == 1) // degrees C
								myPGNData.push([Math.floor(((myPGNValue * 0.03125) - 273)), myTimeStamp]);
							else if(myUnitsFlags  == 2) // degrees Kelvin
								myPGNData.push([Math.floor(((myPGNValue * 0.03125) )), myTimeStamp]);
							else // default is degrees F
								myPGNData.push([Math.floor(((myPGNValue * 0.05625) - 459)), myTimeStamp]);					
										
					}
                            
					else if(myParameterIndex == 5) //  Fuel Level tank 2 (0-100%) 0.4%/bit 
					{
                             
                             myHexStr =  myN2Kdata[3];
                              myHexStr = "0x" + myHexStr.substr((12), 2) ;

                             myPGNValue = parseInt(myHexStr);

				
										myPGNData.push([Math.floor(((myPGNValue * 0.4) )), myTimeStamp]);
					}					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65276 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65276 Battery


// J1939 PGN 65263 (0x0FEEF) Engine Pressures
// myParameterIndex = 0  -> Fuel Pressure 4 kPa/bit
// myParameterIndex = 1  -> Crankcase blowby .05 kPa/bit    
// myParameterIndex = 2  -> Engine Oil Level  0.4% kPa/bit
// myParameterIndex = 3  -> Engine Oil Pressure 4 kPa/bit
// myParameterIndex = 4  -> Crankcase Pressure LSB 0.0078 kPa/bit -250 kPa offset
// myParameterIndex = 3  -> Coolant Pressure 2 kPa/bit  
// myParameterIndex = 4  -> Coolant Leval .4%  kPa/bit      
//
function GetPGN65263(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

                      // Engine Coolant Temperature
 myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // Fuel Pressure 4 kPa/bit
					{
                     
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);


						if(myUnitsFlags  == 8) // PSI
						{
							myHexStr =((myPGNValue * 0.145037738007 * 4) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags == 9) // kPa
						{
							myHexStr =((myPGNValue * 4) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags  == 10) // inHg
						{
							myHexStr =((myPGNValue * 0.295229* 4) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else // default isPSI
						{
							myHexStr =((myPGNValue * 0.145037738007 * 4) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
                     }
					 
					 if(myParameterIndex == 1) // crankcase blowby
					{
                      
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((21-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
							
								if(myUnitsFlags  == 8) // PSI
								{
									myHexStr =((myPGNValue * 0.145037738007 * 0.05) ) ;
									myPGNData.push([myHexStr, myTimeStamp]) ;
								}
								else if(myUnitsFlags == 9) // kPa
								{
									myHexStr =((myPGNValue * 0.05) ) ;
									myPGNData.push([myHexStr, myTimeStamp]) ;
								}
								else if(myUnitsFlags  == 10) // inHg
								{
									myHexStr =((myPGNValue * 0.295229* 0.05) ) ;
									myPGNData.push([myHexStr, myTimeStamp]) ;
								}
								else // default isPSI
								{
									myHexStr =((myPGNValue * 0.145037738007 * 0.05) ) ;
									myPGNData.push([myHexStr, myTimeStamp]) ;
								}
							}
                     }
                           
					else if(myParameterIndex == 2) // Engine Oil Level  0.4%/bit
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" +  myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

               
								
							
			
							myHexStr =((myPGNValue * 0.4) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						
								
                     }
					 else if(myParameterIndex == 3) // Engine Oil Pressure 4 kPa/bit
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((25-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
						if(myUnitsFlags  == 8) // PSI
						{
							myHexStr =((myPGNValue * 0.145037738007 * 4) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags == 9) // kPa
						{
							myHexStr =((myPGNValue  * 4) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags  == 10) // inHg
						{
							myHexStr =((myPGNValue * 0.295229* 4) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else // default isPSI
						{
							myHexStr =((myPGNValue * 0.145037738007 * 4) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
					}
                       
					else if(myParameterIndex == 4) // Crankcase Pressure LSB 0.0078 kPa/bit -250 kPa offset
					{
                             // field 3 Alternator Volts
                             myHexStr =  myN2Kdata[3];
                                 myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);

                             myPGNValue = parseInt(myHexStr);

						if(myUnitsFlags  == 8) // PSI
						{
							myHexStr = (((myPGNValue * 0.0078) -250) * 0.145037738007 ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags == 9) // kPa
						{
							myHexStr =((myPGNValue * 0.1 * 0.0078) - 250 ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags  == 10) // inHg
						{
							myHexStr = (((myPGNValue * 0.0078) -250) * 0.295229 ) ;
						
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else // default isPSI
						{
							myHexStr = (((myPGNValue * 0.0078) -250) * 0.145037738007 ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
					}
                            
					else if(myParameterIndex == 5) //Coolant Pressure 2 kPa/bit
					{
                             // field 4 Fuel Rate
                             myHexStr =  myN2Kdata[3];
                            myHexStr = "0x" +  myHexStr.substr((31-12-7), 2);

                             myPGNValue = parseInt(myHexStr);

							
						if(myUnitsFlags  == 8) // PSI
						{
							myHexStr =((myPGNValue * 0.145037738007 * 2) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags == 9) // kPa
						{
							myHexStr =((myPGNValue * 2) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags  == 10) // inHg
						{
							myHexStr =((myPGNValue * 0.295229* 2) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else // default isPSI
						{
							myHexStr =((myPGNValue * 0.145037738007 * 2) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
                    }
					
                   
					else if(myParameterIndex == 6) // Coolant Leval .4% /bit
					{
                             // field 4 Fuel Rate
                             myHexStr =  myN2Kdata[3];
                            myHexStr = "0x" + myHexStr.substr((33-12-7), 2) ;

                             myPGNValue = parseInt(myHexStr);

							
								myPGNData.push([((myPGNValue * 0.4)), myTimeStamp]);
                    }
                          
          
				 } // Instance match
		} // good checksum
	} // 65263 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65263 Pressures


// J1939 PGN 65272  (0x0FEF8) Transmission
// myParameterIndex = 0  -> clutch pressure
// myParameterIndex = 1  -> oil level  
// myParameterIndex = 2  -> diff pressure
// myParameterIndex = 3  -> tran pressure
// myParameterIndex = 4  -> tran temperature 0.03125 C -273C offset 2 bytes
// myParameterIndex = 5  -> tran oil level
//
function GetPGN65272(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				

				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // 
				{                      


					if(myParameterIndex == 0) // clutch pressure
					{
                      
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((0), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 256) 
							 {
                         
                             }
                             else 
							 {
					
										myPGNData.push([Math.floor(((myPGNValue *0.4) )), myTimeStamp]);
								}
                     }
					 
					 if(myParameterIndex == 1) // Tran oil level
					{
                      
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((2), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 256) 
							 {
                         
                             }
                             else 
							 {
								
							
				
									myPGNData.push([Math.floor(((myPGNValue * 0.4) )), myTimeStamp]);
								}
                     }
                           
					else if(myParameterIndex == 2) //  Differential Pressure (0-500 kPa) 2 kPA/bit
					{
                      
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" +  myHexStr.substr((4), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 256) 
							 {
                         
                             }
                             else 
							 {
								
							
		
										myPGNData.push([Math.floor(((myPGNValue * 0.5) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Tran Pressure (0-4096 kPa) 16 kPA/bit
					{
							 
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((6), 2);
                             myPGNValue = parseInt(myHexStr);

                         
					
						if(myUnitsFlags  == 8) // PSI
						{
							myHexStr =((myPGNValue * 0.145037738007 * 16) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags == 9) // kPa
						{
							myHexStr =((myPGNValue * 16) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else if(myUnitsFlags  == 10) // inHg
						{
							myHexStr =((myPGNValue * 0.295229* 16) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
						else // default isPSI
						{
							myHexStr =((myPGNValue * 0.145037738007 * 16) ) ;
							myPGNData.push([myHexStr, myTimeStamp]) ;
						}
					}
                       
					else if(myParameterIndex == 4) //  tran Temp LSB 
					{
                            
                            myHexStr =  myN2Kdata[3];
                            myHexStr = "0x" + myHexStr.substr((10), 2) + myHexStr.substr((8), 2);

                            myPGNValue = parseInt(myHexStr);
				
							//myPGNData.push([Math.floor(((myPGNValue * 0.03125) )), myTimeStamp]);
										
							if(myUnitsFlags  == 1) // degrees C
								myPGNData.push([Math.floor(((myPGNValue * 0.03125) - 273)), myTimeStamp]);
							else if(myUnitsFlags  == 2) // degrees Kelvin
								myPGNData.push([Math.floor(((myPGNValue * 0.03125) )), myTimeStamp]);
							else // default is degrees F
								myPGNData.push([Math.floor(((myPGNValue * 0.05625) - 459)), myTimeStamp]);			
										
										
										
					}
                            
					else if(myParameterIndex == 5) //  Tran Oil Level (0-100%) 0.4%/bit 
					{
                             
                             myHexStr =  myN2Kdata[3];
                              myHexStr = "0x" + myHexStr.substr((12), 2) ;

                             myPGNValue = parseInt(myHexStr);

				
										myPGNData.push([Math.floor(((myPGNValue * 0.4) )), myTimeStamp]);
					}					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65272 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65272 Transmission




// J1939 AC Basic
// PGN 65014 [0x0FDF6] PGN 65014 (0x0FDF6) UTIL AC BASIC PAASE A
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 2  -> Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset 
// myParameterIndex = 3  -> Engine Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 4  -> Engine Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   

//
function GetPGN65014(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

                      
                      myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // AC Volts Line to Line
					{
                      
                       myHexStr =  myN2Kdata[3];
                        myHexStr = "0x" + myHexStr.substr((21-12-7), 2) + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
					 
					 if(myParameterIndex == 1) // AC Volts Line to Neutral
					{
                      
                       myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
                           
					else if(myParameterIndex == 2) // get Frequency
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 0.0078125) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Amps
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((33-12-7), 2) + myHexStr.substr((31-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
						myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
					}
                       
				
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65262 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65262



// J1939 AC Basic
// PGN 65011 [0x0FDF6] PGN 65014 (0x0FDF6) UTIL AC BASIC PAASE A
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 2  -> Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset 
// myParameterIndex = 3  -> Engine Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 4  -> Engine Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   

//
function GetPGN65011(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

                      
                      myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // AC Volts Line to Line
					{
                      
                       myHexStr =  myN2Kdata[3];
                        myHexStr = "0x" + myHexStr.substr((21-12-7), 2) + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
					 
					 if(myParameterIndex == 1) // AC Volts Line to Neutral
					{
                      
                       myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
                           
					else if(myParameterIndex == 2) // get Frequency
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 0.0078125) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Amps
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((33-12-7), 2) + myHexStr.substr((31-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
						myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
					}
                       
				
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65262 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65262


// J1939 AC Basic
// PGN 65008 [0x0FDF6] PGN 65014 (0x0FDF6) UTIL AC BASIC PAASE A
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 2  -> Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset 
// myParameterIndex = 3  -> Engine Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 4  -> Engine Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   

//
function GetPGN65008(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

                      
                      myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // AC Volts Line to Line
					{
                      
                       myHexStr =  myN2Kdata[3];
                        myHexStr = "0x" + myHexStr.substr((21-12-7), 2) + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
					 
					 if(myParameterIndex == 1) // AC Volts Line to Neutral
					{
                      
                       myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
                           
					else if(myParameterIndex == 2) // get Frequency
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 0.0078125) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Amps
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((33-12-7), 2) + myHexStr.substr((31-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
						myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
					}
                       
				
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65262 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65262


// J1939 AC Basic
// PGN 65017 [0x0FDF6] PGN 65014 (0x0FDF6) UTIL AC BASIC PAASE A
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 2  -> Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset 
// myParameterIndex = 3  -> Engine Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 4  -> Engine Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   

//
function GetPGN65017(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				

				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

                      myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // AC Volts Line to Line
					{
                      
                       myHexStr =  myN2Kdata[3];
                        myHexStr = "0x" + myHexStr.substr((21-12-7), 2) + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
					 
					 if(myParameterIndex == 1) // AC Volts Line to Neutral
					{
                      
                       myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
                           
					else if(myParameterIndex == 2) // get Frequency
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 0.0078125) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Amps
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((33-12-7), 2) + myHexStr.substr((31-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
						myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
					}
                       
				
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65262 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65262



// J1939 AC Basic
// PGN 65005 [0x0FDF6] PGN 65005 (0x0FDED) UTIL AC BASIC PAASE A
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 

//
function GetPGN65005(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

					if(myParameterIndex == 0) // AC Total kWatt Power Export
					{
                      
                       myHexStr =  myN2Kdata[3];
                        myHexStr = "0x" + myHexStr.substr(6, 2) + myHexStr.substr(4, 2) + myHexStr.substr(2, 2) + myHexStr.substr(0, 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue == 0xFFFFFFFF) 
							 {
                         
                             }
                             else 
							 {
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
					 
					 if(myParameterIndex == 1) // AC Total kWatt Power Import
					{
                      
                       myHexStr =  myN2Kdata[3];
                      myHexStr = "0x"  + myHexStr.substr(14, 2) + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) + myHexStr.substr(8, 2);

						myPGNValue = parseInt(myHexStr);

                               if (myPGNValue == 0xFFFFFFFF) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
                           
					
                       
				
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65005 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65005




// J1939 AC Basic
// PGN 65027 [0x0FDF6] PGN 65014 (0x0FDF6) UTIL AC BASIC PAASE A
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 2  -> Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset 
// myParameterIndex = 3  -> Engine Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 4  -> Engine Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   

//
function GetPGN65027(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

                      
                      myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // AC Volts Line to Line
					{
                      
                       myHexStr =  myN2Kdata[3];
                        myHexStr = "0x" + myHexStr.substr((21-12-7), 2) + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
					 
					 if(myParameterIndex == 1) // AC Volts Line to Neutral
					{
                      
                       myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
                           
					else if(myParameterIndex == 2) // get Frequency
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 0.0078125) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Amps
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((33-12-7), 2) + myHexStr.substr((31-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
						myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
					}
                       
				
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65027 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65262



// J1939 AC Basic
// PGN 65024 [0x0FDF6] PGN 65014 (0x0FDF6) UTIL AC BASIC PAASE A
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 2  -> Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset 
// myParameterIndex = 3  -> Engine Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 4  -> Engine Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   

//
function GetPGN65024(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      
                 
                      myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // AC Volts Line to Line
					{
                      
                       myHexStr =  myN2Kdata[3];
                        myHexStr = "0x" + myHexStr.substr((21-12-7), 2) + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
					 
					 if(myParameterIndex == 1) // AC Volts Line to Neutral
					{
                      
                       myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
                           
					else if(myParameterIndex == 2) // get Frequency
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 0.0078125) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Amps
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((33-12-7), 2) + myHexStr.substr((31-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
						myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
					}
                       
				
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65262 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65024


// J1939 AC Basic
// PGN 65021 [0x0FDF6] PGN 65014 (0x0FDF6) UTIL AC BASIC PAASE A
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 2  -> Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset 
// myParameterIndex = 3  -> Engine Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 4  -> Engine Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   

//
function GetPGN65021(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

                      
                      myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // AC Volts Line to Line
					{
                      
                       myHexStr =  myN2Kdata[3];
                        myHexStr = "0x" + myHexStr.substr((21-12-7), 2) + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
					 
					 if(myParameterIndex == 1) // AC Volts Line to Neutral
					{
                      
                       myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
                           
					else if(myParameterIndex == 2) // get Frequency
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 0.0078125) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Amps
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((33-12-7), 2) + myHexStr.substr((31-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
						myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
					}
                       
				
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65262 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65021


// J1939 AC Basic
// PGN 65030 [0x0FDF6] PGN 65014 (0x0FDF6) UTIL AC BASIC PAASE A
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 2  -> Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset 
// myParameterIndex = 3  -> Engine Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 4  -> Engine Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   

//
function GetPGN65030(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      

                      myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((19-12-7), 2) ;

                      myPGNValue = parseInt(myHexStr);

					if(myParameterIndex == 0) // AC Volts Line to Line
					{
                      
                       myHexStr =  myN2Kdata[3];
                        myHexStr = "0x" + myHexStr.substr((21-12-7), 2) + myHexStr.substr((19-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
					 
					 if(myParameterIndex == 1) // AC Volts Line to Neutral
					{
                      
                       myHexStr =  myN2Kdata[3];
                      myHexStr = "0x" + myHexStr.substr((25-12-7), 2) + myHexStr.substr((23-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
                           
					else if(myParameterIndex == 2) // get Frequency
					{
                      // field 1 Oil Temp
                       myHexStr =  myN2Kdata[3];
                       myHexStr = "0x" + myHexStr.substr((29-12-7), 2) + myHexStr.substr((27-12-7), 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue > 32000) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 0.0078125) )), myTimeStamp]);
								}
                     }
					 else if(myParameterIndex == 3) // Amps
					{
							 // field 2 Engine Temp
                             myHexStr = myN2Kdata[3];
                             myHexStr = "0x" + myHexStr.substr((33-12-7), 2) + myHexStr.substr((31-12-7), 2);
                             myPGNValue = parseInt(myHexStr);

                         
						myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
					}
                       
				
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65262 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65030



// J1939 AC Basic
// PGN 65018 [0x0FDF6] PGN 65005 (0x0FDED) UTIL AC BASIC PAASE A
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset 

//
function GetPGN65018(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

	//mySubStrings = myN2Kdata.split("$PCDIN,01F201,");

    //myArrayLength = mySubStrings.length;
	mySubStrings = myN2Kdata[3];


      // Get all the elements and parse into variables
     // for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];;
			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
				// check source match since this is can bus and there is no instance
				if(parseInt(myN2Kdata[2]) == myPGNInstance) // Outside Temp and Baro
				{                      


					if(myParameterIndex == 0) // AC Total kWatt Power Export
					{
                      
                       myHexStr =  myN2Kdata[3];
                        myHexStr = "0x" + myHexStr.substr(6, 2) + myHexStr.substr(4, 2) + myHexStr.substr(2, 2) + myHexStr.substr(0, 2);

						myPGNValue = parseInt(myHexStr);

                             if (myPGNValue == 0xFFFFFFFF) 
							 {
                         
                             }
                             else 
							 {
										myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
					 
					 if(myParameterIndex == 1) // AC Total kWatt Power Import
					{
                      
                       myHexStr =  myN2Kdata[3];
                      myHexStr = "0x"  + myHexStr.substr(14, 2) + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) + myHexStr.substr(8, 2);

						myPGNValue = parseInt(myHexStr);

                               if (myPGNValue == 0xFFFFFFFF) 
							 {
                         
                             }
                             else 
							 {
								
									myPGNData.push([Math.floor(((myPGNValue * 1.0) )), myTimeStamp]);
							}
                     }
                           
					
                       
				
					
                   

                          
          
				 } // Instance match
		} // good checksum
	} // 65018 Array Loop

	return myPGNData;
		

} // end of function GetPGN 65018




// Ststus Parameters
// PGN 65286 [0x000FF06] Custom Dimmer
// myPGNINstance = Instance and type
// Type = myPGNINstance & 0x0F
// Instance = myPGNINstance & 0xF0
// myParameterIndex = 0  -> Dimmer Level %
// myParameterIndex = 1  -> Dimmer Override Value
// myParameterIndex = 2  -> Dimmer Amps
// myParameterIndex = 3  -> Dimmer Statis
// 
//
function GetPGN65286(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 




      // Get all the elements and parse into variables
      //for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
			myHexStr = myN2Kdata[3];
			myHexStr =  myHexStr.substr(0 ,4)
			if(myHexStr == "99E1")
			{
				myHexStr = myN2Kdata[3];
				myHexStr = "0x" + myHexStr.substr(4 ,2) ;

				myInstance = parseInt(myHexStr);
				
				if(myInstance == myPGNInstance) // dimmer 0 value
				{                      
					if(myParameterIndex == 0)
					  {
	                   myHexStr = myN2Kdata[3];
                       myHexStr =  myHexStr.substr(6, 2);

                       myPGNValue = parseInt(myHexStr, 16);

								myPGNData.push([(((myPGNValue * 1.0) )), myTimeStamp]);
			
					  }
					  
					  
					else if(myParameterIndex == 1)  // dimmer 1 value
					{	
                    
                            
	                   myHexStr = myN2Kdata[3];
                       myHexStr =  myHexStr.substr(8, 2) ;

                       myPGNValue = parseInt(myHexStr, 16);

					

								myPGNData.push([(((myPGNValue * 1.0))), myTimeStamp]);
								
						}
						
					else if(myParameterIndex == 2)  // dimmer override value
					{	
                    
                            
	                   myHexStr = myN2Kdata[3];
                       myHexStr =  myHexStr.substr(10, 2) ;

                       myPGNValue = parseInt(myHexStr, 16);

					

								myPGNData.push([(((myPGNValue * 1))), myTimeStamp]);
								
						}
						
					else if(myParameterIndex == 3)  // dimmer amps value
					{	
                    
                            
						myHexStr = myN2Kdata[3];
						myHexStr =  myHexStr.substr(12, 2) ;

						myPGNValue = parseInt(myHexStr, 16);

						if(myPGNValue != 255)
								myPGNData.push([(((myPGNValue * 0.1))), myTimeStamp]);
								
						}
						
					else if(myParameterIndex == 4)  // status
					{	
                    
                            
	                   myHexStr = myN2Kdata[3];
                       myHexStr = myHexStr.substr(14, 2)  ;

                       myPGNValue = parseInt(myHexStr, 16);

					

								myPGNData.push([(((myPGNValue * 1))), myTimeStamp]);
								
						}
						

                          
          
			} // Instance match
		} // Custom PGN match
	  } // good checksum
	} // 65286 Array Loop

	return myPGNData;

} // end of function GetPGN 65286


// Ststus Parameters
// PGN 65292 [0x000FF0C] Custom Indicator Runtime
// myPGNINstance = Instance and type
// Type = myPGNINstance & 0x0F
// Instance = myPGNINstance & 0xF0
// myParameterIndex = 0  -> Dimmer Level %
// myParameterIndex = 1  -> Dimmer Override Value
// myParameterIndex = 2  -> Dimmer Amps
// myParameterIndex = 3  -> Dimmer Statis
// 
//
function GetPGN65292(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
	var myChannel;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 


	//$PCDIN,00FF0C,DTLADC02,AA,99E1000095314C63*33

      // Get all the elements and parse into variables
      //for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
			myHexStr = myN2Kdata[3];
			myHexStr =  myHexStr.substr(0 ,4)
			if(myHexStr == "99E1")
			{
				myHexStr = myN2Kdata[3];
				myHexStr = "0x" + myHexStr.substr(4 ,2) ;

				myInstance = parseInt(myHexStr);
				
				//$PCDIN,00FF0C,DTLADC02,AA,99E1000095314C63*33
				
				if(myInstance == myPGNInstance) // instance match
				{    

					myHexStr = myN2Kdata[3];
					myHexStr = "0x" + myHexStr.substr(6 ,2) ;

					myChannel = parseInt(myHexStr);
					
					
					if((myChannel == 0) && (myParameterIndex == 0)) // runtime 0
					{
							myHexStr = myN2Kdata[3];
							
							myHexStr = "0x" + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) +  myHexStr.substr((8), 2);

							myPGNValue = parseInt(myHexStr, 16);
							
							
							//var vGHour = Math.floor(myPGNValue / 3600);
                            //     var vGMin = myPGNValue - vGHour * 3600;
                             //     vGMin = Math.floor(vGMin / 60);
							//		myPGNData.push([vGHour + "." + vGMin, myTimeStamp]);
							//parseFloat(yourString).toFixed(2)
							if(myUnitsFlags  == 39) // Hours
								myPGNValue  = (parseFloat(myPGNValue) / 3600).toFixed(1); // converted to hours
							else if(myUnitsFlags  == 37) // MPH
								myPGNValue  = (parseFloat(myPGNValue) / 60).toFixed(2); // converted to minutes

							myPGNData.push([((myPGNValue )), myTimeStamp]); // time in seconds
					}
					  
					else if((myChannel == 0) && (myParameterIndex == 1))  // cycles 0
					{	
                            
						myHexStr = myN2Kdata[3];
						myHexStr =  "0x" + myHexStr.substr(14, 2);

						myPGNValue = parseInt(myHexStr, 16);

						myPGNData.push([(((myPGNValue * 1.0))), myTimeStamp]); //cycle count
								
					}
						
					else if((myChannel == 1) && (myParameterIndex == 2)) // runtime 1
					{
							myHexStr = myN2Kdata[3];
							myHexStr = "0x" + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) +  myHexStr.substr((8), 2);

							myPGNValue = parseInt(myHexStr, 16);

							if(myUnitsFlags  == 39) // Hours
								myPGNValue  = (parseFloat(myPGNValue) / 3600).toFixed(1); // converted to hours
							else if(myUnitsFlags  == 37) // MPH
								myPGNValue  = (parseFloat(myPGNValue) / 60).toFixed(2); // converted to minutes

							myPGNData.push([((myPGNValue )), myTimeStamp]); // time in seconds
					}
					  
					else if((myChannel == 1) && (myParameterIndex == 3))  // cycles 1
					{	
                            
						myHexStr = myN2Kdata[3];
						myHexStr =  "0x" + myHexStr.substr(14, 2);

						myPGNValue = parseInt(myHexStr, 16);

						myPGNData.push([(((myPGNValue * 1.0))), myTimeStamp]); //cycle count
								
					}
						
					else if((myChannel == 2) && (myParameterIndex == 4)) // runtime 2
					{
							myHexStr = myN2Kdata[3];
							myHexStr = "0x" + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) +  myHexStr.substr((8), 2);

							myPGNValue = parseInt(myHexStr, 16);

							if(myUnitsFlags  == 39) // Hours
								myPGNValue  = (parseFloat(myPGNValue) / 3600).toFixed(1); // converted to hours
							else if(myUnitsFlags  == 37) // MPH
								myPGNValue  = (parseFloat(myPGNValue) / 60).toFixed(2); // converted to minutes

							myPGNData.push([((myPGNValue )), myTimeStamp]); // time in seconds
					}
					  
					else if((myChannel == 2) && (myParameterIndex == 5))  // cycles 2
					{	
                            
						myHexStr = myN2Kdata[3];
						myHexStr =  "0x" + myHexStr.substr(14, 2);

						myPGNValue = parseInt(myHexStr, 16);

						myPGNData.push([(((myPGNValue * 1.0))), myTimeStamp]); //cycle count
								
					}
                       
					else if((myChannel == 3) && (myParameterIndex == 6)) // runtime 3
					{
							myHexStr = myN2Kdata[3];
							myHexStr = "0x" + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) +  myHexStr.substr((8), 2);

							myPGNValue = parseInt(myHexStr, 16);

							if(myUnitsFlags  == 39) // Hours
								myPGNValue  = (parseFloat(myPGNValue) / 3600).toFixed(1); // converted to hours
							else if(myUnitsFlags  == 37) // MPH
								myPGNValue  = (parseFloat(myPGNValue) / 60).toFixed(2); // converted to minutes

							myPGNData.push([((myPGNValue )), myTimeStamp]); // time in seconds
					}
					  
					else if((myChannel == 3) && (myParameterIndex == 7))  // cycles 3
					{	
                            
						myHexStr = myN2Kdata[3];
						myHexStr =  "0x" + myHexStr.substr(14, 2);

						myPGNValue = parseInt(myHexStr, 16);

						myPGNData.push([(((myPGNValue * 1.0))), myTimeStamp]); //cycle count
								
					}

					else if((myChannel == 4) && (myParameterIndex == 8)) // runtime 4
					{
							myHexStr = myN2Kdata[3];
							myHexStr = "0x" + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) +  myHexStr.substr((8), 2);

							myPGNValue = parseInt(myHexStr, 16);

							if(myUnitsFlags  == 39) // Hours
								myPGNValue  = (parseFloat(myPGNValue) / 3600).toFixed(1); // converted to hours
							else if(myUnitsFlags  == 37) // MPH
								myPGNValue  = (parseFloat(myPGNValue) / 60).toFixed(2); // converted to minutes

							myPGNData.push([((myPGNValue )), myTimeStamp]); // time in seconds
					}
					  
					else if((myChannel == 4) && (myParameterIndex == 9))  // cycles 4
					{	
                            
						myHexStr = myN2Kdata[3];
						myHexStr =  "0x" + myHexStr.substr(14, 2);

						myPGNValue = parseInt(myHexStr, 16);

						myPGNData.push([(((myPGNValue * 1.0))), myTimeStamp]); //cycle count
								
					}					
					
					else if((myChannel == 5) && (myParameterIndex == 10)) // runtime 5
					{
							myHexStr = myN2Kdata[3];
							myHexStr = "0x" + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) +  myHexStr.substr((8), 2);

							myPGNValue = parseInt(myHexStr, 16);

							if(myUnitsFlags  == 39) // Hours
								myPGNValue  = (parseFloat(myPGNValue) / 3600).toFixed(1); // converted to hours
							else if(myUnitsFlags  == 37) // MPH
								myPGNValue  = (parseFloat(myPGNValue) / 60).toFixed(2); // converted to minutes

							myPGNData.push([((myPGNValue )), myTimeStamp]); // time in seconds
					}
					  
					else if((myChannel == 5) && (myParameterIndex == 11))  // cycles 5
					{	
                            
						myHexStr = myN2Kdata[3];
						myHexStr =  "0x" + myHexStr.substr(14, 2);

						myPGNValue = parseInt(myHexStr, 16);

						myPGNData.push([(((myPGNValue * 1.0))), myTimeStamp]); //cycle count
								
					}
										
										
					else if((myChannel == 6) && (myParameterIndex == 12)) // runtime 6
					{
							myHexStr = myN2Kdata[3];
							myHexStr = "0x" + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) +  myHexStr.substr((8), 2);

							myPGNValue = parseInt(myHexStr, 16);

							if(myUnitsFlags  == 39) // Hours
								myPGNValue  = (parseFloat(myPGNValue) / 3600).toFixed(1); // converted to hours
							else if(myUnitsFlags  == 37) // MPH
								myPGNValue  = (parseFloat(myPGNValue) / 60).toFixed(2); // converted to minutes

							myPGNData.push([((myPGNValue )), myTimeStamp]); // time in seconds
					}
					  
					else if((myChannel == 6) && (myParameterIndex == 13))  // cycles 6
					{	
                            
						myHexStr = myN2Kdata[3];
						myHexStr =  "0x" + myHexStr.substr(14, 2);

						myPGNValue = parseInt(myHexStr, 16);

						myPGNData.push([(((myPGNValue * 1.0))), myTimeStamp]); //cycle count
								
					}
					
					else if((myChannel == 7) && (myParameterIndex == 14)) // runtime 7
					{
							myHexStr = myN2Kdata[3];
							myHexStr = "0x" + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) +  myHexStr.substr((8), 2);

							myPGNValue = parseInt(myHexStr, 16);

							if(myUnitsFlags  == 39) // Hours
								myPGNValue  = (parseFloat(myPGNValue) / 3600).toFixed(1); // converted to hours
							else if(myUnitsFlags  == 37) // MPH
								myPGNValue  = (parseFloat(myPGNValue) / 60).toFixed(2); // converted to minutes

							myPGNData.push([((myPGNValue )), myTimeStamp]); // time in seconds
					}
					  
					else if((myChannel == 7) && (myParameterIndex == 15))  // cycles 7
					{	
                            
						myHexStr = myN2Kdata[3];
						myHexStr =  "0x" + myHexStr.substr(14, 2);

						myPGNValue = parseInt(myHexStr, 16);

						myPGNData.push([(((myPGNValue * 1.0))), myTimeStamp]); //cycle count
								
					}
					   
          
			} // Instance match
		} // Custom PGN match
	  } // good checksum
	} // 65286 Array Loop

	return myPGNData;

} // end of function GetPGN 65286



// Ststus Parameters
// PGN 65287 [0x000FF07] AC Power Watt Hours
// myPGNINstance = Instance and type
// Type = myPGNINstance & 0x0F
// Instance = myPGNINstance & 0xF0
// myParameterIndex = 0  -> Watt Hours
// myParameterIndex = 1  -> kWatt Hours
// 
//
function GetPGN65287(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 




      // Get all the elements and parse into variables
      //for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
			myHexStr = myN2Kdata[3];
			myHexStr =  myHexStr.substr(0 ,4)
			if(myHexStr == "99E1")
			{
				myHexStr = myN2Kdata[3];
				myHexStr = "0x" + myHexStr.substr(4 ,2) ;

				myInstance = parseInt(myHexStr);
				
				if(myInstance == myPGNInstance) // watt hours
				{                      
					if(myParameterIndex == 0)
					  {
	                   myHexStr = myN2Kdata[3];
                       myHexStr = myHexStr.substr(14, 2) + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) + myHexStr.substr(8, 2);

                       myPGNValue = parseInt(myHexStr, 16);

								myPGNData.push([(((myPGNValue * 1.0) )), myTimeStamp]);
			
					  }
					  
					  
					else if(myParameterIndex == 1)  // Kwatt hours
					{	
                    
                            
	                   myHexStr = myN2Kdata[3];
                       myHexStr = myHexStr.substr(14, 2) + myHexStr.substr(12, 2) + myHexStr.substr(10, 2) + myHexStr.substr(8, 2);

                       myPGNValue = parseInt(myHexStr, 16);

					

								myPGNData.push([(((myPGNValue * .001))), myTimeStamp]);
								
						}
						

                          
          
			} // Instance match
		} // Custom PGN match
	  } // good checksum
	} // 65287 Array Loop

	return myPGNData;

} // end of function GetPGN 65287



// Ststus Parameters
// PGN 65288 [0x000FF08] AC Power Watt Hours
// myPGNINstance = Instance and type
// Type = myPGNINstance & 0x0F
// Instance = myPGNINstance & 0xF0
// myParameterIndex = 0  -> AC Volts
// myParameterIndex = 1  -> AC Amps
// myParameterIndex = 2  -> AC Sensor Status
// 
//
function GetPGN65288(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 




      // Get all the elements and parse into variables
      //for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {

             myHexStr = myN2Kdata[3];

			 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(16 ,1) == '*')
			{
				var checksum = parseInt("0x" + myHexStr.substr(17 ,2));
				var cs_string = "PCDIN," + String(myN2Kdata[0]) + "," +  String(myN2Kdata[1]) + "," + String(myN2Kdata[2]) + "," + String(myHexStr.substr(0 ,16));
				var N2kchecksum = 0;

				for(var ik=0; ik<cs_string.length; ik++)
				{
					N2kchecksum = 0x00FF & (N2kchecksum ^ cs_string.charCodeAt(ik));
				}
				
			   if(checksum != N2kchecksum)
					return myPGNData;
			
			
			
				var myTimeStamp;
				var myTimeStampStr;
	
				myTimeStampStr = myN2Kdata[1];
				myTimeStamp = parseInt(myTimeStampStr, 32);
				myTimeStamp = myTimeStamp + 1262304000;
				myTimeStamp = myTimeStamp * 1000;
				
			myHexStr = myN2Kdata[3];
			myHexStr =  myHexStr.substr(0 ,4)
			if(myHexStr == "99E1")
			{
				myHexStr = myN2Kdata[3];
				myHexStr = "0x" + myHexStr.substr(4 ,2) ;

				myInstance = parseInt(myHexStr);
				
				if(myInstance == myPGNInstance) // volts
				{                      
					if(myParameterIndex == 0)
					  {
	                   myHexStr = myN2Kdata[3];
                       myHexStr = myHexStr.substr(8, 2) + myHexStr.substr(6, 2);

                       myPGNValue = parseInt(myHexStr, 16);

								myPGNData.push([(((myPGNValue * 0.1) )), myTimeStamp]);
			
					  }
					  
					  
					else if(myParameterIndex == 1)  // Amps
					{	
                    
                            
	                   myHexStr = myN2Kdata[3];
                       myHexStr = myHexStr.substr(12, 2) + myHexStr.substr(10, 2) ;

                       myPGNValue = parseInt(myHexStr, 16);

					

								myPGNData.push([(((myPGNValue * 0.1))), myTimeStamp]);
								
						}
						
					else if(myParameterIndex == 2)  // status
					{	
                    
                            
	                   myHexStr = myN2Kdata[3];
                       myHexStr = myHexStr.substr(14, 2)  ;

                       myPGNValue = parseInt(myHexStr, 16);

					

								myPGNData.push([(((myPGNValue * 1))), myTimeStamp]);
								
						}
						

                          
          
			} // Instance match
		} // Custom PGN match
	  } // good checksum
	} // 65288 Array Loop

	return myPGNData;

} // end of function GetPGN 65288

// Wind Data
// NMEA0183 IIMWD - Wind data
// myParameterIndex = 1  -> Wind Direction True
// myParameterIndex = 1  -> Wind Direction Magnetic
// myParameterIndex = 0  -> Wind Speed Knots
// myParameterIndex = 1  -> Wind Speed M/Sec
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetIIMWD(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myIIMWDStr = new Array();
 
	var myDirectionTrue;
	var myDirectionApparent;
	var mySpeedTrue;
	var mySpeedApparent;

	var myDegreesMagN;
	var myDegreesTrueN;
	
	var myTimeStamp = 0;

	mySubStrings = myN2Kdata.split("$IIMWD,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			myIIMWDStr = myHexStr.split(',');
			// alert(myIIMWDStr[0], myIIMWDStr[1], myIIMWDStr[2], myIIMWDStr[3]);

			if(myParameterIndex == 0) // Wind DIrection True
			{	
				if(myIIMWDStr[0] != '')
				{
					myPGNValue  = myIIMWDStr[0]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			else if(myParameterIndex == 1) // Wind Direction Magnetic
			{	
				if(myIIMWDStr[2] != '')
				{
					myPGNValue  = myIIMWDStr[2]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			else if(myParameterIndex == 2) // Wind Speed Knots
			{	
				if(myIIMWDStr[4] != '')
				{
					myPGNValue  = myIIMWDStr[4]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			else if(myParameterIndex == 3) // Wind Speed Meters/sec
			{	
				if(myIIMWDStr[6] != '')
				{
					myPGNValue  = myIIMWDStr[6]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}


	
	} // IIWMD Array Loop

	return myPGNData;

} // end of function GetIIWMD

// Wind Data
// NMEA0183 IIMWV- Wind data Realitive
// myParameterIndex = 1  -> Wind Direction True
// myParameterIndex = 1  -> Wind Direction Magnetic
// myParameterIndex = 0  -> Wind Speed Knots
// myParameterIndex = 1  -> Wind Speed M/Sec
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetIIMWV(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myIIMWVStr = new Array();
 	var myTimeStamp = 0;

	mySubStrings = myN2Kdata.split("$IIMWV,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			myIIMWVStr = myHexStr.split(',');


			if(myParameterIndex == 0) // Wind DIrection True
			{	
				if(myIIMWVStr[1] == 'R')
				{
					if(myIIMWVStr[0] != '')
					{
						myPGNValue  = myIIMWVStr[0]; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}

			else if(myParameterIndex == 1) // Wind Direction Theortical
			{	
				if(myIIMWVStr[1] == 'T')
				{
					if(myIIMWVStr[0] != '')
					{
						myPGNValue  = myIIMWVStr[0]; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}

			else if(myParameterIndex == 2) // Wind Speed Knots
			{	

				if(myIIMWVStr[3] == 'N')
				{
					if(myIIMWVStr[2] != '')
					{
						myPGNValue  = myIIMWVStr[2]; //
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				} 
				
			}

			else if(myParameterIndex == 3) // Wind Speed Km/hr
			{	
				if(myIIMWVStr[3] == 'K')
				{
					if(myIIMWVStr[2] != '')
					{
						myPGNValue  = myIIMWVStr[2]; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}

			else if(myParameterIndex == 4) // Wind Speed Mi/hr
			{	
				if(myIIMWVStr[3] == 'S')
				{
					if(myIIMWVStr[2] != '')
					{
						myPGNValue  = myIIMWVStr[2]; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}

			else if(myParameterIndex == 5) // Wind Speed M/s
			{	
				if(myIIMWVStr[3] == 'M')
				{
					if(myIIMWVStr[2] != '')
					{
						myPGNValue  = myIIMWVStr[2]; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}

         
	
	} // IIMWV Array Loop

	return myPGNData;

} // end of function GetIIMWV

// Wind Data
// NMEA0183 IIVWR - Wind data
// myParameterIndex = 1  -> Wind Direction True
// myParameterIndex = 1  -> Wind Direction Magnetic
// myParameterIndex = 0  -> Wind Speed Knots
// myParameterIndex = 1  -> Wind Speed M/Sec
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetIIVWR(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myIIVWRDStr = new Array();
	var myTimeStamp = 0;

	mySubStrings = myN2Kdata.split("$IIVWR,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			myIIVWRStr = myHexStr.split(',');
	
			// alert(myIIVWRStr[0]);

			if(myParameterIndex == 0) // Wind DIrection True
			{	
				if(myIIVWRStr[1] == 'L')
				{
					if(myIIVWRStr[0] != '')
					{
						myPGNValue  = '-' + myIIVWRStr[0]; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
				else if(myIIVWRStr[1] == 'R')
				{
					if(myIIVWRStr[0] != '')
					{
						myPGNValue  = myIIVWRStr[0]; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}

			else if(myParameterIndex == 1) // Wind Speed Knots
			{	
				if(myIIVWRStr[2] != '')
				{
					myPGNValue  = myIIVWRStr[2]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 2) // Wind Speed Meters/sec
			{	
				if(myIIVWRStr[2] != '')
				{
					myPGNValue  = myIIVWRStr[4]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 3) // Wind Speed Km/hr
			{	
				if(myIIVWRStr[2] != '')
				{
					myPGNValue  = myIIVWRStr[6]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

        
	
	} // IIVWR Array Loop

	return myPGNData;

} // end of function GetIIVWR

// Heading Data
// NMEA0183 HCHDG - Heading data
// myParameterIndex = 1  -> Wind Direction True
// myParameterIndex = 1  -> Wind Direction Magnetic
// myParameterIndex = 0  -> Wind Speed Knots
// myParameterIndex = 1  -> Wind Speed M/Sec
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetHCHDG(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHCHDGStr = new Array();
	var myTimeStamp = 0; 

	mySubStrings = myN2Kdata.split("$HCHDG,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			myHCHDGStr = myHexStr.split(',');
	

			if(myParameterIndex == 0) // Heading Magnetic
			{	
				if(myHCHDGStr[0] != '')
				{
					myPGNValue  = myHCHDGStr[0]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				 }
			}
			if(myParameterIndex == 1) // Heading True
			{	

				if(myHCHDGStr[4] == 'E')
				{
					if(myHCHDGStr[0] != '')
					{
						myPGNValue  = parseFloat(myHCHDGStr[0]) + parseFloat(myHCHDGStr[3]); // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
				else if (myHCHDGStr[4] == 'W')
				{
					if(myHCHDGStr[0] != '')
					{
						myPGNValue  = parseFloat(myHCHDGStr[0]) - parseFloat(myHCHDGStr[3]); 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}
	

      
	
	} // HCHDG Array Loop

	return myPGNData;

} // end of function GetHCHDG

// Water Heading and Speed Data
// NMEA0183 IIVHW - Water Heading and Speed data
// myParameterIndex = 1  -> Wind Direction True
// myParameterIndex = 1  -> Wind Direction Magnetic
// myParameterIndex = 0  -> Wind Speed Knots
// myParameterIndex = 1  -> Wind Speed M/Sec
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetIIVHW(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myIIVHWStr = new Array();
 
	var myTimeStamp = 0;

	mySubStrings = myN2Kdata.split("$IIVHW,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			myIIVHWStr = myHexStr.split(',');


			if(myParameterIndex == 0) // Water DIrection True
			{	
				if(myIIVHWStr[0] != '')
				{
					myPGNValue  = myIIVHWStr[0]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 1) // Water Direction Magnetic
			{	
				if(myIIVHWStr[2] != '')
				{
					myPGNValue  = myIIVHWStr[2]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 2) // Water Speed Knots
			{	
				if(myIIVHWStr[4] != '')
				{
					myPGNValue  = myIIVHWStr[4]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 3) // Wind Speed Kilometers/sec
			{	
				if(myIIVHWStr[6] != '')
				{
					myPGNValue  = myIIVHWStr[6]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

 
	
	} // IIVHW Array Loop

	return myPGNData;

} // end of function GetIIVHW

// COG & SOG Data
// NMEA0183 IIVTG - COG & SOG data
// myParameterIndex = 0  -> Track Direction True
// myParameterIndex = 1  -> Track Direction Magnetic
// myParameterIndex = 2  -> Track Speed Knots
// myParameterIndex = 3  -> Track Speed M/Sec
//
function GetIIVTG(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myIIVTGStr = new Array();
	var myTimeStamp = 0;
	mySubStrings = myN2Kdata.split("$IIVTG,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			myIIVTGStr = myHexStr.split(',');


			if(myParameterIndex == 0) // Water DIrection True
			{	
				if(myIIVTGStr[0] != '')
				{
					myPGNValue  = myIIVTGStr[0]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 1) // Water Direction Magnetic
			{	
				if(myIIVTGStr[2] != '')
				{
					myPGNValue  = myIIVTGStr[2]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 2) // Water Speed Knots
			{	
				if(myIIVTGStr[4] != '')
				{
					myPGNValue  = myIIVTGStr[4]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 3) // Wind Speed Kilometers/sec
			{	
				if(myIIVTGStr[6] != '')
				{
					myPGNValue  = myIIVTGStr[6]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

	} // IIVTG Array Loop

	return myPGNData;

} // end of function GetIIVTG

// Rate of Turn
// NMEA0183 IIROT - Rate of Turn
// myParameterIndex = 1  -> Wind Direction True
// myParameterIndex = 1  -> Wind Direction Magnetic
// myParameterIndex = 0  -> Wind Speed Knots
// myParameterIndex = 1  -> Wind Speed M/Sec
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetIIROT(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myIIROTStr = new Array();
 
	var myDirectionTrue;
	var myDirectionApparent;
	var mySpeedTrue;
	var mySpeedApparent;

	var myDegreesMagN;
	var myDegreesTrueN;
	var myTimeStamp = 0;
	
	mySubStrings = myN2Kdata.split("$IIROT,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];
			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// look for checksum character in the correct place or skip 
			myIIROTStr = myHexStr.split(',');
		
			if(myParameterIndex == 0) // Wind DIrection True
			{	
				if(myIIROTStr[0] != '')
				{
					myPGNValue  = myIIROTStr[0]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
	
	} // IIROT Array Loop

	return myPGNData;

} // end of function GetIIROT

// Rate of Turn
// NMEA0183 YXXDR - Pitch and Roll
// myParameterIndex = 0  -> Pitch
// myParameterIndex = 1  -> Roll
//
function GetYXXDR(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myYXXDRStr = new Array();
	var myTimeStamp = 0;
	
	mySubStrings = myN2Kdata.split("$YXXDR,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];
			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// look for checksum character in the correct place or skip 
			myYXXDRStr = myHexStr.split(',');
		
			if(myParameterIndex == 0) // Pitch
			{	
				if(myYXXDRStr[1] != '')
				{
					myPGNValue  = myYXXDRStr[1]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

			if(myParameterIndex == 1) // Roll
			{	
				if(myYXXDRStr[5] != '')
				{
					myPGNValue  = myYXXDRStr[5]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
	
	} // YXXDR Array Loop

	return myPGNData;

} // end of function GetYXXDR

// GPS Position Data
// NMEA0183 GPGLL - GPS data
// myParameterIndex = 0  -> Latitude
// myParameterIndex = 1  -> Longitude
// myParameterIndex = 2  -> Time
//
function GetGPGLL(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myGPGLLStr = new Array();
	var myTimeStamp = 0; 

	mySubStrings = myN2Kdata.split("$GPGLL,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			myGPGLLStr = myHexStr.split(',');
		

			if(myParameterIndex == 0) // Latitude
			{	
				if(myGPGLLStr[0] != '')
				{
					if(myGPGLLStr[1] == 'S')
					{
						myPGNValue  = -1.0 * (parseFloat(myGPGLLStr[0]))/100 ; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
					else if(myGPGLLStr[1] == 'N')
					{
						myPGNValue  = 1.0 * (parseFloat(myGPGLLStr[0]))/100 ; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}
			if(myParameterIndex == 1) // Longitude
			{	
				if(myGPGLLStr[2] != '')
				{
					if(myGPGLLStr[3] == 'W')
					{
						myPGNValue  = -1.0 * (parseFloat(myGPGLLStr[2]))/100 ; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
					else if(myGPGLLStr[3] == 'E')
					{
						myPGNValue  = 1.0 * (parseFloat(myGPGLLStr[2]))/100 ; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}
			if(myParameterIndex == 2) // Time
			{	
				if(myGPGLLStr[4] != '')
				{
					myPGNValue  = myGPGLLStr[4]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			


	
	} // GPGLL Array Loop

	return myPGNData;

} // end of function GetGPGLL

// GPS Data
// NMEA0183 GPRMC - GPS data
// myParameterIndex = 1  -> Wind Direction True
// myParameterIndex = 1  -> Wind Direction Magnetic
// myParameterIndex = 0  -> Wind Speed Knots
// myParameterIndex = 1  -> Wind Speed M/Sec
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetGPRMC(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myGPRMCStr = new Array();
	var myTimeStamp = 0;
	
	mySubStrings = myN2Kdata.split("$GPRMC,");

    myArrayLength = mySubStrings.length;

	

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {

	         myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			myGPRMCStr = myHexStr.split(',');

			if(myParameterIndex == 0) // Time
			{	
				if(myGPRMCStr[0] != '')
				{
					myPGNValue  = myGPRMCStr[0]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

    		if(myParameterIndex == 1) // Latitude
			{	
				if(myGPRMCStr[2] != '')
				{
					if(myGPRMCStr[3] == 'S')
					{
						myPGNValue  = -1.0 * (parseFloat(myGPRMCStr[2]))/100 ; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
					else if(myGPRMCStr[3] == 'N')
					{
						myPGNValue  = 1.0 * (parseFloat(myGPRMCStr[2]))/100 ; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}
			if(myParameterIndex == 2) // Longitude
			{	
				if(myGPRMCStr[4] != '')
				{
					if(myGPRMCStr[5] == 'W')
					{
						myPGNValue  = -1.0 * (parseFloat(myGPRMCStr[4]))/100 ; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
					else if(myGPRMCStr[5] == 'E')
					{
						myPGNValue  = 1.0 * (parseFloat(myGPRMCStr[4]))/100 ; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}

			if(myParameterIndex == 3) // SOG
			{	
				if(myGPRMCStr[6] != '')
				{
					myPGNValue  = myGPRMCStr[6]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

			if(myParameterIndex == 4) // track made good
			{	
				if(myGPRMCStr[7] != '')
				{
					myPGNValue  = myGPRMCStr[7]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

			if(myParameterIndex == 5) // date
			{	
				if(myGPRMCStr[8] != '')
				{
					myPGNValue  = myGPRMCStr[8]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

			if(myParameterIndex == 6) // mag variation
			{	
				if(myGPRMCStr[9] != '')
				{
					if(myGPRMCStr[10] == 'W')
					{
						myPGNValue  = -1.0 * (parseFloat(myGPRMCStr[9])) ; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
					else if(myGPRMCStr[10] == 'E')
					{
						myPGNValue  = 1.0 * (parseFloat(myGPRMCStr[9])) ; // 
						myPGNData.push([myPGNValue, myTimeStamp]) ;
					}
				}
			}
			
	
	} // GPRMC Array Loop

	return myPGNData;

} // end of function GetGPRMC

// Sonar Data
// NMEA0183 SDDBT - Sonar data
// myParameterIndex = 0  -> Depth feet
// myParameterIndex = 1  -> depth meters
// myParameterIndex = 2  -> depth fathoms
//
function GetSDDBT(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var mySDDBTStr = new Array();
	var myTimeStamp = 0;
	

	mySubStrings = myN2Kdata.split("$SDDBT,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			mySDDBTStr = myHexStr.split(',');
		

			if(myParameterIndex == 0) // Depth feet
			{	
				if(mySDDBTStr[0] != '')
				{
					myPGNValue  = mySDDBTStr[0]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 1) // Depth meters
			{	
				if(mySDDBTStr[2] != '')
				{
					myPGNValue  = mySDDBTStr[2]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 2) // Depth fathoms
			{	
				if(mySDDBTStr[4] != '')
				{
					myPGNValue  = mySDDBTStr[4]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
		

          
	
	} // SDDBT Array Loop

	return myPGNData;

} // end of function GetSDDBT

// Water temp Data
// NMEA0183 SDMTW - Water Temp data
// myParameterIndex = 0  -> Water temp Celcius
// myParameterIndex = 1  -> Fahariehent
//
function GetSDMTW(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var mySDMTWStr = new Array();
 	var myTimeStamp = 0;
	

	mySubStrings = myN2Kdata.split("$SDMTW,");

    myArrayLength = mySubStrings.length;

	//alert("IIWMD " + mySubStrings[1] + "   " + mySubStrings.length);

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			mySDMTWStr = myHexStr.split(',');
			

			if(myParameterIndex == 0) // Water Temp Celcius
			{	
				if(mySDMTWStr[0] != '')
				{
					myPGNValue  = mySDMTWStr[0]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			if(myParameterIndex == 1) // Wind Temp Fahrenheit
			{	
				if(mySDMTWStr[0] != '')
				{
					myPGNValue  = 32 + (parseFloat(mySDMTWStr[0]) * 1.8); // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			

 
	
	} // SDMTW Array Loop

	return myPGNData;

} // end of function GetSDMTW


// Meteorological Data
// NMEA0183 WIMDA - Meteorological  data
// myParameterIndex = 0  -> Baro InHg
// myParameterIndex = 1  -> Baro Bars
// myParameterIndex = 2  -> Air Temp C
// myParameterIndex = 3  -> Water Temp
// myParameterIndex = 4  -> Humidity R
// myParameterIndex = 5  -> Humidity A
// myParameterIndex = 6  -> Dew Point
// myParameterIndex = 7  -> Wind Dir T
// myParameterIndex = 8  -> Wind Dir M
// myParameterIndex = 9  -> Wind Speed Knots
// myParameterIndex = 10  -> Wind Speed M/s
//
function GetWIMDA(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myWindRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myWIMDAStr = new Array();
	var myTimeStamp = 0;
	
	mySubStrings = myN2Kdata.split("$WIMDA,");

    myArrayLength = mySubStrings.length;

      // Get all the elements and parse into variables
      for (myIndex = 1; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

			 myHexStr = myHexStr.substr(0,myHexStr.indexOf('*'));
			// alert(myHexStr);
			// look for checksum character in the correct place or skip 
			myWIMDAStr = myHexStr.split(',');
	

			if(myParameterIndex == 0) //  Baro InHg
			{	
				if( myWIMDAStr[0] != '')
				{
				myPGNValue  = myWIMDAStr[0]; // 
				myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			else if(myParameterIndex == 1) //  Baro Bars
			{	
				if( myWIMDAStr[2] != '')
				{
					myPGNValue  = myWIMDAStr[2]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			else if(myParameterIndex == 2) // Air Temp
			{	
				if( myWIMDAStr[4] != '')
				{
					myPGNValue  = myWIMDAStr[4]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}
			else if(myParameterIndex == 3) // Water Temp
			{	
				if( myWIMDAStr[6] != '')
				{
					myPGNValue  = myWIMDAStr[6]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

			else if(myParameterIndex == 4) // Humidity R
			{	
				if( myWIMDAStr[8] != '')
				{
					myPGNValue  = myWIMDAStr[8]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

			else if(myParameterIndex == 5) // Humidity A
			{	
				if( myWIMDAStr[9] != '')
				{
					myPGNValue  = myWIMDAStr[9]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

			else if(myParameterIndex == 6) // Dew Point
			{	
				if( myWIMDAStr[10] != '')
				{
					myPGNValue  = myWIMDAStr[10]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

			else if(myParameterIndex == 7) // Wind Dir True
			{	
				if( myWIMDAStr[12] != '')
				{
					myPGNValue  = myWIMDAStr[12]; //
					myPGNData.push([myPGNValue, myTimeStamp]) ; 
				}
			}

			else if(myParameterIndex == 8) // Wind Dir Mag
			{	
				if( myWIMDAStr[14] != '')
				{
					myPGNValue  = myWIMDAStr[14]; //
					myPGNData.push([myPGNValue, myTimeStamp]) ; 
				}
			}

			else if(myParameterIndex == 9) // Wind Speed Knots
			{	
				if( myWIMDAStr[16] != '')
				{
					myPGNValue  = myWIMDAStr[16]; //
					myPGNData.push([myPGNValue, myTimeStamp]) ; 
				}
			}

			else if(myParameterIndex == 10) // Wind Speed M/s
			{	
				if( myWIMDAStr[18] != '')
				{
					myPGNValue  = myWIMDAStr[18]; // 
					myPGNData.push([myPGNValue, myTimeStamp]) ;
				}
			}

          
	
	} // WIMDA Array Loop

	return myPGNData;

} // end of function GetWIMDA