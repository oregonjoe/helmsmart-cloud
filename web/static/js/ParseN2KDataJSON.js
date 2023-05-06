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

var WindGustArray = new Array(0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0);
var gustIndex = 0;
// GetPGNbyNumber
// 
// myN2Kdata   -> DataString
// myPGNInstance  -> INstance Number
// myPGNNumber  -> PGN
//
function GetPGNbyNumber(myN2Kdata, myPGNInstance, myPGNNumber, myParameterIndex, myUnitsFlags )
{



var myN2KValues = new Array();

	switch (myPGNNumber)
	{
		
		case "65287": //PGN65287: SeaSmart ac watt hours 0x0FF07
			myN2KValues = GetPGN65287(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break
		
		case "65288": //PGN65288: SeaSmart ac watt hours 0x0FF07
			myN2KValues = GetPGN65287(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break
		
		case "65014": //#PGN65014: J1939 PGN 65014 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myN2KValues = GetPGN65014(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break
		
		case "65011": //#PGN65011: J1939 PGN 65011 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myN2KValues = GetPGN65011(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break

		
		case "65008": //#PGN65008: J1939 PGN 65008 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myN2KValues = GetPGN65008(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break

		
		case "65017": //#PGN65017: J1939 PGN 65017 - (0x00FDF6) Utility AVG Basic AC Quantities
			myN2KValues = GetPGN65017(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break
		
		case "65005": //#PGN65005: J1939 PGN 65005 - (0x00FDF6) Utility Total AC Energy
			myN2KValues = GetPGN65005(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break


		case "65027": //#PGN65027: J1939 PGN 65014 - (0x00FDF6) Generator Phase A Basic AC Quantities
			myN2KValues = GetPGN65027(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break
		
		case "65024": //#PGN65024: J1939 PGN 65011 - (0x00FDF6) Generator Phase B Basic AC Quantities
			myN2KValues = GetPGN65024(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break

		
		case "65021": //#PGN65021: J1939 PGN 65021 - (0x00FDF6) Generator Phase C Basic AC Quantities
			myN2KValues = GetPGN65021(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break

		case "65030": //#PGN65030: J1939 PGN 6530 - (0x00FDF6) Generator AVG Basic AC Quantities
			myN2KValues = GetPGN65030(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break

		case "65018": //#PGN65018: J1939 PGN 65018 - (0x00FDF6) Generator Total AC Energy
			myN2KValues = GetPGN65018(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break
		
		case "61444": //#PGN61444: J1939 PGN 61444 - (0x00F004) J1939 Electronic Engine Controller 1
			myN2KValues = GetPGN61444(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break
		
		
		case "65262": //#PGN65062: J1939 PGN 65262 - (0x00FEEE) J1939 Engine Temps
			myN2KValues = GetPGN65262(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break
		
		case "65263": //#PGN65263: J1939 PGN 65263 - (0x00FEEF) J1939 Engine Pressure
			myN2KValues = GetPGN65263(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break
		
		case "65271": //#PGN65263: J1939 PGN 65271 - (0x00FEF7) J1939 Vehicle Electrical Power
			myN2KValues = GetPGN65271(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break
		
		case "65292": //#PGN65263: J1939 PGN 65271 - (0x00FF0C) Custom INdicator Runtime
			myN2KValues = GetPGN65292(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break
		
        case "127488":
			myN2KValues = GetPGN127488(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break

		case "127489":
			myN2KValues = GetPGN127489(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
			
		break
		
		
		case "127506":	
		 	myN2KValues = GetPGN127506(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break

		case "127508":	
		 	myN2KValues = GetPGN127508(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break

		case "127505":
	 		myN2KValues = GetPGN127505(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break

		case "127493":
	 		myN2KValues = GetPGN127493(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break
		
		case "127497":
	 		myN2KValues = GetPGN127497(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break
		
		
		// ENviron Data 0x1FD07
		case "130311":		
	 		 myN2KValues = GetPGN130311(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
			
		break
		// Metro Station  Data 0x1FD13
		case "130323":
		//  myN2KValues = GetPGN130323(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
			
		break
		
		// Metro Station  Data 0x1FF82
		case "130946":
			myN2KValues = GetPGN130946(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
			
		break
		
		
		// Wind Data 0x1FD02
		 case "130306":
			myN2KValues = GetPGN130306(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
			
		break
		// Heading 0x1F112
		case "127250":
			 myN2KValues = GetPGN127250(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break
		// Attitude 0x1F119
		case "127257":
			  myN2KValues = GetPGN127257(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);

		break

		// Environmential Temperature 0x1FD08
		case "130312":
				 myN2KValues = GetPGN130312(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break


		// Environmential Temperature extended 0x1FD0C
		case "130316":
				 myN2KValues = GetPGN130316(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break


		// Rudder 0x1FD08
		case "127245":
		//		myN2KValues = GetPGN127245(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);				
		break

		// Rate of Turn 0x1F10D
		case "127251":
		//		myN2KValues = GetPGN127251(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		// Switch Status 0x1F20D
		case "127501":
				myN2KValues = GetPGN127501(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);			
		break

		// COG & SOG				 
		case "129026":
			myN2KValues = GetPGN129026(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		// Water Speed				 
		case "128259":
			myN2KValues = GetPGN128259(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		// Depth				 
		case "128267":
			myN2KValues = GetPGN128267(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break
		
		// Custom SeaSmart - Dimmer				 
		case "65286":
			myN2KValues = GetPGN65286(myN2Kdata, parseInt(myPGNInstance), myParameterIndex, myUnitsFlags);
		break

		case "IIMWD":
		//	myN2KValues = GetIIMWD(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "IIMWV":
		//	myN2KValues = GetIIMWV(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "IIVWR":
		//	myN2KValues = GetIIVWR(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "HCHDG":
			myN2KValues = GetHCHDG(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "IIVHW":
		//	myN2KValues = GetIIVHW(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "IIVTG":
		//	myN2KValues = GetIIVTG(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "IIROT":
		//	myN2KValues = GetIIROT(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "YXXDR":
		//	myN2KValues = GetYXXDR(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "GPGLL":
		//	myN2KValues = GetGPGLL(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "GPRMC":
		//	myN2KValues = GetGPRMC(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "SDDBT":
		//	myN2KValues = GetSDDBT(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "SDMTW":
		//	myN2KValues = GetSDMTW(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break

		case "WIMDA":
		//	myN2KValues = GetWIMDA(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags);
		break


	


		default:
		
		break;
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
    var Instance, myInstanceString;
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


      vGYear = 0;
      vGHour = 0;

   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
		  
		  // need to catch case when there is no entry for this index
		   try{	myPGN = myN2Kdata[myIndex].pgn}catch(err) {myPGN = 'FFFFFF'};if(myPGN == "01F010")
					  
			{

		     myInstanceString = myN2Kdata[myIndex].payload.time_source;

			switch( myInstanceString ) {
				case "GPS":
					myInstance = 0;
					break;

				case "GLONASS":
					myInstance = 1;
					break;

				case "Radio Station":
					myInstance = 2;
					break;

				case "Cesium/Rubid Clock":
					myInstance = 3;
					break;

				case "Cesium/Rubid Clock":
					myInstance = 4;
					break;

				case "Crystal Clock":
					myInstance = 5;
					break;

				case "SeaGauge":
					myInstance = 6;
					break;
					
				case "GNSS":
					myInstance = 7;
					break;

				case "HelmSmart":
					myInstance = 8;
					break;

				case "SeaSmart RTC":
					myInstance = 9;
					break;

				default:
					myInstance = 15;
					break;
			}

				if(myInstance == SystemClockPGNID) // Instance match
				{  
                     myPGNValue = myN2Kdata[myIndex].payload.days;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null && myPGNValue >0 )
					{

	                     vGDay = (myPGNValue * 86400) * 1000;
	
						myPGNValue = myN2Kdata[myIndex].payload.ms;
						if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						{

		                    vGSec = Math.floor(myPGNValue / 1000);
		
		                    vGSec = Math.floor(vGSec + vGDay);
		                    NGTDate.setTime(vGSec);
		
		                    vGN2KTime.push(NGTDate.toUTCString());
	                    }
                   }
                              
                 } // Time Instance
			 } //good checksum character
         } // PGN126992 Array Loop

	return vGN2KTime;
	

} // end of function GetPGN 126992


// J1939 PGN 61444 (0x0F004) Electronic Engine Controller 1
// myParameterIndex = 0  -> Engine torque mode
// myParameterIndex = 1  -> Driver Demand Torque  (-125% to 125%) 1%/bit   
// myParameterIndex = 2  -> Actual Torque  (-125% to 125%) 1%/bit 
// myParameterIndex = 3  -> RPM LB (0-8031) 0.125 rpm/bit
// myParameterIndex = 4  -> Source address
// myParameterIndex = 5  -> Starter mode 
// myParameterIndex = 6  -> engine demand request torque  (-125% to 125%) 1%/bit 
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


    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00F004")
			{
                      
                      
                      if(myParameterIndex == 0) // Engine torque mode
					  {
					  		myPGNValue =myN2Kdata[myIndex].payload.torque_mode;
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue) ) ;
								myPGNData.push(myHexStr) ;
							}
					  }
					   if(myParameterIndex == 1) // Driver Demand Torque  (-125% to 125%) 1%/bit  
					  {
					  		myPGNValue =myN2Kdata[myIndex].payload.torque_demand;
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 1.0) - 125) ;
								myPGNData.push(myHexStr) ;
							}
					  }
					   if(myParameterIndex == 2) // Actual Torque  (-125% to 125%) 1%/bit 
					  {
					  		myPGNValue =myN2Kdata[myIndex].payload.torque_actual;
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 1.0)  - 125) ;
								myPGNData.push(myHexStr) ;
							}
					  }
					  
					  if(myParameterIndex == 3) // RPM LB (0-8031) 0.125 rpm/bit
					  {
					  		myPGNValue =myN2Kdata[myIndex].payload.speed;
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 0.125) ) ;
								myPGNData.push(myHexStr) ;
							}
					  }
					  
					  if(myParameterIndex == 4) //  // Source address
					  {
					  		myPGNValue =myN2Kdata[myIndex].payload.source_address;
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue ) ) ;
								myPGNData.push(myHexStr) ;
							}
					  }
					  
					  if(myParameterIndex == 5) // Starter mode
					  {
					  		myPGNValue =myN2Kdata[myIndex].payload.starter_mode;
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue ) ) ;
								myPGNData.push(myHexStr) ;
							}
					  }
					  
					  if(myParameterIndex == 6) // engine demand request torque  (-125% to 125%) 1%/bit  
					  {
					  		myPGNValue =myN2Kdata[myIndex].payload.torque_request;
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 1.0) - 125 ) ;
								myPGNData.push(myHexStr) ;
							}
					  }

	
		}
	} // 61444 Array Loop

	return myPGNData;

} // end of function GetPGN 61444



// J1939 Engine Temps  PGN 065262 [0x00FEEE] Engine Temps
// myParameterIndex = 0  -> Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
// myParameterIndex = 1  -> Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset
// myParameterIndex = 2  -> Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 3  -> Engine Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
// myParameterIndex = 4  -> Engine Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   
// myParameterIndex = 5  -> Engine Intercooler Thermostat Opening (0-100 %) 0.4%/bit   
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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FEEE")
			{

                                     

                           
							//Engine Coolant Temperature (-40 to 210 deg C) 1C/bit -40 C offset 
     						if(myParameterIndex == 0) // get temperature
							{
                     			myPGNValue = myN2Kdata[myIndex].payload.engine_temp;							
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags == 1) // degrees C
										myPGNData.push(Math.floor(((myPGNValue * 1.0) - 40)));
									else if(myUnitsFlags  == 2) // degrees Kelvin
										myPGNData.push(Math.floor(((myPGNValue * 1.0) - 233 )));
									else // default is degrees F
										myPGNData.push(Math.floor(((myPGNValue * 1.8) - 40)));
								}
                             }

							 //  Engine Fuel Temperature (-40 to 210 deg C) 1C/bit -40 C offset   
                             if(myParameterIndex == 1) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.fuel_temp;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags  == 1) // degrees C
										myPGNData.push(Math.floor(((myPGNValue * 1.0) - 40)));
									else if(myUnitsFlags  == 2) // degrees Kelvin
										myPGNData.push(Math.floor(((myPGNValue * 0.01) - 233 )));
									else // default is degrees F
										myPGNData.push(Math.floor((((myPGNValue) * 1.8) - 40)));
								}
							}
                       

                           	//  Engine Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
                             if(myParameterIndex == 2) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.oil_temp;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags  == 1) // degrees C
										myPGNData.push(Math.floor(((myPGNValue * 0.03125) - 273)));
									else if(myUnitsFlags  == 2) // degrees Kelvin
										myPGNData.push(Math.floor(((myPGNValue * 0.03125) )));
									else // default is degrees F
										myPGNData.push(Math.floor((((myPGNValue) * 0.05625) - 459)));
								}
							}
                       

                           	//  Turbocharger Oil Temperature LSB (-273 to 1735 deg C) 0.03125 C/bit -273 C offset  
                             if(myParameterIndex == 3) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.turbo_temp;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags  == 1) // degrees C
										myPGNData.push(Math.floor(((myPGNValue * 0.03125) - 273)));
									else if(myUnitsFlags  == 2) // degrees Kelvin
										myPGNData.push(Math.floor(((myPGNValue * 0.03125) )));
									else // default is degrees F
										myPGNData.push(Math.floor((((myPGNValue) * 0.05625) - 459)));
								}
							}
							
                           	//  Intercooler Temperature   (-40 to 210 deg C) 1C/bit -40 C offset   
                             if(myParameterIndex == 4) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.intercool_temp;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags  == 1) // degrees C
										myPGNData.push(Math.floor(((myPGNValue * 1.0) - 40)));
									else if(myUnitsFlags  == 2) // degrees Kelvin
										myPGNData.push(Math.floor(((myPGNValue * 0.01) - 233 )));
									else // default is degrees F
										myPGNData.push(Math.floor((((myPGNValue) * 1.8) - 40)));
								}
							}
                        
          
				
		}
		
	} // 065262 Array Loop

	return myPGNData;
		

} // end of function GetPGN 065262



