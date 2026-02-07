import React from 'react';
import { ClipboardList } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import TaskItem from './TaskItem';

interface Task {
  id: string;
  user_id: string;
  title: string;
  description: string | null;
  status: 'pending' | 'completed';
  created_at: string;
  updated_at: string;
}

interface TaskListProps {
  tasks: Task[];
  loading: boolean;
  onToggleStatus: (task: Task) => void;
  onDelete: (id: string) => void;
  onEdit: (id: string, title: string, description: string | null) => void;
}

const TaskList: React.FC<TaskListProps> = ({ tasks, loading, onToggleStatus, onDelete, onEdit }) => {
  if (loading) {
    return (
      <div className="bg-white dark:bg-gray-800 rounded-xl shadow p-6">
        <h2 className="text-xl font-semibold mb-4 text-gray-800 dark:text-gray-100">Loading Tasks...</h2>
        <div className="space-y-4">
          {[...Array(3)].map((_, idx) => (
            <div key={idx} className="animate-pulse flex space-x-4">
              <div className="rounded-full bg-gray-300 dark:bg-gray-600 h-5 w-5 mt-1"></div>
              <div className="flex-1 space-y-2 py-1">
                <div className="h-4 bg-gray-300 dark:bg-gray-600 rounded w-3/4"></div>
                <div className="h-3 bg-gray-300 dark:bg-gray-600 rounded"></div>
              </div>
            </div>
          ))}
        </div>
      </div>
    );
  }

  return (
    <div className="bg-white dark:bg-gray-800 rounded-xl shadow p-6">
      <div className="flex justify-between items-center mb-4">
        <h2 className="text-xl font-semibold text-gray-800 dark:text-gray-100">Your Tasks</h2>
        <span className="text-sm text-gray-500 dark:text-gray-400">{tasks.length} {tasks.length === 1 ? 'task' : 'tasks'}</span>
      </div>

      {tasks.length === 0 ? (
        <div className="text-center py-16">
          <div className="mx-auto w-24 h-24 rounded-full bg-gray-100 dark:bg-gray-700 flex items-center justify-center mb-4">
            <ClipboardList className="h-12 w-12 text-gray-400 dark:text-gray-500" />
          </div>
          <h3 className="mt-2 text-lg font-medium text-gray-900 dark:text-gray-100">No tasks found</h3>
          <p className="mt-1 text-gray-500 dark:text-gray-400">You don&apos;t have any tasks yet.</p>
        </div>
      ) : (
        <ul className="divide-y divide-gray-100">
          <AnimatePresence mode="popLayout">
            {tasks.map((task) => (
              <TaskItem
                key={task.id}
                task={task}
                onToggleStatus={onToggleStatus}
                onDelete={onDelete}
                onEdit={onEdit}
              />
            ))}
          </AnimatePresence>
        </ul>
      )}
    </div>
  );
};

export default TaskList;