import * as reservationService from '../services/reservationService';
import * as lessonService from '../services/lessonService';
import * as userService from '../services/userService';
import * as resourceService from '../services/resourceService';

// Test data
const testUserId = 3; // Using the same user ID as in CreateLesson.tsx (professor role)
const testResourceId = 1; // Replace with a valid resource ID
const testLessonId = 1; // Replace with a valid lesson ID if available
const testReservationId = 1; // Replace with a valid reservation ID if available

// Utility function to log test results
const logResult = (testName: string, result: any) => {
  console.log(`✅ ${testName} - Success:`, result);
  return result;
};

const logError = (testName: string, error: any) => {
  console.error(`❌ ${testName} - Error:`, error);
  return null;
};

// ==================== USER TESTS ====================
export const testUserOperations = async () => {
  console.log('🧪 TESTING USER OPERATIONS 🧪');
  
  try {
    // Get all users
    const users = await userService.getUsers()
      .then(result => logResult('Get All Users', result))
      .catch(error => logError('Get All Users', error));
    
    // Get user by ID
    const user = await userService.getUserById(testUserId)
      .then(result => logResult('Get User By ID', result))
      .catch(error => logError('Get User By ID', error));
    
    // Create user (commented out to prevent unwanted data creation)
    /*
    const newUserData = {
      name: 'Test User',
      email: `test${Date.now()}@example.com`,
      profile_id: 1 // Assuming 1 is a valid profile ID
    };
    
    const newUser = await userService.createUser(testUserId, newUserData)
      .then(result => logResult('Create User', result))
      .catch(error => logError('Create User', error));
    
    // Update user (if a new user was created)
    if (newUser) {
      const updatedUserData = {
        ...newUserData,
        name: 'Updated Test User'
      };
      
      await userService.updateUser(newUser.id, testUserId, updatedUserData)
        .then(result => logResult('Update User', result))
        .catch(error => logError('Update User', error));
      
      // Delete user (if a new user was created)
      await userService.deleteUser(newUser.id, testUserId)
        .then(result => logResult('Delete User', result))
        .catch(error => logError('Delete User', error));
    }
    */
    
    return { users, user };
  } catch (error) {
    console.error('Error in user operations tests:', error);
    return null;
  }
};

// ==================== LESSON TESTS ====================
export const testLessonOperations = async () => {
  console.log('🧪 TESTING LESSON OPERATIONS 🧪');
  
  try {
    // Get all lessons
    const lessons = await lessonService.getLessons()
      .then(result => logResult('Get All Lessons', result))
      .catch(error => logError('Get All Lessons', error));
    
    // Get lesson by ID (if lessons exist)
    let lesson = null;
    if (lessons && lessons.length > 0) {
      const firstLessonId = lessons[0].id;
      lesson = await lessonService.getLessonById(firstLessonId)
        .then(result => logResult('Get Lesson By ID', result))
        .catch(error => logError('Get Lesson By ID', error));
    } else {
      lesson = await lessonService.getLessonById(testLessonId)
        .then(result => logResult('Get Lesson By ID', result))
        .catch(error => logError('Get Lesson By ID', error));
    }
    
    return { lessons, lesson };
  } catch (error) {
    console.error('Error in lesson operations tests:', error);
    return null;
  }
};

// ==================== LESSON CREATION TEST ====================
export const testLessonCreation = async () => {
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
    
    console.log('Attempting to create lesson with data:', lessonData);
    
    // Create the lesson
    const newLesson = await lessonService.createLesson(testUserId, lessonData)
      .then(result => logResult('Create Lesson', result))
      .catch(error => {
        console.log('Full error details:', error);
        return logError('Create Lesson', error);
      });
    
    if (newLesson) {
      console.log('Lesson created successfully with ID:', newLesson.id);
      
      // Clean up - delete the lesson we just created
      await lessonService.deleteLesson(newLesson.id, testUserId)
        .then(result => logResult('Delete Test Lesson', result))
        .catch(error => logError('Delete Test Lesson', error));
    }
    
    return { newLesson };
  } catch (error) {
    console.error('Error in lesson creation test:', error);
    return null;
  }
};