// J1939 PGN 65263 (0x0FEEF) Engine Pressures
// myParameterIndex = 0  -> Fuel Pressure 4 kPa/bit
// myParameterIndex = 1  -> Crankcase blowby .05 kPa/bit
// myParameterIndex = 2  -> Engine Oil Level  0.4% kPa/bit
// myParameterIndex = 3  -> Engine Oil Pressure 4 kPa/bit
// myParameterIndex = 4  -> Crankcase Pressure LSB 0.0078 kPa/bit -250 kPa offset
// myParameterIndex = 5  -> Coolant Pressure 2 kPa/bit    
// myParameterIndex = 6  -> Coolant Leval .4%  kPa/bit  
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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FEEF")
			{

				
							// Fuel Pressure 4 kPa/bit
     						if(myParameterIndex == 0) // get temperature
							{
                     			myPGNValue = myN2Kdata[myIndex].payload.fuel_pressure;							
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags  == 8) // PSI
									{
										myPGNData.push((myPGNValue * 0.0145037738007 * 40) ) ;
										
									}
									else if(myUnitsFlags == 9) // kPa
									{
										myPGNData.push((myPGNValue * 0.1 * 40) ) ;
										
									}
									else if(myUnitsFlags  == 10* 40) // inHg
									{
										myPGNData.push((myPGNValue * 0.0295229* 40) ) ;
										
									}
									else // default isPSI
									{
										myPGNData.push((myPGNValue * 0.0145037738007 * 40) ) ;
										
									}
								}
                             }
                           
							//Crankcase blowby .05 kPa/bit    
     						if(myParameterIndex == 1) // get temperature
							{
                     			myPGNValue = myN2Kdata[myIndex].payload.blowby_pressure;							
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags  == 8) // PSI
									{
										myPGNData.push((myPGNValue * 0.0145037738007 * 0.5) ) ;
										
									}
									else if(myUnitsFlags == 9) // kPa
									{
										myPGNData.push((myPGNValue * 0.1 * 0.5) ) ;
										
									}
									else if(myUnitsFlags  == 10* 40) // inHg
									{
										myPGNData.push((myPGNValue * 0.0295229* 0.5) ) ;
										
									}
									else // default isPSI
									{
										myPGNData.push((myPGNValue * 0.0145037738007 * 0.5) ) ;
										
									}
								}
                             }

							 //  Engine Oil Level  0.4% kPa/bit
                             if(myParameterIndex == 2) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.oil_level;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									myPGNData.push((myPGNValue * 0.4) ) ;
									
								}
							}
							
                        //  Engine Oil Pressure 4 kPa/bit
                             if(myParameterIndex == 3) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.oil_pressure;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags  == 8) // PSI
									{
										myPGNData.push((myPGNValue * 0.0145037738007 * 40) ) ;
										
									}
									else if(myUnitsFlags == 9) // kPa
									{
										myPGNData.push((myPGNValue * 0.1 * 40) ) ;
										
									}
									else if(myUnitsFlags  == 10* 40) // inHg
									{
										myPGNData.push((myPGNValue * 0.0295229* 40) ) ;
										
									}
									else // default isPSI
									{
										myPGNData.push((myPGNValue * 0.0145037738007 * 40) ) ;
										
									}
								}
							}

                           //  Crankcase Pressure LSB 0.0078 kPa/bit -250 kPa offset
                             if(myParameterIndex == 4) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.crankcase_pressure;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags  == 8) // PSI
									{
										myPGNData.push(((myPGNValue * 0.0078) -250) * 0.145037738007 ) ;
									
									}
									else if(myUnitsFlags == 9) // kPa
									{
										myPGNData.push((myPGNValue * 0.1 * 0.0078) - 250 ) ;
										
									}
									else if(myUnitsFlags  == 10) // inHg
									{
										myPGNData.push (((myPGNValue * 0.0078) -250) * 0.295229 ) ;
									
										
									}
									else // default isPSI
									{
										myPGNData.push(((myPGNValue * 0.0078) -250) * 0.145037738007 ) ;
									
									}
								}
							}
							
							// Coolant Pressure 2 kPa/bit       
                             if(myParameterIndex == 5) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.coolant_pressure;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags  == 8) // PSI
									{
										myPGNData.push((myPGNValue * 0.0145037738007 * 20) ) ;
									
									}
									else if(myUnitsFlags == 9) // kPa
									{
										myPGNData.push((myPGNValue * 0.1 * 20) ) ;
									
									}
									else if(myUnitsFlags  == 10) // inHg
									{
										myPGNData.push((myPGNValue * 0.0295229* 20) ) ;
										
									}
									else // default isPSI
									{
										myPGNData.push((myPGNValue * 0.0145037738007 * 20) ) ;
									
									}
								}
							}
							
							// Coolant Leval .4%  kPa/bit      
                             if(myParameterIndex == 6) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.coolant_level;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									myPGNData.push(((myPGNValue * 0.4)));
								}
							}

                          

		}
		
	} // 065263 Array Loop

	return myPGNData;
		

} // end of function GetPGN 065263


// J1939 Engine Temps  PGN 065271 [0x00FEEE] Engine Electrical
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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FEF7")
			{

                                     

                           
							// Net Battery Current (-125 to 125 Amps) 1 Amp/bit
     						if(myParameterIndex == 0) // get temperature
							{
                     			myPGNValue = myN2Kdata[myIndex].payload.battery_current;							
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
						
										myPGNData.push(Math.floor(((myPGNValue ) - 125)));
								}
                             }

							 //  Alternator Current (-125 to 125 Amps) 1 Amp/bit     
                             if(myParameterIndex == 1) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.alternator_current;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
			
										myPGNData.push(Math.floor((((myPGNValue) ) -125)));
								}
							}
                       

                           	// Charging Voltage LSB (0-3212 V) 0.05 V/bit
                             if(myParameterIndex == 2) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.charging_voltage;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
					
										myPGNData.push(((((myPGNValue) * 0.05) )));
								}
							}
                       

                           	//   Battery Voltage LSB (0-3212 V) 0.05 V/bit
                             if(myParameterIndex == 3) // 
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.battery_voltage;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
				
										myPGNData.push(((((myPGNValue) * 0.05) )));
								}
							}
							
                           	//  Keyswitch Voltage LSB (0-3212 V) 0.05 V/bit     
                             if(myParameterIndex == 4) // 
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.keyswitch_voltage;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
			
										myPGNData.push(((((myPGNValue) * 0.05) )));
								}
							}
                        
          
				
		}
		
	} // 065271 Array Loop

	return myPGNData;
		

} // end of function GetPGN 065271

// J1939 PGN 65276 (0x0FEFC) Dash Display
// myParameterIndex = 0  -> Washer Fluid Level (0-100%) 0.4%/bit
// myParameterIndex = 1  -> Fuel Level  (0-100%) 0.4%/bit
// myParameterIndex = 2  -> Fuel Filter Differential Pressure (0-500 kPa) 2 kPA/bit
// myParameterIndex = 3  -> Oil Filter Differential Pressure (0-125 kPa) 0.5 kPA/bit
// myParameterIndex = 4  -> Cargo Ambient Temp MSB (-273 to 1735 deg C) 0.03125 C/bit
// myParameterIndex = 5  -> Fuel Level tank 2 (0-100%) 0.4%/bit

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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FEFC")
			{

                                     

                           
							//  Washer Fluid Level (0-100%) 0.4%/bit
     						if(myParameterIndex == 0) // 
							{
                     			myPGNValue = myN2Kdata[myIndex].payload.washer_level;							
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
						
										myPGNData.push(Math.floor(((myPGNValue * 0.4) )));
								}
                             }

							 //  Fuel Level  (0-100%) 0.4%/bit  
                             if(myParameterIndex == 1) // 
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.fuel1_level;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
			
										myPGNData.push(Math.floor((((myPGNValue) * 0.5 ) )));
								}
							}
                       

                           	// Fuel Filter Differential Pressure (0-500 kPa) 2 kPA/bit
                             if(myParameterIndex == 2) //
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.fuel_filter_differential_pressure;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
					
										myPGNData.push(Math.floor((((myPGNValue) * 2.0) )));
								}
							}
                       

                           	//    Oil Filter Differential Pressure (0-125 kPa) 0.5 kPA/bit
                             if(myParameterIndex == 3) // 
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.oil_filter_differential_pressure;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
				
										myPGNData.push(Math.floor((((myPGNValue) * 0.5) )));
								}
							}
							
                           	//  Cargo Ambient Temp MSB (-273 to 1735 deg C) 0.03125 C/bit    
                             if(myParameterIndex == 4) // 
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.cargo_temperature;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
			
										myPGNData.push(Math.floor((((myPGNValue) * 0.03125) )));
								}
							}
                                 
							//  Fuel Level tank 2 (0-100%) 0.4%/bit 
                             if(myParameterIndex == 5) // 
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.fuel2_level;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
			
										myPGNData.push(Math.floor((((myPGNValue) * 0.4) )));
								}
							}
                        
          
				
		}
		
	} // 065276 Array Loop

	return myPGNData;
		

} // end of function GetPGN 065276

