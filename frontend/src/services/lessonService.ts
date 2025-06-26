import api from './api';

// Get all lessons
export const getLessons = async () => {
  try {
    const response = await api.get('/lessons');
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
    // IMPORTANT: The backend expects the parameters in the opposite order!
    // The URL pattern is /{lesson_id}/{user_id} but the parameters are (user_id, lesson_id)
    // So we need to swap the order in the URL
    const response = await api.put(`/lessons/${userId}/${lessonId}`, data);
    return response.data;
  } catch (error) {
    console.error(`Error updating lesson ${lessonId}:`, error);
    throw error;
  }
};

// Delete a lesson
export const deleteLesson = async (lessonId: number, userId: number) => {
  try {
    // IMPORTANT: The backend expects the parameters in the opposite order!
    // The URL pattern is /{lesson_id}/{user_id} but the parameters are (user_id, lesson_id)
    // So we need to swap the order in the URL
    const response = await api.delete(`/lessons/${userId}/${lessonId}`);
    return response.data;
  } catch (error) {
    console.error(`Error deleting lesson ${lessonId}:`, error);
    throw error;
  }
};