// ==================== RESERVATION TESTS ====================
export const testReservationOperations = async () => {
  console.log('🧪 TESTING RESERVATION OPERATIONS 🧪');
  
  try {
    // Get all reservations
    const reservations = await reservationService.getReservations()
      .then(result => logResult('Get All Reservations', result))
      .catch(error => logError('Get All Reservations', error));
    
    // Get reservation by ID (if reservations exist)
    let reservation = null;
    if (reservations && reservations.length > 0) {
      const firstReservationId = reservations[0].id;
      reservation = await reservationService.getReservationById(firstReservationId)
        .then(result => logResult('Get Reservation By ID', result))
        .catch(error => logError('Get Reservation By ID', error));
    } else {
      reservation = await reservationService.getReservationById(testReservationId)
        .then(result => logResult('Get Reservation By ID', result))
        .catch(error => logError('Get Reservation By ID', error));
    }
    
    // Create reservation (commented out to prevent unwanted data creation)
    /*
    const newReservationData = {
      resource_id: testResourceId,
      lesson_id: testLessonId,
      date: new Date().toISOString().split('T')[0],
      start_time: '14:00:00',
      end_time: '16:00:00'
    };
    
    const newReservation = await reservationService.createReservation(testUserId, newReservationData)
      .then(result => logResult('Create Reservation', result))
      .catch(error => logError('Create Reservation', error));
    
    // Delete reservation (if a new reservation was created)
    if (newReservation) {
      await reservationService.deleteReservation(newReservation.id, testUserId)
        .then(result => logResult('Delete Reservation', result))
        .catch(error => logError('Delete Reservation', error));
    }
    */
    
    return { reservations, reservation };
  } catch (error) {
    console.error('Error in reservation operations tests:', error);
    return null;
  }
};

// ==================== RESOURCE TESTS ====================
export const testResourceOperations = async () => {
  console.log('🧪 TESTING RESOURCE OPERATIONS 🧪');
  
  try {
    // Get all resources
    const resources = await resourceService.getResources()
      .then(result => logResult('Get All Resources', result))
      .catch(error => logError('Get All Resources', error));
    
    // Get resource by ID (if resources exist)
    let resource = null;
    if (resources && resources.length > 0) {
      const firstResourceId = resources[0].id;
      resource = await resourceService.getResourceById(firstResourceId)
        .then(result => logResult('Get Resource By ID', result))
        .catch(error => logError('Get Resource By ID', error));
    } else {
      resource = await resourceService.getResourceById(testResourceId)
        .then(result => logResult('Get Resource By ID', result))
        .catch(error => logError('Get Resource By ID', error));
    }
    
    // Create resource (commented out to prevent unwanted data creation)
    /*
    const newResourceData = {
      name: 'Test Resource',
      description: 'This is a test resource',
      resource_type_id: 1, // Replace with a valid resource type ID
      room_id: 1 // Replace with a valid room ID
    };
    
    const newResource = await resourceService.createResource(testUserId, newResourceData)
      .then(result => logResult('Create Resource', result))
      .catch(error => logError('Create Resource', error));
    
    // Update resource (if a new resource was created)
    if (newResource) {
      const updatedResourceData = {
        ...newResourceData,
        name: 'Updated Test Resource',
        description: 'This is an updated test resource'
      };
      
      await resourceService.updateResource(newResource.id, testUserId, updatedResourceData)
        .then(result => logResult('Update Resource', result))
        .catch(error => logError('Update Resource', error));
      
      // Delete resource (if a new resource was created)
      await resourceService.deleteResource(newResource.id, testUserId)
        .then(result => logResult('Delete Resource', result))
        .catch(error => logError('Delete Resource', error));
    }
    */
    
    return { resources, resource };
  } catch (error) {
    console.error('Error in resource operations tests:', error);
    return null;
  }
};

// ==================== RUN ALL TESTS ====================
export const runAllTests = async () => {
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

// Export a function to run in the browser console
(window as any).runApiTests = runAllTests;
(window as any).testUsers = testUserOperations;
(window as any).testLessons = testLessonOperations;
(window as any).testLessonCreation = testLessonCreation;
(window as any).testReservations = testReservationOperations;
(window as any).testResources = testResourceOperations;

// Log instructions when this file is imported
console.log(`
API Tester loaded! You can run tests using the following commands:
- runApiTests() - Run all API tests
- testUsers() - Test user operations
- testLessons() - Test lesson operations
- testLessonCreation() - Test lesson creation specifically
- testReservations() - Test reservation operations
- testResources() - Test resource operations
`);