// J1939 PGN 65266 (0x0FEF2) Fuel Economy
// myParameterIndex = 0  -> Fuel Rate LSB 0.05 L/bit
// myParameterIndex = 1  -> Instantaneous Fuel Economy LSB 0.001953125 Km/L
// myParameterIndex = 2  -> Average Fuel Economy LSB 0.001953125 Km/L
// myParameterIndex = 3  -> Throttle Position Actual (0-100%)   0.4%/bit
// myParameterIndex = 4  -> engine demand request torque (0-100%)  0.4%/bit 
//
function GetPGN65266(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FEF2")
			{

                                     

                           
							//  Fuel Rate LSB 0.05 L/bit
     						if(myParameterIndex == 0) // 
							{
                     			myPGNValue = myN2Kdata[myIndex].payload.fuel_rate;							
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
						
										myPGNData.push(Math.floor(((myPGNValue * 0.05) )));
								}
                             }

							 // Instantaneous Fuel Economy LSB 0.001953125 Km/L 
                             if(myParameterIndex == 1) // 
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.instantaneous_fuel_economy;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
			
										myPGNData.push(Math.floor((((myPGNValue) * 0.001953125 ) )));
								}
							}
                       

                           	//  Average Fuel Economy LSB 0.001953125 Km/L
                             if(myParameterIndex == 2) //
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.average_fuel_economy;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
					
										myPGNData.push(Math.floor((((myPGNValue) * 0.001953125) )));
								}
							}
                       

                           	//    Throttle Position Actual (0-100%)   0.4%/bit
                             if(myParameterIndex == 3) // 
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.throttle_position;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
				
										myPGNData.push(Math.floor((((myPGNValue) * 0.4) )));
								}
							}
							
                           	// engine demand request torque (0-100%)  0.4%/bit 
                             if(myParameterIndex == 4) // 
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.demand_torque;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
			
										myPGNData.push(Math.floor((((myPGNValue) * 0.4) )));
								}
							}
                                 
							
                        
          
				
		}
		
	} // 065266 Array Loop

	return myPGNData;
		

} // end of function GetPGN 065266


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
    
    var myPGN;
    var myPGNValue;
	var myInstance;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();


    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F200")
			{

		     myInstance = myN2Kdata[myIndex].payload.engine_id;

				if(myInstance == myPGNInstance) // Outside Temp and Baro
				{                      
                      // field 0 Tachometer
                      if(myParameterIndex == 0)
					  {
					  		myPGNValue =myN2Kdata[myIndex].payload.speed;
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 0.25) ) ;
								myPGNData.push(myHexStr) ;
							}
					  }

					  // get Boost pressure
						if(myParameterIndex == 1)  
						{
							myPGNValue =myN2Kdata[myIndex].payload.boost_presure;
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{

								if((myUnitsFlags) == 8) // PSI
								{
									myHexStr =((myPGNValue * 0.0145037738007) ) ;
									myPGNData.push(myHexStr) ;
								}
								else if((myUnitsFlags ) == 9) // kPa
								{
									myHexStr =((myPGNValue * 0.1) ) ;
									myPGNData.push(myHexStr) ;
								}
								else if((myUnitsFlags) == 10) // inHg
								{
									myHexStr =((myPGNValue * 0.0295229) ) ;
									myPGNData.push(myHexStr) ;
								}
								else // default is PSI
								{
									myHexStr =((myPGNValue * 0.0145037738007) ) ;
									myPGNData.push(myHexStr) ;
								}
							}
						}

					// field 2 Trim
                      if(myParameterIndex == 2)
					  {
					  		myPGNValue =myN2Kdata[myIndex].payload.tilt_or_trim;
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 1) ) ;
								myPGNData.push(myHexStr) ;
							}
					  }
                          
          
			} // Instance match
	
		}
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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F201")
			{

		     myInstance = myN2Kdata[myIndex].payload.engine_id;

				if(myInstance == myPGNInstance) // Instance match
				{                                        
                      // field 0 Oil Pressure
                      if(myParameterIndex == 0)
					  {			  
					  	myPGNValue =myN2Kdata[myIndex].payload.oil_pressure;
					  	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						{
						
							if(myUnitsFlags  == 8) // PSI
							{
								myHexStr =((myPGNValue  * 0.0145037738007) ) ;
								myPGNData.push(myHexStr) ;
							}
							else if(myUnitsFlags == 9) // kPa
							{
								myHexStr =((myPGNValue  * 0.1) ) ;
								myPGNData.push(myHexStr) ;
							}
							else if(myUnitsFlags  == 10) // inHg
							{
								myHexStr =((myPGNValue  * 0.0295229) ) ;
								myPGNData.push(myHexStr) ;
							}
							else // default isPSI
							{
								myHexStr =((myPGNValue  * 0.0145037738007) ) ;
								myPGNData.push(myHexStr) ;
							}
						}
					  }
                           

                      // field 1 Oil Temp
     						if(myParameterIndex == 1) // get temperature
							{
                     			myPGNValue = myN2Kdata[myIndex].payload.oil_temp;							
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags == 1) // degrees C
										myPGNData.push(Math.floor(((myPGNValue * 0.1) - 273)));
									else if(myUnitsFlags  == 2) // degrees Kelvin
										myPGNData.push(Math.floor(((myPGNValue * 0.1) )));
									else // default is degrees F
										myPGNData.push(Math.floor(((myPGNValue * 0.18) - 459)));
								}
                             }

							 // field 2 Engine Temp
                             if(myParameterIndex == 2) // get temperature
							 {
                             	myPGNValue =myN2Kdata[myIndex].payload.engine_temp;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 	{
									if(myUnitsFlags  == 1) // degrees C
										myPGNData.push(Math.floor(((myPGNValue * 0.01) - 273)));
									else if(myUnitsFlags  == 2) // degrees Kelvin
										myPGNData.push(Math.floor(((myPGNValue * 0.01) )));
									else // default is degrees F
										myPGNData.push(Math.floor(((myPGNValue * 0.018) - 459)));
								}
							}
                       

                             // field 3 Alternator Volts


							 if(myParameterIndex == 3) // get Voltage
							 {
							 	myPGNValue =myN2Kdata[myIndex].payload.alternator_potential;							 
							 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
								myPGNData.push(((myPGNValue * 0.01)));
							 }
                            
 
                             // field 4 Fuel Rate
							 if(myParameterIndex == 4) // get Fuel Rate
							 {
								myPGNValue =myN2Kdata[myIndex].payload.fuel_rate;	
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)						 
								myPGNData.push(((myPGNValue * 0.0264)));
                             }
                   
                             // field 5 Engine Hours
                        	if(myParameterIndex == 5) // get hour meter
							{     					
									myPGNValue =myN2Kdata[myIndex].payload.total_engine_hours;
 									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
 									{
			                             if (myPGNValue == parseInt("0x7FFFFFFF")) 
										 {
			
			                             }
			                             else 
										 {
			                                 	var vGHour = Math.floor(myPGNValue / 3600);
			                                 	var vGMin = myPGNValue - vGHour * 3600;
			                                 	vGMin = Math.floor(vGMin / 60);
								
												myPGNData.push(vGHour + "." + vGMin);
										}
									}
                                 
                             }

							// field Coolant pressure
							if(myParameterIndex == 6)  // get coolant pressure
							{
								myPGNValue =myN2Kdata[myIndex].payload.coolant_pressure;							
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
								{

									if(myUnitsFlags  == 8) // PSI
									{
										myHexStr =(myPGNValue * 0.0145037738007)  ;
										myPGNData.push(myHexStr) ;
									}
									else if(myUnitsFlags == 9) // kPa
									{
										myHexStr =((myPGNValue * 0.1) ) ;
										myPGNData.push(myHexStr) ;
									}
									else if(myUnitsFlags  == 10) // inHg
									{
										myHexStr =((myPGNValue * 0.0295229) ) ;
										myPGNData.push(myHexStr) ;
									}
									else // default is PSI
									{
										myHexStr =(myPGNValue * 0.0145037738007)  ;
										myPGNData.push(myHexStr) ;
									}
								}
							 }



                             // field 7
							if(myParameterIndex == 7)  // get fuel pressure
							{
								myPGNValue =myN2Kdata[myIndex].payload.fuel_pressure;							
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
								{
									if(myUnitsFlags == 8) // PSI
									{
										myHexStr =((myPGNValue * 0.145037738007) ) ;
										myPGNData.push(myHexStr) ;
									}
									else if(myUnitsFlags  == 9) // kPa
									{
										myHexStr =((myPGNValue * 1) ) ;
										myPGNData.push(myHexStr) ;
									}
									else if(myUnitsFlags  == 10) // inHg
									{
										myHexStr =((myPGNValue * 0.295229) ) ;
										myPGNData.push(myHexStr) ;
									}
									else // default is PSI
									{
										myHexStr =((myPGNValue * 0.145037738007) ) ;
										myPGNData.push(myHexStr) ;
									}
								}
							 }

                          
          
				 } // Instance match
		}
		
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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F205")
			{

		     myInstance = myN2Kdata[myIndex].payload.instance;

				if(myInstance == myPGNInstance) // Instance match
				{                                        
                    
                      // field 1 Oil Pressure
                      if(myParameterIndex == 0)
					  {
						 myPGNValue =myN2Kdata[myIndex].payload.oil_pressure;	
						if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
						{			  
							if(myUnitsFlags  == 8) // PSI
							{
								//myHexStr =((myPGNValue * 0.0145037738007) ) ;
								myHexStr =((myPGNValue * 0.145037738007) ) ;
								myPGNData.push(myHexStr) ;
							}
							else if(myUnitsFlags == 9) // kPa
							{
								//myHexStr =((myPGNValue * 0.1) ) ;
								myHexStr =((myPGNValue * 1) ) ;
								myPGNData.push(myHexStr) ;
							}
							else if(myUnitsFlags  == 10) // inHg
							{
								//myHexStr =((myPGNValue * 0.0295229) ) ;
								myHexStr =((myPGNValue * 0.295229) ) ;
								myPGNData.push(myHexStr) ;
							}
							else // default is kPa
							{
								myHexStr =((myPGNValue * 1) ) ;
								myPGNData.push(myHexStr) ;
							}
						}

					  }
                           

                      // field 1 Oil Temp
						if(myParameterIndex == 1) // get temperature
						{
					 		myPGNValue =myN2Kdata[myIndex].payload.oil_temp;								
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
							{				
								if(myUnitsFlags == 1) // degrees C
									myPGNData.push(Math.floor(((myPGNValue * 0.1) - 273)));
								else if(myUnitsFlags  == 2) // degrees Kelvin
									myPGNData.push(Math.floor(((myPGNValue * 0.1) )));
								else // default is degrees F
									myPGNData.push(Math.floor(((myPGNValue * 0.18) - 459)));
								
							}
                         }

							 
           
                          
          
        } // Instance match
	  } // good checksum
	} // 127493 Array Loop

	return myPGNData;
		
} // end of function GetPGN 127493



// Ststus Parameters
// PGN 127497 [0x01F209] Trip Parameters, Engine
// myPGNINstance = Instance and type
// Type = myPGNINstance & 0x0F
// Instance = myPGNINstance & 0xF0
// myParameterIndex = 0  -> Trip fuel used
// myParameterIndex = 1  -> Fuel Rate, Average
// myParameterIndex = 2  -> Fuel Rate, Economy
// myParameterIndex = 3  -> Instantaneous Fuel Economy
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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F209")
			{

		     myInstance = myN2Kdata[myIndex].payload.instance;

				if(myInstance == myPGNInstance) // Instance match
				{                           

                      // field 0 Trip fuel used
                      if(myParameterIndex == 0) //Trip fuel used
					  {
	 					 	myPGNValue =myN2Kdata[myIndex].payload.trip_fuel_used;				  
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								if(myUnitsFlags == 20) // liters/hr
									myPGNData.push(Math.floor(((myPGNValue * 1.0) )));
								else if(myUnitsFlags  == 21) // gallons/hr
									myPGNData.push((((myPGNValue * 0.264172) )));
								else // default is cubic meters/hr
									myPGNData.push((((myPGNValue * .001) )));
							}
					  }
						
                      // field 1 Fuel Rate, Average
						if(myParameterIndex == 1)  // get Fuel Rate, Average
						{
					 		myPGNValue =myN2Kdata[myIndex].payload.fuel_rate_average;
						
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								if(myUnitsFlags == 19) // liters/hr
									myPGNData.push(Math.floor(((myPGNValue * 0.1) )));
								else if(myUnitsFlags  == 18) // gallons/hr
									myPGNData.push((((myPGNValue * 0.0264172) )));
								else // default is cubic meters/hr
									myPGNData.push((((myPGNValue * .0001) )));
							}
						}

					 // field 2  Fuel Rate, Economy
                       if(myParameterIndex == 2) // get Fuel Rate, Economy
						{
	 					 	myPGNValue =myN2Kdata[myIndex].payload.fuel_rate_economy;					
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								if(myUnitsFlags == 19) // liters/hr
									myPGNData.push(Math.floor(((myPGNValue * 0.1) )));
								else if(myUnitsFlags  == 18) // gallons/hr
									myPGNData.push((((myPGNValue * 0.0264172) )));
								else // default is cubic meters/hr
									myPGNData.push((((myPGNValue * .0001) )));
							}
						}
                          
						// field 3  Instantaneous Fuel Economy
                       if(myParameterIndex == 3) // get Instantaneous Fuel Economy
						{
	 					 	myPGNValue =myN2Kdata[myIndex].payload.instantaneous_fuel_economy;					
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								if(myUnitsFlags == 19) // liters/hr
									myPGNData.push(Math.floor(((myPGNValue * 0.1) )));
								else if(myUnitsFlags  == 18) // gallons/hr
									myPGNData.push((((myPGNValue * 0.0264172) )));
								else // default is cubic meters/hr
									myPGNData.push((((myPGNValue * .0001) )));
							}
						}
          
        } // Instance match
	  } // good checksum
	} // 127497 Array Loop

	return myPGNData;

} // end of function GetPGN 127508








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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F211")
			{

		     //myInstance = myN2Kdata[myIndex].payload.instance + (myN2Kdata[myIndex].payload.type << 4);
			  myInstance = myN2Kdata[myIndex].payload.instance;

				if(myInstance == myPGNInstance) // Instance match
				{                          

                      // field 0 Fluid Level
                      if(myParameterIndex ==  myN2Kdata[myIndex].payload.type)
					  {
					 		myPGNValue =myN2Kdata[myIndex].payload.level;					  
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 0.004) ) ;
								myPGNData.push(myHexStr) ;
							}
					  }
						/*
                            // field 1
							if(myParameterIndex == 1)  // get Capacity
							{
					 			myPGNValue =myN2Kdata[myIndex].payload.tank_capacity;							
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								{
									if(myUnitsFlags  == 20) // liters
									{
										myHexStr =((myPGNValue * 0.1) ) ;
										myPGNData.push(myHexStr) ;
									}
									else if(myUnitsFlags  == 21) // gallons
									{
										myHexStr =((myPGNValue * 0.0264172) ) ;
										myPGNData.push(myHexStr) ;
									}
									else if(myUnitsFlags  == 22) // cubic meters
									{
										myHexStr =((myPGNValue * 0.0001) ) ;
										myPGNData.push(myHexStr) ;
									}
									else // default is liters
									{
										myHexStr =((myPGNValue * 0.1) ) ;
										myPGNData.push(myHexStr) ;
									}
								}
							 }
*/
					
                          
          
        } // Instance match
	  } // good checksum
	} // 127505 Array Loop

	return myPGNData;

} // end of function GetPGN 127505


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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F214")
			{
 
		     myInstance = myN2Kdata[myIndex].payload.instance;

				if(myInstance == parseInt(myPGNInstance)) // Instance match
				{                           

                      // field 0 Voltage
                      if(myParameterIndex == 0)
					  {
	 					 	myPGNValue =myN2Kdata[myIndex].payload.voltage;				  
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 0.01) ) ;
								myPGNData.push(myHexStr) ;
							}
					  }
						
                      // field 1 Current
						if(myParameterIndex == 1)  // get Current
						{
					 		myPGNValue =myN2Kdata[myIndex].payload.current;
						
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 0.1).toFixed(1) ) ;
								myPGNData.push(myHexStr) ;
							}
						}

					 // field 2  Temp
                       if(myParameterIndex == 2) // get temperature
						{
	 					 	myPGNValue =myN2Kdata[myIndex].payload.temperature;					
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								if(myUnitsFlags == 1) // degrees C
									myPGNData.push(Math.floor(((myPGNValue * 0.01) - 273)));
								else if(myUnitsFlags  == 2) // degrees Kelvin
									myPGNData.push(Math.floor(((myPGNValue * 0.01) )));
								else // default is degrees F
									myPGNData.push(Math.floor(((myPGNValue * 0.018) - 459)));
							}
						}
                          
          
        } // Instance match
	  } // good checksum
	} // 127508 Array Loop

	return myPGNData;

} // end of function GetPGN 127508


