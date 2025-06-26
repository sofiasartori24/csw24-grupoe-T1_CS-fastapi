// This script allows running API tests from the command line
// Usage: node runApiTests.js [all|users|lessons|reservations|resources]

// Import required modules
const fs = require('fs');
const path = require('path');
const https = require('https');
const http = require('http');

// Read the API URL from .env file
let apiUrl = '';
try {
  const envContent = fs.readFileSync(path.join(__dirname, '.env'), 'utf8');
  const apiUrlMatch = envContent.match(/REACT_APP_API_URL=(.+)/);
  if (apiUrlMatch && apiUrlMatch[1]) {
    apiUrl = apiUrlMatch[1];
  }
} catch (error) {
  console.error('Error reading .env file:', error.message);
  apiUrl = 'https://1jjdwnh7k5.execute-api.us-east-1.amazonaws.com/Prod'; // Fallback
}

// Remove trailing slash if present
if (apiUrl.endsWith('/')) {
  apiUrl = apiUrl.slice(0, -1);
}

// Simple fetch function using native Node.js http/https modules
const fetchApi = (endpoint, options = {}) => {
  return new Promise((resolve, reject) => {
    const url = new URL(endpoint.startsWith('/') ? `${apiUrl}${endpoint}` : `${apiUrl}/${endpoint}`);
    
    const requestOptions = {
      hostname: url.hostname,
      port: url.port || (url.protocol === 'https:' ? 443 : 80),
      path: url.pathname + url.search,
      method: options.method || 'GET',
      headers: {
        'Content-Type': 'application/json',
        ...options.headers
      }
    };
    
    const client = url.protocol === 'https:' ? https : http;
    
    const req = client.request(requestOptions, (res) => {
      let data = '';
      
      res.on('data', (chunk) => {
        data += chunk;
      });
      
      res.on('end', () => {
        try {
          const parsedData = data ? JSON.parse(data) : {};
          if (res.statusCode >= 200 && res.statusCode < 300) {
            resolve({ data: parsedData, status: res.statusCode });
          } else {
            reject({
              response: {
                data: parsedData,
                status: res.statusCode
              },
              message: `Request failed with status code ${res.statusCode}`
            });
          }
        } catch (error) {
          reject({
            message: `Error parsing response: ${error.message}`,
            response: {
              data: data,
              status: res.statusCode
            }
          });
        }
      });
    });
    
    req.on('error', (error) => {
      reject({ message: error.message });
    });
    
    if (options.body) {
      req.write(JSON.stringify(options.body));
    }
    
    req.end();
  });
};

// Test data
const testUserId = 3; // Using the same user ID as in CreateLesson.tsx (professor role)
const testResourceId = 1; // Replace with a valid resource ID
const testLessonId = 1; // Replace with a valid lesson ID if available
const testReservationId = 1; // Replace with a valid reservation ID if available

// Utility function to log test results
const logResult = (testName, result) => {
  console.log(`✅ ${testName} - Success:`, JSON.stringify(result, null, 2));
  return result;
};

const logError = (testName, error) => {
  console.error(`❌ ${testName} - Error:`, error.message);
  if (error.response) {
    console.error('Response data:', JSON.stringify(error.response.data, null, 2));
    console.error('Response status:', error.response.status);
  }
  return null;
};

// ==================== USER TESTS ====================
const testUserOperations = async () => {
  console.log('🧪 TESTING USER OPERATIONS 🧪');
  
  try {
    // Get all users
    const users = await fetchApi('/users/')
      .then(response => logResult('Get All Users', response.data))
      .catch(error => logError('Get All Users', error));
    
    // Get user by ID
    const user = await fetchApi(`/users/${testUserId}`)
      .then(response => logResult('Get User By ID', response.data))
      .catch(error => logError('Get User By ID', error));
    
    return { users, user };
  } catch (error) {
    console.error('Error in user operations tests:', error.message);
    return null;
  }
};

// ==================== LESSON TESTS ====================
const testLessonOperations = async () => {
  console.log('🧪 TESTING LESSON OPERATIONS 🧪');
  
  try {
    // Get all lessons
    const lessons = await fetchApi('/lessons/')
      .then(response => logResult('Get All Lessons', response.data))
      .catch(error => logError('Get All Lessons', error));
    
    // Get lesson by ID (if lessons exist)
    let lesson = null;
    if (lessons && lessons.length > 0) {
      const firstLessonId = lessons[0].id;
      lesson = await fetchApi(`/lessons/${firstLessonId}`)
        .then(response => logResult('Get Lesson By ID', response.data))
        .catch(error => logError('Get Lesson By ID', error));
    } else {
      lesson = await fetchApi(`/lessons/${testLessonId}`)
        .then(response => logResult('Get Lesson By ID', response.data))
        .catch(error => logError('Get Lesson By ID', error));
    }
    
    return { lessons, lesson };
  } catch (error) {
    console.error('Error in lesson operations tests:', error.message);
    return null;
  }
};

