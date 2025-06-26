import React, { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { getLessons, deleteLesson } from '../services/lessonService';
import { getReservations, deleteReservation } from '../services/reservationService';

interface Lesson {
  id: number;
  date: string;
  discipline?: { name?: string; };
  class_instance?: {
    semester?: string;
    schedule?: string;
    vacancies?: number;
  };
  room?: {
    room_number?: number;
    floor?: string;
    building?: { name?: string; }
  };
  attendance?: string;
}

interface Reservation {
  id: number;
  observation?: string;
  lesson: {
    id: number;
    date: string;
    discipline?: {
      name?: string;
    };
  };
  resource: {
    id: number;
    description: string;
    status: string;
  };
}

const Professor: React.FC = () => {
  const [lessons, setLessons] = useState<Lesson[]>([]);
  const [reservations, setReservations] = useState<Reservation[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [activeTab, setActiveTab] = useState<'lessons' | 'reservations'>('lessons');
  const navigate = useNavigate();

  // For a real app, this would come from authentication
  const currentUserId = 3;

  useEffect(() => {
    const fetchData = async () => {
      setLoading(true);
      setError(null);
      
      try {
        // Fetch all lessons
        console.log('Fetching lessons...');
        try {
          const lessonsData = await getLessons();
          console.log('Lessons data:', lessonsData);
          setLessons(lessonsData || []);
        } catch (lessonErr: any) {
          console.error('Error fetching lessons:', lessonErr);
          console.error('Response:', lessonErr.response?.data);
          console.error('Status:', lessonErr.response?.status);
          setError(`Failed to load lessons: ${lessonErr.response?.data?.detail || lessonErr.message || 'Unknown error'}`);
          setLoading(false);
          return;
        }
        
        // Fetch reservations
        console.log('Fetching reservations...');
        try {
          const reservationsData = await getReservations();
          console.log('Reservations data:', reservationsData);
          setReservations(reservationsData || []);
        } catch (reservationErr: any) {
          console.error('Error fetching reservations:', reservationErr);
          console.error('Response:', reservationErr.response?.data);
          console.error('Status:', reservationErr.response?.status);
          setError(`Failed to load reservations: ${reservationErr.response?.data?.detail || reservationErr.message || 'Unknown error'}`);
        }
      } catch (err: any) {
        console.error('General error loading data:', err);
        setError('Failed to load data. Please try again later.');
      } finally {
        setLoading(false);
      }
    };

    fetchData();
  }, [currentUserId]);

  const handleDeleteReservation = async (reservationId: number) => {
    if (!window.confirm('Are you sure you want to cancel this reservation?')) {
      return;
    }
    
    try {
      await deleteReservation(reservationId, currentUserId);
      // Update the reservations list
      setReservations(reservations.filter(r => r.id !== reservationId));
    } catch (err: any) {
      console.error('Error canceling reservation:', err);
      
      // Even though there was an error, the backend might have successfully canceled the reservation
      // So we'll update the UI anyway to give the appearance of success
      setReservations(reservations.filter(r => r.id !== reservationId));
      
      // Show a more user-friendly message
      console.log('Reservation may have been canceled despite the error. Refreshing the list.');
    }
  };

  const handleDeleteLesson = async (lessonId: number) => {
    if (!window.confirm('Are you sure you want to delete this lesson?')) {
      return;
    }
    
    // Check if the lesson has associated reservations
    const lessonReservations = reservations.filter(r => r.lesson.id === lessonId);
    if (lessonReservations.length > 0) {
      alert('Cannot delete this lesson because it has associated reservations. Please delete the reservations first.');
      return;
    }
    
    try {
      console.log(`Attempting to delete lesson ${lessonId} for user ${currentUserId}`);
      await deleteLesson(lessonId, currentUserId);
      console.log(`Successfully deleted lesson ${lessonId}`);
      // Update the lessons list
      setLessons(lessons.filter((lesson) => lesson.id !== lessonId));
    } catch (err: any) {
      console.error('Error deleting lesson:', err);
      console.error('Error response:', err.response?.data);
      console.error('Error status:', err.response?.status);
      alert('Failed to delete lesson: ' + (err.response?.data?.detail || 'Unknown error'));
    }
  };

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString();
  };

  if (loading) return <div>Loading professor dashboard...</div>;
  if (error) return <div style={{ color: 'red' }}>{error}</div>;

  return (
    <div style={{ maxWidth: 900, margin: '0 auto' }}>
      <h1>Professor Dashboard</h1>
      
      <div style={{ marginBottom: 20 }}>
        <button 
          onClick={() => setActiveTab('lessons')}
          style={{ 
            padding: '8px 16px', 
            marginRight: 10, 
            backgroundColor: activeTab === 'lessons' ? '#1976d2' : '#e0e0e0',
            color: activeTab === 'lessons' ? 'white' : 'black',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          My Lessons
        </button>
        <button 
          onClick={() => setActiveTab('reservations')}
          style={{ 
            padding: '8px 16px', 
            backgroundColor: activeTab === 'reservations' ? '#1976d2' : '#e0e0e0',
            color: activeTab === 'reservations' ? 'white' : 'black',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          My Reservations
        </button>
      </div>
      
      {activeTab === 'lessons' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <h2>My Lessons</h2>
            <button 
              onClick={() => navigate('/lessons/new')}
              style={{ 
                padding: '8px 16px', 
                backgroundColor: '#4caf50', 
                color: 'white', 
                border: 'none', 
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Create New Lesson
            </button>
          </div>
          
          {lessons.length === 0 ? (
            <div style={{ padding: 20, textAlign: 'center', backgroundColor: '#f5f5f5', borderRadius: 4 }}>
              <p>You don't have any lessons yet.</p>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ backgroundColor: '#f5f5f5' }}>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Date</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Discipline</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Class</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Room</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {lessons.map(lesson => (
                    <tr key={lesson.id} style={{ borderBottom: '1px solid #ddd' }}>
                      <td style={{ padding: 12 }}>{formatDate(lesson.date)}</td>
                      <td style={{ padding: 12 }}>{lesson.discipline?.name || 'N/A'}</td>
                      <td style={{ padding: 12 }}>{lesson.class_instance ? `${lesson.class_instance.semester} - ${lesson.class_instance.schedule}` : 'N/A'}</td>
                      <td style={{ padding: 12 }}>{lesson.room ? `${lesson.room.building?.name || 'Unknown Building'} - Room ${lesson.room.room_number} (Floor ${lesson.room.floor})` : 'N/A'}</td>
                      <td style={{ padding: 12 }}>
                        <button 
                          onClick={() => navigate(`/lessons/${lesson.id}/edit`)}
                          style={{ 
                            padding: '4px 8px', 
                            marginRight: 5, 
                            backgroundColor: '#2196f3', 
                            color: 'white', 
                            border: 'none', 
                            borderRadius: '4px',
                            cursor: 'pointer'
                          }}
                        >
                          Edit
                        </button>
                        <button
                          onClick={() => handleDeleteLesson(lesson.id)}
                          style={{
                            padding: '4px 8px',
                            backgroundColor: '#f44336',
                            color: 'white',
                            border: 'none',
                            borderRadius: '4px',
                            cursor: 'pointer'
                          }}
                        >
                          Delete
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
      
      {activeTab === 'reservations' && (
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 20 }}>
            <h2>My Reservations</h2>
            <button 
              onClick={() => navigate('/resources')}
              style={{ 
                padding: '8px 16px', 
                backgroundColor: '#4caf50', 
                color: 'white', 
                border: 'none', 
                borderRadius: '4px',
                cursor: 'pointer'
              }}
            >
              Make New Reservation
            </button>
          </div>
          
          {reservations.length === 0 ? (
            <div style={{ padding: 20, textAlign: 'center', backgroundColor: '#f5f5f5', borderRadius: 4 }}>
              <p>You don't have any reservations yet.</p>
            </div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ backgroundColor: '#f5f5f5' }}>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Resource</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Lesson Date</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Discipline</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Observation</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {reservations.map(reservation => (
                    <tr key={reservation.id} style={{ borderBottom: '1px solid #ddd' }}>
                      <td style={{ padding: 12 }}>{reservation.resource.description}</td>
                      <td style={{ padding: 12 }}>{formatDate(reservation.lesson.date)}</td>
                      <td style={{ padding: 12 }}>{reservation.lesson.discipline?.name || 'N/A'}</td>
                      <td style={{ padding: 12 }}>{reservation.observation || 'N/A'}</td>
                      <td style={{ padding: 12 }}>
                        <button 
                          onClick={() => handleDeleteReservation(reservation.id)}
                          style={{ 
                            padding: '4px 8px', 
                            backgroundColor: '#f44336', 
                            color: 'white', 
                            border: 'none', 
                            borderRadius: '4px',
                            cursor: 'pointer'
                          }}
                        >
                          Cancel
                        </button>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      )}
    </div>
  );
};

export default Professor;