// Ststus Parameters
// PGN 127506 [0x01F213] Battery Status
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
 

    myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F212")
			{
 
		     myInstance = myN2Kdata[myIndex].payload.instance;

				if(myInstance == parseInt(myPGNInstance)) // Instance match
				{                           

                     
						
                      // field 1 stateofcharge
						if(myParameterIndex == 0)  // get stateofcharge
						{
					 		myPGNValue =myN2Kdata[myIndex].payload.stateofcharge;
						
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 1.0).toFixed(1) ) ;
								myPGNData.push(myHexStr) ;
							}
						}
						
						// field 1 stateofhealth
						if(myParameterIndex == 1)  // get stateofhealth
						{
					 		myPGNValue =myN2Kdata[myIndex].payload.stateofhealth;
						
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 1.0).toFixed(1) ) ;
								myPGNData.push(myHexStr) ;
							}
						}
						
						
						// field 1 timeremaining
						if(myParameterIndex == 2)  // get timeremaining
						{
					 		myPGNValue =myN2Kdata[myIndex].payload.timeremaining;
						
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 1.0).toFixed(1) ) ;
								myPGNData.push(myHexStr) ;
							}
						}

					// field 1 ripplevoltage
						if(myParameterIndex == 3)  // get ripplevoltage
						{
					 		myPGNValue =myN2Kdata[myIndex].payload.ripplevoltage;
						
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								myHexStr =((myPGNValue * 1.0).toFixed(1) ) ;
								myPGNData.push(myHexStr) ;
							}
						}
                          
          
        } // Instance match
	  } // good checksum
	} // 127506 Array Loop

	return myPGNData;

} // end of function GetPGN 127506

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
 

   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01FD07")
			{

		     myInstanceString = myN2Kdata[myIndex].payload.temperature_instance;

			switch( myInstanceString ) {
				case "Sea Temperature":
					myInstance = 0;
					break;

				case "Outside Temperature":
					myInstance = 1;
					break;

				case "Inside Temperature":
					myInstance = 2;
					break;

				case "Engine Room Temperature":
					myInstance = 3;
					break;

				case "Main Cabin Temperature":
					myInstance = 4;
					break;

				case "Reserved":
					myInstance = 5;
					break;
					
					
				case "Inside Zone0":
					myInstance = 16;
					break;
					
				case "Inside Zone1":
					myInstance = 17;
					break;
										
				case "Inside Zone2":
					myInstance = 18;
					break;
										
				case "Inside Zone3":
					myInstance = 19;
					break;
										
				case "Inside Zone4":
					myInstance = 20;
					break;
										
				case "Inside Zone5":
					myInstance = 21;
					break;
										
				case "Inside Zone6":
					myInstance = 22;
					break;
										
				case "Inside Zone7":
					myInstance = 23;
					break;
										
										
					

				case "No Data":
					myInstance = 255;
					break;

				default:
					myInstance = 15;
					break;
			}

			
				if(myInstance  == myPGNInstance) // Outside Temp and Baro
				{    
				      
					 if(myParameterIndex == 2) // get baro pressure
					  {   
					  
						myPGNValue =myN2Kdata[myIndex].payload.atmospheric_pressure;
					 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						{
					 
							if(myUnitsFlags  == 8) // PSI
							{
								myHexStr =((myPGNValue * 0.145037738007) ) ;
								myPGNData.push(myHexStr) ;
							}
							else if(myUnitsFlags  == 9) // kPa
							{
								myHexStr =((myPGNValue * 1) ) ;
								myPGNData.push(myHexStr) ;
							}
							else if(myUnitsFlags  == 10) // inHg
							{
								myHexStr =((myPGNValue * 0.295229) ) ;
								myPGNData.push(myHexStr) ;
							}
							else // default is PSI
							{
								myHexStr =((myPGNValue * 0.145037738007) ) ;
								myPGNData.push(myHexStr) ;
							}

					  	}
		    
					 }





					 if(myParameterIndex == 1) // get Humidity %
					 {
					 	myPGNValue =myN2Kdata[myIndex].payload.humidity;	
					 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							myPGNData.push(Math.floor(((myPGNValue))));
					}
          


					 if(myParameterIndex == 0) // get temperature
					 {
						// get temperature
					 	myPGNValue =myN2Kdata[myIndex].payload.temperature;
				 
					 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						{
							if(myUnitsFlags  == 1) // degrees C
								myPGNData.push(Math.floor(((myPGNValue * 1) - 273)));
							else if(myUnitsFlags  == 2) // degrees Kelvin
								myPGNData.push(Math.floor(((myPGNValue * 1) )));
							else // default is degrees F
								myPGNData.push(Math.floor(((myPGNValue * 1.8) - 459)));
						}
					}
          
			} // Outside temp and baro
		} // good checksum
	} // 130311 Array Loop

	return myPGNData;
		//return "this is a test";

} // end of function GetPGN 130311

// Weather station data
// PGN 130312 [0x01FD08] Environmential Parameters
// myParameterIndex = 0  -> Actual Temp
// myParameterIndex = 1  -> Set Temp

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
	var myInstanceString;
   	var myParameterString;
   	var myParameter;
   	
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01FD08")
			{

		     	myInstanceString = myN2Kdata[myIndex].payload.temperature_instance;
		     	if(myInstanceString == myPGNInstance)
				{
				
					myParameterString = myN2Kdata[myIndex].payload.temperature_source;

					switch( myParameterString) {
						case "Sea Temperature":
							myParameter  = 0;
							break;
		
						case "Outside Temperature":
							myParameter  = 1;
							break;
		
						case "Inside Temperature":
							myParameter  = 2;
							break;
		
						case "Engine Room Temperature":
							myParameter  = 3;
							break;
		
						case "Main Cabin Temperature":
							myParameter  = 4;
							break;
		
						case "Live Well":
							myParameter  = 5;
							break;
		
						case "Bait Well":
							myParameter  =6;
							break;
							
						case "Refrigeration":
							myParameter  = 7;
							break;
		
						case "Heating":
							myParameter  = 8;
							break;
		
						case "Dew Point":
							myParameter  = 9;
							break;
		
						case "Wind Chill A":
							myParameter  = 10;
							break;
		
						case "Wind Chill T":
							myParameter  = 11;
							break;
		
						case "Heat Index":
							myParameter  = 12;
							break;
		
						case "Freezer":
							myParameter  =13;
							break;
							
						//case "Reserved":
						//	myInstance = 14;
						//	break;
		
						case "Reserved":
							myParameter  =15;
							break;
		
						case "Reserved 128":
							myParameter  =128;
							break;
		
						case "Reserved 129":
							myParameter  =129;
							break;
		
						case "Reserved 130":
							myParameter  =130;
							break;
		
						case "Reserved 131":
							myParameter  =131;
							break;
		
						case "Reserved 132":
							myParameter  =132;
							break;
		
						case "Reserved 133":
							myParameter  =133;
							break;
		
						case "Reserved 134":
							myParameter  =134;
							break;
		
						case "Reserved 135":
							myParameter  =135;
							break;
		
						case "Reserved 136":
							myParameter  =136;
							break;
		
						case "Reserved 137":
							myParameter  =137;
							break;
		
						case "Reserved 138":
							myParameter  =138;
							break;
		
						case "Reserved 139":
							myParameter  =139;
							break;
		
						case "Error":
							myParameter  =254;
							break;
		
						case "No Data":
							myParameter  =255;
							break;
		
			
		
						default:
							myParameter  = 255;
							break;
					}

			
					if(myParameter  == myParameterIndex) // Outside Temp and Baro
					{    
							// get temperature
						 	myPGNValue =myN2Kdata[myIndex].payload.actual_temperature;
					 
						 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								if(myUnitsFlags  == 1) // degrees C
									myPGNData.push(Math.floor(((myPGNValue * 1) - 273)));
								else if(myUnitsFlags  == 2) // degrees Kelvin
									myPGNData.push(Math.floor(((myPGNValue * 1) )));
								else // default is degrees F
									myPGNData.push(Math.floor(((myPGNValue * 1.8) - 459)));
							}
					}
					
					
          		} // parameter match
			} // Instance match
		} // 130312 Array Loop

	return myPGNData;
		//return "this is a test";

} // end of function GetPGN 130312


// Weather station data
// PGN 130312 [0x01FD08] Environmential Parameters
// myParameterIndex = 0  -> Actual Temp
// myParameterIndex = 1  -> Set Temp

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
	var myInstanceString;
   	var myParameterString;
   	var myParameter;
   	
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 

   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01FD0C")
			{

		     	myInstanceString = myN2Kdata[myIndex].payload.temperature_instance;
		     	if(myInstanceString == myPGNInstance)
				{
				
					myParameterString = myN2Kdata[myIndex].payload.temperature_source;

					switch( myParameterString) {
						case "Sea Temperature":
							myParameter  = 0;
							break;
		
						case "Outside Temperature":
							myParameter  = 1;
							break;
		
						case "Inside Temperature":
							myParameter  = 2;
							break;
		
						case "Engine Room Temperature":
							myParameter  = 3;
							break;
		
						case "Main Cabin Temperature":
							myParameter  = 4;
							break;
		
						case "Live Well":
							myParameter  = 5;
							break;
		
						case "Bait Well":
							myParameter  =6;
							break;
							
						case "Refrigeration":
							myParameter  = 7;
							break;
		
						case "Heating":
							myParameter  = 8;
							break;
		
						case "Dew Point":
							myParameter  = 9;
							break;
		
						case "Wind Chill A":
							myParameter  = 10;
							break;
		
						case "Wind Chill T":
							myParameter  = 11;
							break;
		
						case "Heat Index":
							myParameter  = 12;
							break;
		
						case "Freezer":
							myParameter  =13;
							break;
							
						case "EGT":
							myParameter  =14;
							break;
		
						case "Reserved":
							myParameter  =15;
							break;
		

		
						case "Error":
							myParameter  =254;
							break;
		
						case "No Data":
							myParameter  =255;
							break;
		
			
		
						default:
							myParameter  = 255;
							break;
					}

			
					if(myParameter  == myParameterIndex) // Outside Temp and Baro
					{    
							// get temperature
						 	myPGNValue =myN2Kdata[myIndex].payload.actual_temperature;
					 
						 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								if(myUnitsFlags  == 1) // degrees C
									myPGNData.push(Math.floor(((myPGNValue * 1) - 273)));
								else if(myUnitsFlags  == 2) // degrees Kelvin
									myPGNData.push(Math.floor(((myPGNValue * 1) )));
								else // default is degrees F
									myPGNData.push(Math.floor(((myPGNValue * 1.8) - 459)));
							}
					}
					
					
          		} // parameter match
			} // Instance match
		} // 130316 Array Loop

	return myPGNData;
		//return "this is a test";

} // end of function GetPGN 130316
// Weather station data
// PGN 130312 [0x01FD08] Environmential Parameters
// myParameterIndex = 0  -> Temperature
// myParameterIndex = 1  -> Set Temperature