// Test specifically for lesson creation - using Swagger UI format
const testLessonCreation = async () => {
  console.log('🧪 TESTING LESSON CREATION 🧪');
  
  try {
    // Format date as YYYY-MM-DD for the API
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    
    // Create lesson data in the exact format that Swagger UI uses
    const lessonData = {
      date: formattedDate,
      class_id: 1, // Replace with a valid class ID
      room_id: 1,  // Replace with a valid room ID
      discipline_id: 1, // Replace with a valid discipline ID
      attendance: "Test attendance"
    };
    
    console.log('Attempting to create lesson with data:', JSON.stringify(lessonData, null, 2));
    
    // Log the exact request that will be sent
    console.log('Request URL:', `${apiUrl}/lessons/${testUserId}`);
    console.log('Request method: POST');
    console.log('Request headers:', {
      'Content-Type': 'application/json'
    });
    
    // Create the lesson
    const newLesson = await fetchApi(`/lessons/${testUserId}`, {
      method: 'POST',
      body: lessonData
    })
      .then(response => {
        console.log('Response status:', response.status);
        console.log('Response headers:', response.headers);
        return logResult('Create Lesson', response.data);
      })
      .catch(error => {
        console.log('Full error object:', error);
        if (error.response) {
          console.log('Response status:', error.response.status);
          console.log('Response data:', error.response.data);
        }
        return logError('Create Lesson', error);
      });
    
    if (newLesson) {
      console.log('Lesson created successfully with ID:', newLesson.id);
      
      // Clean up - delete the lesson we just created
      await fetchApi(`/lessons/${testUserId}/${newLesson.id}`, {
        method: 'DELETE'
      })
        .then(response => logResult('Delete Test Lesson', response.data))
        .catch(error => logError('Delete Test Lesson', error));
    }
    
    return { newLesson };
  } catch (error) {
    console.error('Error in lesson creation test:', error.message);
    return null;
  }
};

// Test for CORS issues with lesson creation
const testCorsLessonCreation = async () => {
  console.log('🧪 TESTING CORS FOR LESSON CREATION 🧪');
  
  try {
    // Format date as YYYY-MM-DD for the API
    const today = new Date();
    const formattedDate = today.toISOString().split('T')[0];
    
    // Create lesson data in the exact format that Swagger UI uses
    const lessonData = {
      date: formattedDate,
      class_id: 1,
      room_id: 1,
      discipline_id: 1,
      attendance: "CORS test"
    };
    
    console.log('Testing CORS with fetch API directly:');
    
    // Use the native fetch API to test CORS
    const url = `${apiUrl}/lessons/${testUserId}`;
    console.log('Request URL:', url);
    
    try {
      // First, try a preflight OPTIONS request
      console.log('Sending OPTIONS preflight request...');
      const preflightResponse = await fetch(url, {
        method: 'OPTIONS',
        headers: {
          'Origin': 'http://localhost:8000',
          'Access-Control-Request-Method': 'POST',
          'Access-Control-Request-Headers': 'Content-Type'
        }
      });
      
      console.log('OPTIONS Response status:', preflightResponse.status);
      console.log('OPTIONS Response headers:');
      preflightResponse.headers.forEach((value, key) => {
        console.log(`  ${key}: ${value}`);
      });
      
      // Now try the actual POST request
      console.log('Sending POST request...');
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Origin': 'http://localhost:8000'
        },
        body: JSON.stringify(lessonData)
      });
      
      console.log('POST Response status:', response.status);
      console.log('POST Response headers:');
      response.headers.forEach((value, key) => {
        console.log(`  ${key}: ${value}`);
      });
      
      if (response.ok) {
        const data = await response.json();
        console.log('POST Response data:', JSON.stringify(data, null, 2));
        
        // Clean up - delete the lesson we just created
        if (data && data.id) {
          console.log('Cleaning up - deleting test lesson...');
          const deleteUrl = `${apiUrl}/lessons/${testUserId}/${data.id}`;
          const deleteResponse = await fetch(deleteUrl, {
            method: 'DELETE',
            headers: {
              'Origin': 'http://localhost:8000'
            }
          });
          
          console.log('DELETE Response status:', deleteResponse.status);
          if (deleteResponse.ok) {
            const deleteData = await deleteResponse.json();
            console.log('DELETE Response data:', JSON.stringify(deleteData, null, 2));
          }
        }
        
        return { success: true, data };
      } else {
        const errorData = await response.json().catch(() => ({}));
        console.log('Error response data:', JSON.stringify(errorData, null, 2));
        return { success: false, error: errorData };
      }
    } catch (fetchError) {
      console.error('Fetch error (possible CORS issue):', fetchError);
      return { success: false, error: fetchError.message };
    }
  } catch (error) {
    console.error('Error in CORS test:', error.message);
    return null;
  }
};

