function GetPGNTypeFromSeriesNumber(myPGNNumber, myPGNInstance, myPGNParameter)
{ 
//var myserieskey
var myKeys = new Array();
var myKey = new Array();
//var myPGNNumber= "";
var myPGNSource= "";
//var myPGNInstance= "";
var myPGNType="";
//var myPGNParameter= "";
var myPGNTag="";

/*
	myserieskey = myserieskey.replace(".*.","*.");

	 try{
	myKeys = myserieskey.split(".")
	
	myKey = myKeys[1].split(":");
	myPGNNumber = myKey[1];
	
	myKey = myKeys[2].split(":");
	myPGNSource = myKey[1];
	
	myKey = myKeys[3].split(":");
	myPGNInstance = myKey[1];
	
	myKey = myKeys[4].split(":");
	myPGNType = myKey[1];
	
	myKey = myKeys[5].split(":");
	myPGNParameter = myKey[1];
	}
	catch(err)
	{
		myPGNTag =  "None";
		return myPGNTag;
	}
	
	*/
	
	switch(myPGNNumber)
	{
		case "130944":	//SeaSmart Heartbeat
		
			//switch(myPGNParameter)
			//{
				//case "timestamp":
					//myPGNTag =  "/General/Heartbeat";
				//break;
					

			//}
			
			switch(myPGNParameter)
			{

				case 0://"lat":	
					myPGNTag =  "/General/Heartbeat";
				break;
					
				case 1://"lng":	
					myPGNTag =  "/General/Sessions";
				break;
					

			}
	
		break; // position
		
		case "130942":	//SeaSmart Cellular status
		

			switch(myPGNParameter)
			{

				case 0://"db_status":	
					myPGNTag =  "/Cellular/DB_Strength";
				break;
					
				case 1://"ai_status":	
					myPGNTag =  "/Cellular/Connect_Status";
				break;
					

			}
	
		break; // position

		case "129025":	// position rapid
		
			switch(myPGNParameter)
			{
				case 2://"latlng":
					myPGNTag =  "/Position";
				break;
		
				case 0://"lat":	
					myPGNTag =  "/Position/lat";
				break;
					
				case 1://"lng":	
					myPGNTag =  "/Position/lng";
				break;
					

			}
	
		break; // position
		
		case "129026":	// cogsog
		
			switch(myPGNParameter)
			{
				case 1://"speed_over_ground":
				switch(myPGNInstance)
				{
					case 0://"True":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Speed Over Ground";
					break;
					
					case 1://"Magnetic":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Speed Over Ground Mag";
					break;
					
		
					
				}
				break;
				
				case 0://"course_over_ground":
				switch(myPGNInstance)
				{
					case 0://"True":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Course Over Ground";
					break;
					
					case 1://"Magnetic":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Course Over Ground Mag";
					break;
					

					
				}
				break;
			}	
		break; // cogsog
		
		case "127250":	//	// vessel_heading
		
			switch(myPGNParameter)
			{
				case 0://"heading":
				switch(myPGNInstance)
				{
					case 0://"True":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Heading True";
					break;
					
					case 1://"Magnetic":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Heading Magnetic";
					break;
					
		
					
				}
				break;
				
				
			}	
		break; // vessel_heading
		
		case "127245":	//	// rudder
		
			switch(myPGNParameter)
			{
				case 0://"position":
				switch(myPGNInstance)
				{
					case 0://"True":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Rudder";
					break;
					
					case 1://"Magnetic":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Rudder Mag";
					break;
					
		
					
				}
				break;
				
				
			}	
		break; // rudder	

		case "127251":	//	rateofturn
			switch(myPGNParameter)
			{
				case 0://"rate_of_turn":
					myPGNTag =  "/M2M/Navigation/Rate Of Turn";
				break;
				
				
			}	
		break; // rateofturn			
		
		
		case "127257":	//	attitude
		
			switch(myPGNParameter)
			{
				case 0://"pitch":
				
					myPGNTag =  "/M2M/Attitude/Pitch";
				
				break;
				
				case 1://"roll":
				
					 myPGNTag =  "/M2M/Attitude/Roll";
				
				break;
			}	
		break; // attitude
		
		
		
		case "130311":	//	// environmental_data
		
			switch(myPGNParameter)
			{
				case 0://"temperature":
				switch(myPGNInstance)
				{
					case 0://"Sea Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Water Temperature";
					break;
					
					case 1://"Outside Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Temperature";
					break;
					
					case 2://"Inside Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Inside Temperature";
					break;
					
					case 3://"Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Inside Temperature";
					break;
					
					case 16://"Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 0";
					break;
					
					case 17://"Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 1";
					break;
					

					case 18://"Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 2";
					break;
					

					case 19://"Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 3";
					break;
					

					case 20://"Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 4";
					break;
					

					case 21://"Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 5";
					break;
					

					case 22://"Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 6";
					break;
					

					case 23://"Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 7";
					break;
					
					
					
					
				}
				break;
				
				case 2://"atmospheric_pressure":
				switch(myPGNInstance)
				{
					case 0://"Sea Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Pressure";
					break;
					
					case 1://"Outside Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Pressure";
					break;
					
					case 2://"Inside Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Pressure";
					break;
					
					case 3://"Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Pressure";
					break;
					
				}
				break;
				
				case 1://"humidity":
				switch(myPGNInstance)
				{
					case 3://"No Data":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Relative Humidity (%)";
					break;
					
					case 1://"Outside Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Relative Humidity (%)";
					break;
					
					case 0://"Inside  Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Humidity Inside";
					break;
					
					case 16://"Inside  Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Humidity Inside 0";
					break;

					case 17://"Inside  Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Humidity Inside 1";
					break;
					
					case 18://"Inside  Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Humidity Inside 2";
					break;
					
					case 19://"Inside  Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Humidity Inside 3";
					break;
					
					case 20://"Inside  Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Humidity Inside 4";
					break;
					
					case 21://"Inside  Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Humidity Inside 5";
					break;
					
					case 22://"Inside  Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Humidity Inside 6";
					break;
					
					case 23://"Inside  Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Humidity Inside 7";
					break;
										
			
				}
				break;
			}	
		break; // environmental_data
		
		case "130306":	//	wind_data
		
			switch(myPGNParameter)
			{
				case 0://"wind_speed":
				switch(myPGNInstance)
				{
					case 7://"No Data":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Wind Speed";
					break;
					
					case 0://"TWIND True North":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Wind Speed";
					break;
					
					case 2://"Apparent Wind":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Speed Apparent";
					break;
					
					case 3://"TWIND VCGR":	//	<option value="None"> -------- </option>
						myPGNTag =  "";
					break;
					
					case 5://"Apparent Wind":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Speed Gust";
					break;					
					
					
				}
				break;
				
				case 1://"wind_direction":
				switch(myPGNInstance)
				{
					case 7://"No Data":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Wind Direction";
					break;
					
					case 0://"TWIND True North":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Wind Direction";
					break;
					
					case 2://"Apparent Wind":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Direction Apparent";
					break;
					
					case 3://"ETWIND VCGR":	//	<option value="None"> -------- </option>
						myPGNTag =  "Relative Humidity (%)";
					break;
					
				}
				break;
				
				case 2://"wind_gust":
				switch(myPGNInstance)
				{
					case 7://"No Data":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Wind Gust";
					break;
					
					case 0://"TWIND True North":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Wind Gust";
					break;
					
					case 2://"Apparent Wind":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Gust";
					break;
					
					case 3://"ETWIND VCGR":	//	<option value="None"> -------- </option>
						myPGNTag =  "Relative Humidity (%)";
					break;
					
				}
				break;
				
			}	
		break; // wind_data
						

		case "130946":	//	Rain Gauge
		
			switch(myPGNParameter)
			{
				case 0://"pitch":
					myPGNTag =  "/M2M/Environment/Rain Accumulation";
				break;
				
				case 1://"roll":
					 myPGNTag =  "/M2M/Environment/Rain Duration";
				break;
				
				case 2://"pitch":
					myPGNTag =  "/M2M/Environment/Rain Rate";
				break;
				
				case 3://"roll":
					 myPGNTag =  "/M2M/Environment/Rain Peak Rate";
				break;				
				
				
			}	
		break; // rain gauge
				
		
		
	   case "61444":	//	Electronic Engine Controller 1
		
			switch(myPGNParameter)
			{
				case 0://"speed":
				switch(myPGNInstance)
				{
					case 0:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Generator RPM Port J1939";
					break;
					
	
				}
				break;
				
				

			}
			break;// Electronic Engine Controller 1		
			
		
	   case "65262":	//	J1939 engine temps
		
			switch(myPGNParameter)
			{
				case 0://"temperature":
					myPGNTag =  "/M2M/Engine/Generator Temperature J1939";
				break;
				
				case 1://"temperature":
					myPGNTag =  "/M2M/Engine/Generator Fuel J1939";
				break;
				
				case 2://"temperature":
					myPGNTag =  "/M2M/Engine/Generator OIL J1939";
				break;
				
				
			}
		break;// J1939 engine temps			
		
	   case "65263":	//	J1939 engine pressures
		
			switch(myPGNParameter)
			{
				case 0://"oil pressure":
					myPGNTag =  "/M2M/Engine/Generator Fuel Pressure J1939";
				break;
				
				case 3://"oil pressure":
					myPGNTag =  "/M2M/Engine/Generator OIL Pressure J1939";
				break;
			}
			
			
		break;// J1939 engine pressures			
		
		case "65272":	//	J1939 Transmission
		
			switch(myPGNParameter)
			{
				case 3://"oil pressure":
					myPGNTag =  "/M2M/Engine/Generator Transmission Pressure J1939";
				break;
				
				case 4://"oil temperature":
					myPGNTag =  "/M2M/Engine/enerator Transmission Temperature J1939";
				break;
			}
			
			
		break;// J1939 engine pressures			
		
		case "65271":	//	J1939 engine voltages
		
			switch(myPGNParameter)
			{
				case 0://"Net Battery Current":
					myPGNTag =  "/M2M/Battery/Battery Current J1939";
				break;
				
				case 1://"Alternator Current":
					myPGNTag =  "/M2M/Engine/Generator Alternator Current J1939";
				break;
				
				case 2://" Charging Voltage":
					myPGNTag =  "/M2M/Engine/Generator Alternator Volts J1939";
				break;
				
				case 3://"Battery Voltage":
					myPGNTag =  "/M2M/Battery/Battery Volts J1939";
				break;
			}
			
			
		break;// J1939 engine pressures			
		
		case "65276":	//	J1939 PGN 65276 (0x0FEFC) Dash Display
		
			switch(myPGNParameter)
			{
				case 1://
					myPGNTag =  "/M2M/Engine/Generator Fuel Level J1939";
				break;
			}
			
			
		break;// 
		
	   case "65266":	//	J1939 PGN 65266 (0x0FEF2) Fuel Economy
		
			switch(myPGNParameter)
			{
				case 0://
					myPGNTag =  "/M2M/Engine/Generator Fuel Rate J1939";
				break;
			}
			
			
		break;// J1939 Dash Display		
		

	   case "127488":	//	engine_parameters_rapid_update
		
			switch(myPGNParameter)
			{
				case 0://"speed":
				switch(myPGNInstance)
				{
					case 0:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine RPM Port";
					break;
					
					case 1:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine RPM Starboard";
					break;
					
					case 2:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine RPM Center";
					break;
				}
				break;
				
				case 1://"boost_presure":
				switch(myPGNInstance)
				{
					case 0:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine Boost Port";
					break;
					
					case 1:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine Boost Starboard";
					break;
					
					case 2:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Boost Center";
					break;
				}
				break;
				
				case 2://"tilt_or_trim":
				switch(myPGNInstance)
				{
					case 0:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine Trim Port";
					break;
					
					case 1:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine Trim Starboard";
					break;
					
					case 2:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Trim Center";
					break;
				}
				break;

			}
			break;// engine_parameters_rapid_update
			
			
		case "127489":	//	engine_parameters_dynamic
		
			switch(myPGNParameter)
			{
				case 0://"oil_pressure":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Pressure Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Pressure Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Pressure Center";
						break;
					}
				break;
				
				case 1://"oil_temp":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Temperature Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Temperature Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Temperature Center";
						break;
					}
				break;
				
				
				case 2://"engine_temp":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Temperature Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Temperature Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Temperature Center";
						break;
					}
				break;
				
				case 3://"alternator_potential":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Alternator Volts Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Alternator Volts Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Alternator Volts Center";
						break;
					}
				break;
				
				case 4://"fuel_rate":
				switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Center";
						break;
					}
				break;
				
				case 5://"total_engine_hours":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Hours Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Hours Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Hours Center";
						break;
					}
				break;
				
				case 6://"coolant_pressure":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Coolant Pressure Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Coolant Pressure Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Coolant Pressure Center";
						break;
					}
				break;
				
				case 7://"fuel_pressure":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Pressure Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Pressure Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Pressure Center";
						break;
					}
				break;
			}
			break;// engine_parameters_dynamic			
					
			
		case "127493":	//	transmission_parameters_dynamic
		
			switch(myPGNParameter)
			{
				case 0://"oil_pressure":
				switch(myPGNInstance)
				{
					case 0:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Pressure Port";
					break;
					
					case 1:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Pressure Starboard";
					break;
					
					case 2:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Pressure Center";
					break;
				}
				break;
				
				case 1://"oil_temp":
				switch(myPGNInstance)
				{
					case 0:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Temperature Port";
					break;
					
					case 1:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Temperature Starboard";
					break;
					
					case 2:	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Temperature Center";
					break;
				}
				break;
			}
			break;// transmission_parameters_dynamic
			
		case "127497":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case 0://"Trip Fuel Used":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Trip Fuel Used Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Trip Fuel Used Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Trip Fuel Used Center";
						break;
					}
				break;
				
				case 1://"Fuel Rate Average":
				switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Average Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Average Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Average Center";
						break;
					}
				break;
				
				case 2://"Fuel Rate Economy":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Economy Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Economy Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Economy Center";
						break;
					}
				break;
				
				case 3://"Instantaneous Fuel Economy":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Instantaneous Fuel Economy Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Instantaneous Fuel Economy Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Instantaneous Fuel Economy Center";
						break;
					}
				break;
				
				
				
			}
			break;// Trip Parameters Engine			
			
			
			
		case "127508":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case 0://"voltage":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery Volts Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery Volts Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery Volts Center";
						break;
					}
				break;
				
				case 1://"current":
				switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery Current Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery Current Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery Current Center";
						break;
					}
				break;
				
				case 2://"temperature":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery Temperature Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery Temperature Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery Temperature Center";
						break;
					}
				break;
			}
			break;// battery_status		




		case "127506":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case 0://"StateOfCharge":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery StateOfCharge Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery StateOfCharge Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery StateOfCharge Center";
						break;
					}
				break;
				
				case 1://"StateOfHealth":
				switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery StateOfHealth Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery StateOfHealth Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery StateOfHealth Center";
						break;
					}
				break;
				
				case 2://"TimeRemaining":
					switch(myPGNInstance)
					{
						case 0:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery TimeRemaining Port";
						break;
						
						case 1:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery TimeRemaining Starboard";
						break;
						
						case 2:	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Battery/Battery TimeRemaining Center";
						break;
					}
				break;
			}
			break;// battery_status		

			
			
			case "127505":	//fluid_level
		
			switch(myPGNParameter)
			{
				
						case 0:
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Center";
								break;
								
								case 3:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Fwd";
								break;
								
								case 4:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Aft";
								break;
								
								case 5:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Day1";
								break;

								case 6:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Day2";
								break;
								
								case 7:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Day3";
								break;
								
							
								
								
								
								
							}
						break;
						
						case 1:
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Water Level Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Water Level Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Water Level Center";
								break;
							}
						break;
						
						case 2:
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Waste Level Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Waste Level Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Waste Level Center";
								break;
							}
						break;
						
						case 3:
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Live Well Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Live Well Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Live Well Center";
								break;
							}
						break;
						
						
						case 4:
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Oil Level Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Oil Level Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Oil Level Center";
								break;
							}
						break;
						
						case 5:
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Black Level Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Black Level Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Black Level Center";
								break;
							}
						break;
			
			}
			
			break;// fluid_level
			
			case "130316":	//	temperature
		
	
					switch(myPGNParameter)
					{
						case 14://"EGT Temperature 0":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 0 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 0 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 0 Center";
								break;
							}
						break;
						
						case 15://"EGT Temperature 1":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 1 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 1 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 1 Center";
								break;
							}
						break;
					}
			
			case "130312":	//	temperature
		
	
					switch(myPGNParameter)
					{
						case 0://"Sea Temperature":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Water Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Water Temperature 1";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Water Temperature 2";
								break;
							}
						break;
						
						case 1://"Outside Temperature":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Outside Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Outside Temperature 1";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Outside Temperature 2";
								break;
							}
						break;
						
						case 2://"Inside Temperature":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Inside Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Inside Temperature 1";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Inside Temperature 2";
								break;
							}
						break;
						
						case 3://"Engine Room Temperature":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Engine Room Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Engine Room Temperature Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Engine Room Temperature Center";
								break;
							}
						break;
						
						
						case 4://"Main Cabin Temperature":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Main Cabin Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Main Cabin Temperature Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Main Cabin Temperature Center";
								break;
							}
						break;
						
						case 5://"Live Well":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Live Well Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Live Well Temperature Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Live Well Temperature Center";
								break;
							}
						break;
						
						case 6://"Bait Well":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Bait Well Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Bait Well Temperature Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Bait Well Temperature Center";
								break;
							}
						break;
						
						case 7://"Refrigeration":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Refrigeration 1 Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Refrigeration 2 Temperature";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Refrigeration 3 Temperature";
								break;
							}
						break;
						
						case 8://"Heating":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heating Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heating Temperature Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heating Temperature Center";
								break;
							}
						break;
						
						case 9://"Dew Point":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Dew Point";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									//myPGNTag =  "/M2M/Tank/Black Level Starboard"
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									//myPGNTag =  "/M2M/Tank/Black Level Center"
								break;
							}
						break;
						
						case 2://"Wind Chill A":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill A Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill A Temperature Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill A Temperature Center";
								break;
							}
						break;
						
						case 10://"Wind Chill T":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill T Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill T Temperature Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill T Temperature Center";
								break;
							}
						break;
						
						case 12://"Heat Index":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heat Index";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heat Index Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heat Index Center";
								break;
							}
						break;
						
						case 13://"Freezer":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Freezer Temperature";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Freezer Temperature Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Freezer Temperature Center";
								break;
							}
						break;
						
						case "130"://"Reserved 130":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/Engine Coolant Temperature Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/Engine Coolant Temperature Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/Engine Coolant Temperature Center";
								break;
							}
						break;
						
						case "134"://"Reserved 134":
							switch(myPGNInstance)
							{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Center";
								break;
							}
						break;
				
			}
			
			break;// temperature
			
			case "65286":	//	0x00FF06 seasmartdimmer
		
			switch(myPGNParameter)
			{
				case 0://"value0":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 0 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 0 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 0 Center";
								break;
						}
						break;
						
					case 1://"value1":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 1 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 1 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 1 Center";
								break;
						}
						break;

				case 2://"value2":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 2 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 2 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 2 Center";
								break;
						}
						break;

				case 3://"value3":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 3 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 3 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 3 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 4://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 4 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 4 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Dimmer/Value 4 Center";
								break;
						}
						break;						
				
					
				break;
			}
			
			break;// dimmer
			
			
			
			case "65292":	//	0x00FF0C Indicator Runtime
		
			switch(myPGNParameter)
			{
				case 0://"value0":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 0 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 0 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 0 Center";
								break;
						}
						break;
						
					case 1://"value1":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 0 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 0 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 0 Center";
								break;
						}
						break;

				case 2://"value2":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 1 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 1 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 1 Center";
								break;
						}
						break;

				case 3://"value3":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 1 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 1 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 1 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 4://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 2 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 2 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 2 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 5://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 2 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 2 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 2 Center";
								break;
						}
						break;			
						
					case 6://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 3 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 3 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 3 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 7://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 3 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 3 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 3 Center";
								break;
						}
						break;				
					
				break;	
				
				case 8://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 4 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 4 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 4 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 9://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 4 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 4 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 4 Center";
								break;
						}
						break;				
					
				break;	
				
				case 10://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 5 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 5 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 5 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 11://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 5 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 5 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 5 Center";
								break;
						}
						break;				
					
				break;	
				
				
				case 12://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 6 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 6 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 6 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 13://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 6 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 6 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 6 Center";
								break;
						}
						break;				
					
				break;	

				case 14://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 7 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 7 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Runtime 7 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 15://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 7 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 7 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Cycles 7 Center";
								break;
						}
						break;				
					
				break;				
				
				
				
				
				
				
			}
			
			break;// dimmer
			
			
			
			
			case "127501":	//	seasmartswitch
		
			switch(myPGNParameter)
			{
				case 0://"value0":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 0 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 0 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 0 Center";
								break;
						}
						break;
						
					case 1://"value1":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 1 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 1 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 1 Center";
								break;
						}
						break;

				case 2://"value2":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 2 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 2 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 2 Center";
								break;
						}
						break;

				case 3://"value3":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 3 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 3 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 3 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 4://"value4":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 4 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 4 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 4 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 5://"value5":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 5 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 5 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 5 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 6://"value6":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 6 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 6 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 6 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 7://"value7":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 7 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 7 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 7 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 8://"value8":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 8 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 8 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 8 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 9://"value9":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 9 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 9 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 9 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 10://"value10":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 10 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 10 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 10 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 11://"value11":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 11 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 11 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 11 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 12://"value12":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 12 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 12 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 12 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 13://"value13":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 13 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 13 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 13 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 14://"value14":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 14 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 14 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 14 Center";
								break;
						}
						break;						
				
					
				break;
				
				case 15://"value15":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 15 Port";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 15 Starboard";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 15 Center";
								break;
						}
						break;						
				
					
				break;
				
				
			}
			
			break;// switch
			
			case "65287":	//	0x00FF07 seasmart ac total power
		
			switch(myPGNParameter)
			{
				case 0://"UTIL":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/AC/UTIL/Energy_Phase_A";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/AC/UTIL/Energy_Phase_B";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/AC/UTIL/Energy_Phase_C";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/AC/UTIL/Energy_Avg";
								break;
						}
						break;
						
					case 1://"GEN":
						switch(myPGNInstance)
						{
								case 0:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/AC/GEN/Energy_Phase_A";
								break;
								
								case 1:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/AC/GEN/Energy_Phase_B";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/AC/GEN/Energy_Phase_C";
								break;
								
								case 2:	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/AC/GEN/Energy_Avg";
								break;
						}
						break;

						
				
					
				break;
			}
			
			
			break;// SeaSmart Custom AC_TOTAL_POWER
		

		
		

			case "65014":	//  #PGN65014: J1939 PGN 65014 - (0x00FDF6) Utility Phase A Basic AC Quantities
		
				switch(myPGNParameter)
				{
					case 1://"ac_line_neutral_volts":
						myPGNTag =  "/M2M/AC/UTIL/Volts_Phase_A";		
					break;
					
					case 0://"ac_line_line_volts":
						myPGNTag =  "/M2M/AC/UTIL/Volts_Line_Phase_A";		
					break;
					
					case 2://"ac_frequency":
						myPGNTag =  "/M2M/AC/UTIL/Frequency_Phase_A";		
					break;
					
					case 3://"ac_amps":
						myPGNTag =  "/M2M/AC/UTIL/Amps_Phase_A";		
					break;	

					case 4://"ac_watts":
						myPGNTag =  "/M2M/AC/UTIL/Power_Phase_A";		
					break;				

				}
			
			
			break;// ac_utility_basic_phase_a


			case "65011":	//  #PGN65014: J1939 PGN 65011 - (0x00FDF3) Utility Phase B Basic AC Quantities
		
				switch(myPGNParameter)
				{
					case 1://"ac_line_neutral_volts":
						myPGNTag =  "/M2M/AC/UTIL/Volts_Phase_B";		
					break;
					
					case 0://"ac_line_line_volts":
						myPGNTag =  "/M2M/AC/UTIL/Volts_Line_Phase_B";		
					break;
					
					case 2://"ac_frequency":
						myPGNTag =  "/M2M/AC/UTIL/Frequency_Phase_B";		
					break;
					
					case 3://"ac_amps":
						myPGNTag =  "/M2M/AC/UTIL/Amps_Phase_B";		
					break;	

					case 4://"ac_watts":
						myPGNTag =  "/M2M/AC/UTIL/Power_Phase_B";		
					break;				

				}
			
			
			break;// ac_utility_basic_phase_B

			case "65008":	//  #PGN65014: J1939 PGN 65008 - (0x00FDF0) Utility Phase C Basic AC Quantities
		
				switch(myPGNParameter)
				{
					case 1://"ac_line_neutral_volts":
						myPGNTag =  "/M2M/AC/UTIL/Volts_Phase_C";		
					break;
					
					case 0://"ac_line_line_volts":
						myPGNTag =  "/M2M/AC/UTIL/Volts_Line_Phase_C";		
					break;
					
					case 2://"ac_frequency":
						myPGNTag =  "/M2M/AC/UTIL/Frequency_Phase_C";		
					break;
					
					case 3://"ac_amps":
						myPGNTag =  "/M2M/AC/UTIL/Amps_Phase_C";		
					break;	

					case 4://"ac_watts":
						myPGNTag =  "/M2M/AC/UTIL/Power_Phase_C";		
					break;				

				}
			
			
			break;// ac_utility_basic_phase_C


			case "65017":	//  #PGN65017: J1939 PGN 65017 - (0x00FDF9) Utility Phase Total Basic AC Quantities
		
				switch(myPGNParameter)
				{
					case 1://"ac_line_neutral_volts":
						myPGNTag =  "/M2M/AC/UTIL/Volts_Avg";		
					break;
					
					case 0://"ac_line_line_volts":
						myPGNTag =  "/M2M/AC/UTIL/Volts_Line_Avg";		
					break;
					
					case 2://"ac_frequency":
						myPGNTag =  "/M2M/AC/UTIL/Frequency_Avg";		
					break;
					
					case 3://"ac_amps":
						myPGNTag =  "/M2M/AC/UTIL/Amps_Avg";		
					break;	

					case 4://"ac_watts":
						myPGNTag =  "/M2M/AC/UTIL/Power_Avg";		
					break;				

				}
			
			
			break;// ac_utility_basic_phase_T


			case "65005":	//  #PGN65005: J1939 PGN 65005 - (0x0FDED) Utility  Utility Total AC Energy
		
				switch(myPGNParameter)
				{
					case 0://"ac_TotalEnergy_Export":
						myPGNTag =  "/M2M/AC/UTIL/TotalEnergy_Export";		
					break;
					
					case 1://"ac_TotalEnergy_Import":
						myPGNTag =  "/M2M/AC/UTIL/TotalEnergy_Import";		
					break;

				}
			
			
			break;// ac_utility_basic_phase_a
		

			case "65027":	//  #PGN65027: J1939 PGN 65027 - (0x00FDF6) Utility Phase A Basic AC Quantities
		
				switch(myPGNParameter)
				{
					case 1://"ac_line_neutral_volts":
						myPGNTag =  "/M2M/AC/GEN/Volts_Phase_A";		
					break;
					
					case 0://"ac_line_line_volts":
						myPGNTag =  "/M2M/AC/GEN/Volts_Line_Phase_A";		
					break;
					
					case 2://"ac_frequency":
						myPGNTag =  "/M2M/AC/GEN/Frequency_Phase_A";		
					break;
					
					case 3://"ac_amps":
						myPGNTag =  "/M2M/AC/GEN/Amps_Phase_A";		
					break;	

					case 4://"ac_watts":
						myPGNTag =  "/M2M/AC/GEN/Power_Phase_A";		
					break;				

				}
			
			
			break;// ac_utility_basic_phase_a


			case "65024":	//  #PGN65024: J1939 PGN 65024 - (0x00FDF3) Utility Phase B Basic AC Quantities
		
				switch(myPGNParameter)
				{
					case 1://"ac_line_neutral_volts":
						myPGNTag =  "/M2M/AC/GEN/Volts_Phase_B";		
					break;
					
					case 0://"ac_line_line_volts":
						myPGNTag =  "/M2M/AC/GEN/Volts_Line_Phase_B";		
					break;
					
					case 2://"ac_frequency":
						myPGNTag =  "/M2M/AC/GEN/Frequency_Phase_B";		
					break;
					
					case 3://"ac_amps":
						myPGNTag =  "/M2M/AC/GEN/Amps_Phase_B";		
					break;	

					case 4://"ac_watts":
						myPGNTag =  "/M2M/AC/GEN/Power_Phase_B";		
					break;				

				}
			
			
			break;// ac_utility_basic_phase_B

			case "65021":	//  #PGN65021: J1939 PGN 65021 - (0x00FDF0) Utility Phase C Basic AC Quantities
		
				switch(myPGNParameter)
				{
					case 1://"ac_line_neutral_volts":
						myPGNTag =  "/M2M/AC/GEN/Volts_Phase_C";		
					break;
					
					case 0://"ac_line_line_volts":
						myPGNTag =  "/M2M/AC/GEN/Volts_Line_Phase_C";		
					break;
					
					case 2://"ac_frequency":
						myPGNTag =  "/M2M/AC/GEN/Frequency_Phase_C";		
					break;
					
					case 3://"ac_amps":
						myPGNTag =  "/M2M/AC/GEN/Amps_Phase_C";		
					break;	

					case 4://"ac_watts":
						myPGNTag =  "/M2M/AC/GEN/Power_Phase_C";		
					break;				

				}
			
			
			break;// ac_utility_basic_phase_C


			case "65030":	//  #PGN65030: J1939 PGN 65030 - (0x00FDF9) Generator Phase Total Basic AC Quantities
		
				switch(myPGNParameter)
				{
					case 1://"ac_line_neutral_volts":
						myPGNTag =  "/M2M/AC/GEN/Volts_Avg";		
					break;
					
					case 0://"ac_line_line_volts":
						myPGNTag =  "/M2M/AC/GEN/Volts_Line_Avg";		
					break;
					
					case 2://"ac_frequency":
						myPGNTag =  "/M2M/AC/GEN/Frequency_Avg";		
					break;
					
					case 3://"ac_amps":
						myPGNTag =  "/M2M/AC/GEN/Amps_Avg";		
					break;	

					case 4://"ac_watts":
						myPGNTag =  "/M2M/AC/GEN/Power_Avg";		
					break;				

				}
			
			
			break;// ac_gen_basic_phase_T


			case "65018":	//  #PGN65018: J1939 PGN 65018 - (0x0FDFA) Generator  Utility Total AC Energy
		
				switch(myPGNParameter)
				{
					case 0://"ac_TotalEnergy_Export":
						myPGNTag =  "/M2M/AC/GEN/TotalEnergy_Export";		
					break;
					
					case 1://"ac_TotalEnergy_Import":
						myPGNTag =  "/M2M/AC/GEN/TotalEnergy_Import";		
					break;

				}

		
		
	} // end switch
	
	return myPGNTag
	
}
function PGNTypeFromSeries(myserieskey)
{ 
//var myserieskey
var myKeys = new Array();
var myKey = new Array();
var myPGNNumber= "";
var myPGNSource= "";
var myPGNInstance= "";
var myPGNType="";
var myPGNParameter= "";
var myPGNTag="";

 try{
		myKeys = myserieskey.split(".")
		
		myKey = myKeys[1].split(":");
		myPGNNumber = myKey[1];
		
		myKey = myKeys[2].split(":");
		myPGNSource = myKey[1];
		
		myKey = myKeys[3].split(":");
		myPGNInstance = myKey[1];
		
		myKey = myKeys[4].split(":");
		myPGNType = myKey[1];
		
		myKey = myKeys[5].split(":");
		myPGNParameter = myKey[1];
		
		myPGNTag = GetPGNTypeFromSeries(myserieskey);

		if(myPGNSource == "*")
			document.getElementById("PGNTypeSource").selectedIndex =0;
		else
			document.getElementById("PGNTypeSource").selectedIndex = parseInt(myPGNSource,16)+1;
		
		document.getElementById("PGNTypeID").selectedIndex = 0;;
			
	 for(i=0; i< document.getElementById("PGNTypeID").options.length; i++)
		 {
			myEvent = document.getElementById("PGNTypeID").options[i].value;
			  if(myEvent == myPGNTag)
					document.getElementById("PGNTypeID").selectedIndex = i;
		}  
	}
	catch(err)
	{
		document.getElementById("PGNTypeID").selectedIndex = 0;
		document.getElementById("PGNTypeSource").selectedIndex =0;
	}	
	
}