// myUnitsFlags = 0  -> Degrees F
// myUnitsFlags = 1  -> Degrees C
//
/*
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
 

	mySubStrings = myN2Kdata.split("$PCDIN,01FD08,");

    myArrayLength = mySubStrings.length;



      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
             myHexStr = mySubStrings[myIndex];

	  	 // look for checksum character in the correct place or skip 
			if(myHexStr.substr(28 ,1) == '*')
			{

			 myHexStr = "0x" + myHexStr.substr((21-7) ,2) ;

		     myInstance = parseInt(myHexStr);
				
				if(myInstance == myPGNInstance) // 
				{                      
				  myHexStr = mySubStrings[myIndex];
				  myHexStr = "0x" + myHexStr.substr((23-7) ,2) ;
				  myTempRef = parseInt(myHexStr);

					myTempRef = parseInt(myHexStr);
					// Get Temperature Reference
					// 0 = Sea emp
					// 1 = Outside Temp
					// 2 = Inside Temp
					// 3 = Engine Room Temp
					// 4 = Main Cabin Temp
          
					// get temperature
					myHexStr = mySubStrings[myIndex];
					myHexStr = "0x" + myHexStr.substr((27-7),2) + myHexStr.substr((25-7),2) ;
					myPGNValue = parseInt(myHexStr);

					 if(myParameterIndex == myTempRef) // get temperature
					 {
						if(myUnitsFlags  == 1) // degrees C
							myPGNData.push(Math.floor(((myPGNValue * 0.01) - 273)));
						else if(myUnitsFlags  == 2) // degrees Kelvin
							myPGNData.push(Math.floor(((myPGNValue * 0.01) )));
						else // default is degrees F
							myPGNData.push(Math.floor(((myPGNValue * 0.018) - 459)));
					
					} // Temperature
			} // good instance
		} // good checksum
	} // 130312 Array Loop

	return myPGNData;
		//return "this is a test";

} // end of function GetPGN 130312

*/

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
 



   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01FD13")
			{

		  		    myInstanceString = myN2Kdata[myIndex].payload.wind_reference;

					switch( myInstanceString )
					{
						case "TWIND True North":
							myWindRef = 0;
							break;
		
						case "TWIND Mag North":
							myWindRef = 1;
							break;
		
						case "Apparent Wind":
							myWindRef = 2;
							break;
		
						case "TWIND VCGR":
							myWindRef = 3;
							break;
		
						case "TWIND VCWR":
							myWindRef = 4;
							break;
		
						case "Reserved":
							myWindRef = 5;
							break;
		
						case "Error":
							myWindRef = 6;
							break;
		
						case "NULL":
							myWindRef = 7;
							break;
		
						default:
							myWindRef = 15;
							break;
						}

			
					 				
				if(((myWindRef & 0x0007) == myPGNInstance) || ( myPGNInstance == 8))// Use Reference
				{          
                    
			
      
				
					  if(myParameterIndex == 5) // Wind Direction
					  {
					 		myPGNValue =myN2Kdata[myIndex].payload.wind_direction;
					 		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{

							  	myDegreesMagN = Math.floor(myPGNValue * 1); // converted to degrees
								if(myDegreesMagN >= 360)
									myDegreesMagN = myDegreesMagN - 360;	
							 
								if(myPGNInstance == 8)
								{
									if((myWindRef & 0x0007) == 0) // Wind ref to True North
										myPGNData.push(myDegreesMagN + ":T") ;
									else if((myWindRef & 0x0007) == 1) // Wind ref to Mag North
										myPGNData.push(myDegreesMagN + ":M") ;
									else if((myWindRef & 0x0007) == 2) // Wind ref to Apparent
										myPGNData.push(myDegreesMagN + ":A") ;	
								}
								else
								{
									//alert(myDegreesMagN);
									myPGNData.push(myDegreesMagN);
								}
					 		 }
					  }
		    
				
					 // get Wind Speed											
					   if(myParameterIndex == 4) // Wind Speed
					   {
					  		myPGNValue =myN2Kdata[myIndex].payload.wind_speed; 
					  		if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								  if(myUnitsFlags  == 4) // Knots
									myPGNValue  = myPGNValue * 1.94384449 * 1; // converted to Knots
								  else if(myUnitsFlags  == 5) // MPH
									myPGNValue  = myPGNValue * 2.23694 * 1; // converted to MPH
								  else if(myUnitsFlags  == 6) // KPH
									myPGNValue  = myPGNValue * 3.6 * 1; // converted to KPH									
								  else if(myUnitsFlags  == 7) // KPH
									myPGNValue  = myPGNValue * 1.0 * 1; // converted to KPH
								  else //  default knots
									myPGNValue  = myPGNValue * 1.94384449 * 1; // converted to Knots
		
								if(myPGNInstance == 8)
								{
									if((myWindRef & 0x0007) == 0) // Speed ref to True North
										myPGNData.push(myPGNValue + ":T") ;
									else if((myWindRef & 0x0007) == 1) // Speed ref to Mag North
										myPGNData.push(myPGNValue + ":M") ;
									else if((myWindRef & 0x0007) == 2) // Speed ref to Apparent
										myPGNData.push(myPGNValue + ":A") ;
								}
								else
									myPGNData.push(myPGNValue);
							}
					}   
					

					  if(myParameterIndex == 7) // get baro pressure
					  {   
					  
						myPGNValue =myN2Kdata[myIndex].payload.atmospheric_pressure;
					 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						{
					 
							if(myUnitsFlags  == 8) // PSI
							{
								myHexStr =((myPGNValue * 0.145037738007) ) ;
								myPGNData.push(myHexStr) ;
							}
							else if(myUnitsFlags  == 9) // kPa
							{
								myHexStr =((myPGNValue * 1) ) ;
								myPGNData.push(myHexStr) ;
							}
							else if(myUnitsFlags  == 10) // inHg
							{
								myHexStr =((myPGNValue * 0.295229) ) ;
								myPGNData.push(myHexStr) ;
							}
							else // default is PSI
							{
								myHexStr =((myPGNValue * 0.145037738007) ) ;
								myPGNData.push(myHexStr) ;
							}

					  	}
		    
					 }



          


					 if(myParameterIndex == 8) // get temperature
					 {
						// get temperature
					 	myPGNValue =myN2Kdata[myIndex].payload.temperature;
				 
					 	if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						{
							if(myUnitsFlags  == 1) // degrees C
								myPGNData.push(Math.floor(((myPGNValue * 1) - 273)));
							else if(myUnitsFlags  == 2) // degrees Kelvin
								myPGNData.push(Math.floor(((myPGNValue * 1) )));
							else // default is degrees F
								myPGNData.push(Math.floor(((myPGNValue * 1.8) - 459)));
						}
					}



  
				} // Wind Reference
		} // 130323 PGN match
	} // 130323 Array Loop
	
	return myPGNData;

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

  myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F112")
			{

		     myInstanceString = myN2Kdata[myIndex].payload.heading_reference;
			
			switch( myInstanceString ) {
				case "True":
					myWindRef = 0;
				break;
				case "Magnetic":
					myWindRef = 1;
				break;
				default:
					myWindRef = 15;
				break;
				}

			
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
					
					  		myPGNValue = myN2Kdata[myIndex].payload.heading;// converted to degrees
	
				
		 					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						 	myPGNData.push(Math.floor(myPGNValue)) ;
						 
					  }
		    
				
					    if(myParameterIndex == 1) // deviation
					   {
						  
					     	myPGNValue = myN2Kdata[myIndex].payload.deviation;// converted to degrees
				
			 				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							 myPGNData.push(Math.floor(myPGNValue)) ;
					   }

          
	
					     if(myParameterIndex == 2)
					   {

						    myPGNValue = myN2Kdata[myIndex].payload.variation;// converted to degrees
						
			 				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)						
						 	myPGNData.push(Math.floor(myPGNValue)) ;
					   }

				
          
			} // Magnetic Fix
		} //good checksum
	} // 127250 Array Loop

	//alert(myPGNData.pop());
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

	var windSpeedMin = 0;
	var windSpeedMax = 0;
	var windSpeedGust = 0;
	
	
   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01FD02")
			{

		     myInstanceString = myN2Kdata[myIndex].payload.wind_reference;

			switch( myInstanceString ) {
				case "TWIND True North":
					myWindRef = 0;
					break;

				case "TWIND Mag North":
					myWindRef = 1;
					break;

				case "Apparent Wind":
					myWindRef = 2;
					break;

				case "TWIND VCGR":
					myWindRef = 3;
					break;

				case "TWIND VCWR":
					myWindRef = 4;
					break;

				case "Gust":
					myWindRef = 5;
					break;

				case "Error":
					myWindRef = 6;
					break;

				case "NULL":
					myWindRef = 7;
					break;

				default:
					myWindRef = 15;
					break;
			}

			
					 				
				if(((myWindRef & 0x0007) == myPGNInstance) || ( myPGNInstance == 8))// Use Reference
				{          
                    
					myPGNValue =myN2Kdata[myIndex].payload.wind_direction;
          			if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
					{
							if(myPGNValue == 65535)
							{
								
							} // invalid value
							else
							{
							   myDegreesMagN = Math.floor(myPGNValue * 1); // converted to degrees
								if(myDegreesMagN >= 360)
									myDegreesMagN = myDegreesMagN - 360;
		
							  if(myParameterIndex == 1) // Wind Direction
							  {
							 // alert(myPGNInstance);
								if(myPGNInstance == 8)
								{
									if((myWindRef & 0x0007) == 0) // Wind ref to True North
										myPGNData.push(myDegreesMagN + ":T") ;
									else if((myWindRef & 0x0007) == 1) // Wind ref to Mag North
										myPGNData.push(myDegreesMagN + ":M") ;
									else if((myWindRef & 0x0007) == 2) // Wind ref to Apparent
										myPGNData.push(myDegreesMagN + ":A") ;
		
										
		
								}
								else
								{
									//alert(myDegreesMagN);
									myPGNData.push(myDegreesMagN);
								}
							  }
				    
							} // valid value
					}
					 // get Wind Speed
					myPGNValue =myN2Kdata[myIndex].payload.wind_speed;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
					{

							if(myPGNValue == 65535)
							{
								
							}
							else
							{
														//A wind "gust" is also reported when the peak "instantaneous" wind during the most recent ten-minutes prior to the observation is more than 10 knots //greater than the lowest "lull" in the wind during that time. If that is the case, the highest instantaneous wind during that ten minute window is //reported as the gust value
											//
											//Is a sudden, brief increase in speed of the wind. According to U.S. weather observing practice, gusts are reported when the peak wind speed reaches //at least 16 knots and the variation in wind speed between the peaks and lulls is at least 9 knots. The duration of a gust is usually less than 20 //seconds
											

											
											if(myParameterIndex == 2) // Wind Gust Caluclated
											{
												
												WindGustArray[gustIndex++] = myPGNValue;
												if (gustIndex >= 32)
													gustIndex = 0;				
												
												 windSpeedMin = 99999;
												 windSpeedMax = 0;
												 windSpeedGust = 0;
												
												for(var i=0; i<32; i++)
												{
													
													if ( WindGustArray[i] <= windSpeedMin)
													windSpeedMin = WindGustArray[i];
													
													if ( WindGustArray[i] >= windSpeedMax)
													windSpeedMax = WindGustArray[i];
													
													
													
												}
												
												if(((windSpeedMax - windSpeedMin) * ( 1.94384449 * .01)) > 2)
													windSpeedGust = windSpeedMax;
												
											
											if(myUnitsFlags  == 4) // Knots
												myPGNValue  = windSpeedGust * 1.94384449 * .01; // converted to Knots
											  else if(myUnitsFlags  == 5) // MPH
												myPGNValue  = windSpeedGust * 2.23694 * .01; // converted to MPH
											  else if(myUnitsFlags  == 6) // KPH
												myPGNValue  = windSpeedGust * 3.6 * .01; // converted to KPH
											 else if(myUnitsFlags  == 7) // KPH
												myPGNValue  = windSpeedGust * 1.0 * .01; // converted to KPH
											  else //  default knots
												myPGNValue  = windSpeedGust * 1.94384449 * .01; // converted to Knots
											
											myPGNData.push(myPGNValue);
											
											}
						
							    if(myParameterIndex == 0) // Wind Speed
							   {
								  if(myUnitsFlags  == 4) // Knots
									myPGNValue  = myPGNValue * 1.94384449 * .01; // converted to Knots
								  else if(myUnitsFlags  == 5) // MPH
									myPGNValue  = myPGNValue * 2.23694 * .01; // converted to MPH
								  else if(myUnitsFlags  == 6) // KPH
									myPGNValue  = myPGNValue * 3.6 * 1; // converted to KPH									
									
								  else if(myUnitsFlags  == 7) // KPH
									myPGNValue  = myPGNValue * 1.0 * .01; // converted to KPH
								  else //  default knots
									myPGNValue  = myPGNValue * 1.94384449 * 1; // converted to Knots
		
								if(myPGNInstance == 8)
								{
									if((myWindRef & 0x0007) == 0) // Speed ref to True North
										myPGNData.push(myPGNValue + ":T") ;
									else if((myWindRef & 0x0007) == 1) // Speed ref to Mag North
										myPGNData.push(myPGNValue + ":M") ;
									else if((myWindRef & 0x0007) == 2) // Speed ref to Apparent
										myPGNData.push(myPGNValue + ":A") ;
								}
								else
									myPGNData.push(myPGNValue);
								     
							   }
						}
					}
          
			} // Wind Reference
		} // good checksum
	} // 130306 Array Loop

	return myPGNData;

} // end of function GetPGN 130306
     


// Rain Gauge
// PGN 130946 [0x01FF82] Vesel Attitude
// myParameterIndex = 0  -> accumulation
// myParameterIndex = 1  -> duration
// myParameterIndex = 2  -> rate
// myParameterIndex = 3  -> peak rate
//
function GetPGN130946(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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
 


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01FF82")
			{	      

		// check it is a SeaSmart dimmer PGN E199
			    if(myN2Kdata[myIndex].payload.pgntype == 39393)
				{
		


					if(myParameterIndex == 0) // accumulation
					{
						myPGNValue = myN2Kdata[myIndex].payload.rainaccum;
						
						if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
						{
								if(myUnitsFlags  == 44) // mm
									myPGNValue  = myPGNValue * 1.0; // converted to mm
								  else if(myUnitsFlags  == 45) // inches
									myPGNValue  = myPGNValue * 0.039370; // converted to inches
								  else //  default meters
									myPGNValue  = myPGNValue * 0.001; // converted to meters
									
							myPGNData.push(myPGNValue) ;									
						}
					}
				
					if(myParameterIndex == 1) // duration
					{
						myPGNValue = myN2Kdata[myIndex].payload.rainduration;
						
						if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
						{
								
							myPGNValue  = myPGNValue * 1.0; // converted to sec
								 
									
							myPGNData.push(myPGNValue) ;									
						}
					}

					 if(myParameterIndex == 2) // rate
					 {
						myPGNValue = myN2Kdata[myIndex].payload.rainrate;
						
						if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
						{
								if(myUnitsFlags  == 44) // mm
									myPGNValue  = myPGNValue * 1.0; // converted to mm
								  else if(myUnitsFlags  == 45) // inches
									myPGNValue  = myPGNValue * 0.039370; // converted to inches
								  else //  default meters
									myPGNValue  = myPGNValue * 0.001; // converted to meters
									
							myPGNData.push(myPGNValue) ;									
						}					}
					
					 if(myParameterIndex == 3) // peak rate
					 {
						myPGNValue = myN2Kdata[myIndex].payload.rainpeak;
						
						if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
						{
								if(myUnitsFlags  == 44) // mm
									myPGNValue  = myPGNValue * 1.0; // converted to mm
								  else if(myUnitsFlags  == 45) // inches
									myPGNValue  = myPGNValue * 0.039370; // converted to inches
								  else //  default meters
									myPGNValue  = myPGNValue * 0.001; // converted to meters
									
							myPGNData.push(myPGNValue) ;									
						}
					}

				}
				
		} // good PGN
	} // 130946 Array Loop

	return myPGNData;

} // end of function GetPGN 130946	 
	 
	 
	 
	 
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

   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F119")
			{	      

				 myPitch= myN2Kdata[myIndex].payload.pitch;
				 myRoll= myN2Kdata[myIndex].payload.roll;

				if(myParameterIndex == 0) // Yaw
				{
					myPGNValue = myN2Kdata[myIndex].payload.yaw;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
					myPGNData.push(myPGNValue) ;
				}
		    
				if(myParameterIndex == 1) // Pitch
				{
					if(typeof(myPitch) != 'undefined' && myPitch != null)	
					myPGNData.push(myPitch) ;
				}

				 if(myParameterIndex == 2) // Roll
				 {
					if(typeof(myRoll) != 'undefined' && myRoll != null)	
					myPGNData.push(myRoll) ;
				}


				if(myParameterIndex == 3) // Roll & Pitch
				{
					if(typeof(myPitch) != 'undefined' && myPitch != null)
					{	
						if(typeof(myRoll) != 'undefined' && myRoll != null)	
						myPGNData.push(myPitch + ":" + myRoll) ;
					}
				}
		} // good PGN
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F113")
			{					
					myPGNValue= myN2Kdata[myIndex].payload.rateofturn;
      
         			if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
         			{	
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
							myPGNData.push(myPGNValue) ;
						  }
			    
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

   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F10D")
			{

		     	myInstanceString = myN2Kdata[myIndex].payload.instance;
		     	if(myInstanceString == myPGNInstance)
				{
    				if(myParameterIndex == 0) // Rudder angle
					{
					      
						myPGNValue= myN2Kdata[myIndex].payload.angle_order;
	         			if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
	         			{	
							myPGNData.push(myPGNValue) ;
						}
		    
					 }
					 
					 if(myParameterIndex == 1) // Rudder position
					{
					      
						myPGNValue= myN2Kdata[myIndex].payload.position;
	         			if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)	
	         			{	
							myPGNData.push(myPGNValue) ;
						}
		    
					 }

				} // Instance match


					
			} // PGN match
					
		
	} // 127245 Array Loop

	return myPGNData;

} // end of function GetPGN 127245

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

  myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F802")
			{

		     myInstanceString = myN2Kdata[myIndex].payload.cog_reference;
			
			switch( myInstanceString ) {
				case "True":
					myWindRef = 0;
				break;
				case "Magnetic":
					myWindRef = 1;
				break;
				default:
					myWindRef = 15;
				break;
				}

			
				if((myWindRef & 0x03) == myPGNInstance) // True/Magnetic Fix
				{          


					  if(myParameterIndex == 0)
					  {
					   		myPGNValue = myN2Kdata[myIndex].payload.course_over_ground;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						 	myPGNData.push(Math.floor(myPGNValue)) ;
					  }
		    
				
					    if(myParameterIndex == 1) // Speed over ground
					   {
						  
						   myPGNValue = myN2Kdata[myIndex].payload.speed_over_ground;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								// 1 knot = 1.852 Km/hr
								// 1 knot = 0.51444 m/s
								// 1 m/sec = 1.94384449 knots
								// 1 m/sec = 2.23694
								
								
								 if(myUnitsFlags  == 4) // Knots
									myPGNValue  = myPGNValue * 1.94384449 * 1; // converted to Knots
								  else if(myUnitsFlags  == 5) // MPH
									myPGNValue  = myPGNValue * 2.23694 * 1; // converted to MPH
								  else if(myUnitsFlags  == 6) // KPH
									myPGNValue  = myPGNValue * 3.6 * 1; // converted to KPH
								 else if(myUnitsFlags  == 7) // KPH
									myPGNValue  = myPGNValue * 1.0 * 1; // converted to meters / sec
								  else //  default knots
									myPGNValue  = myPGNValue * 1.94384449 * 1; // converted to Knots
		
								     myPGNData.push(myPGNValue) ;
						     }
						
					   }

          
        } // COG Reference
	  } // good checksum
	} // 129026 Array Loop

	return myPGNData;

} // end of function GetPGN 129026

