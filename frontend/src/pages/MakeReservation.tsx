import React, { useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { createReservation } from '../services/reservationService';
import { getLessons } from '../services/lessonService';

interface Lesson {
  id: number;
  date: string;
  discipline?: {
    name?: string;
  };
  class_instance?: {
    name?: string;
  };
  room?: {
    name?: string;
  };
  attendance?: string;
}

const MakeReservation: React.FC = () => {
  const { resourceId } = useParams<{ resourceId: string }>();
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [selectedLessonId, setSelectedLessonId] = useState<number | ''>('');
  const [observation, setObservation] = useState('');
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const navigate = useNavigate();

  useEffect(() => {
    const fetchLessons = async () => {
      try {
        const data = await getLessons();
        console.log('Lessons data:', data);
        setLessons(data || []);
      } catch (err: any) {
        console.error('Error loading lessons:', err);
        setError('Failed to load lessons. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchLessons();
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    
    if (!selectedLessonId) {
      setError('Please select a lesson');
      return;
    }

    if (!resourceId) {
      setError('Resource ID is missing');
      return;
    }

    setSubmitting(true);
    setError(null);

    try {
      // In a real application, you would get this from authentication
      // We need a user with Professor profile
      const userId = 2; // Try with user ID 2 (assuming this is a professor)
      
      console.log('Submitting reservation with data:', {
        lesson_id: Number(selectedLessonId),
        resource_id: Number(resourceId),
        observation: observation || undefined
      });
      
      await createReservation(userId, {
        lesson_id: Number(selectedLessonId),
        resource_id: Number(resourceId),
        observation: observation || undefined
      });
      
      navigate('/resources');
    } catch (err: any) {
      console.error('Error creating reservation:', err);
      
      // Check for permission error
      if (err.response?.status === 403) {
        setError('Permission denied: Only professors can make reservations. Please log in as a professor.');
      } else if (err.response?.status === 404 && err.response?.data?.detail?.includes('User not found')) {
        setError('User not found. Please create a professor user first.');
      } else {
        setError(err.response?.data?.detail || 'Failed to create reservation. Please try again.');
      }
    } finally {
      setSubmitting(false);
    }
  };

  if (loading) return <div>Loading lessons...</div>;

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto' }}>
      <h2>Make Reservation</h2>
      <p>You are reserving resource ID: {resourceId}</p>
      
      {error && <div style={{ color: 'red', marginBottom: 16 }}>{error}</div>}
      
      <form onSubmit={handleSubmit}>
        <div style={{ marginBottom: 16 }}>
          <label>Select Lesson:</label>
          <select 
            value={selectedLessonId} 
            onChange={(e) => setSelectedLessonId(e.target.value ? Number(e.target.value) : '')}
            style={{ width: '100%', padding: 8 }}
            required
          >
            <option value="">-- Select a lesson --</option>
            {lessons.length > 0 ? (
              lessons.map((lesson) => (
                <option key={lesson.id} value={lesson.id}>
                  {new Date(lesson.date).toLocaleDateString()} -
                  {lesson.discipline?.name || 'Unknown Discipline'} -
                  {lesson.class_instance?.name || 'Unknown Class'} -
                  {lesson.room?.name || 'Unknown Room'}
                </option>
              ))
            ) : (
              <option value="" disabled>No lessons available</option>
            )}
          </select>
        </div>
        
        <div style={{ marginBottom: 16 }}>
          <label>Observation (optional):</label>
          <textarea
            value={observation}
            onChange={(e) => setObservation(e.target.value)}
            style={{ width: '100%', padding: 8 }}
            rows={4}
          />
        </div>
        
        <button 
          type="submit" 
          disabled={submitting} 
          style={{ padding: '8px 24px', backgroundColor: '#1976d2', color: 'white', border: 'none', borderRadius: '4px', cursor: submitting ? 'not-allowed' : 'pointer' }}
        >
          {submitting ? 'Submitting...' : 'Make Reservation'}
        </button>
      </form>
    </div>
  );
};

export default MakeReservation;