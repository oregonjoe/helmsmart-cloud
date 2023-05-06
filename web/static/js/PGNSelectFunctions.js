function GetPGNTypeFromSeries(myserieskey)
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

//var dialindex=document.getElementById("DialID").selectedIndex;
	myserieskey = myserieskey.replace(".*.","*.");
	//myserieskey = DialPGNNumber[dialindex] ;
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
	
	
	

	
	
	switch(myPGNNumber)
	{
		
		
		case "helmsmartstat":	
		
			//switch(myPGNParameter)
			//{
				//case "timestamp":
					myPGNTag =  "/General/Status";
				//break;
					

			//}
	
		break; // position		
		
		
		case "heartbeat":	
		
			
			switch(myPGNParameter)
			{
				case "timestamp":
					myPGNTag =  "/General/Heartbeat";
				break;
		
				case "sessionid":	
					myPGNTag =  "/General/Sessions";
				break;
			
					

			}
			
			
	
		break; // heartbeat		
		
		case "cellular_status":	
		
			
			switch(myPGNParameter)
			{
				case "db_status":
					myPGNTag =  "/Cellular/DB_Strength";
				break;
		
				case "ai_status":	
					myPGNTag =  "/Cellular/Connect_Status";
				break;
			
					

			}
			
			
	
		break; // heartbeat				
		
		case "position_rapid":	
		
			switch(myPGNParameter)
			{
				case "latlng":
					myPGNTag =  "/Position";
				break;
		
				case "lat":	
					myPGNTag =  "/Position/lat";
				break;
					
				case "lng":	
					myPGNTag =  "/Position/lng";
				break;
					

			}
	
		break; // position
		
		case "cogsog":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "speed_over_ground":
				switch(myPGNType)
				{
					case "True":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Speed Over Ground";
					break;
					
					case "Magnetic":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Speed Over Ground Mag";
					break;
					
		
					
				}
				break;
				
				case "course_over_ground":
				switch(myPGNType)
				{
					case "True":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Course Over Ground";
					break;
					
					case "Magnetic":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Course Over Ground Mag";
					break;
					

					
				}
				break;
			}	
		break; // cogsog
		
		case "heading":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "heading":
				switch(myPGNType)
				{
					case "True":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Heading True";
					break;
					
					case "Magnetic":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Heading Magnetic";
					break;
					
		
					
				}
				break;
				
				
			}	
		break; // vessel_heading
		
		case "rudder":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "position":
				switch(myPGNType)
				{
					case "True":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Rudder";
					break;
					
					case "Magnetic":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Navigation/Rudder Mag";
					break;
					
		
					
				}
				break;
				
				
			}	
		break; // rudder	

		case "rot":	//	<option value="None"> -------- </option>
			switch(myPGNParameter)
			{
				case "rateofturn":
					myPGNTag =  "/M2M/Navigation/Rate Of Turn";
				break;
				
				
			}	
		break; // rateofturn		

		case "water_depth":	//	<option value="None"> -------- </option>
			switch(myPGNParameter)
			{
				case "depth":
					myPGNTag =  "/M2M/Navigation/Depth";
				break;
			}	
		break; // water depth	
		
		case "water_speed":	//	<option value="None"> -------- </option>
			switch(myPGNParameter)
			{
				case "waterspeed":
					myPGNTag =  "/M2M/Navigation/Water Speed";
				break;
			}	
		break; // waterspeed		
		
		
		case "attitude":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "pitch":
				
					myPGNTag =  "/M2M/Attitude/Pitch";
				
				break;
				
				case "roll":
				
					 myPGNTag =  "/M2M/Attitude/Roll";
				
				break;
			}	
		break; // attitude
		
		case "rain_gauge":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "accumulation":
				
					myPGNTag =  "/M2M/Environment/Rain Accumulation";
				
				break;
				
				case "rainduration":
				
					 myPGNTag =  "/M2M/Environment/Rain Duration";
				
				break;
				
				case "rate":
				
					 myPGNTag =  "/M2M/Environment/Rain Rate";
				
				break;
				
				case "peak":
				
					 myPGNTag =  "/M2M/Environment/Rain Peak Rate";
				
				break;
			}	
		break; // attitude		
		
		case "environmental_data":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "temperature":
				switch(myPGNType)
				{
					case "Sea Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Water Temperature";
					break;
					
					case "Outside Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Temperature";
					break;
					
					case "Inside Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Temperature Inside";
					break;
					
					case "Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Inside Temperature";
					break;
					
					case "Inside Zone0":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 0";
					break;
					
					case "Inside Zone1":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 1";
					break;
					
					case "Inside Zone2":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 2";
					break;
					
					case "Inside Zone3":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 3";
					break;
					
					case "Inside Zone4":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 4";
					break;
					
					case "Inside Zone5":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 5";
					break;
					
					case "Inside Zone6":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 6";
					break;
					
					case "Inside Zone7":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Temperature Inside 7";
					break;
					
				}
				break;
				
				case "atmospheric_pressure":
				switch(myPGNType)
				{
					case "Sea Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Pressure";
					break;
					
					case "Outside Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Pressure";
					break;
					
					case "Inside Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Pressure";
					break;
					
					case "Engine Room Temperature":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Air Pressure";
					break;
					
				}
				break;
				
				case "humidity":
				switch(myPGNType)
				{
					case "No Data":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Relative Humidity (%)";
					break;
					
					case "Outside Humidity":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Relative Humidity (%)";
					break;
					
					case "Inside Humidity":	//	<option value="None"> -------- </option>
						switch(myPGNInstance)
						{
							case "0":
								myPGNTag =  "/Environmental/Humidity Inside";
							break;
							
							case "16":
								myPGNTag =  "/Environmental/Humidity Inside 0";
							break;
							
							case "17":
								myPGNTag =  "/Environmental/Humidity Inside 1";
							break;
							
							case "18":
								myPGNTag =  "/Environmental/Humidity Inside 2";
							break;
							
							case "19":
								myPGNTag =  "/Environmental/Humidity Inside 3";
							break;
							
							case "20":
								myPGNTag =  "/Environmental/Humidity Inside 4";
							break;
							
							case "21":
								myPGNTag =  "/Environmental/Humidity Inside 5";
							break;
							
							case "22":
								myPGNTag =  "/Environmental/Humidity Inside 6";
							break;
							
							case "23":
								myPGNTag =  "/Environmental/Humidity Inside 7";
							break;
							
							
							
							
							
							
							
						}
						
					break;
	
			
				}
				break;
			}	
		break; // environmental_data
		
		case "wind_data":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "wind_speed":
				switch(myPGNType)
				{
					//case "No Data":	//	<option value="None"> -------- </option>
					//	myPGNTag =  "/Environmental/Wind Speed";
					//break;
					
					case "TWIND True North":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Wind Speed";
					break;
					
					case "TWIND Mag North":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Wind Speed Magnetic";
					break;
					
					case "Apparent Wind":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Speed Apparent";
					break;
					
					case "TWIND VCGR":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Speed Ground";
					break;
					
					case "TWIND VCWR":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Speed Water";
					break;
					
					case "Gust":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Speed Gust";
					break;
					
				}
				break;
				
				case "wind_gusts":
				switch(myPGNType)
				{

					
					case "Gust":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Speed Gust";
					break;
					
				}
				break;				
				
				case "wind_direction":
				switch(myPGNType)
				{
					//case "No Data":	//	<option value="None"> -------- </option>
					//	myPGNTag =  "/Environmental/Wind Direction";
					//break;
					
					case "TWIND True North":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Wind Direction";
					break;
					
					case "TWIND Mag North":	//	<option value="None"> -------- </option>
						myPGNTag =  "/Environmental/Wind Direction Magnetic";
					break;
					
					case "Apparent Wind":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Direction Apparent";
					break;
					
					case "TWIND VCGR":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Direction Ground";
					break;
					
					case "TWIND VCWR":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Direction Water";
					break;
					

					
				}
				break;
			}	
		break; // wind_data
		

	   case "engine_parameters_rapid_update":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "speed":
				switch(myPGNType)
				{
					case "NULL":
						switch(myPGNInstance)
						{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine RPM Port";
						break;

						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine RPM Starboard";
						break;

						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine RPM Center";
						break;
						}
					break;

					case "J1939":
						myPGNTag =  "/M2M/Engine/Generator RPM J1939";
					break;
				}
				break;
				
				case "boost_presure":
				switch(myPGNInstance)
				{
					case "0":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine Boost Port";
					break;
					
					case "1":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine Boost Starboard";
					break;
					
					case "2":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Boost Center";
					break;
				}
				break;
				
				case "tilt_or_trim":
				switch(myPGNInstance)
				{
					case "0":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine Trim Port";
					break;
					
					case "1":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Engine Trim Starboard";
					break;
					
					case "2":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Environment/Wind Trim Center";
					break;
				}
				break;

			}
			break;// engine_parameters_rapid_update
			
			
		case "engine_parameters_dynamic":	//	<option value="None"> -------- </option>
		
		switch(myPGNType)
		{
			case "NULL":		
			switch(myPGNParameter)
			{
				case "oil_pressure":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Pressure Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Pressure Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Pressure Center";
						break;
					}
				break;
				
				case "oil_temp":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Temperature Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Temperature Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine OIL Temperature Center";
						break;
					}
				break;
				
				
				case "engine_temp":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Temperature Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Temperature Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Temperature Center";
						break;
					}
				break;
				
				case "alternator_potential":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Alternator Volts Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Alternator Volts Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Alternator Volts Center";
						break;
					}
				break;
				
				case "fuel_rate":
				switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Center";
						break;
					}
				break;
				
				case "total_engine_hours":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Hours Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Hours Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Hours Center";
						break;
					}
				break;
				
				case "coolant_pressure":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Coolant Pressure Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Coolant Pressure Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Coolant Pressure Center";
						break;
					}
				break;
				
				case "fuel_pressure":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Pressure Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Pressure Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Pressure Center";
						break;
					}
				break;
			}
			break;
			


			case "J1939":
			switch(myPGNParameter)
			{
				case "oil_pressure":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Generator OIL Pressure J1939";
						break;
						

					}
				break;
				
				case "oil_temp":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Generator OIL Temperature J1939";
						break;
						
	
					}
				break;
				
				case "fuel_temp":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Generator Fuel Temperature J1939";
						break;
						
	
					}
				break;
				
				
				case "engine_temp":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Generator Temperature J1939";
						break;
			
					}
				break;
				
				case "alternator_potential":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>Generator Alternator Volts J1939
							myPGNTag =  "/M2M/Engine/Generator Alternator Volts J1939";
						break;
						

					}
				break;
				
				case "fuel_rate":
				switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Generator Fuel Rate J1939";
						break;

					}
				break;
				
				case "total_engine_hours":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Generator Hours J1939";
						break;

					}
				break;
				
				case "coolant_pressure":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Generator Coolant Pressure J1939";
						break;
						

					}
				break;
				
				case "fuel_pressure":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Generator Fuel Pressure J1939";
						break;
						
		
					}
				break;
			}
			break;
		}

		break;// engine_parameters_dynamic			
							
					
			
		case "transmission_parameters_dynamic":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "oil_pressure":
				switch(myPGNInstance)
				{
					case "0":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Pressure Port";
					break;
					
					case "1":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Pressure Starboard";
					break;
					
					case "2":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Pressure Center";
					break;
				}
				break;
				
				case "oil_temp":
				switch(myPGNInstance)
				{
					case "0":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Temperature Port";
					break;
					
					case "1":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Temperature Starboard";
					break;
					
					case "2":	//	<option value="None"> -------- </option>
						myPGNTag =  "/M2M/Engine/Transmission OIL Temperature Center";
					break;
				}
				break;
			}
			break;// transmission_parameters_dynamic
			
			
			
		case "trip_parameters_engine":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "trip_fuel_used":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Trip Fuel Used Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Trip Fuel Used Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Trip Fuel Used Center";
						break;
					}
				break;
				
				case "fuel_rate_average":
				switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Average Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Average Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Average Center";
						break;
					}
				break;
				
				case "fuel_rate_economy":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Economy Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Economy Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Fuel Rate Economy Center";
						break;
					}
				break;
				
				case "instantaneous_fuel_economy":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Instantaneous Fuel Economy Port";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Instantaneous Fuel Economy Starboard";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/Engine/Engine Instantaneous Fuel Economy Center";
						break;
					}
				break;
				
				
			}
			break;//trip_parameters_engine				
			
			
			
			
			
			
		case "battery_status":	//	<option value="None"> -------- </option>
		switch(myPGNType)
		{
			case "NULL":
	
		
				switch(myPGNParameter)
				{
					case "voltage":
						switch(myPGNInstance)
						{
							case "0":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery Volts Port";
							break;
							
							case "1":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery Volts Starboard";
							break;
							
							case "2":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery Volts Center";
							break;
						}
					break;
					
					case "current":
					switch(myPGNInstance)
						{
							case "0":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery Current Port";
							break;
							
							case "1":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery Current Starboard";
							break;
							
							case "2":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery Current Center";
							break;
						}
					break;
					
					case "temperature":
						switch(myPGNInstance)
						{
							case "0":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery Temperature Port";
							break;
							
							case "1":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery Temperature Starboard";
							break;
							
							case "2":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery Temperature Center";
							break;
						}
					break;
					
					case "stateofcharge":
						switch(myPGNInstance)
						{
							case "0":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery StateOfCharge Port";
							break;
							
							case "1":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery StateOfCharge Starboard";
							break;
							
							case "2":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery StateOfCharge Center";
							break;
						}
					break;
					
					case "timeremaining":
						switch(myPGNInstance)
						{
							case "0":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery TimeRemaining Port";
							break;
							
							case "1":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery TimeRemaining Starboard";
							break;
							
							case "2":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/Battery/Battery TimeRemaining Center";
							break;
						}
					break;
					
					
					
				}
			break;
			
			
			case "J1939":
	
		
				switch(myPGNParameter)
				{
					case "voltage":
								myPGNTag =  "/M2M/Battery/Battery Volts J1939";
					break;
					
					case "current":		
								myPGNTag =  "/M2M/Battery/Battery Current J1939";
					break;

				}
			break;
		}
		break;// battery_status		

		case "ac_watthours":	//	<option value="None"> -------- </option>
		switch(myPGNType)
		{
			case "UTIL":	//	<option value="None"> -------- </option>

				switch(myPGNParameter)
				{
					case "ac_kwatthours":
						switch(myPGNInstance)
						{
							case "0":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/AC/UTIL/Energy_Phase_A";
							break;
							
							case "1":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/AC/UTIL/Energy_Phase_B";
							break;
							
							case "2":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/AC/UTIL/Energy_Phase_C";
							break;
							
							case "3":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/AC/UTIL/Energy_Avg";
							break;
						}
					break;
				}
				break;
				
			case "GEN":	//	<option value="None"> -------- </option>

				switch(myPGNParameter)
				{
					case "ac_kwatthours":
						switch(myPGNInstance)
						{
							case "0":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/AC/GEN/Energy_Phase_A";
							break;
							
							case "1":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/AC/GEN/Energy_Phase_B";
							break;
							
							case "2":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/AC/GEN/Energy_Phase_C";
							break;
							
							case "3":	//	<option value="None"> -------- </option>
								myPGNTag =  "/M2M/AC/GEN/Energy_Avg";
							break;
						}
					break;
				}
				break;
			}
		break;// ac_watthours	
			
		case "ac_basic":	//	<option value="None"> -------- </option>
		switch(myPGNType)
		{
			case "UTIL":	//	<option value="None"> -------- </option>

			switch(myPGNParameter)
			{
				case "ac_line_line_volts":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Volts_Line_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Volts_Line_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Volts_Line_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Volts_Line_Avg";
						break;
					}
				break;
				
				case "ac_line_neutral_volts":
				switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Volts_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Volts_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Volts_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Volts_Avg";
						break;
					}
				break;
				
				case "ac_frequency":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Frequency_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Frequency_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Frequency_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Frequency_Avg";
						break;
						
						
					}
				break;
				
			case "ac_amps":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Amps_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Amps_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Amps_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Amps_Avg";
						break;
					}
				break;	
				
				case "ac_watts":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Power_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Power_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Power_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/UTIL/Power_Avg";
						break;
					}
				break;	
				
			}
			break;
			
			case "GEN":	//	<option value="None"> -------- </option>

			switch(myPGNParameter)
			{
				case "ac_line_line_volts":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Volts_Line_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Volts_Line_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Volts_Line_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Volts_Line_Avg";
						break;
					}
				break;
				
				case "ac_line_neutral_volts":
				switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Volts_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Volts_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Volts_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Volts_Avg";
						break;
					}
				break;
				
				case "ac_frequency":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Frequency_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Frequency_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Frequency_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Frequency_Avg";
						break;
						
						
					}
				break;
				
			case "ac_amps":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Amps_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Amps_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Amps_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Amps_Avg";
						break;
					}
				break;	
				
				case "ac_watts":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Power_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Power_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Power_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/GEN/Power_Avg";
						break;
					}
				break;	
				
			}
			break;
			
			case "LIGHTS":	//	<option value="None"> -------- </option>

			switch(myPGNParameter)
			{
				case "ac_line_line_volts":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Volts_Line_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Volts_Line_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Volts_Line_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Volts_Line_Avg";
						break;
					}
				break;
				
				case "ac_line_neutral_volts":
				switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Volts_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Volts_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Volts_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Volts_Avg";
						break;
					}
				break;
				
				case "ac_frequency":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Frequency_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Frequency_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Frequency_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Frequency_Avg";
						break;
						
						
					}
				break;
				
			case "ac_amps":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Amps_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Amps_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Amps_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Amps_Avg";
						break;
					}
				break;	
				
				case "ac_watts":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Power_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Power_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Power_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/LIGHTS/Power_Avg";
						break;
					}
				break;	
				
			}
			break;
			
			case "HEAT":	//	<option value="None"> -------- </option>

			switch(myPGNParameter)
			{
				case "ac_line_line_volts":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Volts_Line_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Volts_Line_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Volts_Line_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Volts_Line_Avg";
						break;
					}
				break;
				
				case "ac_line_neutral_volts":
				switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Volts_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Volts_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Volts_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Volts_Avg";
						break;
					}
				break;
				
				case "ac_frequency":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Frequency_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Frequency_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Frequency_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Frequency_Avg";
						break;
						
						
					}
				break;
				
			case "ac_amps":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Amps_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Amps_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Amps_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Amps_Avg";
						break;
					}
				break;	
				
				case "ac_watts":
					switch(myPGNInstance)
					{
						case "0":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Power_Phase_A";
						break;
						
						case "1":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Power_Phase_B";
						break;
						
						case "2":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Power_Phase_C";
						break;
						
						case "3":	//	<option value="None"> -------- </option>
							myPGNTag =  "/M2M/AC/HEAT/Power_Avg";
						break;
					}
				break;	
				
			}
			break;
			
		}
		
		break;// ac_utility_basic		

		case "ac_total_energy":	//	<option value="None"> -------- </option>
		switch(myPGNType)
		{
			case "UTIL":	//	<option value="None"> -------- </option>
				switch(myPGNParameter)
				{
					case "export_kwatt_hours":
						myPGNTag =  "/M2M/AC/UTIL/TotalEnergy_Export";
					break;
							

					break;
					
					case "import_kwatt_hours":
						myPGNTag =  "/M2M/AC/UTIL/TotalEnergy_Import";
					break;				
					
				}
			break;
			
			case "GEN":	//	<option value="None"> -------- </option>
			
				switch(myPGNParameter)
				{
					case "export_kwatt_hours":
						myPGNTag =  "/M2M/AC/GEN/TotalEnergy_Export";
					break;
							

					break;
					
					case "import_kwatt_hours":
						myPGNTag =  "/M2M/AC/GEN/TotalEnergy_Import";
					break;				
					
				}
			break;
		}
		break;// ac_total_energy		

			
			
			case "fluid_level":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "level":
					switch(myPGNType)
					{
						case "0":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Center";
								break;
								
								case "3":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Fwd";
								break;
								
								case "4":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Aft";
								break;
								
								case "5":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Day1";
								break;								
								
								case "6":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Day2";
								break;
								
								case "7":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Fuel Level Day3";
								break;		
								
								
								
							}
						break;
						
						case "1":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Water Level Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Water Level Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Water Level Center";
								break;
							}
						break;
						
						case "2":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Waste Level Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Waste Level Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Waste Level Center";
								break;
							}
						break;
						
						case "3":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Live Well Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Live Well Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Live Well Center";
								break;
							}
						break;
						
						
						case "4":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Oil Level Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Oil Level Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Oil Level Center";
								break;
							}
						break;
						
						case "5":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Black Water Level Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Black Water Level Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Black Water Level Center";
								break;
							}
						break;
						
						case "6":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Bilge Level Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Bilge Level Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Tank/Bilge Level Center";
								break;
							}
						break;
						
						case "8":
								myPGNTag =  "/M2M/Engine/Generator Fuel Level J1939";
						break;
						
						
					}
				break;
			}
			
			break;// fluid_level
			
			case "temperature_extended":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "actual_temperature":
					switch(myPGNType)
					{
						case "EGT":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 0 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 0 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 0 Center";
								break;
							}
						break;		
						
						case "Custom":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 1 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 1 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT Temperature 1 Center";
								break;
							}
						break;							
			
					}
			}
			break; // temperature extended
			
			
			case "temperature":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "actual_temperature":
					switch(myPGNType)
					{
						case "Sea Temperature":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Water Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Water Temperature 1";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Water Temperature 2";
								break;
							}
						break;
						
						case "Outside Temperature":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Outside Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Outside Temperature 1";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Outside Temperature 2";
								break;
							}
						break;
						
						case "Inside Temperature":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Inside Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Inside Temperature 1";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Inside Temperature 2";
								break;
							}
						break;
						
						case "Engine Room Temperature":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Engine Room Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Engine Room Temperature Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Engine Room Temperature Center";
								break;
							}
						break;
						
						
						case "Main Cabin Temperature":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Main Cabin Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Main Cabin Temperature Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Main Cabin Temperature Center";
								break;
							}
						break;
						
						case "Live Well":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Live Well Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Live Well Temperature Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Live Well Temperature Center";
								break;
							}
						break;
						
						case "Bait Well":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Bait Well Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Bait Well Temperature Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Bait Well Temperature Center";
								break;
							}
						break;
						
						case "Refrigeration":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Refrigeration 1 Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Refrigeration 2 Temperature";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Refrigeration 3 Temperature";
								break;
							}
						break;
						
						case "Heating":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heating Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heating Temperature Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heating Temperature Center";
								break;
							}
						break;
						
						case "Dew Point":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Dew Point";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									//myPGNTag =  "/M2M/Tank/Black Level Starboard"
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									//myPGNTag =  "/M2M/Tank/Black Level Center"
								break;
							}
						break;
						
						case "Wind Chill A":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill A Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill A Temperature Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill A Temperature Center";
								break;
							}
						break;
						
						case "Wind Chill T":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill T Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill T Temperature Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Wind Chill T Temperature Center";
								break;
							}
						break;
						
						case "Heat Index":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heat Index";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heat Index Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Heat Index Center";
								break;
							}
						break;
						
						case "Freezer":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Freezer Temperature";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Freezer 2 Temperature";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Freezer 3 Temperature";
								break;
							}
						break;
						
						case "Reserved 130":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Engine Coolant Temperature Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Engine Coolant Temperature Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/Engine Coolant Temperature Center";
								break;
							}
						break;
						
						case "Reserved 134":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/EGT Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/EGT Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Domestic/EGT Center";
								break;
							}
						break;
						
						case "EGT":
							switch(myPGNInstance)
							{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT 0 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT 0 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Engine/EGT 0 Center";
								break;
							}
						break;
					}
				break;
			}
			
			break;// temperature
			
			case "seasmartdimmer":	//	<option value="None"> -------- </option>
		
			switch(myPGNType)
			{
				case "LED 1 Channel":
				
					switch(myPGNInstance)
					{
						case "0":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 0";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 0";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 0";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 0";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 0";
								break;								
								

							}
						break;
						
						case "1":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 1";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 1";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 1";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 1";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 1";
								break;								
								

							}
						break;

						
						case "2":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 2";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 2";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 2";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 2";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 2";
								break;								
								

							}
						break;

						
						case "3":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 3";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 3";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 3";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 3";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 3";
								break;								
								

							}
						break;

						
						case "4":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 4";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 4";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 4";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 4";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 4";
								break;								
								

							}
						break;

						
						case "5":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 5";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 5";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 5";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 5";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 5";
								break;								
								

							}
						break;

						
						case "6":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 6";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 6";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 6";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 6";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 6";
								break;								
								

							}
						break;

						
						case "7":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 7";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 7";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 7";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 7";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 7";
								break;								
								

							}
						break;

						
						case "8":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 8";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 8";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 8";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 8";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 8";
								break;								
								

							}
						break;

						
						case "9":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 9";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 9";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 9";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 9";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 9";
								break;								
								

							}
						break;

						case "10":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 10";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 10";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 10";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 10";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 10";
								break;								
								

							}
						break;
						
						case "11":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 11";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 11";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 11";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 11";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 11";
								break;								
								

							}
						break;

						
						case "12":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 12";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 12";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 12";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 12";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 12";
								break;								
								

							}
						break;

						
						case "13":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 13";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 13";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 13";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 13";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 13";
								break;								
								

							}
						break;

						
						case "14":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 14";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 14";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 14";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 14";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 14";
								break;								
								

							}
						break;

						
						case "15":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 15";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 15";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 15";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 15";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 15";
								break;								
								

							}
						break;

						
						case "16":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 16";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 16";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 16";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 16";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 16";
								break;								
								

							}
						break;

						
						case "17":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 17";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 17";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 17";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 17";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 17";
								break;								
								

							}
						break;

						
						case "18":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 18";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 18";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 18";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 18";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 18";
								break;								
								

							}
						break;

						
						case "19":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 19";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 19";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 19";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 19";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 19";
								break;								
								

							}
						break;


						case "20":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 20";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 20";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 20";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 20";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 20";
								break;								
								

							}
						break;
						
						case "21":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 21";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 21";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 21";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 21";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 21";
								break;								
								

							}
						break;

						
						case "22":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 22";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 22";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 22";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 22";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 22";
								break;								
								

							}
						break;

						
						case "23":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 23";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 23";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 23";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 23";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 23";
								break;								
								

							}
						break;

						
						case "24":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 24";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 24";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 24";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 24";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 24";
								break;								
								

							}
						break;

						
						case "25":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 25";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 25";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 25";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 25";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 25";
								break;								
								

							}
						break;

						
						case "26":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 26";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 26";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 26";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 26";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 26";
								break;								
								

							}
						break;

						
						case "27":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 27";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 27";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 27";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 27";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 27";
								break;								
								

							}
						break;

						
						case "28":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 28";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 28";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 28";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 28";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 28";
								break;								
								

							}
						break;

						
						case "29":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 29";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 29";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 29";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 29";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 29";
								break;								
								

							}
						break;

						case "30":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 30";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 30";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 30";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 30";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 30";
								break;								
								

							}
						break;
						
						case "31":
							switch(myPGNParameter)
							{
								case "value0":
									myPGNTag =  "/M2M/LED Dimmer/Value 0 Zone 31";
								break;
										
								case "value1":	
									myPGNTag =  "/M2M/LED Dimmer/Value 1 Zone 31";
								break;
								
								case "value2":
									myPGNTag =  "/M2M/LED Dimmer/Value 2 Zone 31";
								break;
										
								case "value3":	
									myPGNTag =  "/M2M/LED Dimmer/Value 3 Zone 31";
								break;
										
								case "value4":	
									myPGNTag =  "/M2M/LED Dimmer/Value 4 Zone 31";
								break;								
								

							}
						break;

						


						
					}			

							
				break;
				
				case "LED 4 Channel":
					switch(myPGNParameter)
					{
						case "value0":
								switch(myPGNInstance)
								{
									
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 0 Zone 0";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 0 Zone 1";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 0 Zone 2";
										break;
										
										case "3":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 0 Zone 3";
										break;
										
										case "4":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 0 Zone 4";
										break;
										
										case "5":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 0 Zone 5";
										break;
										
										case "6":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 0 Zone 6";
										break;
										
										case "7":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 0 Zone 7";
										break;
								}
								break;
								
							case "value1":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 1 Zone 0";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 1 Zone 1";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 1 Zone 2";
										break;
										
										case "3":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 1 Zone 3";
										break;
										
										case "4":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 1 Zone 4";
										break;
										
										case "5":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 1 Zone 5";
										break;
										
										case "6":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 1 Zone 6";
										break;
										
										case "7":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 1 Zone 7";
										break;
								}
								break;

						case "value2":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 2 Zone 0";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 2 Zone 1";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 2 Zone 2";
										break;
										
										case "3":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 2 Zone 3";
										break;
										
										case "4":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 2 Zone 4";
										break;
										
										case "5":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 2 Zone 5";
										break;
										
										case "6":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 2 Zone 6";
										break;
										
										case "7":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 2 Zone 7";
										break;
								}
								break;

						case "value3":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 3 Zone 0";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 3 Zone 1";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 3 Zone 2";
										break;
										
										case "3":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 3 Zone 3";
										break;
										
										case "4":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 3 Zone 4";
										break;
										
										case "5":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 3 Zone 5";
										break;
										
										case "6":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 3 Zone 6";
										break;
										
										case "7":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 3 Zone 7";
										break;
								}
								break;						
						
							
						break;
						
						case "value4":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 4 Zone 0";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 4 Zone 1";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 4 Zone 2";
										break;
										
										case "3":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 4 Zone 3";
										break;
										
										case "4":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 4 Zone 4";
										break;
										
										case "5":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 4 Zone 5";
										break;
										
										case "6":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 4 Zone 6";
										break;
										
										case "7":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/LED Dimmer 4 Channel/Value 4 Zone 7";
										break;
								}
								break;						
					}
							
						break;


				case "RGB 1 Channel":
					switch(myPGNParameter)
					{
						case "value0":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 0 Zone 0";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 0 Zone 1";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 0 Zone 2";
										break;
										
										case "3":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 0 Zone 3";
										break;
										
										case "4":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 0 Zone 4";
										break;
										
										case "5":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 0 Zone 5";
										break;
										
										case "6":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 0 Zone 6";
										break;
										
										case "7":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 0 Zone 7";
										break;
								}
								break;
								
							case "value1":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 1 Zone 0";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 1 Zone 1";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 1 Zone 2";
										break;
										
										case "3":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 1 Zone 3";
										break;
										
										case "4":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 1 Zone 4";
										break;
										
										case "5":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 1 Zone 5";
										break;
										
										case "6":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 1 Zone 6";
										break;
										
										case "7":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 1 Zone 7";
										break;
								}
								break;

						case "value2":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 2 Zone 0";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 2 Zone 1";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 2 Zone 2";
										break;
										
										case "3":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 2 Zone 3";
										break;
										
										case "4":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 2 Zone 4";
										break;
										
										case "5":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 2 Zone 5";
										break;
										
										case "6":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 2 Zone 6";
										break;
										
										case "7":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 2 Zone 7";
										break;
								}
								break;

						case "value3":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 3 Zone 0";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 3 Zone 1";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 3 Zone 2";
										break;
										
										case "3":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 3 Zone 3";
										break;
										
										case "4":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 3 Zone 4";
										break;
										
										case "5":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 3 Zone 5";
										break;
										
										case "6":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 3 Zone 6";
										break;
										
										case "7":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 3 Zone 7";
										break;
								}
								break;						
						
							
						break;
						
						case "value4":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 4 Zone 0";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 4 Zone 1";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 4 Zone 2";
										break;
										
										case "3":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 4 Zone 3";
										break;
										
										case "4":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 4 Zone 4";
										break;
										
										case "5":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 4 Zone 5";
										break;
										
										case "6":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 4 Zone 6";
										break;
										
										case "7":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/RGB Dimmer/Value 4 Zone 7";
										break;
								}
								break;						
						
							
						break;
					}
				break;
			}
			break;// dimmer
			
			case "seasmartindicator":	//	<option value="None"> -------- </option>
			switch(myPGNType)
			{
				case "0":
					switch(myPGNParameter)
					{
						case "runtime_sec":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 0 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 0 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 0 Center";
										break;
								}
								break;
						break;
						
						case "cycles":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 0 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 0 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 0 Center";
										break;
								}
								break;
						break;				
					}
				break;	
				
				case "1":
					switch(myPGNParameter)
					{
						case "runtime_sec":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 1 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 1 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 1 Center";
										break;
								}
								break;
						break;
						
						case "cycles":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 1 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 1 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 1 Center";
										break;
								}
								break;
						break;				
					}
				break;	

				case "2":
					switch(myPGNParameter)
					{
						case "runtime_sec":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 2 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 2 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 2 Center";
										break;
								}
								break;
						break;
						
						case "cycles":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 2 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 2 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 2 Center";
										break;
								}
								break;
						break;				
					}
				break;	

				case "3":
					switch(myPGNParameter)
					{
						case "runtime_sec":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 3 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 3 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 3 Center";
										break;
								}
								break;
						break;
						
						case "cycles":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 3 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 3 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 3 Center";
										break;
								}
								break;
						break;				
					}
				break;	

				case "4":
					switch(myPGNParameter)
					{
						case "runtime_sec":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 4 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 4 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 4 Center";
										break;
								}
								break;
						break;
						
						case "cycles":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 4 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 4 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 4 Center";
										break;
								}
								break;
						break;				
					}
				break;	

				case "5":
					switch(myPGNParameter)
					{
						case "runtime_sec":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 5 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 5 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 5 Center";
										break;
								}
								break;
						break;
						
						case "cycles":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 5 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 5 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 5 Center";
										break;
								}
								break;
						break;				
					}
				break;	

				case "6":
					switch(myPGNParameter)
					{
						case "runtime_sec":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 6 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 6 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 6 Center";
										break;
								}
								break;
						break;
						
						case "cycles":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 6 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 6 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 6 Center";
										break;
								}
								break;
						break;				
					}
				break;	

				case "7":
					switch(myPGNParameter)
					{
						case "runtime_sec":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 7 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 7 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Runtime 7 Center";
										break;
								}
								break;
						break;
						
						case "cycles":
								switch(myPGNInstance)
								{
										case "0":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 7 Port";
										break;
										
										case "1":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 7 Starboard";
										break;
										
										case "2":	//	<option value="None"> -------- </option>
											myPGNTag =  "/M2M/Switch/Cycles 7 Center";
										break;
								}
								break;
						break;				
					}
				break;					
				
				
			}
			break;			
			
			case "seasmartswitch":	//	<option value="None"> -------- </option>
		
			switch(myPGNParameter)
			{
				case "value0":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 0 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 0 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 0 Center";
								break;
						}
						break;
						
					case "value1":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 1 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 1 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 1 Center";
								break;
						}
						break;

				case "value2":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 2 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 2 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 2 Center";
								break;
						}
						break;

				case "value3":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 3 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 3 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 3 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "value4":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 4 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 4 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 4 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "value5":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 5 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 5 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 5 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "value6":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 6 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 6 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 6 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "value7":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 7 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 7 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 7 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "value8":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 8 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 8 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 8 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "value9":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 9 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 9 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 9 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "value10":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 10 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 10 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 10 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "value11":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 11 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 11 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 11 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "value12":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 12 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 12 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 12 Center";
								break;
						}
						break;						
				
					
				break;	
				
				case "value13":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 13 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 13 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 13 Center";
								break;
						}
						break;						
				
					
				break;	
				
				case "value14":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 14 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 14 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 14 Center";
								break;
						}
						break;						
				
					
				break;			
				
				case "value15":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 15 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 15 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Value 15 Center";
								break;
						}
						break;						
				
					
				break;		
				
				case "bank0":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Bank 0 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Bank 0 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Bank 0 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "bank1":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Bank 1 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Bank 1 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Bank 1 Center";
								break;
						}
						break;						
				
					
				break;
				
				case "bank2":
						switch(myPGNInstance)
						{
								case "0":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Bank 2 Port";
								break;
								
								case "1":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Bank 2 Starboard";
								break;
								
								case "2":	//	<option value="None"> -------- </option>
									myPGNTag =  "/M2M/Switch/Bank 2 Center";
								break;
						}
						break;						
				
					
				break;
				
				
			}
			
			break;// switch
			
			
			
		
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
	
	DialPGNNumber[dialindex] = myserieskey;

}

