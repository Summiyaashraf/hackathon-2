import React, { useState, useEffect } from 'react';
import { useRouter } from 'next/router';
import { Plus } from 'lucide-react';
import { Task, apiService } from '../services/api';
import { getUserIdFromToken, isAuthenticated, removeAuthToken } from '../utils/auth';
import DashboardLayout from '../components/DashboardLayout';
import TaskList from '../components/TaskList';
import TaskModal from '../components/TaskModal';

const Dashboard: React.FC = () => {
  const router = useRouter();
  const [tasks, setTasks] = useState<Task[]>([]);
  const [filteredTasks, setFilteredTasks] = useState<Task[]>([]);
  const [loading, setLoading] = useState<boolean>(true);
  const [userId, setUserId] = useState<string | null>(null);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState<boolean>(false);
  const [filter, setFilter] = useState<'all' | 'pending' | 'completed'>('all');

  // Check authentication and load tasks on component mount
  useEffect(() => {
    const checkAuthAndLoadTasks = async () => {
      if (!isAuthenticated()) {
        window.location.href = '/auth/login'; // Redirect to login if not authenticated
        return;
      }

      const userId = getUserIdFromToken();
      if (!userId) {
        setError('Invalid user session. Please log in again.');
        setLoading(false);
        return;
      }

      setUserId(userId);

      try {
        await loadTasks();
      } catch (error) {
        console.error('Failed to load tasks:', error);
        setError('Failed to load tasks. Please refresh the page.');
      } finally {
        setLoading(false);
      }
    };

    checkAuthAndLoadTasks();
  }, []);

  // Handle filter changes
  useEffect(() => {
    // Get filter from URL query param
    const queryFilter = router.query.filter as string;

    if (queryFilter === 'pending') {
      setFilter('pending');
    } else if (queryFilter === 'completed') {
      setFilter('completed');
    } else {
      setFilter('all');
    }
  }, [router.query]);

  // Apply filter when tasks or filter changes
  useEffect(() => {
    if (filter === 'pending') {
      setFilteredTasks(tasks.filter(task => task.status === 'pending'));
    } else if (filter === 'completed') {
      setFilteredTasks(tasks.filter(task => task.status === 'completed'));
    } else {
      setFilteredTasks(tasks);
    }
  }, [tasks, filter]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      const tasksData = await apiService.getTasks();
      setTasks(tasksData);
    } catch (error) {
      console.error('Failed to load tasks:', error);
      setError('Failed to load tasks. Please try again.');
      throw error;
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (title: string, description: string) => {
    try {
      const newTask = await apiService.createTask({
        title: title,
        description: description || undefined,
      });

      // Refresh the tasks list to ensure the latest data is displayed
      await loadTasks();
      setError(null); // Clear any previous error
    } catch (error) {
      console.error('Failed to create task:', error);
      setError('Failed to create task. Please try again.');
    }
  };

  const handleToggleStatus = async (task: Task) => {
    try {
      const updatedStatus = task.status === 'pending' ? 'completed' : 'pending';
      const updatedTask = await apiService.updateTask(task.id, {
        status: updatedStatus,
      });

      // Refresh the tasks list to ensure the latest data is displayed
      await loadTasks();
      setError(null); // Clear any previous error
    } catch (error) {
      console.error('Failed to update task status:', error);
      setError('Failed to update task. Please try again.');
    }
  };

  const handleDeleteTask = async (id: string) => {
    try {
      await apiService.deleteTask(id);
      // Refresh the tasks list to ensure the latest data is displayed
      await loadTasks();
      setError(null); // Clear any previous error
    } catch (error) {
      console.error('Failed to delete task:', error);
      setError('Failed to delete task. Please try again.');
    }
  };

  const handleEditTask = async (id: string, title: string, description: string | null) => {
    try {
      const updatedTask = await apiService.updateTask(id, {
        title: title,
        description: description || undefined,
      });

      // Refresh the tasks list to ensure the latest data is displayed
      await loadTasks();
      setError(null); // Clear any previous error
    } catch (error) {
      console.error('Failed to update task:', error);
      setError('Failed to update task. Please try again.');
    }
  };

  const handleLogout = () => {
    removeAuthToken();
    setUserId(null);
    window.location.href = '/auth/login'; // Redirect to login page
  };

  const clearError = () => {
    setError(null);
  };

  if (!isAuthenticated()) {
    return null; // This page should redirect automatically if not authenticated
  }

  return (
    <DashboardLayout
      onLogout={handleLogout}
      pageTitle="Dashboard"
      errorMessage={error}
      onClearError={clearError}
    >
      <div className="max-w-4xl mx-auto">
        {/* Stats and Header */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
          <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
            <div className="text-sm text-gray-500 dark:text-gray-400">Total Tasks</div>
            <div className="text-2xl font-bold text-gray-800 dark:text-gray-100">{tasks.length}</div>
          </div>
          <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
            <div className="text-sm text-gray-500 dark:text-gray-400">Completed</div>
            <div className="text-2xl font-bold text-green-600 dark:text-green-400">{tasks.filter(t => t.status === 'completed').length}</div>
          </div>
          <div className="bg-white dark:bg-gray-800 p-4 rounded-xl shadow-sm border border-gray-100 dark:border-gray-700">
            <div className="text-sm text-gray-500 dark:text-gray-400">Pending</div>
            <div className="text-2xl font-bold text-blue-600 dark:text-blue-400">{tasks.filter(t => t.status === 'pending').length}</div>
          </div>
        </div>

        {/* Action Bar */}
        <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4 mb-6">
          <div className="flex space-x-2">
            <button
              onClick={() => {
                setFilter('all');
                router.push('/', undefined, { shallow: true });
              }}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === 'all'
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 border border-blue-300 dark:border-blue-700'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              All Tasks
            </button>
            <button
              onClick={() => {
                setFilter('pending');
                router.push('/?filter=pending', undefined, { shallow: true });
              }}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === 'pending'
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 border border-blue-300 dark:border-blue-700'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              Pending
            </button>
            <button
              onClick={() => {
                setFilter('completed');
                router.push('/?filter=completed', undefined, { shallow: true });
              }}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                filter === 'completed'
                  ? 'bg-blue-100 dark:bg-blue-900 text-blue-700 dark:text-blue-300 border border-blue-300 dark:border-blue-700'
                  : 'bg-gray-100 dark:bg-gray-700 text-gray-700 dark:text-gray-300 hover:bg-gray-200 dark:hover:bg-gray-600'
              }`}
            >
              Completed
            </button>
          </div>
          <button
            onClick={() => setShowCreateModal(true)}
            className="bg-blue-600 hover:bg-blue-700 text-white font-medium py-2 px-4 rounded-lg transition-colors flex items-center self-start sm:self-auto"
          >
            <Plus className="h-5 w-5 mr-1" />
            New Task
          </button>
        </div>

        {/* Task List */}
        <TaskList
          tasks={filteredTasks}
          loading={loading}
          onToggleStatus={handleToggleStatus}
          onDelete={handleDeleteTask}
          onEdit={handleEditTask}
        />

        {/* Create Task Modal */}
        <TaskModal
          isOpen={showCreateModal}
          onClose={() => setShowCreateModal(false)}
          onCreateTask={handleCreateTask}
          loading={false}
        />
      </div>
    </DashboardLayout>
  );
};

export default Dashboard;