// Water Speed
// PGN 128256 [0x01F503] Environmential Parameters
// myParameterIndex = 0  -> Speed over water
// myParameterIndex = 1  -> Speed over Ground
// myUnitsFlags = 0  -> Knots
// myUnitsFlags = 4  -> MPH
// myUnitsFlags = 8  -> KPH
//
function GetPGN128256(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var mySpeedRef;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 
	var myDegreesTrueN;
	var myDegreesMagN;

  myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F503")
			{

		     myInstanceString = myN2Kdata[myIndex].payload.type_reference;
			
			switch( myInstanceString ) {
				case "Paddle Wheel":
					mySpeedRef = 0;
				break;

				case "Pitot Tube":
					mySpeedRef = 1;
				break;
				case "Paddle Wheel":
					mySpeedRef = 2;
				break;

				case "Doppler Log":
					mySpeedRef = 3;
				break;

				case "Correlation Log":
					mySpeedRef = 4;
				break;

				case "EM Log":
					mySpeedRef = 5;
				break;

				default:
					mySpeedRef = 15;
				break;
				}

			
				if((mySpeedRef & 0x03) == myPGNInstance) // sensor type
				{          


				
					    if(myParameterIndex == 0) // Speed over water
					   {
						  
						   myPGNValue = myN2Kdata[myIndex].payload.waterspeed;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								 if(myUnitsFlags  == 4) // Knots
									myPGNValue  = myPGNValue * 1.94384449 * 1; // converted to Knots
								  else if(myUnitsFlags  == 5) // MPH
									myPGNValue  = myPGNValue * 2.23694 * 1; // converted to MPH
								  else if(myUnitsFlags  == 6) // KPH
									myPGNValue  = myPGNValue * 3.6 * 1; // converted to KPH									
								  else if(myUnitsFlags  == 7) // KPH
									myPGNValue  = myPGNValue * 1.0 * 1; // converted to KPH
								  else //  default knots
									myPGNValue  = myPGNValue * 1.94384449 * 1; // converted to Knots
		
								     myPGNData.push(myPGNValue) ;
						     }
						
					   }

					   
					    if(myParameterIndex == 1) // Speed over ground
					   {
						  
						   myPGNValue = myN2Kdata[myIndex].payload.groundspeed;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								 if(myUnitsFlags  == 4) // Knots
									myPGNValue  = myPGNValue * 1.94384449 * 1; // converted to Knots
								  else if(myUnitsFlags  == 5) // MPH
									myPGNValue  = myPGNValue * 2.23694 * 1; // converted to MPH
								  else if(myUnitsFlags  == 6) // KPH
									myPGNValue  = myPGNValue * 1.0 * 1; // converted to KPH
								  else //  default knots
									myPGNValue  = myPGNValue * 1.94384449 * 1; // converted to Knots
		
								     myPGNData.push(myPGNValue) ;
						     }
						
					   }

          
        } // Water sped type Reference
	  } // good checksum
	} // 128256 Array Loop

	return myPGNData;

} // end of function GetPGN 128256


// Water Depth
// PGN 128267 [0x01F50B] Water Depth
// myParameterIndex = 0  -> Depth
// myParameterIndex = 1  -> offset
// myUnitsFlags = 30  -> Meters
// myUnitsFlags = 31  -> Feet
// myUnitsFlags = 32  -> Fathoms
//
function GetPGN128267(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
   
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();
 
	var myDegreesTrueN;
	var myDegreesMagN;

  myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F20B")
			{
				
					if(myParameterIndex == 0) // depth
					   {
						  
						   myPGNValue = myN2Kdata[myIndex].payload.depth;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								 if(myUnitsFlags  == 33) // Meters
									myPGNValue  = myPGNValue * 1.0; // converted to Meters
								  else if(myUnitsFlags  == 34) // Feet
									myPGNValue  = myPGNValue * 3.28084; // converted to Feet
								  else if(myUnitsFlags  == 35) // Fathoms
									myPGNValue  = myPGNValue * 0.546806649; // converted to Fathoms
								  else //  default meters
									myPGNValue  = myPGNValue * 1.0; // converted to Meters
		
								     myPGNData.push(myPGNValue) ;
						     }
						
					   }

					   if(myParameterIndex == 1) // offset
					   {
						  
						   myPGNValue = myN2Kdata[myIndex].payload.transducer_offset;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							{
								 if(myUnitsFlags  == 33) // Meters
									myPGNValue  = myPGNValue * 1.0; // converted to Meters
								  else if(myUnitsFlags  == 34) // Feet
									myPGNValue  = myPGNValue * 3.28084; // converted to Feet
								  else if(myUnitsFlags  == 35) // Fathoms
									myPGNValue  = myPGNValue * 0.546806649; // converted to Fathoms
								  else //  default meters
									myPGNValue  = myPGNValue * 1.0; // converted to Meters
		
								     myPGNData.push(myPGNValue) ;
						     }
						
					   }

	
          
       
	  } // good checksum
	} // 128267 Array Loop

	return myPGNData;

} // end of function GetPGN 128267

// Switch Status
// PGN 127501 [0x01F20D] Switch Status
// myParameterIndex = 0  -> Switch0
// myParameterIndex = 1  -> Switch1
//
//
// myParameterIndex = 28  -> Switch28
//
function GetPGN127501(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


	

   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "01F20D")
			{
				if((myN2Kdata[myIndex].payload.instance ) == myPGNInstance) // sensor type
				{          

					   if(myParameterIndex == 0) // indicator 0
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic01;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 1) // indicator 1
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic02;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 2) // indicator 2
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic03;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 3) // indicator 3
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic04;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 4) // indicator 4
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic05;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 5) // indicator 5
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic06;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 6) // indicator 6
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic07;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 7) // indicator 7
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic08;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 8) // indicator 8
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic09;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 9) // indicator 9
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic10;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }					   
					   if(myParameterIndex == 10) // indicator 10
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic11;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 11) // indicator 11
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic12;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 12) // indicator 12
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic13;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 13) // indicator 13
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic14;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 14) // indicator 14
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic15;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 15) // indicator 15
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic16;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 16) // indicator 16
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic17;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 17) // indicator 17
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic18;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 18) // indicator 18
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic19;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
					   if(myParameterIndex == 19) // indicator 19
					   {
						   myPGNValue = myN2Kdata[myIndex].payload.indic20;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								     myPGNData.push(myPGNValue) ;
					   }
				}	
		} // good checksum
	} // 127501 Array Loop

	return myPGNData;

} // end of function GetPGN 127501


// Dimmer Status
// PGN 65286 [0x01FF06] Dimmer Status
// myParameterIndex = 0  -> Dimmer0
// myParameterIndex = 1  -> Dimmer1
//
//
// myParameterIndex = 4  -> Dimmer4
//
function GetPGN65286(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


	

   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FF06")
			{
				// check it is a SeaSmart dimmer PGN 99E1
			    if(myN2Kdata[myIndex].payload.pgntype == 57753)
				{
					if((myN2Kdata[myIndex].payload.dimmertype ) == "RGB 1 Channel" && myPGNInstance >= 0x80 && myPGNInstance <= 0xBF) // sensor type
					{
						if((myN2Kdata[myIndex].payload.instance ) == (myPGNInstance & 0x0F)) // sensor type
						{          

						   if(myParameterIndex == 0) // dimmer 0
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer0;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						   if(myParameterIndex == 1) // dimmer 1
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer1;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						   if(myParameterIndex == 2) // dimmer 2
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer2;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						   if(myParameterIndex == 3) // dimmer 3
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer3;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						   if(myParameterIndex == 4) // dimmer 4
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.control;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						}
					}
					else if((myN2Kdata[myIndex].payload.dimmertype ) == "LED 4 Channel" && myPGNInstance >= 0xC0 ) // sensor type
					{
						if((myN2Kdata[myIndex].payload.instance ) == (myPGNInstance & 0x0F)) // sensor type
						{          

						   if(myParameterIndex == 0) // dimmer 0
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer0;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						   if(myParameterIndex == 1) // dimmer 1
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer1;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						   if(myParameterIndex == 2) // dimmer 2
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer2;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						   if(myParameterIndex == 3) // dimmer 3
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer3;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						   if(myParameterIndex == 4) // dimmer 4
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.control;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						}
					}
					else if((myN2Kdata[myIndex].payload.dimmertype ) == "LED 1 Channel" && myPGNInstance < 0x80) // sensor type
					{
						if((myN2Kdata[myIndex].payload.instance ) == myPGNInstance & 0x0F) // sensor type
						{          

						   if(myParameterIndex == 0) // dimmer 0
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer0;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
						   if(myParameterIndex == 1) // dimmer 1
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer1;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								{
									if(myUnitsFlags  == 44) // amps * 10
										myPGNData.push(myPGNValue) * 0.10 ;
									else
										myPGNData.push(myPGNValue) ;
								}
						   }
						   if(myParameterIndex == 2) // dimmer 2
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer2;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								{
									if(myUnitsFlags  == 44) // amps * 10
										myPGNData.push(myPGNValue) * 0.10 ;
									else
										myPGNData.push(myPGNValue) ;
								}
						   }
						   if(myParameterIndex == 3) // dimmer 3
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.dimmer3;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								{
									if(myUnitsFlags  == 44) // amps * 10
										myPGNData.push(myPGNValue) * 0.10 ;
									else
										myPGNData.push(myPGNValue) ;
								};
						   }
						   if(myParameterIndex == 4) // dimmer 4
						   {
							   myPGNValue = myN2Kdata[myIndex].payload.control;// converted to degrees
								if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
										myPGNData.push(myPGNValue) ;
						   }
					}   
				}
			}				
		} // good checksum
	} // 130946 Array Loop

	return myPGNData;

} // end of function GetPGN 130946 - SeaSmart Dimmer


// Indicator Runtime Status
// PGN 65292 [0x01FF0C] Dimmer Status
// myParameterIndex = 0  -> Runtime Seconds
// myParameterIndex = 1  -> Cycles
//
//
// myParameterIndex = 0  -> Channel 0 Runtime Seconds 
// myParameterIndex = 1  -> Channel 0 Cycle Count   
// myParameterIndex = 2  -> Channel 1 Runtime Seconds 
// myParameterIndex = 3  -> Channel 1 Cycle Count    
// myParameterIndex = 4  -> Channel 2 Runtime Seconds
// myParameterIndex = 5  -> Channel 2 Cycle Count    
// myParameterIndex = 6  -> Channel 3 Runtime Seconds   
// myParameterIndex = 7  -> Channel 3 Cycle Count    
// myParameterIndex = 8  -> Channel 4 Runtime Seconds 
// myParameterIndex = 9  -> Channel 4 Cycle Count   
// myParameterIndex = 10  -> Channel 5 Runtime Seconds 
// myParameterIndex = 11  -> Channel 5 Cycle Count    
// myParameterIndex = 12  -> Channel 6 Runtime Seconds
// myParameterIndex = 13  -> Channel 6 Cycle Count    
// myParameterIndex = 14  -> Channel 7 Runtime Seconds   
// myParameterIndex = 15  -> Channel 7 Cycle Count    

