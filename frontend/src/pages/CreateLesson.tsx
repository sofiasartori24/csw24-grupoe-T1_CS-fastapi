import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createLesson, getLessonById, updateLesson } from '../services/lessonService';
import { getRooms } from '../services/roomService';
import { getClasses } from '../services/classService';
import { getDisciplines } from '../services/disciplineService';

interface Room {
  id: number;
  room_number: number;
  capacity: number;
  floor: string;
  building: {
    name: string;
  };
}

interface Discipline {
  id: number;
  name: string;
  credits: number;
  program: string;
}

interface Class {
  id: number;
  semester: string;
  schedule: string;
  vacancies: number;
}

const CreateLesson: React.FC = () => {
  const { id } = useParams<{ id: string }>();
  const isEditMode = !!id;
  const lessonId = id ? parseInt(id, 10) : null;

  const [date, setDate] = useState<string>('');
  const [classId, setClassId] = useState<number | ''>('');
  const [roomId, setRoomId] = useState<number | ''>('');
  const [disciplineId, setDisciplineId] = useState<number | ''>('');
  const [attendance, setAttendance] = useState<string>('');
  
  const [classes, setClasses] = useState<Class[]>([]);
  const [rooms, setRooms] = useState<Room[]>([]);
  const [disciplines, setDisciplines] = useState<Discipline[]>([]);
  
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  
  const navigate = useNavigate();
  
  // For a real app, this would come from authentication
  const currentUserId = 2; // Assuming user ID 2 is a professor

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // Fetch data from API
        const [classesData, roomsData, disciplinesData] = await Promise.all([
          getClasses(),
          getRooms(),
          getDisciplines()
        ]);
        
        console.log('Classes data:', classesData);
        console.log('Rooms data:', roomsData);
        console.log('Disciplines data:', disciplinesData);
        
        setClasses(classesData || []);
        setRooms(roomsData || []);
        setDisciplines(disciplinesData || []);

        // If in edit mode, fetch the lesson data
        if (isEditMode && lessonId) {
          const lessonData = await getLessonById(lessonId);
          console.log('Lesson data for editing:', lessonData);
          
          // Format date for input field (YYYY-MM-DD)
          const formattedDate = new Date(lessonData.date).toISOString().split('T')[0];
          
          setDate(formattedDate);
          setClassId(lessonData.class_id || '');
          setRoomId(lessonData.room_id || '');
          setDisciplineId(lessonData.discipline_id || '');
          setAttendance(lessonData.attendance || '');
        }
      } catch (err: any) {
        console.error('Error loading data:', err);
        setError('Failed to load data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [isEditMode, lessonId]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!date) {
      setError('Please select a date');
      return;
    }
    
    if (!classId) {
      setError('Please select a class');
      return;
    }
    
    if (!roomId) {
      setError('Please select a room');
      return;
    }
    
    if (!disciplineId) {
      setError('Please select a discipline');
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      // Format the date as YYYY-MM-DD for the API
      const formattedDate = new Date(date).toISOString().split('T')[0];
      
      const lessonData = {
        date: formattedDate,
        class_id: Number(classId),
        room_id: Number(roomId),
        discipline_id: Number(disciplineId),
        attendance: attendance || undefined
      };
      
      if (isEditMode && lessonId) {
        console.log(`Updating lesson ${lessonId} with data:`, lessonData);
        await updateLesson(lessonId, currentUserId, lessonData);
      } else {
        console.log('Creating new lesson with data:', lessonData);
        await createLesson(currentUserId, lessonData);
      }
      
      navigate('/professor');
    } catch (err: any) {
      console.error(`Error ${isEditMode ? 'updating' : 'creating'} lesson:`, err);
      
      // Check for permission error
      if (err.response?.status === 403) {
        setError('Permission denied: Only professors can manage lessons.');
      } else if (err.response?.status === 404 && err.response?.data?.detail?.includes('User not found')) {
        setError('User not found. Please check your credentials.');
      } else {
        setError(err.response?.data?.detail || `Failed to ${isEditMode ? 'update' : 'create'} lesson. Please try again.`);
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div>Loading...</div>;

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto' }}>
      <h2>{isEditMode ? 'Edit Lesson' : 'Create New Lesson'}</h2>
      
      {error && <div style={{ color: 'red', marginBottom: 16 }}>{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 16 }}>
          <label>Date:</label>
          <input
            type="date"
            value={date}
            onChange={(e) => setDate(e.target.value)}
            style={{ width: '100%', padding: 8 }}
            required
          />
        </div>
        
        <div style={{ marginBottom: 16 }}>
          <label>Class:</label>
          <select 
            value={classId} 
            onChange={(e) => setClassId(e.target.value ? Number(e.target.value) : '')}
            style={{ width: '100%', padding: 8 }}
            required
          >
            <option value="">-- Select a class --</option>
            {classes.length > 0 ? (
              classes.map((classItem) => (
                <option key={classItem.id} value={classItem.id}>
                  {classItem.semester} - {classItem.schedule} - Vacancies: {classItem.vacancies}
                </option>
              ))
            ) : (
              <option value="" disabled>No classes available</option>
            )}
          </select>
        </div>
        
        <div style={{ marginBottom: 16 }}>
          <label>Room:</label>
          <select 
            value={roomId} 
            onChange={(e) => setRoomId(e.target.value ? Number(e.target.value) : '')}
            style={{ width: '100%', padding: 8 }}
            required
          >
            <option value="">-- Select a room --</option>
            {rooms.length > 0 ? (
              rooms.map((room) => (
                <option key={room.id} value={room.id}>
                  {room.building?.name || 'Unknown Building'} - Room {room.room_number} - Capacity: {room.capacity}
                </option>
              ))
            ) : (
              <option value="" disabled>No rooms available</option>
            )}
          </select>
        </div>
        
        <div style={{ marginBottom: 16 }}>
          <label>Discipline:</label>
          <select 
            value={disciplineId} 
            onChange={(e) => setDisciplineId(e.target.value ? Number(e.target.value) : '')}
            style={{ width: '100%', padding: 8 }}
            required
          >
            <option value="">-- Select a discipline --</option>
            {disciplines.length > 0 ? (
              disciplines.map((discipline) => (
                <option key={discipline.id} value={discipline.id}>
                  {discipline.name} - Credits: {discipline.credits}
                </option>
              ))
            ) : (
              <option value="" disabled>No disciplines available</option>
            )}
          </select>
        </div>
        
        <div style={{ marginBottom: 16 }}>
          <label>Attendance (optional):</label>
          <textarea
            value={attendance}
            onChange={(e) => setAttendance(e.target.value)}
            style={{ width: '100%', padding: 8 }}
            rows={4}
          />
        </div>
        
        <div style={{ display: 'flex', gap: 10 }}>
          <button 
            type="button" 
            onClick={() => navigate('/professor')}
            style={{ 
              padding: '8px 24px', 
              backgroundColor: '#e0e0e0', 
              color: 'black', 
              border: 'none', 
              borderRadius: '4px',
              cursor: 'pointer'
            }}
          >
            Cancel
          </button>
          
          <button 
            type="submit" 
            disabled={submitting} 
            style={{ 
              padding: '8px 24px', 
              backgroundColor: '#1976d2', 
              color: 'white', 
              border: 'none', 
              borderRadius: '4px', 
              cursor: submitting ? 'not-allowed' : 'pointer',
              flexGrow: 1
            }}
          >
            {submitting ? (isEditMode ? 'Updating...' : 'Creating...') : (isEditMode ? 'Update Lesson' : 'Create Lesson')}
          </button>
        </div>
      </form>
    </div>
  );
};

export default CreateLesson;