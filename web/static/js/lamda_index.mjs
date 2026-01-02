export async function handler(event, context) {
  console.log("Post confirmation trigger initiated.");
  
  const userName = event.userName;
  const userEmail = event.request.userAttributes.email;
  const userPhone = event.request.userAttributes.phone_number;
  const userEmailVerified = event.request.userAttributes.email_verified ;
  const userPhoneVerified = event.request.userAttributes.phone_number_verified ;
  const device = event.request.userAttributes.name;
  const apiUrl = `https://www.helmsmart-cloud.com/aws_cognito_user_added?username=${userName}&device=${device}&email=${userEmail}&emailverified=${userEmailVerified}&phone=${userPhone}&phoneverified=${userPhoneVerified}`;
  
  try {
      const response = await fetch(apiUrl, {
          method: 'GET',
          headers: {
              // Add any necessary headers, e.g., API keys or authorization tokens
              'Authorization': 'Bearer YOUR_API_TOKEN' 
          }
      });

      if (!response.ok) {
          console.error(`HTTP error! status: ${response.status}`);
      } else {
          const data = await response.json();
          console.log("External API response data:", data);
      }
      
  } catch (error) {
      console.error("Failed to make HTTP GET request:", error);
  }
  
  // Amazon Cognito expects the original event object back
  return event;
}