//
function GetPGN65292(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
{
  var mySubStrings = new Array();
   var myIndex;
    var myRowIndex;
    
    var myPGN;
    var myPGNValue;
	var myHours;
 	var myMins;  
    var myPGNData = new Array();
    var myHexStr = new String();
    var myHexLBStr = new String();


	

   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FF0C")
			{
				// check it is a SeaSmart dimmer PGN 99E1
			    if(myN2Kdata[myIndex].payload.pgntype == 57753)
				{
					///if((myN2Kdata[myIndex].payload.dimmertype ) == "RGB 1 Channel" && myPGNInstance >= 0x80 && myPGNInstance <= 0xBF) // sensor type
					{
						if((myN2Kdata[myIndex].payload.instance ) == (myPGNInstance & 0x0F)) // sensor type
						{          

						   if(myParameterIndex == 0) // runtime 0
						   {
							   if(myN2Kdata[myIndex].payload.channel == 0)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.runtime_sec;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
									{
										if(myUnitsFlags  == 37) // HH:MM
										{
											myHours = Math.floor(myPGNValue / (60*60));
											myMins = Math.floor((myPGNValue % (60*60)) / 60);
											myPGNValue = parseFloat(myHours + (myMins * 0.01));
										}
											myPGNData.push(myPGNValue) ;
									}
								}
						   }
						   if(myParameterIndex == 1) // cycles 0
						   {
							   if(myN2Kdata[myIndex].payload.channel == 0)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.cycles;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
											myPGNData.push(myPGNValue) ;
								}
						   }
						   
					   if(myParameterIndex == 2) // runtime 1
						   {
							   if(myN2Kdata[myIndex].payload.channel == 1)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.runtime_sec;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
									{
										if(myUnitsFlags  == 37) // HH:MM
										{
											myHours = Math.floor(myPGNValue / (60*60));
											myMins = Math.floor((myPGNValue % (60*60)) / 60);
											myPGNValue = parseFloat(myHours + (myMins * 0.01));
										}
											myPGNData.push(myPGNValue) ;
									}
								}
						   }
						   if(myParameterIndex == 3) // cycles 1
						   {
							   if(myN2Kdata[myIndex].payload.channel == 1)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.cycles;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
											myPGNData.push(myPGNValue) ;
								}
						   }
						   
					   if(myParameterIndex == 4) // runtime 2
						   {
							   if(myN2Kdata[myIndex].payload.channel == 2)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.runtime_sec;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
									{
										if(myUnitsFlags  == 37) // HH:MM
										{
											myHours = Math.floor(myPGNValue / (60*60));
											myMins = Math.floor((myPGNValue % (60*60)) / 60);
											myPGNValue = parseFloat(myHours + (myMins * 0.01));
										}
											myPGNData.push(myPGNValue) ;
									}
								}
						   }
						   if(myParameterIndex == 5) // cycles 2
						   {
							   if(myN2Kdata[myIndex].payload.channel == 2)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.cycles;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
											myPGNData.push(myPGNValue) ;
								}
						   }
						   
					   if(myParameterIndex == 6) // runtime 3
						   {
							   if(myN2Kdata[myIndex].payload.channel == 3)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.runtime_sec;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
									{
										if(myUnitsFlags  == 37) // HH:MM
										{
											myHours = Math.floor(myPGNValue / (60*60));
											myMins = Math.floor((myPGNValue % (60*60)) / 60);
											myPGNValue = parseFloat(myHours + (myMins * 0.01));
										}
											myPGNData.push(myPGNValue) ;
									}
								}
						   }
						   if(myParameterIndex == 7) // cycles 3
						   {
							   if(myN2Kdata[myIndex].payload.channel == 3)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.cycles;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
											myPGNData.push(myPGNValue) ;
								}
						   }
						   
					   if(myParameterIndex == 8) // runtime 4
						   {
							   if(myN2Kdata[myIndex].payload.channel == 4)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.runtime_sec;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
									{
										if(myUnitsFlags  == 37) // HH:MM
										{
											myHours = Math.floor(myPGNValue / (60*60));
											myMins = Math.floor((myPGNValue % (60*60)) / 60);
											myPGNValue = parseFloat(myHours + (myMins * 0.01));
										}
											myPGNData.push(myPGNValue) ;
									}
								}
						   }
						   if(myParameterIndex == 9) // cycles 4
						   {
							   if(myN2Kdata[myIndex].payload.channel == 4)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.cycles;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
											myPGNData.push(myPGNValue) ;
								}
						   }
						   
					   if(myParameterIndex == 10) // runtime 5
						   {
							   if(myN2Kdata[myIndex].payload.channel == 5)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.runtime_sec;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
									{
										if(myUnitsFlags  == 37) // HH:MM
										{
											myHours = Math.floor(myPGNValue / (60*60));
											myMins = Math.floor((myPGNValue % (60*60)) / 60);
											myPGNValue = parseFloat(myHours + (myMins * 0.01));
										}
											myPGNData.push(myPGNValue) ;
									}
								}
						   }
						   if(myParameterIndex == 11) // cycles 5
						   {
							   if(myN2Kdata[myIndex].payload.channel == 5)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.cycles;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
											myPGNData.push(myPGNValue) ;
								}
						   }
						   
					   if(myParameterIndex == 12) // runtime 6
						   {
							   if(myN2Kdata[myIndex].payload.channel == 6)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.runtime_sec;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
									{
										if(myUnitsFlags  == 37) // HH:MM
										{
											myHours = Math.floor(myPGNValue / (60*60));
											myMins = Math.floor((myPGNValue % (60*60)) / 60);
											myPGNValue = parseFloat(myHours + (myMins * 0.01));
										}
											myPGNData.push(myPGNValue) ;
									}
								}
						   }
						   if(myParameterIndex == 13) // cycles 6
						   {
							   if(myN2Kdata[myIndex].payload.channel == 6)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.cycles;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
											myPGNData.push(myPGNValue) ;
								}
						   }
						   
					   if(myParameterIndex == 14) // runtime 7
						   {
							   if(myN2Kdata[myIndex].payload.channel == 7)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.runtime_sec;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
									{
										if(myUnitsFlags  == 37) // HH:MM
										{
											myHours = Math.floor(myPGNValue / (60*60));
											myMins = Math.floor((myPGNValue % (60*60)) / 60);
											myPGNValue = parseFloat(myHours + (myMins * 0.01));
										}
											myPGNData.push(myPGNValue) ;
									}
								}
						   }
						   if(myParameterIndex == 15) // cycles 7
						   {
							   if(myN2Kdata[myIndex].payload.channel == 7)
							   {
								   myPGNValue = myN2Kdata[myIndex].payload.cycles;
									if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
											myPGNData.push(myPGNValue) ;
								}
						   }
						   						   
					}   
				}
			}				
		} // good checksum
	} // 65292 Array Loop

	return myPGNData;

} // end of function GetPGN 65292 - SeaSmart Dimmer

// PGN65287: SeaSmart ac watt hours 0x0FF07
// myParameterIndex = 0  -> AMPS
// myParameterIndex = 1  -> TOTAL POWER kWattHours
//

function GetPGN65287(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


	

   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FF07")
			{
				// check it is a SeaSmart dimmer PGN 99E1
			    if(myN2Kdata[myIndex].payload.pgntype == 57753)
				{
					if((myN2Kdata[myIndex].payload.instance ) == myPGNInstance) // sensor type
					{          

					myParameterString = myN2Kdata[myIndex].payload.ac_type;

					switch( myParameterString) {
						case "UTIL":
							myParameter  = 0;
							break;
		
						case "GEN":
							myParameter  = 1;
							break;
		
						case "LED":
							myParameter  = 2;
							break;
		
						
		
						case "Error":
							myParameter  =254;
							break;
		
						case "No Data":
							myParameter  =255;
							break;
		
			
		
						default:
							myParameter  = 255;
							break;
					}

			
					if(myParameter  == myParameterIndex) // ac_kwatt_hours
					{  
	
						   myPGNValue = myN2Kdata[myIndex].payload.ac_kwatt_hours;// converted to degrees
							if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
								
							 if(myUnitsFlags  == 30) // watts/hr
									myPGNValue  = myPGNValue * 1000.0 ; // converted to Watts
								  else //  default knots
									myPGNValue  = myPGNValue * 1.0 ; // converted to kWatts
							
							
									myPGNData.push(myPGNValue) ;
					   }
					   
					   
				}
			}				
		} // good checksum
	} // 65287 Array Loop

	return myPGNData;

} // end of function GetPGN PGN65287: SeaSmart ac watt hours 0x0FF07



// PGN65014: J1939 PGN 65014 - (0x00FDF6) Utility Phase A Basic AC Quantities
// myParameterIndex = 0  -> Line-line AC Volts
// myParameterIndex = 1  -> Line-Neutral AC Volts
// myParameterIndex = 2  -> AC Frequency
// myParameterIndex = 3  -> AC Amps
// myParameterIndex = 4  -> AC Watts
function GetPGN65014(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
			try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FDF6")
			{
				
				if(myParameterIndex == 0) // ac_line_line_volts
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_line_line_volts;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							myPGNData.push(myPGNValue ) ;
				}
				if(myParameterIndex == 1) // ac_line_neutral_volts
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_line_neutral_volts;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
				 }
				if(myParameterIndex == 2) // ac_frequency
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_frequency;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							myPGNData.push(myPGNValue * 0.0078125) ;
				}
				if(myParameterIndex == 3) // ac_amps
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_amps;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
				 }
				if(myParameterIndex == 4) // ac_watts
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_watts;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
				 }					   
					
			} // pgn match
			else if((myN2Kdata[myIndex].pgn == "00FF08") && (myN2Kdata[myIndex].payload.ac_type == "UTIL") && (myN2Kdata[myIndex].payload.instance  == 0) )// SeaSmart AC Detail maps to saem PGN
			{
				if(myParameterIndex == 1) // ac_volts_detail
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_volts_detail;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							myPGNData.push(myPGNValue ) ;
				}

				if(myParameterIndex == 3) // ac_amps
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_amps_detail;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
				 }
			}
			
			
			
			
		} // 65014 Array Loop

	return myPGNData;

} // end of function GetPGN 1939 PGN 65014 - (0x0FDF6) Utility Phase A Basic AC Quantities


// PGN65011: J1939 PGN 65011 - (0x00FDF6) Utility Phase B Basic AC Quantities
// myParameterIndex = 0  -> Line-line AC Volts
// myParameterIndex = 1  -> Line-Neutral AC Volts
// myParameterIndex = 2  -> AC Frequency
// myParameterIndex = 3  -> AC Amps
// myParameterIndex = 4  -> AC Watts
function GetPGN65011(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
		  try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FDF3")
			{
			if(myParameterIndex == 0) // ac_line_line_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_line_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
			}
			if(myParameterIndex == 1) // ac_line_neutral_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_neutral_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 2) // ac_frequency
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_frequency;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue * 0.0078125) ;
			}
			if(myParameterIndex == 3) // ac_amps
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_amps;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 4) // ac_watts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_watts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }	

			}// pgn match	
			else if((myN2Kdata[myIndex].pgn == "00FF08") && (myN2Kdata[myIndex].payload.ac_type == "UTIL") && (myN2Kdata[myIndex].payload.instance  == 1) )// SeaSmart AC Detail maps to saem PGN
			{
				if(myParameterIndex == 1) // ac_volts_detail
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_volts_detail;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							myPGNData.push(myPGNValue ) ;
				}

				if(myParameterIndex == 3) // ac_amps
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_amps_detail;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
				 }
			}
			
					
		} // 65011 Array Loop

	return myPGNData;

} // end of function GetPGN 1939 PGN 65008 - (0x0FDF6) Utility Phase B Basic AC Quantities


// PGN65028: J1939 PGN 65008 - (0x00FDF6) Utility Phase C Basic AC Quantities
// myParameterIndex = 0  -> Line-line AC Volts
// myParameterIndex = 1  -> Line-Neutral AC Volts
// myParameterIndex = 2  -> AC Frequency
// myParameterIndex = 3  -> AC Amps
// myParameterIndex = 4  -> AC Watts
function GetPGN65008(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
		try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FDF0")
		{
			if(myParameterIndex == 0) // ac_line_line_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_line_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
			}
			if(myParameterIndex == 1) // ac_line_neutral_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_neutral_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 2) // ac_frequency
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_frequency;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue * 0.0078125) ;
			}
			if(myParameterIndex == 3) // ac_amps
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_amps;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 4) // ac_watts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_watts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }					   
		  }	// pgn match
		  else if((myN2Kdata[myIndex].pgn == "00FF08") && (myN2Kdata[myIndex].payload.ac_type == "UTIL") && (myN2Kdata[myIndex].payload.instance  == 2) )// SeaSmart AC Detail maps to saem PGN
		  {
				if(myParameterIndex == 1) // ac_volts_detail
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_volts_detail;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
							myPGNData.push(myPGNValue ) ;
				}

				if(myParameterIndex == 3) // ac_amps
				{
					myPGNValue = myN2Kdata[myIndex].payload.ac_amps_detail;
					if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
				 }
		  }
		} // 65014 Array Loop

	return myPGNData;

} // end of function GetPGN 1939 PGN 65008 - (0x0FDF6) Utility Phase C Basic AC Quantities


// PGN65017: J1939 PGN 65017 - (0x00FDF6) Utility Total Basic AC Quantities
// myParameterIndex = 0  -> Line-line AC Volts
// myParameterIndex = 1  -> Line-Neutral AC Volts
// myParameterIndex = 2  -> AC Frequency
// myParameterIndex = 3  -> AC Amps
// myParameterIndex = 4  -> AC Watts
function GetPGN65017(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
		  try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FDF9")
			{
			if(myParameterIndex == 0) // ac_line_line_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_line_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
			}
			if(myParameterIndex == 1) // ac_line_neutral_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_neutral_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 2) // ac_frequency
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_frequency;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue * 0.0078125) ;
			}
			if(myParameterIndex == 3) // ac_amps
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_amps;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 4) // ac_watts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_watts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }					   
			} // pgn match	
		} // 65017 Array Loop

	return myPGNData;

} // end of function GetPGN 1939 PGN 65017 - (0x0FDF6) Utility Total Basic AC Quantities


// PGN65005: J1939 PGN 65005 - (0x00FDED) Generaror Total Basic AC Quantities
// myParameterIndex = 0  -> Line-line AC Volts
// myParameterIndex = 1  -> Line-Neutral AC Volts
// myParameterIndex = 2  -> AC Frequency
// myParameterIndex = 3  -> AC Amps
// myParameterIndex = 4  -> AC Watts
function GetPGN65005(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
		  try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FDED")
			{
			if(myParameterIndex == 0) // import_kwatt_hours
			{
				myPGNValue = myN2Kdata[myIndex].payload.import_kwatt_hours;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
			}
			if(myParameterIndex == 1) // export_kwatt_hours
			{
				myPGNValue = myN2Kdata[myIndex].payload.export_kwatt_hours;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			
			} // pgn match	
		} // 65005 Array Loop

	return myPGNData;

} // end of function GetPGN 1939 PGN 65005 - (0x0FDED) Utility Total Basic AC Quantities



// PGN65027: J1939 PGN 65027 - (0x0FE03) Generaror Phase A Basic AC Quantities
// myParameterIndex = 0  -> Line-line AC Volts
// myParameterIndex = 1  -> Line-Neutral AC Volts
// myParameterIndex = 2  -> AC Frequency
// myParameterIndex = 3  -> AC Amps
// myParameterIndex = 4  -> AC Watts
function GetPGN65027(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
		  try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FE03")
			{
				
			if(myParameterIndex == 0) // ac_line_line_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_line_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
			}
			if(myParameterIndex == 1) // ac_line_neutral_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_neutral_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 2) // ac_frequency
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_frequency;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue * 0.0078125) ;
			}
			if(myParameterIndex == 3) // ac_amps
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_amps;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 4) // ac_watts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_watts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }					   
					
			} // pgn match
		} // 65027 Array Loop

	return myPGNData;

} // end of function GetPGN 1939 PGN 65024 - (0x0FE03) Generaror Phase A Basic AC Quantities



