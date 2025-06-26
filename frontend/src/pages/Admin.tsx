import { useEffect, useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  createUser,
  getUsers,
  deleteUser,
  updateUser,
} from '../services/userService';
import {
  getResources,
  createResource,
  updateResource,
  deleteResource
} from '../services/resourceService';

interface Resource {
  id: number;
  description: string;
  status: string;
  resource_type_id: number;
}

const Admin = () => {
  const navigate = useNavigate();
  const [activeTab, setActiveTab] = useState<'users' | 'resources'>('users');
  
  // Users state
  const [users, setUsers] = useState<any[]>([]);
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [birthDate, setBirthDate] = useState('');
  const [gender, setGender] = useState('');
  const [role, setRole] = useState(3); // 3 = Professor
  const [editingUserId, setEditingUserId] = useState<number | null>(null);
  const [adminId] = useState(8); // Admin user ID, now using ID 8 as required
  const [professorId] = useState(3); // Professor user ID, fixed for this example
  
  // Resources state
  const [resources, setResources] = useState<Resource[]>([]);
  const [resourceDescription, setResourceDescription] = useState('');
  const [resourceStatus, setResourceStatus] = useState('available');
  const [resourceTypeId, setResourceTypeId] = useState(1);
  const [editingResourceId, setEditingResourceId] = useState<number | null>(null);
  const [resourceLoading, setResourceLoading] = useState(false);
  const [resourceError, setResourceError] = useState<string | null>(null);

  // Fetch users
  const fetchUsers = async () => {
    try {
      const data = await getUsers();
      setUsers(data);
    } catch (error) {
      console.error('Error fetching users:', error);
    }
  };
  
  // Fetch resources
  const fetchResources = async () => {
    setResourceLoading(true);
    setResourceError(null);
    try {
      const data = await getResources();
      setResources(data);
    } catch (error: any) {
      console.error('Error fetching resources:', error);
      setResourceError(error.response?.data?.detail || 'Error loading resources');
    } finally {
      setResourceLoading(false);
    }
  };

  const handleCreateOrUpdateUser = async () => {
    if (!name.trim()) return;

    const userData = {
      name,
      email,
      birth_date: birthDate,
      gender,
      profile_id: professorId,
    };

    try {
      if (editingUserId) {
        await updateUser( editingUserId,adminId, userData); // 1 = admin
      } else {
        await createUser(adminId, userData); // 1 = admin
      }

      resetForm();
      fetchUsers();
    } catch (error) {
      console.error('Error saving user:', error);
    }
  };

  const handleDeleteUser = async (userId: number) => {
    try {
      await deleteUser( userId,adminId);
      fetchUsers();
    } catch (error) {
      console.error('Error deleting user:', error);
    }
  };

  const handleEditUser = (user: any) => {
    setEditingUserId(user.id);
    setName(user.name);
    setEmail(user.email);
    setBirthDate(user.birth_date);
    setGender(user.gender);
    setRole(user.profile_id);
  };

  const resetForm = () => {
    setName('');
    setEmail('');
    setBirthDate('');
    setGender('');
    setRole(3);
    setEditingUserId(null);
  };

  useEffect(() => {
    if (activeTab === 'users') {
      fetchUsers();
    } else if (activeTab === 'resources') {
      fetchResources();
    }
  }, [activeTab]);

  // Handle resource form submission
  const handleCreateOrUpdateResource = async () => {
    if (!resourceDescription.trim()) return;

    const resourceData = {
      description: resourceDescription,
      status: resourceStatus,
      resource_type_id: resourceTypeId
    };

    try {
      if (editingResourceId) {
        await updateResource(editingResourceId, adminId, resourceData);
      } else {
        await createResource(adminId, resourceData);
      }

      resetResourceForm();
      fetchResources();
    } catch (error) {
      console.error('Error saving resource:', error);
    }
  };

  // Handle resource deletion
  const handleDeleteResource = async (resourceId: number) => {
    if (!window.confirm('Are you sure you want to delete this resource?')) {
      return;
    }
    
    try {
      await deleteResource(resourceId, adminId);
      fetchResources();
    } catch (error) {
      console.error('Error deleting resource:', error);
    }
  };

  // Handle resource editing
  const handleEditResource = (resource: Resource) => {
    setEditingResourceId(resource.id);
    setResourceDescription(resource.description);
    setResourceStatus(resource.status);
    setResourceTypeId(resource.resource_type_id);
  };

  // Reset resource form
  const resetResourceForm = () => {
    setResourceDescription('');
    setResourceStatus('available');
    setResourceTypeId(1);
    setEditingResourceId(null);
  };

  return (
    <div style={{ padding: '2rem' }}>
      <h2>Administrator Panel</h2>
      
      <div style={{ marginBottom: 20 }}>
        <button
          onClick={() => setActiveTab('users')}
          style={{
            padding: '8px 16px',
            marginRight: 10,
            backgroundColor: activeTab === 'users' ? '#1976d2' : '#e0e0e0',
            color: activeTab === 'users' ? 'white' : 'black',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Users
        </button>
        <button
          onClick={() => setActiveTab('resources')}
          style={{
            padding: '8px 16px',
            backgroundColor: activeTab === 'resources' ? '#1976d2' : '#e0e0e0',
            color: activeTab === 'resources' ? 'white' : 'black',
            border: 'none',
            borderRadius: '4px',
            cursor: 'pointer'
          }}
        >
          Resources
        </button>
      </div>

      {activeTab === 'users' && (
        <div>
          <h4>{editingUserId ? 'Edit user' : 'Create new user (professor)'}</h4>
      <input
        type="text"
        placeholder="Name"
        value={name}
        onChange={(e) => setName(e.target.value)}
      />
      <input
        type="email"
        placeholder="Email"
        value={email}
        onChange={(e) => setEmail(e.target.value)}
      />
      <input
        type="date"
        placeholder="Birth date"
        value={birthDate}
        onChange={(e) => setBirthDate(e.target.value)}
      />
      <input
        type="text"
        placeholder="Gender"
        value={gender}
        onChange={(e) => setGender(e.target.value)}
      />
      <button onClick={handleCreateOrUpdateUser}>
        {editingUserId ? 'Update' : 'Create'}
      </button>
      {editingUserId && <button onClick={resetForm}>Cancel</button>}

      <h4 style={{ marginTop: '2rem' }}>Registered Users</h4>
          <ul>
            {users.map((user: any) => (
              <li key={user.id}>
                {user.name} ({user.email}){' '}
                <button onClick={() => handleEditUser(user)}>Edit</button>{' '}
                <button onClick={() => handleDeleteUser(user.id)}>Delete</button>
              </li>
            ))}
          </ul>
        </div>
      )}

      {activeTab === 'resources' && (
        <div>
          <h3>Resources</h3>
          
          <div style={{ marginBottom: '2rem' }}>
            <h4>{editingResourceId ? 'Edit resource' : 'Create new resource'}</h4>
            <div style={{ marginBottom: 16 }}>
              <label>Description:</label>
              <textarea
                value={resourceDescription}
                onChange={(e) => setResourceDescription(e.target.value)}
                required
                style={{ width: '100%', padding: 8 }}
              />
            </div>
            <div style={{ marginBottom: 16 }}>
              <label>Status:</label>
              <select
                value={resourceStatus}
                onChange={(e) => setResourceStatus(e.target.value)}
                style={{ width: '100%', padding: 8 }}
              >
                <option value="available">Available</option>
                <option value="taken">In use</option>
                <option value="maintenance">In maintenance</option>
              </select>
            </div>
            <div style={{ marginBottom: 16 }}>
              <label>Resource Type:</label>
              <select
                value={resourceTypeId}
                onChange={(e) => setResourceTypeId(Number(e.target.value))}
                style={{ width: '100%', padding: 8 }}
              >
                <option value="1">Type 1</option>
                <option value="2">Type 2</option>
                <option value="3">Type 3</option>
              </select>
            </div>
            <button
              onClick={handleCreateOrUpdateResource}
              style={{
                padding: '8px 16px',
                backgroundColor: '#4caf50',
                color: 'white',
                border: 'none',
                borderRadius: '4px',
                cursor: 'pointer',
                marginRight: '10px'
              }}
            >
              {editingResourceId ? 'Update' : 'Create'}
            </button>
            {editingResourceId && (
              <button
                onClick={resetResourceForm}
                style={{
                  padding: '8px 16px',
                  backgroundColor: '#f44336',
                  color: 'white',
                  border: 'none',
                  borderRadius: '4px',
                  cursor: 'pointer'
                }}
              >
                Cancel
              </button>
            )}
          </div>

          <h4>Registered Resources</h4>
          {resourceLoading ? (
            <div>Loading resources...</div>
          ) : resourceError ? (
            <div style={{ color: 'red' }}>{resourceError}</div>
          ) : resources.length === 0 ? (
            <div>No resources found.</div>
          ) : (
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse' }}>
                <thead>
                  <tr style={{ backgroundColor: '#f5f5f5' }}>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>ID</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Description</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Status</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Type</th>
                    <th style={{ padding: 12, textAlign: 'left', borderBottom: '1px solid #ddd' }}>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {resources.map((resource) => (
                    <tr key={resource.id} style={{ borderBottom: '1px solid #ddd' }}>
                      <td style={{ padding: 12 }}>{resource.id}</td>
                      <td style={{ padding: 12 }}>{resource.description}</td>
                      <td style={{ padding: 12 }}>
                        <span style={{
                          color: resource.status === 'available' ? 'green' :
                                 resource.status === 'taken' ? 'orange' :
                                 resource.status === 'maintenance' ? 'red' : 'gray'
                        }}>
                          {resource.status}
                        </span>
                      </td>
                      <td style={{ padding: 12 }}>{resource.resource_type_id}</td>
                      <td style={{ padding: 12 }}>
                        <button
                          onClick={() => handleEditResource(resource)}
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
                          onClick={() => handleDeleteResource(resource.id)}
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
    </div>
  );
};

export default Admin;