function ConstructPGNTypeID(mydeviceid, dialindex )
{
var index = document.getElementById("PGNTypeID").selectedIndex;
var Source =  document.getElementById("PGNTypeSource").options[document.getElementById("PGNTypeSource").selectedIndex].value;
//var dialindex = document.getElementById("PGNDialID").selectedIndex;
var myserieskey = "";
var myPGNNumber= "";
var myPGNSource= "";
var myPGNInstance= "";
var myPGNType="";
var myPGNParameter= "";
var myEventType = document.getElementById("PGNTypeID").options[index].value

	//makePGNfromEvent(myEventType, Source);

	myserieskey = "deviceid:" + mydeviceid + ".";
   
	myserieskey = myserieskey + makePGNfromEvent(myEventType, Source);
	
	//DialPGNNumber[dialindex] = myserieskey;

}

function makePGNNumberfromEvent(myEventType, Source)
{

var myserieskey = "";
var myPGNNumber= "0";
var myPGNSource= "0";
var myPGNInstance= "0";
var myPGNType="0";
var myPGNParameter= "0";

	switch(myEventType)
	{
	
		case 0:	//	<option value="None"> -------- </option>
			myPGNNumber="";
			myPGNSource="";
			myPGNInstance="";
			myPGNType="";
			myPGNParameter="";
		break;
		
		case "/General/Heartbeat":	//	<option value="/Position">GPS Position</option>
			myPGNNumber="130944";//"heartbeat";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/General/Sessions":	//	<option value="/Position">GPS Position</option>
			myPGNNumber="130944";//"heartbeat";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		
		case "/Cellular/DB_Strength":	//	<option value="/Position">GPS Position</option>
			myPGNNumber="130942";//"cellular_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Cellular/Connect_Status":	//	<option value="/Position">GPS Position</option>
			myPGNNumber="130942";//"cellular_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;
			
		case "/Position":	//	<option value="/Position">GPS Position</option>
			myPGNNumber="129025";//"position_rapid";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
		case "/Position/lat":	//	<option value="/Position">GPS Position Lat</option>
			myPGNNumber="129025";//"position_rapid";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Position/lng":	//	<option value="/Position">GPS Position Lng</option>
			myPGNNumber="129025";//"position_rapid";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		
		case "/M2M/Navigation/Speed Over Ground":	//	<option value="/M2M/Navigation/Speed Over Ground">Navigation - Speed Over Ground </option>
			myPGNNumber="129026";//"cogsog";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		case "/M2M/Navigation/Course Over Ground":	//	<option value="/M2M/Navigation/Course Over Ground">Navigation - Speed Over Ground </option>
			myPGNNumber="129026";//"cogsog";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Navigation/Speed Over Ground Mag":	//	<option value="/M2M/Navigation/Speed Over Ground">Navigation - Speed Over Ground </option>
			myPGNNumber="129026";//"cogsog";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		case "/M2M/Navigation/Course Over Ground Mag":	//	<option value="/M2M/Navigation/Course Over Ground">Navigation - Speed Over Ground </option>
			myPGNNumber="129026";//"cogsog";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Navigation/Heading True":	//	<option value="/M2M/Navigation/Heading True">Navigation - Heading True</option>
			myPGNNumber="127250";//"vessel_heading";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Navigation/Heading Magnetic":	//	<option value="/M2M/Navigation/Heading Magnetic">Navigation - Heading Magnetic</option>
			myPGNNumber="127250";//"vessel_heading";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="1";
			myPGNParameter="0";
		break;
		
		case "/M2M/Navigation/Rudder":	//	<option value="/M2M/Navigation/Rudder">Navigation - Rudder </option>
			myPGNNumber="127245";//"rudder";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;		
		
		case "/M2M/Navigation/Rate Of Turn":	//	<option value="/M2M/Navigation/Rate Of Turn">Navigation - Rate Of Turn </option>
			myPGNNumber="127251";//"rateofturn";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	

		case "/M2M/Attitude/Pitch":	//	<option value="/M2M/Attitude/Pitch">Attitude - Pitch </option>
			myPGNNumber="127257";//"attitude";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	

		case "/M2M/Attitude/Roll":	//	<option value="/M2M/Attitude/Pitch">Attitude - Roll </option>
			myPGNNumber="127257";//"attitude";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;			
		
		case "/Environmental/Wind Speed":	//	<option value="/Environmental/Wind Speed">Wind Speed</option>
			myPGNNumber="130306";//"wind_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Wind Direction":	//	<option value="/Environmental/Wind Direction">Wind Direction</option>
			myPGNNumber="130306";//"wind_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		case "/M2M/Environmental/Wind Gust":	//	<option value="/Environmental/Wind Direction">Wind Direction</option>
			myPGNNumber="130306";//"wind_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="5";
			myPGNParameter="0";
		break;
		
		case "/M2M/Environment/Wind Speed Apparent":	//	<option value="/Environmental/Wind Speed">Wind Speed</option>
			myPGNNumber="130306";//"wind_data";
			myPGNSource=Source; 
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Environment/Wind Direction Apparent":	//	<option value="/Environmental/Wind Direction">Wind Direction</option>
			myPGNNumber="130306";//"wind_data";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		case "/Environmental/Air Pressure":	//	<option value="/Environmental/Air Pressure">Air Pressure</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
		case "/Environmental/Air Pressure Inside":	//	<option value="/Environmental/Air Pressure">Air Pressure</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
		case "/Environmental/Air Temperature":	//	<option value="/Environmental/Air Temperature">Air Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Air Temperature Inside":	//	<option value="/Environmental/Air Temperature">Air Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Outside Temperature":	//	<option value="/Environmental/Air Temperature">Air Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Water Temperature":	//	<option value="/Environmental/Water Temperature">Water Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Relative Humidity (%)":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		case "/Environmental/Temperature Inside 0":	//	<option value="/Environmental/Water Temperature">Water Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="16";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Humidity Inside 0":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="16";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
			case "/Environmental/Temperature Inside 1":	//	<option value="/Environmental/Water Temperature">Water Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="17";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Humidity Inside 1":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="17";
			myPGNType="0";
			myPGNParameter="1";
		break;

		case "/Environmental/Temperature Inside 2":	//	<option value="/Environmental/Water Temperature">Water Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="18";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Humidity Inside 2":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="18";
			myPGNType="0";
			myPGNParameter="1";
		break;

		case "/Environmental/Temperature Inside 3":	//	<option value="/Environmental/Water Temperature">Water Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="19";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Humidity Inside 3":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="19";
			myPGNType="0";
			myPGNParameter="1";
		break;

		case "/Environmental/Temperature Inside 4":	//	<option value="/Environmental/Water Temperature">Water Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="20";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Humidity Inside 4":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="20";
			myPGNType="0";
			myPGNParameter="1";
		break;

		case "/Environmental/Temperature Inside 5":	//	<option value="/Environmental/Water Temperature">Water Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="21";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Humidity Inside 5":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="21";
			myPGNType="0";
			myPGNParameter="1";
		break;

		case "/Environmental/Temperature Inside 6":	//	<option value="/Environmental/Water Temperature">Water Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="22";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Humidity Inside 6":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="22";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
			case "/Environmental/Temperature Inside 7":	//	<option value="/Environmental/Water Temperature">Water Temperature</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="23";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/Environmental/Humidity Inside 7":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="23";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		
		case "/Environmental/Humidity Inside 7":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130311";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="23";
			myPGNType="0";
			myPGNParameter="1";
		break;		

		
		
		case "/M2M/Environment/Rain Accumulation":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130946";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Environment/Rain Duration":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130946";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;			
		
		case "/M2M/Environment/Rain Rate":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130946";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;			
		
		case "/M2M/Environment/Rain Peak Rate":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="130946";//"environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;			
	
		/*
		case 0:	//	<option value="/M2M/Navigation/Speed Over Ground">Speed Over Ground </option>
		case 0:	//	<option value="/M2M/Navigation/Course over Ground">Course over Ground </option>
		case 0:	//	<option value="/M2M/Navigation/Heading True">Heading True</option>
		case 0:	//	<option value="/M2M/Navigation/Heading Magnetic">Heading Magnetic</option>
		case 0:	//	<option value="/M2M/Navigation/Depth">Water Depth </option>
		case 0:	//	<option value="/M2M/Navigation/Rate Of Turn">Rate Of Turn </option>
		case 0:	//	<option value="/General/Engine Started">Engine Started</option>
		case 0:	//	<option value="/General/Engine Stopped">Engine Stopped</option>
		case 0:	//	<option value="/General/Diesel Tank Level">Diesel Tank Level %</option>
		case 0:	//	<option value="/General/Water Tank1">Water Tank1 Level%</option>
		case 0:	//	<option value="/General/Water Tank2">Water Tank2 Level%</option>
		case 0:	//	<option value="/M2M/Battery/Battery Volts Port">Battery Volts Port </option>
		case 0:	//					<option value="/M2M/Battery/Battery Volts Starboard">Battery Volts Starboard </option>
		case 0:	//					<option value="/M2M/Battery/Battery Volts Center">Battery Volts Center </option>
		case 0:	//					<option value="/M2M/Battery/Battery Current Port">Battery Current Port </option>
		case 0:	//					<option value="/M2M/Battery/Battery Current Starboard">Battery Current Starboard </option>
		case 0:	//					<option value="/M2M/Battery/Battery Current Center">Battery Current Center </option>
		case 0:	//					<option value="/M2M/Domestic/Main Cabin Temperature">Main Cabin Temperature</option>
		case 0:	//					<option value="/M2M/Domestic/Live Well Temperature">Live Well Temperature</option>
		case 0:	//					<option value="/M2M/Domestic/Bait Well Temperature">Bait Well Temperature</option>
		case 0:	//					<option value="/M2M/Domestic/Refrigeration 1 Temperature">Refrigeration 1 Temperature</option>
		case 0:	//					<option value="/M2M/Domestic/Refrigeration 2 Temperature">Refrigeration 2 Temperature</option>
		case 0:	//					<option value="/M2M/Domestic/Heating Temperature">Heating Temperature</option>
		case 0:	//					<option value="/M2M/Domestic/Wind Chill A Temperature">Wind Chill A Temperature</option>
		case 0:	//					<option value="/M2M/Domestic/Wind Chill T Temperature">Wind Chill T Temperature</option>
		case 0:	//					<option value="/M2M/Domestic/Heat Index">Heat Index </option>
		case 0:	//					<option value="/M2M/Domestic/Freezer Temperature">Freezer Temperature</option>
		case 0:	//					<option value="/M2M/Engine/Engine RPM Port">Engine RPM Port </option>
		*/
		
		case "/M2M/Engine/Engine RPM Port":	//<option value="/M2M/Engine/Engine RPM Port">Engine RPM Port </option>
			myPGNNumber="127488";//"engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Engine/Engine Boost Port":	//<option value="/M2M/Engine/Engine Boost Port">Engine Boost Port </option>
			myPGNNumber="127488";//"engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		case "/M2M/Engine/Engine Trim Port":	//<option value="/M2M/Engine/Engine Trim Port">Engine Trim Port</option>
			myPGNNumber="127488";//"engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
		case "/M2M/Engine/Engine RPM Starboard":	//<option value="/M2M/Engine/Engine RPM Starboard">Engine RPM Starboard </option>
			myPGNNumber="127488";//"engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Engine/Engine Boost Starboard":	//<option value="/M2M/Engine/Engine Boost Starboard">Engine Boost Starboard </option>
			myPGNNumber="127488";//"engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		case "/M2M/Engine/Engine Trim Starboard":	//<option value="/M2M/Engine/Engine Trim Starboard">Engine Trim Starboard</option>
			myPGNNumber="127488";//"engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
		case "/M2M/Engine/Engine RPM Center":	//<option value="/M2M/Engine/Engine RPM Center">Engine RPM Center </option>
			myPGNNumber="127488";//"engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Engine/Engine Boost Center":	//<option value="/M2M/Engine/Engine Boost Center">Engine Boost Center </option>
			myPGNNumber="127488";//"engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		case "/M2M/Engine/Engine Trim Center":	//<option value="/M2M/Engine/Engine Trim Center">Engine Trim Center</option>
			myPGNNumber="127488";//"engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
		
		case "/M2M/Engine/Engine Temperature Port":	//<option value="/M2M/Engine/Engine Temperature Port">Engine Temperature Port</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;		

		case "/M2M/Engine/Engine OIL Temperature Port":	//<option value="/M2M/Engine/Engine OIL Temperature Port">Engine OIL Temperature Port</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	

		case "/M2M/Engine/Engine OIL Pressure Port":	//<option value="/M2M/Engine/Engine OIL Pressure Port">Engine OIL Pressure Port</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	

		case "/M2M/Engine/Engine Alternator Volts Port":	//<option value="/M2M/Engine/Engine Alternator Volts Port">Engine Alternator Volts Port</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Port":	//<option value="/M2M/Engine/Engine Fuel Rate Port">Engine Fuel Rate Port</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;	
		
		
			
		case "/M2M/Engine/Engine Trip Fuel Used Port":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Average Port":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Economy Port":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	
		
	
		case "/M2M/Engine/Engine Instantaneous Fuel Economy Port":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	
		
		
		
		
		

		case "/M2M/Engine/Engine Coolant Pressure Port":	//<option value="/M2M/Engine/Engine Coolant Pressure Port">Engine Coolant Pressure Port</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="6";
		break;	

		case "/M2M/Engine/Engine Fuel Pressure Port":	//<option value="/M2M/Engine/Engine Fuel Pressure Port">Engine Fuel Pressure Port</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="7";
		break;

		case "/M2M/Engine/Engine Coolant Temperature Port":	
			myPGNNumber="127489";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="130";
			myPGNParameter="0";
		break;			

		case "/M2M/Engine/EGT Port":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="134";
			myPGNParameter="0";
		break;			

		
		
		case "/M2M/Engine/Engine Hours Port":	//<option value="/M2M/Engine/Engine Hours Port">Engine Hours Port</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="5";
		break;		
		
		case "/M2M/Engine/Engine Temperature Starboard":	//<option value="/M2M/Engine/Engine Temperature Starboard">Engine Temperature Starboard</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="2";
		break;		

		case "/M2M/Engine/Engine OIL Temperature Starboard":	//<option value="/M2M/Engine/Engine OIL Temperature Starboard">Engine OIL Temperature Starboard</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="1";
		break;	

		case "/M2M/Engine/Engine OIL Pressure Starboard":	//<option value="/M2M/Engine/Engine OIL Pressure Starboard">Engine OIL Pressure Starboard</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="0";
		break;	

		case "/M2M/Engine/Engine Alternator Volts Starboard":	//<option value="/M2M/Engine/Engine Alternator Volts Starboard">Engine Alternator Volts Starboard</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="3";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Starboard":	//<option value="/M2M/Engine/Engine Fuel Rate Starboard">Engine Fuel Rate Starboard</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="4";
		break;	
		
		
			
		case "/M2M/Engine/Engine Trip Fuel Used Starboard":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="0";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Average Starboard":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="1";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Economy Starboard":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="2";
		break;	
		
	
		case "/M2M/Engine/Engine Instantaneous Fuel Economy Starboard":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="3";
		break;	
		
		
		
		
		

		case "/M2M/Engine/Engine Coolant Pressure Starboard":	//<option value="/M2M/Engine/Engine Coolant Pressure Starboard">Engine Coolant Pressure Starboard</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="6";
		break;	

		case "/M2M/Engine/Engine Fuel Pressure Starboard":	//<option value="/M2M/Engine/Engine Fuel Pressure Starboard">Engine Fuel Pressure Starboard</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="7";
		break;			
		
		case "/M2M/Engine/Engine Coolant Temperature Starboard":	
			myPGNNumber="127489";//"temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="130";
			myPGNParameter="0";
		break;			

		case "/M2M/Engine/EGT Starboard":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="134";
			myPGNParameter="0";
		break;			

		
		case "/M2M/Engine/Engine Hours Starboard":	//<option value="/M2M/Engine/Engine Hours Starboard">Engine Hours Starboard</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="5";
		break;	


		case "/M2M/Engine/Engine Temperature Center":	//<option value="/M2M/Engine/Engine Temperature Center">Engine Temperature Center</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="2";
		break;		

		case "/M2M/Engine/Engine OIL Temperature Center":	//<option value="/M2M/Engine/Engine OIL Temperature Center">Engine OIL Temperature Center</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="1";
		break;	

		case "/M2M/Engine/Engine OIL Pressure Center":	//<option value="/M2M/Engine/Engine OIL Pressure Center">Engine OIL Pressure Center</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="0";
		break;	

		case "/M2M/Engine/Engine Alternator Volts Center":	//<option value="/M2M/Engine/Engine Alternator Volts Center">Engine Alternator Volts Center</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="2";
		break;	

		
			case "/M2M/Engine/Engine Fuel Rate Center":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="4";
		break;	
		
		
	
		case "/M2M/Engine/Engine Trip Fuel Used Center":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="0";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Average Center":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="1";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Economy Center":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="2";
		break;	
		
	
		case "/M2M/Engine/Engine Instantaneous Fuel Economy Center":	
			myPGNNumber="127497"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="3";
		break;	
		
		
		

		case "/M2M/Engine/Engine Coolant Pressure Center":	
			myPGNNumber="127489"; //"Trip Parameters, Engine";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="6";
		break;	

		case "/M2M/Engine/Engine Fuel Pressure Center":	//<option value="/M2M/Engine/Engine Fuel Pressure Center">Engine Fuel Pressure Center</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="7";
		break;		

		case "/M2M/Engine/Engine Coolant Temperature Center":	
			myPGNNumber="127489";//"temperature";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="130";
			myPGNParameter="0";
		break;			

		case "/M2M/Engine/EGT Center":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="134";
			myPGNParameter="0";
		break;			
		
		case "/M2M/Engine/Engine Hours Center":	//<option value="/M2M/Engine/Engine Hours Center">Engine Hours Center</option>
			myPGNNumber="127489";//"engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="5";
		break;	

		case "/M2M/Engine/Transmission OIL Pressure Port":	//<option value="/M2M/Engine/Transmission OIL Pressure Port">Transmission OIL Pressure Port </option>
			myPGNNumber="127493";//"transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Engine/Transmission OIL Temperature Port":	//<option value="/M2M/Engine/Transmission OIL Temperature Port">Transmission OIL Temperature Port </option>
			myPGNNumber="127493";//"transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	

		case "/M2M/Engine/Transmission OIL Pressure Starboard":	//<option value="/M2M/Engine/Transmission OIL Pressure Starboard">Transmission OIL Pressure Starboard </option>
			myPGNNumber="127493";//"transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Engine/Transmission OIL Temperature Starboard":	//<option value="/M2M/Engine/Transmission OIL Temperature Starboard">Transmission OIL Temperature Starboard </option>
			myPGNNumber="127493";//"transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="1";
		break;		
		
		case "/M2M/Engine/Transmission OIL Pressure Center":	//<option value="/M2M/Engine/Transmission OIL Pressure Center">Transmission OIL Pressure Center </option>
			myPGNNumber="127493";//"transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Engine/Transmission OIL Temperature Center":	//<option value="/M2M/Engine/Transmission OIL Temperature Center">Transmission OIL Temperature Center </option>
			myPGNNumber="127493";//"transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="1";
		break;	

		case "/M2M/Battery/Battery Volts Port":	
			myPGNNumber="127508";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Battery/Battery Current Port":	
			myPGNNumber="127508";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;		
		
		case "/M2M/Battery/Battery Temperature Port":	
			myPGNNumber="127508";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	

		case "/M2M/Battery/Battery StateOfCharge Port":	
			myPGNNumber="127506";//"battery_status detail";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Battery";
			myPGNParameter="0";
		break;	

		case "/M2M/Battery/Battery TimeRemaining Port":	
			myPGNNumber="127506";//"battery_status detail";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Battery";
			myPGNParameter="2";
		break;	



		case "/M2M/Battery/Battery Volts Starboard":	
			myPGNNumber="127508";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Battery/Battery Current Starboard":	
			myPGNNumber="127508";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="1";
		break;		
		
		case "/M2M/Battery/Battery Temperature Starboard":	
			myPGNNumber="127508";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="2";
		break;	

		
		case "/M2M/Battery/Battery StateOfCharge Starboard":	
			myPGNNumber="127506";//"battery_status detail";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="Battery";
			myPGNParameter="0";
		break;	

		case "/M2M/Battery/Battery TimeRemaining Starboard":	
			myPGNNumber="127506";//"battery_status detail";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="Battery";
			myPGNParameter="0";
		break;	


		
		
		

		case "/M2M/Battery/Battery Volts Center":	
			myPGNNumber="127508";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Battery/Battery Current Center":	
			myPGNNumber="127508";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="1";
		break;		
		
		case "/M2M/Battery/Battery Temperature Center":	
			myPGNNumber="127508";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="2";
		break;	
		
		
		case "/M2M/Battery/Battery StateOfCharge Center":	
			myPGNNumber="127506";//"battery_status detail";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="Battery";
			myPGNParameter="0";
		break;	

		case "/M2M/Battery/Battery TimeRemaining Center":	
			myPGNNumber="127506";//"battery_status detail";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="Battery";
			myPGNParameter="2";
		break;	


		
		
		
		
		case "/M2M/Battery/Battery Volts J1939":	
			myPGNNumber="65271";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	
				
		case "/M2M/Battery/Battery Current J1939":	
			myPGNNumber="65271";//"battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Engine/Generator RPM J1939":	//<option value="/M2M/Engine/Engine RPM Center">Engine RPM Center </option>
			myPGNNumber="61444";//"engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;
		
		
		case "/M2M/Engine/Generator Temperature J1939":	//<option value="/M2M/Engine/Generator Temperature J1939">Generator - J1939 - Temperature</option>
			myPGNNumber="65262";//
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		case "/M2M/Engine/Generator OIL Temperature J1939":	//<option value="/M2M/Engine/Generator Temperature J1939">Generator - J1939 - Temperature</option>
			myPGNNumber="65262";//
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
		case "/M2M/Engine/Generator Fuel Temperature J1939":	//<option value="/M2M/Engine/Generator Fuel Temperature J1939">Generator - J1939 - Temperature</option>
			myPGNNumber="65262";//
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;

		
		case "/M2M/Engine/Generator OIL Pressure J1939":	//<option value="/M2M/Engine/Generator OIL Pressure J1939">Generator - J1939 - OIL Pressure</option>
			myPGNNumber="65263";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;
		
		case "/M2M/Engine/Generator Transmission Pressure J1939":	//<option value="/M2M/Engine/Generator OIL Pressure J1939">Generator - J1939 - OIL Pressure</option>
			myPGNNumber="65272";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;
		
		case "/M2M/Engine/Generator Transmission Temperature J1939":	//<option value="/M2M/Engine/Generator OIL Pressure J1939">Generator - J1939 - OIL Pressure</option>
			myPGNNumber="65272";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;
		
		case "/M2M/Engine/Generator Alternator Volts J1939": //	<option value="/M2M/Engine/Generator Alternator Volts J1939">Generator - J1939 - Alternator Volts</option>
			myPGNNumber="65271";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
		case "/M2M/Engine/Generator Alternator Current J1939": //	<option value="/M2M/Engine/Generator Alternator Volts J1939">Generator - J1939 - Alternator Volts</option>
			myPGNNumber="65271";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;

		
		
		case "/M2M/Engine/Generator Fuel Level J1939": //	<option value="/M2M/Engine/Generator Fuel Level J1939">Generator - J1939 - Alternator Volts</option>
			myPGNNumber="65276";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;

		case "/M2M/Engine/Generator Fuel Rate J1939": //	<option value="/M2M/Engine/Generator Fuel Rate J1939">Generator - J1939 - Alternator Volts</option>
			myPGNNumber="65266";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;
		
		
		
		case "/M2M/AC/UTIL/Energy_Phase_A":	
			myPGNNumber="65287"; //"SeaSmart ac watt hours ";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;		
		
		case "/M2M/AC/UTIL/Energy_Phase_B":	
			myPGNNumber="65287"; //"SeaSmart ac watt hours ";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="0";
		break;			
		
			case "/M2M/AC/UTIL/Energy_Phase_C":	
			myPGNNumber="65287"; //"SeaSmart ac watt hours ";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="0";
		break;		
		
		case "/M2M/AC/UTIL/Energy_Avg":	
			myPGNNumber="65287"; //"SeaSmart ac watt hours ";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/AC/UTIL/Volts_Line_Phase_A":			
			myPGNNumber="65014"; //J1939 PGN 65014 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	


		case "/M2M/AC/UTIL/Volts_Phase_A":			
			myPGNNumber="65014"; //J1939 PGN 65014 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	


		case "/M2M/AC/UTIL/Amps_Phase_A":			
			myPGNNumber="65014"; //J1939 PGN 65014 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	


		case "/M2M/AC/UTIL/Frequency_Phase_A":			
			myPGNNumber="65014"; //J1939 PGN 65014 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	


		case "/M2M/AC/UTIL/Power_Phase_A":			
			myPGNNumber="65014"; //J1939 PGN 65014 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;	

		case "/M2M/AC/UTIL/Volts_Line_Phase_B":			
			myPGNNumber="65011"; //J1939 PGN 65011 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	


		case "/M2M/AC/UTIL/Volts_Phase_B":			
			myPGNNumber="65011"; //J1939 PGN 65011 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	


		case "/M2M/AC/UTIL/Amps_Phase_B":			
			myPGNNumber="65011"; //J1939 PGN 65011 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	


		case "/M2M/AC/UTIL/Frequency_Phase_B":			
			myPGNNumber="65011"; //J1939 PGN 65011 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	


		case "/M2M/AC/UTIL/Power_Phase_B":			
			myPGNNumber="65011"; //J1939 PGN 65011 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;	

		
		case "/M2M/AC/UTIL/Volts_Line_Phase_C":			
			myPGNNumber="65008"; //J1939 PGN 65008 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	


		case "/M2M/AC/UTIL/Volts_Phase_C":			
			myPGNNumber="65008"; //J1939 PGN 65008 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	


		case "/M2M/AC/UTIL/Amps_Phase_C":			
			myPGNNumber="65008"; //J1939 PGN 65008 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	


		case "/M2M/AC/UTIL/Frequency_Phase_C":			
			myPGNNumber="65008"; //J1939 PGN 65008 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	


		case "/M2M/AC/UTIL/Power_Phase_C":			
			myPGNNumber="65008"; //J1939 PGN 65008 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;	
		
		
		case "/M2M/AC/UTIL/Volts_Line_Avg":			
			myPGNNumber="65017"; //J1939 PGN 65014 - (0x00FDF6) Utility Phase T Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	


		case "/M2M/AC/UTIL/Volts_Avg":			
			myPGNNumber="65017"; //J1939 PGN 65014 - (0x00FDF6) Utility Phase T Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	


		case "/M2M/AC/UTIL/Amps_Avg":			
			myPGNNumber="65017"; //J1939 PGN 65014 - (0x00FDF6) Utility Phase T Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	


		case "/M2M/AC/UTIL/Frequency_Avg":			
			myPGNNumber="65017"; //J1939 PGN 65014 - (0x00FDF6) Utility Phase T Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	


		case "/M2M/AC/UTIL/Power_Avg":			
			myPGNNumber="65017"; //J1939 PGN 65014 - (0x00FDF6) Utility Phase T Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;	
		
		case "/M2M/AC/UTIL/TotalEnergy_Import":			
			myPGNNumber="65005"; //J1939 PGN 65005 - (0x00FDED) UTILITY TOTAL AC ENERGY
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/AC/UTIL/TotalEnergy_Export":			
			myPGNNumber="65005"; //J1939 PGN 65005 - (0x00FDED) UTILITY TOTAL AC ENERGY
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	
		
		
		case "/M2M/AC/GEN/Energy_Phase_A":	
			myPGNNumber="65287"; //"SeaSmart ac watt hours ";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;		
		
		case "/M2M/AC/GEN/Energy_Phase_B":	
			myPGNNumber="65287"; //"SeaSmart ac watt hours ";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="1";
		break;			
		
			case "/M2M/AC/GEN/Energy_Phase_C":	
			myPGNNumber="65287"; //"SeaSmart ac watt hours ";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="1";
		break;		
		
		case "/M2M/AC/GEN/Energy_Avg":	
			myPGNNumber="65287"; //"SeaSmart ac watt hours ";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="0";
			myPGNParameter="1";
		break;	
		
		case "/M2M/AC/GEN/Volts_Line_Phase_A":			
			myPGNNumber="65027"; //J1939 PGN 65027 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	


		case "/M2M/AC/GEN/Volts_Phase_A":			
			myPGNNumber="65027"; //J1939 PGN 65027 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	


		case "/M2M/AC/GEN/Amps_Phase_A":			
			myPGNNumber="65027"; //J1939 PGN 65027 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	


		case "/M2M/AC/GEN/Frequency_Phase_A":			
			myPGNNumber="65027"; //J1939 PGN 65027 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	


		case "/M2M/AC/GEN/Power_Phase_A":			
			myPGNNumber="65027"; //J1939 PGN 65027 - (0x00FDF6) Utility Phase A Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;	

		case "/M2M/AC/GEN/Volts_Line_Phase_B":			
			myPGNNumber="65024"; //J1939 PGN 65024 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	


		case "/M2M/AC/GEN/Volts_Phase_B":			
			myPGNNumber="65024"; //J1939 PGN 65024 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	


		case "/M2M/AC/GEN/Amps_Phase_B":			
			myPGNNumber="65024"; //J1939 PGN 65024 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	


		case "/M2M/AC/GEN/Frequency_Phase_B":			
			myPGNNumber="65024"; //J1939 PGN 65024 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	


		case "/M2M/AC/GEN/Power_Phase_B":			
			myPGNNumber="65024"; //J1939 PGN 65024 - (0x00FDF6) Utility Phase B Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;	

		
		case "/M2M/AC/GEN/Volts_Line_Phase_C":			
			myPGNNumber="65021"; //J1939 PGN 65021 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	


		case "/M2M/AC/GEN/Volts_Phase_C":			
			myPGNNumber="65021"; //J1939 PGN 65021 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	


		case "/M2M/AC/GEN/Amps_Phase_C":			
			myPGNNumber="65021"; //J1939 PGN 65021 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	


		case "/M2M/AC/GEN/Frequency_Phase_C":			
			myPGNNumber="65021"; //J1939 PGN 65021 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	


		case "/M2M/AC/GEN/Power_Phase_C":			
			myPGNNumber="65021"; //J1939 PGN 65021 - (0x00FDF6) Utility Phase C Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;	
		
		
		case "/M2M/AC/GEN/Volts_Line_Avg":			
			myPGNNumber="65030"; //J1939 PGN 65030 - (0x00FDF6) Utility Phase T Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	


		case "/M2M/AC/GEN/Volts_Avg":			
			myPGNNumber="65030"; //J1939 PGN 65030 - (0x00FDF6) Utility Phase T Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	


		case "/M2M/AC/GEN/Amps_Avg":			
			myPGNNumber="65030"; //J1939 PGN 65030 - (0x00FDF6) Utility Phase T Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;	


		case "/M2M/AC/GEN/Frequency_Avg":			
			myPGNNumber="65030"; //J1939 PGN 65030 - (0x00FDF6) Utility Phase T Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	


		case "/M2M/AC/GEN/Power_Avg":			
			myPGNNumber="65030"; //J1939 PGN 65030 - (0x00FDF6) Utility Phase T Basic AC Quantities
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;	
		
		case "/M2M/AC/GEN/TotalEnergy_Import":			
			myPGNNumber="65018"; //J1939 PGN 65018 - (0x00FDED) UTILITY TOTAL AC ENERGY
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/AC/GEN/TotalEnergy_Export":			
			myPGNNumber="65018"; //J1939 PGN 65018 - (0x00FDED) UTILITY TOTAL AC ENERGY
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;		
		
		
		case "/M2M/Tank/Fuel Level Port":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Tank/Fuel Level Starboard":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Tank/Fuel Level Center":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="0";
		break;
		
		
		case "/M2M/Tank/Fuel Level Fwd":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Tank/Fuel Level Aft":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Tank/Fuel Level Day1":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNParameter="0";
		break;
				
		case "/M2M/Tank/Fuel Level Day2":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="6";
	
			myPGNParameter="0";
		break;	
		
		case "/M2M/Tank/Fuel Level Day3":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNParameter="0";
		break;		
		
		
		
		
		
		
		
		

		case "/M2M/Tank/Water Level Port":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="1";
		break;	
		
		case "/M2M/Tank/Water Level Starboard":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="1";
		break;	
		
		case "/M2M/Tank/Water Level Center":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="1";
		break;		
		
		case "/M2M/Tank/Waste Level Port":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="2";
		break;	
		
		case "/M2M/Tank/Waste Level Starboard":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="2";
		break;	
		
		case "/M2M/Tank/Waste Level Center":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="2";
		break;		
						
		case "/M2M/Tank/Live Well Port":	
			myPGNNumber="129025";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="3";
		break;	
		
		case "/M2M/Tank/Live Well Starboard":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="3";
		break;	
		
		case "/M2M/Tank/Live Well Center":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="3";
		break;	
		
		case "/M2M/Tank/Oil Level Port":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="4";
		break;	
		
		case "/M2M/Tank/Oil Level Starboard":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="4";
		break;	
		
		case "/M2M/Tank/Oil Level Center":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="4";
		break;	

		case "/M2M/Tank/Black Water Level Port":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="5";
		break;	
		
		case "/M2M/Tank/Black Water Level Starboard":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="5";
		break;	
		
		case "/M2M/Tank/Black Water Level Center":	
			myPGNNumber="127505";//"fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="5";
		break;	
		
		
		case "/M2M/Domestic/Water Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Domestic/Outside Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="1";
		break;	
		
		case "/M2M/Domestic/Inside Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="2";
		break;	
		
		case "/M2M/Domestic/Engine Room Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="3";
		break;	
		
		case "/M2M/Domestic/Main Cabin Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="4";
		break;	
		
		case "/M2M/Domestic/Live Well Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="5";
		break;	

		
		case "/M2M/Domestic/Bait Well Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="6";
		break;	

		
		case "/M2M/Domestic/Refrigeration 1 Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="7";
		break;	

		case "/M2M/Domestic/Refrigeration 2 Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="7";
		break;	
		
		case "/M2M/Domestic/Heating Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="8";
		break;	
		
		case "/M2M/Domestic/Dew Point":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="9";
		break;	
		
		case "/M2M/Domestic/Freezer Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="13";
		break;	
		
		case "/M2M/Domestic/Freezer Temperature Starboard":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="13";
		break;	
		
		case "/M2M/Domestic/Freezer Temperature Center":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="13";
		break;	

		
		case "/M2M/Domestic/Wind Chill A Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="10";
		break;	


		
		case "/M2M/Domestic/Wind Chill T Temperature":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="11";
		break;	

		
		case "/M2M/Domestic/Heat Index":	
			myPGNNumber="130312";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="12";
		break;	
		
		
		case "/M2M/Engine/EGT 0 Port":	
			myPGNNumber="130316";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="14";
		break;	
		
		
		case "/M2M/Engine/EGT 0 Starboard":	
			myPGNNumber="130316";//"temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="14";
		break;	

		
				
		
		case "/M2M/Engine/EGT 0 Center":	
			myPGNNumber="130316";//"temperature";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="14";
		break;	

		
		
		
		case "/M2M/Engine/EGT 1 Port":	
			myPGNNumber="130316";//"temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="15";
		break;	
		
		
		case "/M2M/Engine/EGT 1 Starboard":	
			myPGNNumber="130316";//"temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="15";
		break;	

		
				
		
		case "/M2M/Engine/EGT 1 Center":	
			myPGNNumber="130316";//"temperature";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="15";
		break;	

		
		
		
		case "/M2M/Dimmer/Value 0 Port":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="0";
		break;	

		case "/M2M/Dimmer/Value 1 Port":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="1";
		break;	
		case "/M2M/Dimmer/Value 2 Port":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="2";
		break;	
		
		case "/M2M/Dimmer/Value 3 Port":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="3";
		break;	
		
		case "/M2M/Dimmer/Value 4 Port":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNParameter="4";
		break;	
		
		case "/M2M/Dimmer/Value 0 Starboard":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="0";
		break;	

		case "/M2M/Dimmer/Value 1 Starboard":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="1";
		break;	
		case "/M2M/Dimmer/Value 2 Starboard":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="2";
		break;	
		
		case "/M2M/Dimmer/Value 3 Starboard":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="3";
		break;	
		
		case "/M2M/Dimmer/Value 4 Starboard":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNParameter="4";
		break;	
		
		case "/M2M/Dimmer/Value 0 Center":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="0";
		break;	

		case "/M2M/Dimmer/Value 1 Center":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="1";
		break;	
		case "/M2M/Dimmer/Value 2 Center":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="2";
		break;	
		
		case "/M2M/Dimmer/Value 3 Center":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="3";
		break;	
		
		case "/M2M/Dimmer/Value 4 Center":	
			myPGNNumber="65286";//"seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNParameter="4";
		break;	
		

	
		
		case "/M2M/Switch/Value 0 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Switch/Runtime 0 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Switch/Cycles 0 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;	
		
		case "/M2M/Switch/Value 1 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		
		case "/M2M/Switch/Runtime 1 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;	
		
		case "/M2M/Switch/Cycles 1 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;			
		
		case "/M2M/Switch/Value 2 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
				
		case "/M2M/Switch/Runtime 2 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;	
		
		case "/M2M/Switch/Cycles 2 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="5";
		break;	
		
		case "/M2M/Switch/Value 3 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="3";
		break;
		
				
		case "/M2M/Switch/Runtime 3 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="6";
		break;	
		
		case "/M2M/Switch/Cycles 3 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="7";
		break;	
		
		case "/M2M/Switch/Value 4 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="4";
		break;
		
		
		case "/M2M/Switch/Runtime 4 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="8";
		break;	
		
		case "/M2M/Switch/Cycles 4 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="9";
		break;			
		
		case "/M2M/Switch/Value 5 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="5";
		break;
		
		case "/M2M/Switch/Runtime 5 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="10";
		break;	
		
		case "/M2M/Switch/Cycles 5 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="11";
		break;			
		
		case "/M2M/Switch/Value 6 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="6";
		break;
		
		case "/M2M/Switch/Runtime 6 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="12";
		break;	
		
		case "/M2M/Switch/Cycles 6 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="13";
		break;		
		
		case "/M2M/Switch/Value 7 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="7";
		break;
		
		case "/M2M/Switch/Runtime 7 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="14";
		break;	
		
		case "/M2M/Switch/Cycles 7 Port":	
			myPGNNumber="65292";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="15";
		break;	
		
		case "/M2M/Switch/Value 8 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="8";
		break;
		
		
		case "/M2M/Switch/Value 9 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="9";
		break;
		
		case "/M2M/Switch/Value 10 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="10";
		break;
		
		case "/M2M/Switch/Value 11 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="11";
		break;
		
		case "/M2M/Switch/Value 12 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="12";
		break;
		
		case "/M2M/Switch/Value 13 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="13";
		break;
		
		case "/M2M/Switch/Value 14 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="14";
		break;
		
		case "/M2M/Switch/Value 15 Port":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="15";
		break;
		
		
	
		
		case "/M2M/Switch/Value 0 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Switch/Value 1 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		case "/M2M/Switch/Value 2 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
		case "/M2M/Switch/Value 3 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="3";
		break;
		
		case "/M2M/Switch/Value 4 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="4";
		break;
		
		case "/M2M/Switch/Value 5 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="5";
		break;
		
		case "/M2M/Switch/Value 6 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="6";
		break;
		
		case "/M2M/Switch/Value 7 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="7";
		break;
		
		case "/M2M/Switch/Value 8 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="8";
		break;
		
		
		case "/M2M/Switch/Value 9 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="9";
		break;
		
		case "/M2M/Switch/Value 10 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="10";
		break;
		
		case "/M2M/Switch/Value 11 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="11";
		break;
		
		case "/M2M/Switch/Value 12 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="12";
		break;
		
		case "/M2M/Switch/Value 13 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="13";
		break;
		
		case "/M2M/Switch/Value 14 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="14";
		break;
		
		case "/M2M/Switch/Value 15 Starboard":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="15";
		break;		
		
	

	
		
		case "/M2M/Switch/Value 0 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="0";
		break;	
		
		case "/M2M/Switch/Value 1 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="1";
		break;
		
		case "/M2M/Switch/Value 2 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="2";
		break;
		
		case "/M2M/Switch/Value 3 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="3";
		break;
		
		case "/M2M/Switch/Value 4 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="4";
		break;
		
		case "/M2M/Switch/Value 5 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="5";
		break;
		
		case "/M2M/Switch/Value 6 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="6";
		break;
		
		case "/M2M/Switch/Value 7 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="7";
		break;
		
		case "/M2M/Switch/Value 8 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="8";
		break;
		
		
		case "/M2M/Switch/Value 9 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="9";
		break;
		
		case "/M2M/Switch/Value 10 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="10";
		break;
		
		case "/M2M/Switch/Value 11 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="11";
		break;
		
		case "/M2M/Switch/Value 12 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="12";
		break;
		
		case "/M2M/Switch/Value 13 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="13";
		break;
		
		case "/M2M/Switch/Value 14 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="14";
		break;
		
		case "/M2M/Switch/Value 15 Center":	
			myPGNNumber="127501";//"seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="15";
		break;		
		



	
		/*
		case 0:	//					<option value="/M2M/Tank/Fuel Level Port">Fuel Level Port </option>
		case 0:	//					<option value="/M2M/Tank/Fuel Level Starboard">Fuel Level Starboard </option>
		case 0:	//					<option value="/M2M/Tank/Fuel Level Center">Fuel Level Center </option>
		case 0:	//					<option value="/M2M/Tank/Water Level Port">Water Level Port </option>
		case 0:	//					<option value="/M2M/Tank/Water Level Starboard">Water Level Starboard </option>
		case 0:	//					<option value="/M2M/Tank/Water Level Center">Water Level Center </option>
		case 0:	//					<option value="/M2M/Tank/Black Water Level Port">Black Water Level Port </option>
		case 0:	//					<option value="/M2M/Tank/Black Level Starboard">Black Level Starboard </option>
		case 0:	//					<option value="/M2M/Tank/Black Level Center">Black Level Center </option>
		
		
		case 0:	//					<option value="/M2M/Engine/Engine Temperature Port">Engine Temperature Port </option>
		case 0:	//					<option value="/M2M/Engine/Engine Temperature Starboard">Engine Temperature Starboard </option>
		case 0:	//					<option value="/M2M/Engine/Engine Temperature Center">Engine Temperature Center </option>
		case 0:	//					<option value="/M2M/Engine/Engine OIL Temperature Port">Engine OIL Temperature Port </option>
		case 0:	//					<option value="/M2M/Engine/Engine OIL Temperature Starboard">Engine OIL Temperature Starboard </option>
		case 0:	//					<option value="/M2M/Engine/Engine OIL Temperature Center">Engine OIL Temperature Center </option>
		case 0:	//					<option value="/M2M/Engine/Engine OIL Pressure Port">Engine OIL Pressure Port </option>
		case 0:	//					<option value="/M2M/Engine/Engine OIL Pressure Starboard">Engine OIL Pressure Starboard </option>
		case 0:	//					<option value="/M2M/Engine/Engine OIL Pressure Center">Engine OIL Pressure Center </option>
		case 0:	//					<option value="/M2M/Engine/Engine Alternator Volts Port">Engine Alternator Volts Port </option>
		case 0:	//					<option value="/M2M/Engine/Engine Alternator Volts Starboard">Engine Alternator Volts Starboard </option>
		case 0:	//					<option value="/M2M/Engine/Engine Alternator Volts Center">Engine Alternator Volts Center </option>
		case 0:	//					<option value="/M2M/Engine/Engine Hours Port">Engine Hours Port </option>
		case 0:	//					<option value="/M2M/Engine/Engine Hours Starboard">Engine Hours Starboard </option>
		case 0:	//					<option value="/M2M/Engine/Engine Hours Center">Engine Hours Center </option>
		case 0:	//					<option value="/M2M/Engine/Engine Fuel Pressure Port">Engine Fuel Pressure Port </option>
		case 0:	//					<option value="/M2M/Engine/Engine Fuel Pressure Starboard">Engine Fuel Pressure Starboard </option>
		case 0:	//					<option value="/M2M/Engine/Engine Fuel Pressure Center">Engine Fuel Pressure Center </option>
		case 0:	//					<option value="/M2M/Engine/Transmission OIL Temperature Port">Transmission OIL Temperature Port </option>
		case 0:	//					<option value="/M2M/Engine/Transmission OIL Temperature Starboard">Transmission OIL Temperature Starboard </option>
		case 0:	//					<option value="/M2M/Engine/Transmission OIL Temperature Center">Transmission OIL Temperature Center </option>
		case 0:	//					<option value="/M2M/Engine/Transmission OIL Pressure Port">Transmission OIL Pressure Port </option>
		case 0:	//					<option value="/M2M/Engine/Transmission OIL Pressure Starboard">Transmission OIL Pressure Starboard </option>
		case 0:	//					<option value="/M2M/Engine/Transmission OIL Pressure Center">Transmission OIL Pressure Center </option>
		*/
		/*
		case 0:	//					<option value="/M2M/Engine/Engine Room Temperature">Engine Room Temperature</option>
		case 0:	//					<option value="/M2M/Engine/EGT Port">EGT Port </option>
		case 0:	//					<option value="/M2M/Engine/EGT Starboard">EGT Starboard </option>
		case 0:	//					<option value="/M2M/Engine/EGT Center">EGT Center </option>
		case 0:	//					<option value="/M2M/Environment/Wind Direction True">Wind Direction True</option>
		case 0:	//					<option value="/M2M/Environment/Wind Direction Apparent">Wind Direction Apparent</option>
		case 0:	//					<option value="/M2M/Environment/Wind Speed True">Wind Speed True</option>
		case 0:	//					<option value="/M2M/Environment/Wind Speed Apparent">Wind Speed Apparent</option>
		case 0:	//					<option value="/M2M/Environment/Water Temperature">Water Temperature </option>
		case 0:	//					<option value="/M2M/Environment/Outside Temperature">Outside Temperature </option>
		case 0:	//					<option value="/M2M/Environment/Inside Temperature">Inside Temperature </option>

		case 0:	//					<option value="/M2M/Instruments/Tracker Battery Voltage">Tracker Battery Voltage</option>			</select>
*/
	}// end of switch
		
//var mydeviceid = document.getElementById("DeviceID").value;
			
		   // myserieskey = "deviceid:" + mydeviceid;
            myserieskey =  "sensor:" + myPGNNumber;
            myserieskey = myserieskey  + ".source:" + myPGNSource;
            myserieskey = myserieskey  + ".instance:" + myPGNInstance;
            myserieskey = myserieskey  + ".type:" + myPGNType;
            myserieskey = myserieskey  + ".parameter:" + myPGNParameter;
            myserieskey = myserieskey  + ".HelmSmart"; 
			
			return myserieskey;
			
		//DialPGNNumber[dialindex] = myserieskey;
		
} 