import api from './api';

// Get all lessons
export const getLessons = async () => {
  try {
    const response = await api.get('/lessons/');
    return response.data;
  } catch (error) {
    console.error('Error fetching lessons:', error);
    throw error;
  }
};


// Get a specific lesson by ID
export const getLessonById = async (lessonId: number) => {
  try {
    const response = await api.get(`/lessons/${lessonId}`);
    return response.data;
  } catch (error) {
    console.error(`Error fetching lesson ${lessonId}:`, error);
    throw error;
  }
};

// Create a new lesson
export const createLesson = async (userId: number, data: any) => {
  try {
    console.log('Creating lesson with data:', data);
    const response = await api.post(`/lessons/${userId}`, data);
    return response.data;
  } catch (error) {
    console.error('Error creating lesson:', error);
    throw error;
  }
};

// Update an existing lesson
export const updateLesson = async (lessonId: number, userId: number, data: any) => {
  try {
    console.log(`Updating lesson with ID ${lessonId} for user ${userId}`);
    console.log(`Using URL: /lessons/${lessonId}/${userId}`);
    console.log('Update data:', data);
    
    // Using the standard PUT method with the CORS proxy
    const response = await api.put(`/lessons/${lessonId}/${userId}`, data);
    console.log('Update response:', response);
    return response.data;
  } catch (error: any) {
    console.error(`Error updating lesson ${lessonId}:`, error);
    if (error.response) {
      console.error('Error response:', error.response.data);
      console.error('Error status:', error.response.status);
    }
    throw error;
  }
};

// Delete a lesson
export const deleteLesson = async (lessonId: number, userId: number) => {
  try {
    console.log(`Deleting lesson with ID ${lessonId} for user ${userId}`);
    console.log(`Using URL: /lessons/${lessonId}/${userId}`);
    
    // Using the standard DELETE method with the CORS proxy
    const response = await api.delete(`/lessons/${lessonId}/${userId}`);
    console.log('Delete response:', response);
    return response.data;
  } catch (error: any) {
    console.error(`Error deleting lesson ${lessonId}:`, error);
    if (error.response) {
      console.error('Error response:', error.response.data);
      console.error('Error status:', error.response.status);
    }
    throw error;
  }
};