// ==================== RESERVATION TESTS ====================
const testReservationOperations = async () => {
  console.log('🧪 TESTING RESERVATION OPERATIONS 🧪');
  
  try {
    // Get all reservations
    const reservations = await fetchApi('/reservations/')
      .then(response => logResult('Get All Reservations', response.data))
      .catch(error => logError('Get All Reservations', error));
    
    // Get reservation by ID (if reservations exist)
    let reservation = null;
    if (reservations && reservations.length > 0) {
      const firstReservationId = reservations[0].id;
      reservation = await fetchApi(`/reservations/${firstReservationId}`)
        .then(response => logResult('Get Reservation By ID', response.data))
        .catch(error => logError('Get Reservation By ID', error));
    } else {
      reservation = await fetchApi(`/reservations/${testReservationId}`)
        .then(response => logResult('Get Reservation By ID', response.data))
        .catch(error => logError('Get Reservation By ID', error));
    }
    
    return { reservations, reservation };
  } catch (error) {
    console.error('Error in reservation operations tests:', error.message);
    return null;
  }
};

// ==================== RESOURCE TESTS ====================
const testResourceOperations = async () => {
  console.log('🧪 TESTING RESOURCE OPERATIONS 🧪');
  
  try {
    // Get all resources
    const resources = await fetchApi('/resources/')
      .then(response => logResult('Get All Resources', response.data))
      .catch(error => logError('Get All Resources', error));
    
    // Get resource by ID (if resources exist)
    let resource = null;
    if (resources && resources.length > 0) {
      const firstResourceId = resources[0].id;
      resource = await fetchApi(`/resources/${firstResourceId}`)
        .then(response => logResult('Get Resource By ID', response.data))
        .catch(error => logError('Get Resource By ID', error));
    } else {
      resource = await fetchApi(`/resources/${testResourceId}`)
        .then(response => logResult('Get Resource By ID', response.data))
        .catch(error => logError('Get Resource By ID', error));
    }
    
    return { resources, resource };
  } catch (error) {
    console.error('Error in resource operations tests:', error.message);
    return null;
  }
};

// ==================== RUN ALL TESTS ====================
const runAllTests = async () => {
  console.log('🧪🧪🧪 STARTING API TESTS 🧪🧪🧪');
  console.log('=====================================');
  
  const userResults = await testUserOperations();
  console.log('-------------------------------------');
  
  const lessonResults = await testLessonOperations();
  console.log('-------------------------------------');
  
  const lessonCreationResult = await testLessonCreation();
  console.log('-------------------------------------');
  
  const reservationResults = await testReservationOperations();
  console.log('-------------------------------------');
  
  const resourceResults = await testResourceOperations();
  console.log('-------------------------------------');
  
  console.log('🧪🧪🧪 ALL TESTS COMPLETED 🧪🧪🧪');
  
  return {
    userResults,
    lessonResults,
    lessonCreationResult,
    reservationResults,
    resourceResults
  };
};

// Parse command line arguments
const args = process.argv.slice(2);
const testType = args[0] || 'all';

// Run the appropriate tests based on command line arguments
(async () => {
  try {
    switch (testType.toLowerCase()) {
      case 'users':
        await testUserOperations();
        break;
      case 'lessons':
        await testLessonOperations();
        break;
      case 'lesson-creation':
        await testLessonCreation();
        break;
      case 'cors-test':
        await testCorsLessonCreation();
        break;
      case 'reservations':
        await testReservationOperations();
        break;
      case 'resources':
        await testResourceOperations();
        break;
      case 'all':
      default:
        await runAllTests();
        break;
    }
  } catch (error) {
    console.error('Error running tests:', error.message);
  }
})();