// PGN65024: J1939 PGN 65024 - (0x000FE00) Generaror Phase B Basic AC Quantities
// myParameterIndex = 0  -> Line-line AC Volts
// myParameterIndex = 1  -> Line-Neutral AC Volts
// myParameterIndex = 2  -> AC Frequency
// myParameterIndex = 3  -> AC Amps
// myParameterIndex = 4  -> AC Watts
function GetPGN65024(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
		  try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FE00")
			{
			if(myParameterIndex == 0) // ac_line_line_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_line_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
			}
			if(myParameterIndex == 1) // ac_line_neutral_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_neutral_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 2) // ac_frequency
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_frequency;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue * 0.0078125) ;
			}
			if(myParameterIndex == 3) // ac_amps
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_amps;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 4) // ac_watts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_watts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }	

			}// pgn match			 
					
		} // 65024 Array Loop

	return myPGNData;

} // end of function GetPGN 1939 PGN 65024 - (0x0FDF6) Generaror Phase B Basic AC Quantities


// PGN65021: J1939 PGN 65021 - (0x00FDFD) UtiGenerarorlity Phase C Basic AC Quantities
// myParameterIndex = 0  -> Line-line AC Volts
// myParameterIndex = 1  -> Line-Neutral AC Volts
// myParameterIndex = 2  -> AC Frequency
// myParameterIndex = 3  -> AC Amps
// myParameterIndex = 4  -> AC Watts
function GetPGN65021(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
		try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FDFD")
		{
			if(myParameterIndex == 0) // ac_line_line_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_line_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
			}
			if(myParameterIndex == 1) // ac_line_neutral_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_neutral_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 2) // ac_frequency
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_frequency;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue * 0.0078125) ;
			}
			if(myParameterIndex == 3) // ac_amps
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_amps;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 4) // ac_watts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_watts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }					   
		  }	// pgn match
		} // 65021 Array Loop

	return myPGNData;

} // end of function GetPGN 1939 PGN 65021 - (0x0FDF6) Generaror Phase C Basic AC Quantities


// PGN65030: J1939 PGN 65030 - (0x00FE06) Generaror Total Basic AC Quantities
// myParameterIndex = 0  -> Line-line AC Volts
// myParameterIndex = 1  -> Line-Neutral AC Volts
// myParameterIndex = 2  -> AC Frequency
// myParameterIndex = 3  -> AC Amps
// myParameterIndex = 4  -> AC Watts
function GetPGN65030(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
		  try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FE06")
			{
			if(myParameterIndex == 0) // ac_line_line_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_line_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
			}
			if(myParameterIndex == 1) // ac_line_neutral_volts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_line_neutral_volts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 2) // ac_frequency
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_frequency;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue * 0.0078125) ;
			}
			if(myParameterIndex == 3) // ac_amps
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_amps;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			if(myParameterIndex == 4) // ac_watts
			{
				myPGNValue = myN2Kdata[myIndex].payload.ac_watts;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }					   
			} // pgn match	
		} // 65030 Array Loop

	return myPGNData;

} // end of function GetPGN 1939 PGN 65030 - (0x0FE06) Generaror Total Basic AC Quantities

// PGN65018: J1939 PGN 65018 - (0x00FDFA) Generaror Total Basic AC Quantities
// myParameterIndex = 0  -> Line-line AC Volts
// myParameterIndex = 1  -> Line-Neutral AC Volts
// myParameterIndex = 2  -> AC Frequency
// myParameterIndex = 3  -> AC Amps
// myParameterIndex = 4  -> AC Watts
function GetPGN65018(myN2Kdata, myPGNInstance, myParameterIndex, myUnitsFlags )
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


   myArrayLength = myN2Kdata.length;

      // Get all the elements and parse into variables
      for (myIndex = 0; myIndex < myArrayLength; myIndex++) 
	  {
		  try{myPGN = myN2Kdata[myIndex].pgn}catch(err){myPGN = 'FFFFFF'}; if(myPGN == "00FDFA")
			{
			if(myParameterIndex == 0) // import_kwatt_hours
			{
				myPGNValue = myN2Kdata[myIndex].payload.import_kwatt_hours;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
						myPGNData.push(myPGNValue) ;
			}
			if(myParameterIndex == 1) // export_kwatt_hours
			{
				myPGNValue = myN2Kdata[myIndex].payload.export_kwatt_hours;
				if(typeof(myPGNValue) != 'undefined' && myPGNValue != null)
					myPGNData.push(myPGNValue) ;
			 }
			
			} // pgn match	
		} // 65018 Array Loop

	return myPGNData;

} // end of function GetPGN 1939 PGN 65018 - (0x0FDFA) Utility Total Basic AC Quantities



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
					myPGNData.push(myPGNValue) ;
				}
			}
			else if(myParameterIndex == 1) // Wind Direction Magnetic
			{	
				if(myIIMWDStr[2] != '')
				{
					myPGNValue  = myIIMWDStr[2]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			else if(myParameterIndex == 2) // Wind Speed Knots
			{	
				if(myIIMWDStr[4] != '')
				{
					myPGNValue  = myIIMWDStr[4]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			else if(myParameterIndex == 3) // Wind Speed Meters/sec
			{	
				if(myIIMWDStr[6] != '')
				{
					myPGNValue  = myIIMWDStr[6]; // 
					myPGNData.push(myPGNValue) ;
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
						myPGNData.push(myPGNValue) ;
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
						myPGNData.push(myPGNValue) ;
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
						myPGNData.push(myPGNValue) ;
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
						myPGNData.push(myPGNValue) ;
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
						myPGNData.push(myPGNValue) ;
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
						myPGNData.push(myPGNValue) ;
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
						myPGNData.push(myPGNValue) ;
					}
				}
				else if(myIIVWRStr[1] == 'R')
				{
					if(myIIVWRStr[0] != '')
					{
						myPGNValue  = myIIVWRStr[0]; // 
						myPGNData.push(myPGNValue) ;
					}
				}
			}

			else if(myParameterIndex == 1) // Wind Speed Knots
			{	
				if(myIIVWRStr[2] != '')
				{
					myPGNValue  = myIIVWRStr[2]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 2) // Wind Speed Meters/sec
			{	
				if(myIIVWRStr[2] != '')
				{
					myPGNValue  = myIIVWRStr[4]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 3) // Wind Speed Km/hr
			{	
				if(myIIVWRStr[2] != '')
				{
					myPGNValue  = myIIVWRStr[6]; // 
					myPGNData.push(myPGNValue) ;
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
					myPGNData.push(myPGNValue) ;
				 }
			}
			if(myParameterIndex == 1) // Heading True
			{	

				if(myHCHDGStr[4] == 'E')
				{
					if(myHCHDGStr[0] != '')
					{
						myPGNValue  = parseFloat(myHCHDGStr[0]) + parseFloat(myHCHDGStr[3]); // 
						myPGNData.push(myPGNValue) ;
					}
				}
				else if (myHCHDGStr[4] == 'W')
				{
					if(myHCHDGStr[0] != '')
					{
						myPGNValue  = parseFloat(myHCHDGStr[0]) - parseFloat(myHCHDGStr[3]); 
						myPGNData.push(myPGNValue) ;
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
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 1) // Water Direction Magnetic
			{	
				if(myIIVHWStr[2] != '')
				{
					myPGNValue  = myIIVHWStr[2]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 2) // Water Speed Knots
			{	
				if(myIIVHWStr[4] != '')
				{
					myPGNValue  = myIIVHWStr[4]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 3) // Wind Speed Kilometers/sec
			{	
				if(myIIVHWStr[6] != '')
				{
					myPGNValue  = myIIVHWStr[6]; // 
					myPGNData.push(myPGNValue) ;
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
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 1) // Water Direction Magnetic
			{	
				if(myIIVTGStr[2] != '')
				{
					myPGNValue  = myIIVTGStr[2]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 2) // Water Speed Knots
			{	
				if(myIIVTGStr[4] != '')
				{
					myPGNValue  = myIIVTGStr[4]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 3) // Wind Speed Kilometers/sec
			{	
				if(myIIVTGStr[6] != '')
				{
					myPGNValue  = myIIVTGStr[6]; // 
					myPGNData.push(myPGNValue) ;
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
					myPGNData.push(myPGNValue) ;
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
					myPGNData.push(myPGNValue) ;
				}
			}

			if(myParameterIndex == 1) // Roll
			{	
				if(myYXXDRStr[5] != '')
				{
					myPGNValue  = myYXXDRStr[5]; // 
					myPGNData.push(myPGNValue) ;
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
						myPGNData.push(myPGNValue) ;
					}
					else if(myGPGLLStr[1] == 'N')
					{
						myPGNValue  = 1.0 * (parseFloat(myGPGLLStr[0]))/100 ; // 
						myPGNData.push(myPGNValue) ;
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
						myPGNData.push(myPGNValue) ;
					}
					else if(myGPGLLStr[3] == 'E')
					{
						myPGNValue  = 1.0 * (parseFloat(myGPGLLStr[2]))/100 ; // 
						myPGNData.push(myPGNValue) ;
					}
				}
			}
			if(myParameterIndex == 2) // Time
			{	
				if(myGPGLLStr[4] != '')
				{
					myPGNValue  = myGPGLLStr[4]; // 
					myPGNData.push(myPGNValue) ;
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
					myPGNData.push(myPGNValue) ;
				}
			}

    		if(myParameterIndex == 1) // Latitude
			{	
				if(myGPRMCStr[2] != '')
				{
					if(myGPRMCStr[3] == 'S')
					{
						myPGNValue  = -1.0 * (parseFloat(myGPRMCStr[2]))/100 ; // 
						myPGNData.push(myPGNValue) ;
					}
					else if(myGPRMCStr[3] == 'N')
					{
						myPGNValue  = 1.0 * (parseFloat(myGPRMCStr[2]))/100 ; // 
						myPGNData.push(myPGNValue) ;
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
						myPGNData.push(myPGNValue) ;
					}
					else if(myGPRMCStr[5] == 'E')
					{
						myPGNValue  = 1.0 * (parseFloat(myGPRMCStr[4]))/100 ; // 
						myPGNData.push(myPGNValue) ;
					}
				}
			}

			if(myParameterIndex == 3) // SOG
			{	
				if(myGPRMCStr[6] != '')
				{
					myPGNValue  = myGPRMCStr[6]; // 
					myPGNData.push(myPGNValue) ;
				}
			}

			if(myParameterIndex == 4) // track made good
			{	
				if(myGPRMCStr[7] != '')
				{
					myPGNValue  = myGPRMCStr[7]; // 
					myPGNData.push(myPGNValue) ;
				}
			}

			if(myParameterIndex == 5) // date
			{	
				if(myGPRMCStr[8] != '')
				{
					myPGNValue  = myGPRMCStr[8]; // 
					myPGNData.push(myPGNValue) ;
				}
			}

			if(myParameterIndex == 6) // mag variation
			{	
				if(myGPRMCStr[9] != '')
				{
					if(myGPRMCStr[10] == 'W')
					{
						myPGNValue  = -1.0 * (parseFloat(myGPRMCStr[9])) ; // 
						myPGNData.push(myPGNValue) ;
					}
					else if(myGPRMCStr[10] == 'E')
					{
						myPGNValue  = 1.0 * (parseFloat(myGPRMCStr[9])) ; // 
						myPGNData.push(myPGNValue) ;
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
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 1) // Depth meters
			{	
				if(mySDDBTStr[2] != '')
				{
					myPGNValue  = mySDDBTStr[2]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 2) // Depth fathoms
			{	
				if(mySDDBTStr[4] != '')
				{
					myPGNValue  = mySDDBTStr[4]; // 
					myPGNData.push(myPGNValue) ;
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
					myPGNData.push(myPGNValue) ;
				}
			}
			if(myParameterIndex == 1) // Wind Temp Fahrenheit
			{	
				if(mySDMTWStr[0] != '')
				{
					myPGNValue  = 32 + (parseFloat(mySDMTWStr[0]) * 1.8); // 
					myPGNData.push(myPGNValue) ;
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
				myPGNData.push(myPGNValue) ;
				}
			}
			else if(myParameterIndex == 1) //  Baro Bars
			{	
				if( myWIMDAStr[2] != '')
				{
					myPGNValue  = myWIMDAStr[2]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			else if(myParameterIndex == 2) // Air Temp
			{	
				if( myWIMDAStr[4] != '')
				{
					myPGNValue  = myWIMDAStr[4]; // 
					myPGNData.push(myPGNValue) ;
				}
			}
			else if(myParameterIndex == 3) // Water Temp
			{	
				if( myWIMDAStr[6] != '')
				{
					myPGNValue  = myWIMDAStr[6]; // 
					myPGNData.push(myPGNValue) ;
				}
			}

			else if(myParameterIndex == 4) // Humidity R
			{	
				if( myWIMDAStr[8] != '')
				{
					myPGNValue  = myWIMDAStr[8]; // 
					myPGNData.push(myPGNValue) ;
				}
			}

			else if(myParameterIndex == 5) // Humidity A
			{	
				if( myWIMDAStr[9] != '')
				{
					myPGNValue  = myWIMDAStr[9]; // 
					myPGNData.push(myPGNValue) ;
				}
			}

			else if(myParameterIndex == 6) // Dew Point
			{	
				if( myWIMDAStr[10] != '')
				{
					myPGNValue  = myWIMDAStr[10]; // 
					myPGNData.push(myPGNValue) ;
				}
			}

			else if(myParameterIndex == 7) // Wind Dir True
			{	
				if( myWIMDAStr[12] != '')
				{
					myPGNValue  = myWIMDAStr[12]; //
					myPGNData.push(myPGNValue) ; 
				}
			}

			else if(myParameterIndex == 8) // Wind Dir Mag
			{	
				if( myWIMDAStr[14] != '')
				{
					myPGNValue  = myWIMDAStr[14]; //
					myPGNData.push(myPGNValue) ; 
				}
			}

			else if(myParameterIndex == 9) // Wind Speed Knots
			{	
				if( myWIMDAStr[16] != '')
				{
					myPGNValue  = myWIMDAStr[16]; //
					myPGNData.push(myPGNValue) ; 
				}
			}

			else if(myParameterIndex == 10) // Wind Speed M/s
			{	
				if( myWIMDAStr[18] != '')
				{
					myPGNValue  = myWIMDAStr[18]; // 
					myPGNData.push(myPGNValue) ;
				}
			}

          
	
	} // WIMDA Array Loop

	return myPGNData;

} // end of function GetWIMDA