function makePGNfromEvent(myEventType, Source)
{

var myserieskey = "";
var myPGNNumber= "";
var myPGNSource= "";
var myPGNInstance= "";
var myPGNType="";
var myPGNParameter= "";

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
			myPGNNumber="heartbeat";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="timestamp";
		break;
		
		case "/General/Sessions":	//	<option value="/Position">GPS Position</option>
			myPGNNumber="heartbeat";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="sessionid";
		break;
		
		case "/Cellular/DB_Strength":	//	<option value="/Position">GPS Position</option>
			myPGNNumber="cellular_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="db_status";
		break;
		
		case "/Cellular/Connect_Status":	//	<option value="/Position">GPS Position</option>
			myPGNNumber="cellular_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="ai_status";
		break;
		
		case "/General/Status":	//	<option value="/Position">GPS Position</option>
			myPGNNumber="helmsmartstat";
			myPGNSource="FF";
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="write_records";
		break;
			
		case "/Position":	//	<option value="/Position">GPS Position</option>
			myPGNNumber="position_rapid";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="latlng";
		break;
		
		case "/Position/lat":	//	<option value="/Position">GPS Position Lat</option>
			myPGNNumber="position_rapid";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="lat";
		break;
		
		case "/Position/lng":	//	<option value="/Position">GPS Position Lng</option>
			myPGNNumber="position_rapid";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="lng";
		break;
		
		
		case "/M2M/Navigation/Speed Over Ground":	//	<option value="/M2M/Navigation/Speed Over Ground">Navigation - Speed Over Ground </option>
			myPGNNumber="cogsog";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="True";
			myPGNParameter="speed_over_ground";
		break;
		
		case "/M2M/Navigation/Course Over Ground":	//	<option value="/M2M/Navigation/Course Over Ground">Navigation - Speed Over Ground </option>
			myPGNNumber="cogsog";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="True";
			myPGNParameter="course_over_ground";
		break;
		
		case "/M2M/Navigation/Speed Over Ground Mag":	//	<option value="/M2M/Navigation/Speed Over Ground">Navigation - Speed Over Ground </option>
			myPGNNumber="cogsog";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Magnetic";
			myPGNParameter="speed_over_ground";
		break;
		
		case "/M2M/Navigation/Course Over Ground Mag":	//	<option value="/M2M/Navigation/Course Over Ground">Navigation - Speed Over Ground </option>
			myPGNNumber="cogsog";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Magnetic";
			myPGNParameter="course_over_ground";
		break;
		
		case "/M2M/Navigation/Heading True":	//	<option value="/M2M/Navigation/Heading True">Navigation - Heading True</option>
			myPGNNumber="heading";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="True";
			myPGNParameter="heading";
		break;
		
		case "/M2M/Navigation/Heading Magnetic":	//	<option value="/M2M/Navigation/Heading Magnetic">Navigation - Heading Magnetic</option>
			myPGNNumber="heading";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Magnetic";
			myPGNParameter="heading";
		break;
		
		case "/M2M/Navigation/Rudder":	//	<option value="/M2M/Navigation/Rudder">Navigation - Rudder </option>
			myPGNNumber="rudder";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="True";
			myPGNParameter="position";
		break;		
		
		case "/M2M/Navigation/Rate Of Turn":	//	<option value="/M2M/Navigation/Rate Of Turn">Navigation - Rate Of Turn </option>
			myPGNNumber="rot";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="rateofturn";
		break;	

		case "/M2M/Attitude/Pitch":	//	<option value="/M2M/Attitude/Pitch">Attitude - Pitch </option>
			myPGNNumber="attitude";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="pitch";
		break;	

		case "/M2M/Attitude/Roll":	//	<option value="/M2M/Attitude/Pitch">Attitude - Roll </option>
			myPGNNumber="attitude";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="roll";
		break;			
		
		case "/M2M/Environment/Rain Accumulation":	//	<option value="/M2M/Attitude/Pitch">Attitude - Roll </option>
			myPGNNumber="rain_gauge";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="accumulation";
		break;			
				
		
		case "/M2M/Environment/Rain Duration":	//	<option value="/M2M/Attitude/Pitch">Attitude - Roll </option>
			myPGNNumber="rain_gauge";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="rainduration";
		break;			
				

		
		case "/M2M/Environment/Rain Rate":	//	<option value="/M2M/Attitude/Pitch">Attitude - Roll </option>
			myPGNNumber="rain_gauge";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="rate";
		break;			
				

		
		case "/M2M/Environment/Rain Peak Rate":	//	<option value="/M2M/Attitude/Pitch">Attitude - Roll </option>
			myPGNNumber="rain_gauge";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="peak";
		break;			
								
		
		
		
		case "/Environmental/Wind Speed":	//	<option value="/Environmental/Wind Speed">Wind Speed</option>
			myPGNNumber="wind_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="TWIND True North";
			myPGNParameter="wind_speed";
		break;
		
		case "/Environmental/Wind Direction":	//	<option value="/Environmental/Wind Direction">Wind Direction</option>
			myPGNNumber="wind_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="TWIND True North";
			myPGNParameter="wind_direction";
		break;
		
		case "/Environmental/Wind Speed Magnetic":	//	<option value="/Environmental/Wind Speed">Wind Speed</option>
			myPGNNumber="wind_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="TWIND Mag North";
			myPGNParameter="wind_speed";
		break;
		
		case "/Environmental/Wind Direction Magnetic":	//	<option value="/Environmental/Wind Direction">Wind Direction</option>
			myPGNNumber="wind_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="TWIND Mag North";
			myPGNParameter="wind_direction";
		break;
		
		case "/M2M/Environment/Wind Speed Apparent":	//	<option value="/Environmental/Wind Speed">Wind Speed</option>
			myPGNNumber="wind_data";
			myPGNSource=Source; 
			myPGNInstance="0";
			myPGNType="Apparent Wind";
			myPGNParameter="wind_speed";
		break;
		
		case "/M2M/Environment/Wind Direction Apparent":	//	<option value="/Environmental/Wind Direction">Wind Direction</option>
			myPGNNumber="wind_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Apparent Wind";
			myPGNParameter="wind_direction";
		break;
		
		case "/M2M/Environment/Wind Speed Ground":	//	<option value="/Environmental/Wind Speed">Wind Speed</option>
			myPGNNumber="wind_data";
			myPGNSource=Source; 
			myPGNInstance="0";
			myPGNType="TWIND VCGR";
			myPGNParameter="wind_speed";
		break;
		
		case "/M2M/Environment/Wind Direction Ground":	//	<option value="/Environmental/Wind Direction">Wind Direction</option>
			myPGNNumber="wind_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="TWIND VCGR";
			myPGNParameter="wind_direction";
		break;
		
		case "/M2M/Environment/Wind Speed Water":	//	<option value="/Environmental/Wind Speed">Wind Speed</option>
			myPGNNumber="wind_data";
			myPGNSource=Source; 
			myPGNInstance="0";
			myPGNType="TWIND VCWR";
			myPGNParameter="wind_speed";
		break;
		
		case "/M2M/Environment/Wind Speed Gust":	//	<option value="/Environmental/Wind Speed">Wind Speed</option>
			myPGNNumber="wind_data";
			myPGNSource=Source; 
			myPGNInstance="0";
			myPGNType="Gust";
			myPGNParameter="wind_gusts";
		break;
		
		case "/M2M/Environment/Wind Direction Water":	//	<option value="/Environmental/Wind Direction">Wind Direction</option>
			myPGNNumber="wind_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="TWIND VCWR";
			myPGNParameter="wind_direction";
		break;
		
		case "/Environmental/Air Pressure":	//	<option value="/Environmental/Air Pressure">Air Pressure</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Outside Temperature";
			myPGNParameter="atmospheric_pressure";
		break;
		
		case "/Environmental/Air Pressure Inside":	//	<option value="/Environmental/Air Pressure">Air Pressure</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Inside Temperature";
			myPGNParameter="atmospheric_pressure";
		break;
		
		case "/Environmental/Air Temperature":	//	<option value="/Environmental/Air Temperature">Air Temperature</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Outside Temperature";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Air Temperature Inside":	//	<option value="/Environmental/Air Temperature">Air Temperature</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Inside Temperature";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Outside Temperature":	//	<option value="/Environmental/Air Temperature">Air Temperature</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Outside Temperature";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Water Temperature":	//	<option value="/Environmental/Water Temperature">Water Temperature</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Sea Temperature";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Relative Humidity (%)":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Outside Humidity";
			myPGNParameter="humidity";
		break;
		
		case "/Environmental/Humidity Inside":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Inside Humidity";
			myPGNParameter="humidity";
		break;
		
		case "/Environmental/Temperature Inside 0":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="16";
			myPGNType="Inside Zone0";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Humidity Inside 0":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="16";
			myPGNType="Inside Humidity";
			myPGNParameter="humidity";
		break;

		
		case "/Environmental/Temperature Inside 1":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="17";
			myPGNType="Inside Zone1";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Humidity Inside 1":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="17";
			myPGNType="Inside Humidity";
			myPGNParameter="humidity";
		break;
		
		
		case "/Environmental/Temperature Inside 2":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="18";
			myPGNType="Inside Zone2";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Humidity Inside 2":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="18";
			myPGNType="Inside Humidity";
			myPGNParameter="humidity";
		break;
		
		
		case "/Environmental/Temperature Inside 3":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="19";
			myPGNType="Inside Zone3";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Humidity Inside 3":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="19";
			myPGNType="Inside Humidity";
			myPGNParameter="humidity";
		break;
		
		
		case "/Environmental/Temperature Inside 4":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="20";
			myPGNType="Inside Zone4";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Humidity Inside 4":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="20";
			myPGNType="Inside Humidity";
			myPGNParameter="humidity";
		break;
		
		
		case "/Environmental/Temperature Inside 5":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="31";
			myPGNType="Inside Zone5";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Humidity Inside 5":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="21";
			myPGNType="Inside Humidity";
			myPGNParameter="humidity";
		break;
		
		
		case "/Environmental/Temperature Inside 6":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="22";
			myPGNType="Inside Zone6";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Humidity Inside 6":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="22";
			myPGNType="Inside Humidity";
			myPGNParameter="humidity";
		break;
		
		
		case "/Environmental/Temperature Inside 7":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="23";
			myPGNType="Inside Zone7";
			myPGNParameter="temperature";
		break;
		
		case "/Environmental/Humidity Inside 7":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="environmental_data";
			myPGNSource=Source;
			myPGNInstance="23";
			myPGNType="Inside Humidity";
			myPGNParameter="humidity";
		break;
		
		
		
		case "/M2M/Navigation/Depth":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="water_depth";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="depth";
		break;
		
		case "/M2M/Navigation/Water Speed":	//	<option value="/Environmental/Relative Humidity (%)">Relative Humidity (%)</option>
			myPGNNumber="water_speed";
			myPGNSource=Source;
			myPGNInstance="0";
			//myPGNType="NULL";
			myPGNType="*";
			myPGNParameter="waterspeed";
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
			myPGNNumber="engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="speed";
		break;
		
		case "/M2M/Engine/Engine Boost Port":	//<option value="/M2M/Engine/Engine Boost Port">Engine Boost Port </option>
			myPGNNumber="engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="boost_presure";
		break;
		
		case "/M2M/Engine/Engine Trim Port":	//<option value="/M2M/Engine/Engine Trim Port">Engine Trim Port</option>
			myPGNNumber="engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="tilt_or_trim";
		break;
		
		case "/M2M/Engine/Engine RPM Starboard":	//<option value="/M2M/Engine/Engine RPM Starboard">Engine RPM Starboard </option>
			myPGNNumber="engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="speed";
		break;
		
		case "/M2M/Engine/Engine Boost Starboard":	//<option value="/M2M/Engine/Engine Boost Starboard">Engine Boost Starboard </option>
			myPGNNumber="engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="boost_presure";
		break;
		
		case "/M2M/Engine/Engine Trim Starboard":	//<option value="/M2M/Engine/Engine Trim Starboard">Engine Trim Starboard</option>
			myPGNNumber="engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="tilt_or_trim";
		break;
		
		case "/M2M/Engine/Engine RPM Center":	//<option value="/M2M/Engine/Engine RPM Center">Engine RPM Center </option>
			myPGNNumber="engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="speed";
		break;
		
		case "/M2M/Engine/Engine Boost Center":	//<option value="/M2M/Engine/Engine Boost Center">Engine Boost Center </option>
			myPGNNumber="engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="boost_presure";
		break;
		
		case "/M2M/Engine/Engine Trim Center":	//<option value="/M2M/Engine/Engine Trim Center">Engine Trim Center</option>
			myPGNNumber="engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="tilt_or_trim";
		break;
		
		
		case "/M2M/Engine/Engine Temperature Port":	//<option value="/M2M/Engine/Engine Temperature Port">Engine Temperature Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="engine_temp";
		break;		

		case "/M2M/Engine/Engine OIL Temperature Port":	//<option value="/M2M/Engine/Engine OIL Temperature Port">Engine OIL Temperature Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="oil_temp";
		break;	

		case "/M2M/Engine/Engine OIL Pressure Port":	//<option value="/M2M/Engine/Engine OIL Pressure Port">Engine OIL Pressure Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="oil_pressure";
		break;	

		case "/M2M/Engine/Engine Alternator Volts Port":	//<option value="/M2M/Engine/Engine Alternator Volts Port">Engine Alternator Volts Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="alternator_potential";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Port":	//<option value="/M2M/Engine/Engine Fuel Rate Port">Engine Fuel Rate Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="fuel_rate";
		break;


		
		
		case "/M2M/Engine/Engine Trip Fuel Used Port":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="trip_fuel_used";
		break;	
		
		case "/M2M/Engine/Engine Fuel Rate Average Port":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="fuel_rate_average";
		break;	
		
		case "/M2M/Engine/Engine Fuel Rate Economy Port":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="fuel_rate_economy";
		break;	
		
		case "/M2M/Engine/Engine Instantaneous Fuel Economy Port":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="instantaneous_fuel_economy";
		break;	
		
		


		

		case "/M2M/Engine/Engine Coolant Pressure Port":	//<option value="/M2M/Engine/Engine Coolant Pressure Port">Engine Coolant Pressure Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="coolant_pressure";
		break;	

		case "/M2M/Engine/Engine Fuel Pressure Port":	//<option value="/M2M/Engine/Engine Fuel Pressure Port">Engine Fuel Pressure Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="fuel_pressure";
		break;

		case "/M2M/Engine/Engine Coolant Temperature Port":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Reserved 130";
			myPGNParameter="actual_temperature";
		break;			


		case "/M2M/Engine/EGT 0 Port":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="EGT";
			myPGNParameter="actual_temperature";
		break;			
		
		
		case "/M2M/Domestic/EGT Port":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Reserved 134";
			myPGNParameter="actual_temperature";
		break;			

		
		
		case "/M2M/Engine/Engine Hours Port":	//<option value="/M2M/Engine/Engine Hours Port">Engine Hours Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="total_engine_hours";
		break;		
		
		case "/M2M/Engine/Engine Temperature Starboard":	//<option value="/M2M/Engine/Engine Temperature Starboard">Engine Temperature Starboard</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="engine_temp";
		break;		

		case "/M2M/Engine/Engine OIL Temperature Starboard":	//<option value="/M2M/Engine/Engine OIL Temperature Starboard">Engine OIL Temperature Starboard</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="oil_temp";
		break;	

		case "/M2M/Engine/Engine OIL Pressure Starboard":	//<option value="/M2M/Engine/Engine OIL Pressure Starboard">Engine OIL Pressure Starboard</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="oil_pressure";
		break;	

		case "/M2M/Engine/Engine Alternator Volts Starboard":	//<option value="/M2M/Engine/Engine Alternator Volts Starboard">Engine Alternator Volts Starboard</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="alternator_potential";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Starboard":	//<option value="/M2M/Engine/Engine Fuel Rate Starboard">Engine Fuel Rate Starboard</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="fuel_rate";
		break;	
		
		
				
		
		case "/M2M/Engine/Engine Trip Fuel Used Starboard":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="trip_fuel_used";
		break;	
		
		case "/M2M/Engine/Engine Fuel Rate Average Starboard":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="fuel_rate_average";
		break;	
		
		case "/M2M/Engine/Engine Fuel Rate Economy Starboard":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="fuel_rate_economy";
		break;	
		
		case "/M2M/Engine/Engine Instantaneous Fuel Economy Starboard":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="instantaneous_fuel_economy";
		break;	
		
		

		

		case "/M2M/Engine/Engine Coolant Pressure Starboard":	//<option value="/M2M/Engine/Engine Coolant Pressure Starboard">Engine Coolant Pressure Starboard</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="coolant_pressure";
		break;	

		case "/M2M/Engine/Engine Fuel Pressure Starboard":	//<option value="/M2M/Engine/Engine Fuel Pressure Starboard">Engine Fuel Pressure Starboard</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="fuel_pressure";
		break;			
		
		case "/M2M/Engine/Engine Coolant Temperature Starboard":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="Reserved 130";
			myPGNParameter="actual_temperature";
		break;			


		case "/M2M/Engine/EGT 0 Starboard":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="EGT";
			myPGNParameter="actual_temperature";
		break;			
		
		case "/M2M/Domestic/EGT Starboard":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="Reserved 134";
			myPGNParameter="actual_temperature";
		break;			

		
		case "/M2M/Engine/Engine Hours Starboard":	//<option value="/M2M/Engine/Engine Hours Starboard">Engine Hours Starboard</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="total_engine_hours";
		break;	


		case "/M2M/Engine/Engine Temperature Center":	//<option value="/M2M/Engine/Engine Temperature Center">Engine Temperature Center</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="engine_temp";
		break;		

		case "/M2M/Engine/Engine OIL Temperature Center":	//<option value="/M2M/Engine/Engine OIL Temperature Center">Engine OIL Temperature Center</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="oil_temp";
		break;	

		case "/M2M/Engine/Engine OIL Pressure Center":	//<option value="/M2M/Engine/Engine OIL Pressure Center">Engine OIL Pressure Center</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="oil_pressure";
		break;	

		case "/M2M/Engine/Engine Alternator Volts Center":	//<option value="/M2M/Engine/Engine Alternator Volts Center">Engine Alternator Volts Center</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="alternator_potential";
		break;	

		case "/M2M/Engine/Engine Fuel Rate Center":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="fuel_rate";
		break;	
		
		
		case "/M2M/Engine/Engine Trip Fuel Used Center":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="trip_fuel_used";
		break;	
		
		case "/M2M/Engine/Engine Fuel Rate Average Center":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="fuel_rate_average";
		break;	
		
		case "/M2M/Engine/Engine Fuel Rate Economy Center":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="fuel_rate_economy";
		break;	
		
		case "/M2M/Engine/Engine Instantaneous Fuel Economy Center":	//<option value="/M2M/Engine/Engine Fuel Rate Center">Engine Fuel Rate Center</option>
			myPGNNumber="trip_parameters_engine";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="instantaneous_fuel_economy";
		break;	
		
		
		

		case "/M2M/Engine/Engine Coolant Pressure Center":	//<option value="/M2M/Engine/Engine Coolant Pressure Center">Engine Coolant Pressure Center</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="coolant_pressure";
		break;	

		case "/M2M/Engine/Engine Fuel Pressure Center":	//<option value="/M2M/Engine/Engine Fuel Pressure Center">Engine Fuel Pressure Center</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="fuel_pressure";
		break;		

		case "/M2M/Engine/Engine Coolant Temperature Center":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="Reserved 130";
			myPGNParameter="actual_temperature";
		break;	

		case "/M2M/Engine/EGT 0 Center":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="EGT";
			myPGNParameter="actual_temperature";
		break;		

		case "/M2M/Domestic/EGT Center":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="Reserved 134";
			myPGNParameter="actual_temperature";
		break;			
		
		case "/M2M/Engine/Engine Hours Center":	//<option value="/M2M/Engine/Engine Hours Center">Engine Hours Center</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="total_engine_hours";
		break;	
		
		case "/M2M/Engine/Generator RPM J1939":	//<option value="/M2M/Engine/Engine RPM Center">Engine RPM Center </option>
			myPGNNumber="engine_parameters_rapid_update";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="speed";
		break;		
		
		
		case "/M2M/Engine/Generator Temperature J1939":	//<option value="/M2M/Engine/Engine Temperature Port">Engine Temperature Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="engine_temp";
		break;		



		case "/M2M/Engine/Generator OIL Pressure J1939": //<option value="/M2M/Engine/Generator OIL Pressure J1939">Generator - J1939 - OIL Pressure</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="oil_pressure";
		break;		
		
		case "/M2M/Engine/Generator Alternator Volts J1939": //<option value="/M2M/Engine/Generator Alternator Volts J1939">Generator - J1939 - Alternator Volts</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="alternator_potential";
		break;	

		case "/M2M/Engine/Generator Battery Volts J1939": //<option value="/M2M/Engine/Generator Alternator Volts J1939">Generator - J1939 - Alternator Volts</option>
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="voltage";
		break;				
		
		
		case "/M2M/Engine/Generator OIL Temperature J1939":	//<option value="/M2M/Engine/Engine Temperature Port">Engine Temperature Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="oil_temp";
		break;	
		
		case "/M2M/Engine/Generator Fuel Temperature J1939":	//<option value="/M2M/Engine/Engine Temperature Port">Engine Temperature Port</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="fuel_temp";
		break;		



		case "/M2M/Engine/Generator Fuel Level J1939": //<option value="/M2M/Engine/Generator OIL Pressure J1939">Generator - J1939 - OIL Pressure</option>
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="level";
		break;		
		
		case "/M2M/Engine/Generator Fuel Rate J1939": //<option value="/M2M/Engine/Generator Alternator Volts J1939">Generator - J1939 - Alternator Volts</option>
			myPGNNumber="engine_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="fuel_rate";
		break;			
		
		
		
		
		
		
		
		

		case "/M2M/Engine/Transmission OIL Pressure Port":	//<option value="/M2M/Engine/Transmission OIL Pressure Port">Transmission OIL Pressure Port </option>
			myPGNNumber="transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="oil_pressure";
		break;
		
		case "/M2M/Engine/Transmission OIL Temperature Port":	//<option value="/M2M/Engine/Transmission OIL Temperature Port">Transmission OIL Temperature Port </option>
			myPGNNumber="transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="oil_temp";
		break;	

		case "/M2M/Engine/Transmission OIL Pressure Starboard":	//<option value="/M2M/Engine/Transmission OIL Pressure Starboard">Transmission OIL Pressure Starboard </option>
			myPGNNumber="transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="oil_pressure";
		break;
		
		case "/M2M/Engine/Transmission OIL Temperature Starboard":	//<option value="/M2M/Engine/Transmission OIL Temperature Starboard">Transmission OIL Temperature Starboard </option>
			myPGNNumber="transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="oil_temp";
		break;		
		
		case "/M2M/Engine/Transmission OIL Pressure Center":	//<option value="/M2M/Engine/Transmission OIL Pressure Center">Transmission OIL Pressure Center </option>
			myPGNNumber="transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="oil_pressure";
		break;
		
		case "/M2M/Engine/Transmission OIL Temperature Center":	//<option value="/M2M/Engine/Transmission OIL Temperature Center">Transmission OIL Temperature Center </option>
			myPGNNumber="transmission_parameters_dynamic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="oil_temp";
		break;	

		case "/M2M/Battery/Battery Volts Port":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="voltage";
		break;
		
		case "/M2M/Battery/Battery Current Port":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="current";
		break;		
		
		case "/M2M/Battery/Battery Temperature Port":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="temperature";
		break;	
		
		case "/M2M/Battery/Battery StateOfCharge Port":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="stateofcharge";
		break
		
		case "/M2M/Battery/Battery TimeRemaining Port":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="timeremaining";
		break


		case "/M2M/Battery/Battery Volts Starboard":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="voltage";
		break;
		
		case "/M2M/Battery/Battery Current Starboard":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="current";
		break;		
		
		case "/M2M/Battery/Battery Temperature Starboard":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="temperature";
		break;	

		case "/M2M/Battery/Battery StateOfCharge Starboard":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="stateofcharge";
		break
		
		case "/M2M/Battery/Battery TimeRemaining Starboard":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="timeremaining";
		break
		
		case "/M2M/Battery/Battery Volts Center":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="voltage";
		break;
		
		case "/M2M/Battery/Battery Current Center":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="current";
		break;		
		
		case "/M2M/Battery/Battery Temperature Center":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="temperature";
		break;	
		
		case "/M2M/Battery/Battery StateOfCharge Center":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="stateofcharge";
		break
		
		case "/M2M/Battery/Battery TimeRemaining Center":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="timeremaining";
		break		
		
		case "/M2M/Battery/Battery Volts J1939":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="voltage";
		break;
		
		case "/M2M/Battery/Battery Current J1939":	
			myPGNNumber="battery_status";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="J1939";
			myPGNParameter="current";
		break;		
		
		
		
	
		case "/M2M/AC/UTIL/Volts_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="UTIL";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/UTIL/Volts_Line_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="UTIL";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/UTIL/Amps_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="UTIL";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/UTIL/Frequency_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="UTIL";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/UTIL/Power_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="UTIL";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/UTIL/Energy_Phase_A":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="UTIL";
			myPGNParameter="ac_kwatthours";
		break;		
		

		
		case "/M2M/AC/UTIL/Volts_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="UTIL";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/UTIL/Volts_Line_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="UTIL";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/UTIL/Amps_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="UTIL";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/UTIL/Frequency_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="UTIL";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/UTIL/Power_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="UTIL";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/UTIL/Energy_Phase_B":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="UTIL";
			myPGNParameter="ac_kwatthours";
		break;		
		
		
		case "/M2M/AC/UTIL/Volts_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="UTIL";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/UTIL/Volts_Line_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="UTIL";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/UTIL/Amps_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="UTIL";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/UTIL/Frequency_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="UTIL";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/UTIL/Power_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="UTIL";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/UTIL/Energy_Phase_C":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="UTIL";
			myPGNParameter="ac_kwatthours";
		break;			
		
		
		
		case "/M2M/AC/UTIL/Volts_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="UTIL";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/UTIL/Volts_Line_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="UTIL";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/UTIL/Amps_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="UTIL";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/UTIL/Frequency_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="UTIL";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/UTIL/Power_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="UTIL";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/UTIL/Energy_Avg":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="UTIL";
			myPGNParameter="ac_kwatthours";
		break;			
		
		
		
		case "/M2M/AC/UTIL/TotalEnergy_Import":	
			myPGNNumber="ac_total_energy";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="UTIL";
			myPGNParameter="import_kwatt_hours";
		break;		
		
			
		case "/M2M/AC/UTIL/TotalEnergy_Export":	
			myPGNNumber="ac_total_energy";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="UTIL";
			myPGNParameter="export_kwatt_hours";
		break;	
		
		
		
		
	
		case "/M2M/AC/GEN/Volts_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="GEN";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/GEN/Volts_Line_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="GEN";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/GEN/Amps_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="GEN";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/GEN/Frequency_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="GEN";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/GEN/Power_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="GEN";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/GEN/Energy_Phase_A":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="GEN";
			myPGNParameter="ac_kwatthours";
		break;		
		

		
		case "/M2M/AC/GEN/Volts_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="GEN";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/GEN/Volts_Line_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="GEN";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/GEN/Amps_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="GEN";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/GEN/Frequency_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="GEN";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/GEN/Power_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="GEN";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/GEN/Energy_Phase_B":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="GEN";
			myPGNParameter="ac_kwatthours";
		break;		
		
		
		case "/M2M/AC/GEN/Volts_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="GEN";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/GEN/Volts_Line_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="GEN";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/GEN/Amps_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="GEN";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/GEN/Frequency_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="GEN";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/GEN/Power_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="GEN";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/GEN/Energy_Phase_C":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="GEN";
			myPGNParameter="ac_kwatthours";
		break;			
		
		
		
		case "/M2M/AC/GEN/Volts_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="GEN";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/GEN/Volts_Line_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="GEN";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/GEN/Amps_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="GEN";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/GEN/Frequency_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="GEN";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/GEN/Power_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="GEN";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/GEN/Energy_Avg":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="GEN";
			myPGNParameter="ac_kwatthours";
		break;			
		
		
		
		case "/M2M/AC/GEN/TotalEnergy_Import":	
			myPGNNumber="ac_total_energy";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="GEN";
			myPGNParameter="import_kwatt_hours";
		break;		
		
			
		case "/M2M/AC/GEN/TotalEnergy_Export":	
			myPGNNumber="ac_total_energy";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="GEN";
			myPGNParameter="export_kwatt_hours";
		break;		




		
	
		case "/M2M/AC/LIGHTS/Volts_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LIGHTS";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/LIGHTS/Volts_Line_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LIGHTS";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/LIGHTS/Amps_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LIGHTS";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/LIGHTS/Frequency_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LIGHTS";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/LIGHTS/Power_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LIGHTS";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/LIGHTS/Energy_Phase_A":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LIGHTS";
			myPGNParameter="ac_kwatthours";
		break;		
		

		
		case "/M2M/AC/LIGHTS/Volts_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LIGHTS";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/LIGHTS/Volts_Line_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LIGHTS";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/LIGHTS/Amps_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LIGHTS";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/LIGHTS/Frequency_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LIGHTS";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/LIGHTS/Power_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LIGHTS";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/LIGHTS/Energy_Phase_B":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LIGHTS";
			myPGNParameter="ac_kwatthours";
		break;		
		
		
		case "/M2M/AC/LIGHTS/Volts_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LIGHTS";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/LIGHTS/Volts_Line_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LIGHTS";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/LIGHTS/Amps_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LIGHTS";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/LIGHTS/Frequency_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LIGHTS";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/LIGHTS/Power_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LIGHTS";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/LIGHTS/Energy_Phase_C":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LIGHTS";
			myPGNParameter="ac_kwatthours";
		break;			
		
		
		
		case "/M2M/AC/LIGHTS/Volts_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LIGHTS";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/LIGHTS/Volts_Line_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LIGHTS";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/LIGHTS/Amps_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LIGHTS";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/LIGHTS/Frequency_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LIGHTS";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/LIGHTS/Power_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LIGHTS";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/LIGHTS/Energy_Avg":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LIGHTS";
			myPGNParameter="ac_kwatthours";
		break;		
		
		
		
		
		
			
	
		case "/M2M/AC/HEAT/Volts_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="HEAT";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/HEAT/Volts_Line_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="HEAT";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/HEAT/Amps_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="HEAT";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/HEAT/Frequency_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="HEAT";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/HEAT/Power_Phase_A":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="HEAT";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/HEAT/Energy_Phase_A":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="HEAT";
			myPGNParameter="ac_kwatthours";
		break;		
		

		
		case "/M2M/AC/HEAT/Volts_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="HEAT";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/HEAT/Volts_Line_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="HEAT";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/HEAT/Amps_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="HEAT";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/HEAT/Frequency_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="HEAT";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/HEAT/Power_Phase_B":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="HEAT";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/HEAT/Energy_Phase_B":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="HEAT";
			myPGNParameter="ac_kwatthours";
		break;		
		
		
		case "/M2M/AC/HEAT/Volts_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="HEAT";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/HEAT/Volts_Line_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="HEAT";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/HEAT/Amps_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="HEAT";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/HEAT/Frequency_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="HEAT";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/HEAT/Power_Phase_C":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="HEAT";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/HEAT/Energy_Phase_C":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="HEAT";
			myPGNParameter="ac_kwatthours";
		break;			
		
		
		
		case "/M2M/AC/HEAT/Volts_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="HEAT";
			myPGNParameter="ac_line_neutral_volts";
		break;
		
		case "/M2M/AC/HEAT/Volts_Line_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="HEAT";
			myPGNParameter="ac_line_line_volts";
		break;		
		
		case "/M2M/AC/HEAT/Amps_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="HEAT";
			myPGNParameter="ac_amps";
		break;		
		
		case "/M2M/AC/HEAT/Frequency_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="HEAT";
			myPGNParameter="ac_frequency";
		break;	
		
		case "/M2M/AC/HEAT/Power_Avg":	
			myPGNNumber="ac_basic";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="HEAT";
			myPGNParameter="ac_watts";
		break;
		
		case "/M2M/AC/HEAT/Energy_Avg":	
			myPGNNumber="ac_watthours";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="HEAT";
			myPGNParameter="ac_kwatthours";
		break;			


		
		
		
		case "/M2M/Tank/Fuel Level Port":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Fuel Level Starboard":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Fuel Level Center":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="level";
		break;
		
		case "/M2M/Tank/Fuel Level Fwd":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="0";
			myPGNParameter="level";
		break;
		
		case "/M2M/Tank/Fuel Level Aft":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="0";
			myPGNParameter="level";
		break;
		
		case "/M2M/Tank/Fuel Level Day1":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="0";
			myPGNParameter="level";
		break;
		
		case "/M2M/Tank/Fuel Level Day2":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="0";
			myPGNParameter="level";
		break;
		
		case "/M2M/Tank/Fuel Level Day3":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="0";
			myPGNParameter="level";
		break;
		
		
		
		
		
		
		
		
		

		case "/M2M/Tank/Water Level Port":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="1";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Water Level Starboard":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="1";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Water Level Center":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="1";
			myPGNParameter="level";
		break;		
		
		case "/M2M/Tank/Waste Level Port":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="2";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Waste Level Starboard":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="2";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Waste Level Center":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="2";
			myPGNParameter="level";
		break;		
						
		case "/M2M/Tank/Live Well Port":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="3";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Live Well Starboard":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="3";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Live Well Center":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="3";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Oil Level Port":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="4";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Oil Level Starboard":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="4";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Oil Level Center":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="4";
			myPGNParameter="level";
		break;	

		case "/M2M/Tank/Black Water Level Port":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="5";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Black Water Level Starboard":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="5";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Black Water Level Center":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="5";
			myPGNParameter="level";
		break;	
		
	   case "/M2M/Tank/Bilge Level Port":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="6";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Bilge Level Starboard":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="6";
			myPGNParameter="level";
		break;	
		
		case "/M2M/Tank/Bilge Level Center":	
			myPGNNumber="fluid_level";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="6";
			myPGNParameter="level";
		break;	
		
		
		case "/M2M/Domestic/Water Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Sea Temperature";
			myPGNParameter="actual_temperature";
		break;		
		
		case "/M2M/Domestic/Outside Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Outside Temperature";
			myPGNParameter="actual_temperature";
		break;	
		
		case "/M2M/Domestic/Inside Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Inside Temperature";
			myPGNParameter="actual_temperature";
		break;			
		
		
		case "/M2M/Domestic/Engine Room Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Engine Room Temperature";
			myPGNParameter="actual_temperature";
		break;	
		
		case "/M2M/Domestic/Main Cabin Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Main Cabin Temperature";
			myPGNParameter="actual_temperature";
		break;	
		
		case "/M2M/Domestic/Live Well Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Live Well";
			myPGNParameter="actual_temperature";
		break;	

		
		case "/M2M/Domestic/Bait Well Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Bait Well";
			myPGNParameter="actual_temperature";
		break;	

		
		case "/M2M/Domestic/Refrigeration 1 Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Refrigeration";
			myPGNParameter="actual_temperature";
		break;	

		case "/M2M/Domestic/Refrigeration 2 Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="Refrigeration";
			myPGNParameter="actual_temperature";
		break;	
		
		case "/M2M/Domestic/Heating Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Heating";
			myPGNParameter="actual_temperature";
		break;	

		
		case "/M2M/Domestic/Freezer Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Freezer";
			myPGNParameter="actual_temperature";
		break;	
		
		case "/M2M/Domestic/Freezer 2 Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="Freezer";
			myPGNParameter="actual_temperature";
		break;	
		
		case "/M2M/Domestic/Freezer 3 Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="Freezer";
			myPGNParameter="actual_temperature";
		break;	

		
		case "/M2M/Domestic/Wind Chill A Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Wind Chill A";
			myPGNParameter="actual_temperature";
		break;	

		
		case "/M2M/Domestic/Wind Chill T Temperature":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Wind Chill T";
			myPGNParameter="actual_temperature";
		break;	

		
		case "/M2M/Domestic/Heat Index":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Heat Index";
			myPGNParameter="actual_temperature";
		break;	
		
		case "/M2M/Domestic/Dew Point":	
			myPGNNumber="temperature";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="Dew Point";
			myPGNParameter="actual_temperature";
		break;	
		
		case "/M2M/LED Dimmer/Value 0 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		case "/M2M/LED Dimmer/Value 2 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		case "/M2M/LED Dimmer/Value 2 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
				
		
		case "/M2M/LED Dimmer/Value 0 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		case "/M2M/LED Dimmer/Value 2 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
				
		
		case "/M2M/LED Dimmer/Value 0 Zone 3":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 3":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		case "/M2M/LED Dimmer/Value 2 Zone 3":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 3":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 3":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
				
		
		case "/M2M/LED Dimmer/Value 0 Zone 4":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 4":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 4":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 4":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 4":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
				
		case "/M2M/LED Dimmer/Value 0 Zone 5":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 5":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
			
		case "/M2M/LED Dimmer/Value 2 Zone 5":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 5":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 5":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
			
		
		case "/M2M/LED Dimmer/Value 0 Zone 6":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 6":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 6":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 6":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 6":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
				
		case "/M2M/LED Dimmer/Value 0 Zone 7":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 7":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		case "/M2M/LED Dimmer/Value 2 Zone 7":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 7":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 7":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
				
		
		case "/M2M/LED Dimmer/Value 0 Zone 8":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="8";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 8":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="8";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 8":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="8";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 8":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="8";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 8":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="8";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
				
		case "/M2M/LED Dimmer/Value 0 Zone 9":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="9";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 9":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="9";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 9":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="9";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 9":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="9";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 9":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="9";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
				
		
		case "/M2M/LED Dimmer/Value 0 Zone 10":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="10";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 10":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="10";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 10":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="10";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 10":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="10";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 10":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="10";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 11":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="11";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	
	
		case "/M2M/LED Dimmer/Value 1 Zone 11":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="11";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;			
		
		case "/M2M/LED Dimmer/Value 2 Zone 11":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="11";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 11":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="11";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 11":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="11";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		

		
		
		case "/M2M/LED Dimmer/Value 0 Zone 12":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="12";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 12":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="12";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 12":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="12";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 12":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="12";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 12":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="12";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 13":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="13";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 13":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="13";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 13":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="13";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 13":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="13";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 13":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="13";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 14":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="14";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 14":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="14";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 14":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="14";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 14":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="14";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 14":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="14";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 15":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="15";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 15":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="15";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 15":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="15";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 15":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="15";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 15":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="15";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 16":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="16";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 16":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="16";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 16":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="16";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 16":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="16";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 16":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="16";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 17":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="17";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 17":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="17";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 17":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="17";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 17":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="17";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 17":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="17";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 18":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="18";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 18":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="18";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 18":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="18";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 18":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="18";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 18":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="18";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 19":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="19";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 19":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="19";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		

		
		case "/M2M/LED Dimmer/Value 2 Zone 19":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="19";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;
		
		case "/M2M/LED Dimmer/Value 3 Zone 19":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="19";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;
		
		case "/M2M/LED Dimmer/Value 4 Zone 19":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="19";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;
		
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 20":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="20";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 20":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="20";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		case "/M2M/LED Dimmer/Value 2 Zone 20":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="20";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 20":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="20";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 20":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="20";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
				
		case "/M2M/LED Dimmer/Value 0 Zone 21":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="21";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 21":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="21";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 21":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="21";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 21":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="21";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 21":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="21";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 22":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="22";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 22":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="22";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 22":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="22";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 22":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="22";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 22":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="22";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 23":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="23";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 23":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="23";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 23":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="23";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 23":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="23";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 23":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="23";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 24":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="24";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 24":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="24";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 24":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="24";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 24":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="24";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 24":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="24";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 25":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="25";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 25":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="25";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 25":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="25";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 25":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="25";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 25":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="25";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 26":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="26";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 26":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="26";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 26":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="26";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 26":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="26";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 26":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="26";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 27":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="27";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 27":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="27";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 27":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="27";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 27":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="27";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 27":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="27";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 28":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="28";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 28":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="28";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
		
		
		case "/M2M/LED Dimmer/Value 2 Zone 28":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="28";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 28":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="28";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 28":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="28";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 29":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="29";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	
		

		case "/M2M/LED Dimmer/Value 1 Zone 29":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="29";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;
		
		case "/M2M/LED Dimmer/Value 2 Zone 29":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="29";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 29":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="29";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 29":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="29";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
	
		
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 30":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="30";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 30":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="30";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;	

		
		case "/M2M/LED Dimmer/Value 2 Zone 30":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="30";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 30":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="30";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 30":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="30";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
		
		
		
		case "/M2M/LED Dimmer/Value 0 Zone 31":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="31";
			myPGNType="LED 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer/Value 1 Zone 31":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="31";
			myPGNType="LED 1 Channel";
			myPGNParameter="value1";
		break;		
				
				
			
		case "/M2M/LED Dimmer/Value 2 Zone 31":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="31";
			myPGNType="LED 1 Channel";
			myPGNParameter="value2";
		break;	

		case "/M2M/LED Dimmer/Value 3 Zone 31":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="31";
			myPGNType="LED 1 Channel";
			myPGNParameter="value3";
		break;		


		case "/M2M/LED Dimmer/Value 4 Zone 31":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="31";
			myPGNType="LED 1 Channel";
			myPGNParameter="value4";
		break;	
		
			
		
		
		case "/M2M/LED Dimmer 4 Channel/Value 0 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LED 4 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer 4 Channel/Value 1 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LED 4 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/LED Dimmer 4 Channel/Value 2 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LED 4 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/LED Dimmer 4 Channel/Value 3 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LED 4 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/LED Dimmer 4 Channel/Value 4 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="LED 4 Channel";
			myPGNParameter="value4";
		break;	
		
		case "/M2M/LED Dimmer 4 Channel/Value 0 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 4 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer 4 Channel/Value 1 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 4 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/LED Dimmer 4 Channel/Value 2 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 4 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/LED Dimmer 4 Channel/Value 3 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 4 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/LED Dimmer 4 Channel/Value 4 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 4 Channel";
			myPGNParameter="value4";
		break;	
		
		case "/M2M/LED Dimmer 4 Channel/Value 0 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 4 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/LED Dimmer 4 Channel/Value 1 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 4 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/LED Dimmer 4 Channel/Value 2 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 4 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/LED Dimmer 4 Channel/Value 3 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 4 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/LED Dimmer 4 Channel/Value 4 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="LED 4 Channel";
			myPGNParameter="value4";
		break;	
		
		
		

		case "/M2M/RGB Dimmer/Value 0 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/RGB Dimmer/Value 1 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/RGB Dimmer/Value 2 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/RGB Dimmer/Value 3 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/RGB Dimmer/Value 4 Zone 0":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value4";
		break;	
		
		case "/M2M/RGB Dimmer/Value 0 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/RGB Dimmer/Value 1 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/RGB Dimmer/Value 2 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/RGB Dimmer/Value 3 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/RGB Dimmer/Value 4 Zone 1":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value4";
		break;	
		
		case "/M2M/RGB Dimmer/Value 0 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/RGB Dimmer/Value 1 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/RGB Dimmer/Value 2 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/RGB Dimmer/Value 3 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/RGB Dimmer/Value 4 Zone 2":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value4";
		break;	
		

		case "/M2M/RGB Dimmer/Value 0 Zone 3":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/RGB Dimmer/Value 1 Zone 3":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/RGB Dimmer/Value 2 Zone 3":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/RGB Dimmer/Value 3 Zone 3":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/RGB Dimmer/Value 4 Zone 3":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="3";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value4";
		break;	

		case "/M2M/RGB Dimmer/Value 0 Zone 4":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/RGB Dimmer/Value 1 Zone 4":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/RGB Dimmer/Value 2 Zone 4":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/RGB Dimmer/Value 3 Zone 4":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/RGB Dimmer/Value 4 Zone 4":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="4";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value4";
		break;	

		case "/M2M/RGB Dimmer/Value 0 Zone 5":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/RGB Dimmer/Value 1 Zone 5":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/RGB Dimmer/Value 2 Zone 5":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/RGB Dimmer/Value 3 Zone 5":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/RGB Dimmer/Value 4 Zone 5":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="5";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value4";
		break;	

		case "/M2M/RGB Dimmer/Value 0 Zone 6":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/RGB Dimmer/Value 1 Zone 6":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/RGB Dimmer/Value 2 Zone 6":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/RGB Dimmer/Value 3 Zone 6":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/RGB Dimmer/Value 4 Zone 6":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="6";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value4";
		break;	

		case "/M2M/RGB Dimmer/Value 0 Zone 7":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/RGB Dimmer/Value 1 Zone 7":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/RGB Dimmer/Value 2 Zone 7":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/RGB Dimmer/Value 3 Zone 7":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/RGB Dimmer/Value 4 Zone 7":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="7";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value4";
		break;	

		case "/M2M/RGB Dimmer/Value 0 Zone 8":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="8";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value0";
		break;	

		case "/M2M/RGB Dimmer/Value 1 Zone 8":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="8";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value1";
		break;	
		case "/M2M/RGB Dimmer/Value 2 Zone 8":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="8";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value2";
		break;	
		
		case "/M2M/RGB Dimmer/Value 3 Zone 8":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="8";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value3";
		break;	
		
		case "/M2M/RGB Dimmer/Value 4 Zone 8":	
			myPGNNumber="seasmartdimmer";
			myPGNSource=Source;
			myPGNInstance="8";
			myPGNType="RGB 1 Channel";
			myPGNParameter="value4";
		break;			
		
		
		
		
		case "/M2M/Switch/Value 0 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value0";
		break;	
		
		case "/M2M/Switch/Runtime 0 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 0 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="0";
			myPGNParameter="cycles";
		break;	
				
		
		
		
		
		
		case "/M2M/Switch/Value 1 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value1";
		break;
		
				
		case "/M2M/Switch/Runtime 1 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="1";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 1 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="1";
			myPGNParameter="cycles";
		break;	
				
		
		
		
		case "/M2M/Switch/Value 2 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value2";
		break;
		
		
		case "/M2M/Switch/Runtime 2 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="2";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 2 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="2";
			myPGNParameter="cycles";
		break;	
				
		
				
		
		case "/M2M/Switch/Value 3 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value3";
		break;
		
		
		case "/M2M/Switch/Runtime 3 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="3";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 3 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="3";
			myPGNParameter="cycles";
		break;	
				
		
				
		
		
		
		case "/M2M/Switch/Value 4 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/Switch/Runtime 4 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="4";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 4 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="4";
			myPGNParameter="cycles";
		break;	
				
		
				
		
		
		case "/M2M/Switch/Value 5 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value5";
		break;
		
		
		
		case "/M2M/Switch/Runtime 5 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="5";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 5 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="5";
			myPGNParameter="cycles";
		break;	
				
		
				
		
		
		case "/M2M/Switch/Value 6 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value6";
		break;
		
		
		
		case "/M2M/Switch/Runtime 6 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="6";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 6 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="6";
			myPGNParameter="cycles";
		break;	
				
		
				
		
		case "/M2M/Switch/Value 7 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value7";
		break;
		
		
		
		case "/M2M/Switch/Runtime 7 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="7";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 7 Port":	
			myPGNNumber="seasmartindicator";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="7";
			myPGNParameter="cycles";
		break;	
				
		
				
		
		
		case "/M2M/Switch/Value 8 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value8";
		break;
		
		
		case "/M2M/Switch/Value 9 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value9";
		break;
		
		case "/M2M/Switch/Value 10 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value10";
		break;
		
		case "/M2M/Switch/Value 11 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value11";
		break;
		
		case "/M2M/Switch/Value 12 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value12";
		break;
		
		case "/M2M/Switch/Value 13 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value13";
		break;
		
		case "/M2M/Switch/Value 14 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value14";
		break;
		
		case "/M2M/Switch/Value 15 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="value15";
		break;
		
		case "/M2M/Switch/Bank 0 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="bank0";
		break;
		
		case "/M2M/Switch/Bank 1 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="bank1";
		break;
		
		case "/M2M/Switch/Bank 2 Port":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="0";
			myPGNType="NULL";
			myPGNParameter="bank2";
		break;
		
		case "/M2M/Switch/Value 0 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value0";
		break;	
		
		
		case "/M2M/Switch/Runtime 0 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 0 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="0";
			myPGNParameter="cycles";
		break;	
				
		
				
		
		
		case "/M2M/Switch/Value 1 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value1";
		break;
		
		
		case "/M2M/Switch/Runtime 1 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="1";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 1 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="1";
			myPGNParameter="cycles";
		break;	
				
				
		
		
		case "/M2M/Switch/Value 2 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value2";
		break;

		
		case "/M2M/Switch/Runtime 2 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="2";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 2 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="2";
			myPGNParameter="cycles";
		break;	
				
				
		
		case "/M2M/Switch/Value 3 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value3";
		break;
		
		
		case "/M2M/Switch/Runtime 3 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="3";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 3 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="3";
			myPGNParameter="cycles";
		break;	
				
						
		
		case "/M2M/Switch/Value 4 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/Switch/Runtime 4 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="4";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 4 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="4";
			myPGNParameter="cycles";
		break;	
				
						
		
		case "/M2M/Switch/Value 5 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value5";
		break;
		
		
		case "/M2M/Switch/Runtime 5 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="5";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 5 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="5";
			myPGNParameter="cycles";
		break;	
				
						
		
		case "/M2M/Switch/Value 6 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value6";
		break;
		
		
		case "/M2M/Switch/Runtime 6 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="6";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 6 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="6";
			myPGNParameter="cycles";
		break;	
				
						
		
		case "/M2M/Switch/Value 7 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value7";
		break;
		
		
		
		case "/M2M/Switch/Runtime 7 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="7";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 7 Starboard":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="7";
			myPGNParameter="cycles";
		break;	
				
						
		
		
		case "/M2M/Switch/Value 8 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value8";
		break;
		
		
		case "/M2M/Switch/Value 9 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value9";
		break;
		
		case "/M2M/Switch/Value 10 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value10";
		break;
		
		case "/M2M/Switch/Value 11 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value11";
		break;
		
		case "/M2M/Switch/Value 12 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value12";
		break;
		
		case "/M2M/Switch/Value 13 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value13";
		break;
		
		case "/M2M/Switch/Value 14 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value14";
		break;
		
		case "/M2M/Switch/Value 15 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="value15";
		break;
		
		case "/M2M/Switch/Bank 0 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="bank0";
		break;
		
		case "/M2M/Switch/Bank 1 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="bank1";
		break;
		
		case "/M2M/Switch/Bank 2 Starboard":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="1";
			myPGNType="NULL";
			myPGNParameter="bank2";
		break;
			
		
		
		
		case "/M2M/Switch/Value 0 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value0";
		break;	
		
		
		case "/M2M/Switch/Runtime 0 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 0 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="0";
			myPGNParameter="cycles";
		break;	
				
						
		
		case "/M2M/Switch/Value 1 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value1";
		break;
		
		
		case "/M2M/Switch/Runtime 1 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="1";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 1 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="1";
			myPGNParameter="cycles";
		break;			
		
		case "/M2M/Switch/Value 2 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value2";
		break;
		
		
		case "/M2M/Switch/Runtime 2 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="2";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 2 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="2";
			myPGNParameter="cycles";
		break;			
		
		case "/M2M/Switch/Value 3 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value3";
		break;
		
		
		case "/M2M/Switch/Runtime 3 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="3";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 3 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="3";
			myPGNParameter="cycles";
		break;			
		
		case "/M2M/Switch/Value 4 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value4";
		break;
		
		
		case "/M2M/Switch/Runtime 4 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="4";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 4 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="4";
			myPGNParameter="cycles";
		break;			
		
		case "/M2M/Switch/Value 5 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value5";
		break;	
		
		case "/M2M/Switch/Runtime 5 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="5";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 5 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="5";
			myPGNParameter="cycles";
		break;			
		

		
		case "/M2M/Switch/Value 6 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value6";
		break;
		
		
		case "/M2M/Switch/Runtime 6 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="6";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 6 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="6";
			myPGNParameter="cycles";
		break;			
		
		case "/M2M/Switch/Value 7 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value7";
		break;
		
		
		case "/M2M/Switch/Runtime 7 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="7";
			myPGNParameter="runtime_sec";
		break;	
		
		case "/M2M/Switch/Cycles 7 Center":	
			myPGNNumber="indicator_runtime";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="7";
			myPGNParameter="cycles";
		break;			
		
		case "/M2M/Switch/Value 8 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value8";
		break;
		
		
		case "/M2M/Switch/Value 9 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value9";
		break;
		
		case "/M2M/Switch/Value 10 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value10";
		break;
		
		case "/M2M/Switch/Value 11 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value11";
		break;
		
		case "/M2M/Switch/Value 12 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value12";
		break;
		
		case "/M2M/Switch/Value 13 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value13";
		break;
		
		case "/M2M/Switch/Value 14 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value14";
		break;
		
		case "/M2M/Switch/Value 15 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="value15";
		break;
		
		case "/M2M/Switch/Bank 0 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="bank0";
		break;
		
		case "/M2M/Switch/Bank 1 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="Center";
		break;
		
		case "/M2M/Switch/Bank 2 Center":	
			myPGNNumber="seasmartswitch";
			myPGNSource=Source;
			myPGNInstance="2";
			myPGNType="NULL";
			myPGNParameter="bank2";
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